import pip
from pypixplore.remote import Index

class InstalledPackages:
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
        installed_packages = self.list_installed()
        upgradeable_list = list()
        for package in installed_packages:
            package = str(package).split()
            package_name = package[0]
            installed_version = package[1]
            package_json = Index()
            package_json = package_json._get_JSON(package_name)
            latest_version = package_json['info']['version']
            if installed_version != latest_version:
                upgradeable_list.append(package_name)
        if not upgradeable_list:
            print("There are no upgradable packages")
        else:
            return upgradeable_list




