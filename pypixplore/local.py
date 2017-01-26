import pip
<<<<<<< HEAD
from pypixplore.remote import Index
=======
import subprocess
import json
from distutils.version import LooseVersion as lsvrs
from tinydb import TinyDB, Query
from pathlib import Path

>>>>>>> d87534a04c514091cf8f47dae9c33d4a78b2349c

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
<<<<<<< HEAD
        installed_packages = self.list_installed()
        upgradeable_list = list()
        for package in installed_packages:
            package = str(package).split()
            package_name = package[0]
            installed_version = package[1]
            package_json = Index()
            package_json = package_json._get_JSON(package_name)
            if package_json:
                latest_version = package_json['info']['version']
                python_requirement = package_json['info']['requires_python']
                if installed_version != latest_version:
                    if python_requirement == '':
                        python_requirement = 'None'
                    upgradeable_package = {'Name': package_name, 'Release': latest_version,
                                           'Python Requirement': python_requirement}
                    upgradeable_list.append(upgradeable_package)
        if not upgradeable_list:
            print("There are no upgradable packages")
        else:
            return upgradeable_list




=======
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
            return "Non installed package -- {}".format(str(package_name))
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

    def dependency_graph(self, package_name):
        raise NotImplementedError
>>>>>>> d87534a04c514091cf8f47dae9c33d4a78b2349c
