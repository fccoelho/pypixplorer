import pip
import subprocess
import json
from distutils.version import LooseVersion as lsvrs
from tinydb import TinyDB, Query


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

    def get_dependencies(self, package_name):
        """
        Get the dependencies of a given installed package
        :param package_name: name of the package
        :return: a dictionary of dependencies and their versions
        """
        deptree = subprocess.getoutput('pipdeptree -j')
        pack_json = json.loads(deptree)

        pack_db = TinyDB("pack_db.json")
        pack_db.purge()  # the method clears the database on every call, avoiding rewrites of packages
        pack_db.insert_multiple(pack_json)

        Pack = Query()
        list_version = pack_db.search(Pack.package.package_name == str(package_name))

        if len(list_version) == 0:
            return "Non installed package -- {}".format(str(package_name))
        elif len(list_version) == 1:
            return list_version[0]  # still need to improve the output
        else:
            max_idx, max_ver = 0, '0'
            for idx, dic in enumerate(list_version):
                version = dic["package"]["installed_version"]
                if lsvrs(version) > lsvrs(max_ver):
                    max_idx, max_ver = idx, version
            return list_version[max_idx]

    def dependency_graph(self, package_name):
        raise NotImplementedError
