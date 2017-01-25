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




