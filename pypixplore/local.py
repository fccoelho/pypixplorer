import pip
import subprocess
import json
from asciitree import LeftAligned
from asciitree.drawing import BoxStyle, BOX_DOUBLE


class InstalledPackages:
    """
    Gets installed packages and their dependencies
    """

    def __init__(self):
        self.installed = pip.get_installed_distributions()
        self.cache = 0

    def list_installed(self):
        """
        Lists the locally installed packages
        :return: list of package names
        """
        return self.installed

    def show(self, package_name):
        return pip.main(['show', package_name])

    def upgradeable(self):
        raise NotImplementedError

    def make_dep_json(self):
        """
        Get the dependencies of all packages installed and cache the result in a json.
        :return: a tinydb database
        """
        deptree = subprocess.getoutput('pipdeptree -j')  # run pipdeptree (python module) on the terminal: outputs json
        deptree = json.loads(deptree)
        pack_db = {}
        for pack in deptree:
            pack_db[str(pack['package']['key'])] = pack
        self.cache = pack_db

    def get_dependencies(self, package_name):
        """
        Get the dependencies of a given installed package
        :param package_name: name of the package
        :return: a dictionary of dependencies and their versions
        """
        package_name = package_name.lower()
        if self.cache is 0:  # test if cache exists
            self.make_dep_json()  # make cache
            pack_db = self.cache
            pack = pack_db.get(package_name, None)
        else:
            pack_db = self.cache
            pack = pack_db.get(package_name, None)
            if pack is None:  # test if package is in cache
                self.make_dep_json()  # update cache because package may have been installed in the meantime
                pack_db = self.cache
                pack = pack_db.get(package_name, None)

        if pack is None:
            raise Exception("""package {} not installed! or are you requesting dependencies of a standard library
            package? they don't have those!""".format(package_name))

        deps_dict = {str(package_name): pack['package']['installed_version'], 'dependencies': {}}
        for dependency in pack['dependencies']:  # changing output to dict
            deps_dict["dependencies"][dependency['key']] = {"required_version": dependency["required_version"],
                                                            "installed_version": dependency["installed_version"]}

        return deps_dict

    def sub_graph(self, package_name):
        """
        :param package_name:
        :return: dictionary of dictionaries with the dependencies of package_name as keys
        """
        sub_dict = self.get_dependencies(package_name)
        deps_dict = sub_dict['dependencies']
        for dep in deps_dict:
            deps_dict[dep] = {}
        return deps_dict

    def dependency_graph(self, package_name):
        """
        takes package_name and outputs its dependencies and their own dependencies plus an asciitree of this arrangement
        :param package_name:
        :return: asciitree of the dependencies of the given package, up to the second level
        """
        package_name = package_name.lower()
        sub_tr = {package_name: self.sub_graph(package_name)}
        tree = sub_tr
        for node in sub_tr[package_name]:
            tree[package_name][node] = self.sub_graph(node)
        box_tr = LeftAligned(draw=BoxStyle(gfx=BOX_DOUBLE, horiz_len=1))
        return box_tr(tree)

    def package_status(self, package_name):
        """
        Check whether package_name is installed. If so, returns its version
        :param package_name: str to be consulted by function
        :return:  if installed - returns tuple with name of package and version
                  if not installed - returns None
        """
        for item in self.installed:
            name_version = str(item).split(' ')
            if package_name == name_version[0]:
                return tuple(name_version)
