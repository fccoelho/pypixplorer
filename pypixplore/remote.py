import xmlrpc.client as xmlrpcclient
import requests
from tinydb import TinyDB, Query
import datetime
import time
import json


class Index:
    """
    Connects with remote server. PyPI by default.
    """
    def __init__(self, server='https://pypi.python.org/pypi', cache_path='pypiexplorer_cache.json'):
        self.client = xmlrpcclient.ServerProxy(server)
        self.cache = TinyDB(cache_path)

    def _get_JSON(self, package_name):
        """
        Gets JSON record for a given package
        :param package_name: name of the package
        :return: dictionary
        """
        Package = Query()
        results = self.cache.search(Package.info.name == package_name)
        # TODO: check if the package data has been updated since last time.
        if results != []:
            data = results[0]
            # print("fetched from cache")
        else:
            url = 'http://pypi.python.org/pypi/{}/json'.format(package_name)
            ans = requests.get(url)
            try:
                data = ans.json()
                self._update_cache(data)
            except ValueError:
                data = []
        return data

    def package_info(self, pkgn):
        a = self._get_JSON(pkgn)
        name = a["info"]['name']
        description = a['info']['description']
        return (name, description)

    def _update_cache(self, data):
        self.cache.insert(data)

    def get_latest_releases(self, package_name):
        return self.client.package_releases(package_name)

    # moved get_dependencies and dependency_graph to local.py, as they can't be obtained remotely

    def get_popularity(self, package_name):
        """
        Gets number of downloads for a given package
        :param package_name: name of the package
        :return: dictionary of number of downloads. keys are 'last_month', 'last_week' and 'last_day'
        """

        return self._get_JSON(package_name)["info"]["downloads"]

    def release_series(self, package_name):
        """
        Gets most recent releases for a given package
        :param package_name: name of the package
        :return: List of itens of the last 10 most recent releases of the package
        """

        releases_list = list(self._get_JSON(package_name)['releases'].keys())
        releases_list.sort(reverse=True)
        last_ten = releases_list[:10]

        return last_ten

    def get_by_TROVE_classifier(self, trove):
        raise NotImplementedError


    def get_well_maintained(self):
        """
        Get packages which have had at least one release in the last six months, sorted by most recently updated
        """
        raise NotImplementedError

    def count_releases(self, package_name, time_days):
        json = self._get_JSON(package_name)
        if json == []:
            return 0
        keys = json["releases"].keys()
        count = 0
        for key in keys:
            if json["releases"][key] == []:
                break
            date = json["releases"][key][0]["upload_time"]
            date = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), 0, 0, 0)
            current_time = time.strftime("%Y-%m-%d").split('-')
            current_time = datetime.datetime(int(current_time[0]), int(current_time[1]), int(current_time[2]), 0, 0, 0)
            difference = current_time - date
            if difference.days < time_days:
                count += 1
            else:
                break
        return count

    def rank_of_packages_by_recent_release(self, time_days = 30, size = None):
        list_of_all_packages = self.client.list_packages()
        results = [self.count_releases(i, time_days) for i in list_of_all_packages[0:size]]
        dictionary = dict(zip(list_of_all_packages, results))
        rank = sorted(dictionary, key=dictionary.get, reverse=True)
        return(rank)

    def get_number_forks(self, package_name):
        forks = requests.get('https://api.github.com/repos/fccoelho/{}/forks'.format(package_name))
        if forks.ok:
            forks.content
            forks = forks.text
            forks = json.loads(forks)
            forks = len(forks)
        return forks

    def get_number_stars(self, package_name):
        stars = requests.get('https://api.github.com/repos/fccoelho/{}/stargazers'.format(package_name))
        if stars.ok:
            stars.content
            stars = stars.text
            stars = json.loads(stars)  # json to dict
            stars = len(stars)
        return stars

    def get_number_watchers(self, package_name):
        watchers = requests.get('https://api.github.com/repos/fccoelho/{}/subscribers'.format(package_name))
        if watchers.ok:
            watchers.content
            watchers = watchers.text
            watchers = json.loads(watchers)  # json to dict
            watchers = len(watchers)
        return watchers
