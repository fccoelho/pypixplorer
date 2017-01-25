import pip


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
        raise NotImplementedError

    def package_status(self, package_name):
        """
        Check whether package_name is installed. If so, returns its version
        :param package_name: str to be consulted by function
        :return:  if installed - returns tuple with name of package and version
                  if not installed - returns 0
        """
        pack_list = self.installed
        for item in pack_list:
            name_version = str(item).split(' ')
            if package_name == name_version[0]:
                return tuple(name_version)
        return 0
