import pip

from pypixplore.remote import Index
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

    def upgradeable(self, *args):
        """
        Lists upgradeable packages, their latest version and python requirements
        :param args: optional, names of packages to check if upgradeable
        :return: a dictionary which contains the name of upgradeable package, latest version
        and its python requirements
        """
        installed_packages = self.list_installed()
        version_installed_pckgs = {}
        names_installed_pckgs = list()
        for package in installed_packages:
            package = str(package).split()
            version_installed_pckgs[package[0]] = package[1]
            names_installed_pckgs.append(package[0])
        index = Index()
        JSON = index.get_multiple_JSONs(names_installed_pckgs)
        upgradeable_list = list()
        for package in JSON:
            latest_version = package['info']['version']
            python_requirement = package['info']['requires_python']
            if installed_version != version_installed_pckgs[package]:
                if python_requirement == '':
                    python_requirement = 'None'
                upgradeable_package = {'Name': package, 'Release': latest_version,
                                       'Python Requirement': python_requirement}
                upgradeable_list.append(upgradeable_package)
        if upgradeable_list:
            if not args:
                return upgradeable_list
            else:
                possible_upgrades = list()
                for arg in args:
                    for item in upgradeable_list:
                        if arg == item['Name']:
                            possible_upgrades.append(item)
                            break
                if not possible_upgrades:
                    print("None of the packages specified are upgradeable")
                else:
                    return possible_upgrades
        else:
            print('There are no upgradeable packages')

    def upgrade(self, *args):
        """
        Downloads the latest version of upgradeable packages (all or specified)
        :param args: optional, names of packages to upgrade (if they are upgradeable)
        """
        packages = self.upgradeable(args)
        if packages is not None:
            package_names = list()
            for item in self.upgradeable():
                package_names.append(item['Name'])
            if args:
                for arg in args:
                    if arg in package_names:
                        print('Upgrading package {}'.format(arg))
                        pip.main(['install', arg])
                    else:
                        print('The package {} is not upgradeable'.format(arg))
            else:
                for package in package_names:
                    print('Upgrading package {}'.format(package))
                    pip.main(['install', package])


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
        :return: a dictionary of dependencies and their versions
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
            package? they don't have those!""".format(package_name))
        elif len(list_version) == 1:
            deps = list_version[0]
        else:  # check which version is latest
            max_idx, max_ver = 0, '0'
            for idx, dic in enumerate(list_version):
                version = dic["package"]["installed_version"]
                if lsvrs(version) > lsvrs(max_ver):
                    max_idx, max_ver = idx, version
            deps = list_version[max_idx]

        deps_dict = {str(package_name): deps['package']['installed_version'], 'dependencies': {}}
        for dependency in deps['dependencies']:  # changing output to dict
            deps_dict['dependencies'][dependency['package_name']] = {'required_version': dependency['required_version'],
                                                     'installed_version': dependency['installed_version']}

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
        takes package_name and outputs its dependencies and their own dependencies plus an asciitree of this arrangement.
        :param package_name:
        :return: asciitree of the dependencies of the given package
        """
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
