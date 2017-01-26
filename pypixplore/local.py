import pip
import subprocess
import json
from distutils.version import LooseVersion as lsvrs
from tinydb import TinyDB, Query
from pathlib import Path
from asciitree import LeftAligned
from asciitree.drawing import BoxStyle, BOX_DOUBLE


class InstalledPackages:
    """
    Gets installed packages and their dependencies
    """

    def __init__(self):
        self.installed = pip.get_installed_distributions()

    def list_installed(self):
        """
        Lists the locally installed packages
        :return: list of package names
        """
        return self.installed

    def show(self, name=None):
        raise NotImplementedError

    def upgradeable(self):
        raise NotImplementedError

    def make_dep_json(self):
        """
        Get the dependencies of all packages installed and cache the result in a json.
        :return: a tinydb database
        """
        deptree = subprocess.getoutput('pipdeptree -j')  # run pipdeptree (python module) on the terminal: outputs json
        pack_json = json.loads(deptree)  # load json to python environment

        pack_db = TinyDB("pack_db.json")
        pack_db.purge()  # the method clears the database on every call, avoiding rewrites of packages (duplicates)
        pack_db.insert_multiple(pack_json)
        return pack_db

    def get_dependencies(self, package_name):
        """
        Get the dependencies of a given installed package
        :param package_name: name of the package
        :return: a dictionary of dependencies and their versions, or a string saying package is not installed
        """
        my_file = Path("pack_db.json")
        if not my_file.is_file():  # test if cache exists
            pack_db = self.make_dep_json()  # make cache
            Pack = Query()
            list_version = pack_db.search(Pack.package.package_name == str(package_name))  # query cache for package
        else:
            pack_db = TinyDB("pack_db.json")
            Pack = Query()
            list_version = pack_db.search(Pack.package.package_name == str(package_name))
            if len(list_version) == 0:  # test if package is in cache
                pack_db = self.make_dep_json()  # update cache because package may have been installed in the meantime
                # Pack = Query() #no need
                list_version = pack_db.search(Pack.package.package_name == str(package_name))

        if len(list_version) == 0:
            raise Exception("""package {} not installed! or are you requesting dependencies of a standard library
            package?\n\tthey don't have those!""".format(package_name))
        elif len(list_version) == 1:
            deps = list_version[0]
        else:  # check which version is latest
            max_idx, max_ver = 0, '0'
            for idx, dic in enumerate(list_version):
                version = dic["package"]["installed_version"]
                if lsvrs(version) > lsvrs(max_ver):
                    max_idx, max_ver = idx, version
            deps = list_version[max_idx]

        deps_dict = {}
        for dependency in deps['dependencies']:  # changing output to dict
            deps_dict[dependency['package_name']] = {'required_version': dependency['required_version'],
                                                     'installed_version': dependency['installed_version']}

        return deps_dict  # , list(deps_dict.keys())

    def sub_graph(self, package_name):
        """
        :param package_name:
        :return: dictionary of dictionaries with the dependencies of package_name as keys
        """
        deps_dict = self.get_dependencies(package_name)
        for dep in deps_dict:
            deps_dict[dep] = {}
        return deps_dict

    def dependency_graph(self, package_name):
        """
        takes package_name and outputs its dependencies and their own dependencies plus an asciitree of this arrangement.
        :param package_name:
        :return: dictionary of dictionaries with dependencies of package name
        """
        sub_tr = {package_name: self.sub_graph(package_name)}
        tree = sub_tr
        for node in sub_tr[package_name]:
            tree[package_name][node] = self.sub_graph(node)
        box_tr = LeftAligned(draw=BoxStyle(gfx=BOX_DOUBLE, horiz_len=1))
        print(box_tr(tree))
        return tree