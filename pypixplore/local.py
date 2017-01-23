import pip

class InstalledPackages:
    def __init__(self):
        self.installed = pip.get_installed_distributions()

    def list_installed(self):
        return self.installed

    def show(self, name=None):
        raise NotImplementedError

    def upgradeable(self):
        raise NotImplementedError
