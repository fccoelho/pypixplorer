import xmlrpc.client as xmlrpcclient
import datetime
import time
import json
import requests
import concurrent.futures
from ratelimit import rate_limited
import pickle
import dbm
import os
import random as rd

class Index:
    """
    Connects with remote server. PyPI by default.
    """

    def __init__(self, server='https://pypi.python.org/pypi', cache_path=os.path.join(os.path.expanduser('~'), '.pypiexplorer_cache')):
        self.client = xmlrpcclient.ServerProxy(server)
        self.cache = dbm.open(cache_path, 'c')
 #       self.cache.reorganize()  # optimize the cache

    @rate_limited(10)
    def _get_JSON(self, package_name, update_cache=True):
        """
        Gets JSON record for a given package
        :param package_name: name of the package
        :return: dictionary
        """
        results = self.cache.get(package_name, None)
        # TODO: check if the package data has been updated since last time.
        if results is not None:
            data = pickle.loads(results)
            # print("fetched from cache")
        else:
            try:
                url = 'http://pypi.python.org/pypi/{}/json'.format(package_name)
                ans = requests.get(url, timeout=15)
                data = ans.json()
                if update_cache:
                    self._update_cache(package_name, data)
            except (ValueError, requests.exceptions.ConnectionError):
                data = []
            except:
                data = []

        return data

    def get_multiple_JSONs(self, pkg_list):
        output = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(self._get_JSON, pkg_name, False): pkg_name for pkg_name in pkg_list}
            for future in concurrent.futures.as_completed(future_to_url):
                pkg_name = future_to_url[future]
                try:
                    JSON = future.result()
                    output[pkg_name] = JSON
                except Exception as exc:
                    print('%r generated an exception: %s' % (pkg_name, exc))
        return output


    def package_info(self, pkgn):
        a = self._get_JSON(pkgn)
        name = a["info"]["name"]
        description = a["info"]["description"]
        if len(description) > 2000:
            description = description[:2000] + " [...]"
        return name, description

    def _update_cache(self, package_name, data):
        # self.cache.insert(data)
        self.cache[package_name] = pickle.dumps(data)
    def get_latest_releases(self, package_name):
        return self.client.package_releases(package_name)

    # moved get_dependencies and dependency_graph to local.py, as they can't be obtained remotely

    def get_downloads(self, package_name):
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

    def count_releases(self, json, time_days):
        """
        This function count how many releases a package received in a period of time in days.
        :param json: The json of a package.
        :param time_days: The period of time that the function will use to count how many releases the package has.
        :return: The amount of releases a package received in the given period.
        """
        time_days = int(time_days)
        if json == []:
            return 0
        keys = json["releases"].keys()
        order_process = {i.replace('.', ''): i for i in keys }
        keys_in_order = [order_process[i] for i in sorted(order_process.keys(), reverse=True)]
        count = 0
        for key in keys_in_order:
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


    def rank_of_packages_by_recent_release(self, time_days = 30, list_size = None, rank_size = None):
        """
        This function gets the packages and rank them by amount of releases in a period of time.
        :param time_days: The period of time in days that de function count_releases will use.
        :param list_size: If given a -list_size-, the function use the first -list_size- packages of the list_of_all_packages.
        :param rank_size: If given a -rank_size-, the function will return the first -rank_size- of the rank.
        :return: The rank by recent release using the time in days, the -list_size- and the -rank_size- given.
        """
        list_of_packages = self.client.list_packages()
        list_of_packages= list_of_packages[0:list_size]
        dict_package_json = self.get_multiple_JSONs(list_of_packages)
        dictionary = {i : self.count_releases(dict_package_json[i], time_days) for i in  list_of_packages}
        rank = sorted(dictionary, key=dictionary.get, reverse=True)
        rank = rank[0:rank_size]
        return(rank)

    def get_len_response(self, response):

        if response.ok:
            count = len(json.loads(response.text))

        else:
            count = None

        return count

    def get_github_repo_by_name(self, hyperlink):
        parts = hyperlink.split('/')
        user = parts[-2]
        repo = parts[-1]
        return 'https://api.github.com/repos/{}/{}/'.format(user, repo)

    def get_git_stats(self, of='', package_name=''):

        if of == '':
            raise AttributeError('No information specified on "of:"')

        if package_name == '':
            raise AttributeError('No package specified')

        json = self._get_JSON(package_name)

        if len(json) == 0:
            print('Package not found')
            raise AttributeError

        hyperlink = json["info"]['home_page']

        name = json['info']['name']

        if 'github' in hyperlink:
            git_repo_api = self.get_github_repo_by_name(hyperlink)

        else:
            print('Package does not have a GitHub Repo as an official homepage.\n')
            return None
            # git_repo_api = self.get_github_repo_by_search(name)


        # get info from github api
        if of == 'forks':
            response = requests.get(git_repo_api + 'forks')

        elif of == 'stars':
            response = requests.get(git_repo_api + 'stargazers')

        elif of == 'watchers':
            response = requests.get(git_repo_api + 'subscribers')

        else:
            print('{} is not a possible option for "of".\n If you think that it should be implemented, implement!')
            raise AttributeError

        return self.get_len_response(response)

    def how_many_packages_version_py(self, n_sample=700):
        """
        print('This command can take a while, do you wish to continue? /n type Y or N')
        aux = input()
        aux = aux.capitalize()
        if aux == 'N':
            return None
        elif aux != 'Y':
            print('Por favor, digite S para sim ou N para não')
            self.how_many_packages_version_py()
        """
        n_sample = int(n_sample)

        list_of_all_packages = self.client.list_packages()

        rd.shuffle(list_of_all_packages)

        all_packages = self.get_multiple_JSONs(list_of_all_packages[:n_sample])

        count2master = 0
        count3master = 0
        both = 0
        unknown = 0

        for key, package in all_packages.items():

            if len(package) > 0:
                package_classifiers = package['info']['classifiers']
            else:
                continue

            pyt2 = any(['Python :: 2' in version_control for version_control in package_classifiers])
            pyt3 = any(['Python :: 3' in version_control for version_control in package_classifiers])

            if pyt2 and pyt3:
                both += 1
            elif pyt2 and not pyt3:
                count2master += 1
            elif pyt3 and not pyt2:
                count3master += 1
            else:
                unknown += 1

        count_final = [round((both / n_sample), 2) * 100, round((count2master / n_sample), 2) * 100,
                       round((count3master / n_sample), 2) * 100, round((unknown / n_sample), 2) * 100]

        return count_final

    def print_graphics(self, results):
        b, python2, python3, u = results

        string_to_print = 'Both 2.x and 3.x |{} {}%\nOnly Python 2.x.x|{} {}%\n' \
                          'Only Python 3.x.x|{} {}%\nUnknown          |{} {}%'.format('*' * int(b), b,
                                                                                      '*' * int(python2), python2,
                                                                                      '*' * int(python3), python3,
                                                                                      '*' * int(u), u)

        return string_to_print
