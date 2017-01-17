import xmlrpc.client as xmlrpcclient

class Index:
    """
    Connects with remote server. PyPI by default.
    """
    def __init__(self, server='https://pypi.python.org/pypi'):
        self.client = xmlrpcclient.ServerProxy(server)

    def get_releases(self, package_name):
        return self.client.package_releases(package_name)

    def get_dependencies(self, package_name):
        pass
