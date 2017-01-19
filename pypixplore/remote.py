import xmlrpc.client as xmlrpcclient
import requests


class Index:
    """
    Connects with remote server. PyPI by default.
    """

    def __init__(self, server='https://pypi.python.org/pypi'):
        self.client = xmlrpcclient.ServerProxy(server)

    def _get_JSON(self, package_name):
        url = 'http://pypi.python.org/pypi/{}/json'.format(package_name)
        ans = requests.get(url)
        return ans.json()

    def get_releases(self, package_name):
        return self.client.package_releases(package_name)

    def get_dependencies(self, package_name):
        pass

    def dependency_graph(self, package_name):
        pass

    def get_popularity(self, package_name):
        pass
