import xmlrpc.client as xmlrpcclient
from tinydb import TinyDB, Query
import datetime
import time
import json
import requests


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
            except (ValueError, requests.exceptions.ConnectionError):
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

    def count_releases(self, package_name, time_days):
        """
        This function count how many releases a package received in a period of time in days.
        :param package_name: The name of the package.
        :param time_days: The period of time that the function will use to count how many releases the package has.
        :return: The amount of releases a package received in the given period.
        """
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

    def rank_of_packages_by_recent_release(self, time_days = 30, list_size = None, rank_size = None):
        """
        This function gets the packages and rank them by amount of releases in a period of time.
        :param time_days: The period of time in days that de function count_releases will use.
        :param list_size: If given a -list_size-, the function use the first -list_size- packages of the list_of_all_packages.
        :param rank_size: If given a -rank_size-, the function will return the first -rank_size- of the rank.
        :return: The rank by recent release using the time in days, the -list_size- and the -rank_size- given.
        """
        if list_size < rank_size:
            rank_size = list_size
        list_of_all_packages = self.client.list_packages()
        results = [self.count_releases(i, time_days) for i in list_of_all_packages[0:list_size]]
        dictionary = dict(zip(list_of_all_packages, results))
        rank = sorted(dictionary, key=dictionary.get, reverse=True)
        rank = rank[0:rank_size]
        return(rank)

    def get_len_request(self, request):

        if not isinstance(request, requests.models.Response):
            print('Class expected as input. <requests.models.Response>')
            raise AttributeError

        if request.ok:
            count = len(json.loads(request.text))

            if isinstance(count, int):
                return count

            else:
                print('Not an int')
                raise AttributeError
        else:
            print('Page could not be loaded. Error:')
            print(request)
            return None

    def get_github_repo_by_name(self, hyperlink):

        if not isinstance(hyperlink, str):
            print('String expected as input')
            raise AttributeError

        *useless, user, repo = hyperlink.split('/')

        return 'https://api.github.com/repos/{}/{}/'.format(user, repo)
    """
    def get_github_repo_by_search(self, name):

        if not isinstance(name, str):
            print('String expected as input')
            raise AttributeError

        request_api = requests.get('https://api.github.com/search/repositories?q={}'.format(name))

        if request_api.ok:
            request_api_json = json.load(request_api.text)

            if request_api_json['total_count'] == 0:
                print('\nPackage {} not found on GitHub\n'.format(name))
                return None

            else:
                print('{} repositories were found on GitHub '
                      'based on the package name'.format(request_api_json['total_count']))

                print('Here are the first 5 results. Type 0 - 4 to choose the one that is the correct.'
                      'Type 9 otherwise to quit.')
                for i in range(5):
                    print('\n[{}]\nName:{}\nLink:{}'.format(i,request_api_json['items'][i]['name'],
                                                      request_api_json['items'][i]['url']))

                num = input('Type number here: ')

                if num == 9:
                    return None

                if num <= 4:
                    return request_api_json['items'][num]['url']

                else:
                    print("Not allowed value")
                    raise AttributeError
        else:
            print('Page could not be loaded. Error:')
            print(request_api)
            return None
    """
    def get_git_number(self, of='', package_name=''):

        if of == '':
            print('No information specified on "of:"')
            raise AttributeError

        if package_name == '':
            print('No package specified')
            raise AttributeError

        json = self._get_JSON(package_name)

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
            request = requests.get(git_repo_api + 'forks')

        elif of == 'stars':
            request = requests.get(git_repo_api + 'stargazers')

        elif of == 'watchers':
            request = requests.get(git_repo_api + 'subscribers')

        else:
            print('{} is not a possible option for "of".\n If you think that it should be implemented, implement!')
            raise AttributeError


        return self.get_len_request(request)

    def how_many_packages_version_py(self):
        print('This command can take a while, do you wish to continue? /n type Y or N')
        aux = input()
        if aux == 'N':
            return
        elif aux != 'y':
            print('Por favor, digite S para sim ou N para não')
            self.how_many_packages_version_py()

        list_of_all_packages = self.client.list_packages()

        count2master = 0
        count3master = 0

        for package_name in list_of_all_packages:
            package_classifiers = self._get_JSON(package_name)['info']['classifiers']

            python2counter = 0
            python3counter = 0

            for version_control in package_classifiers:
                if 'Python :: 2' in version_control & python2counter == 0:
                    python2counter += 1
                    count2master += 1
                else:
                    pass
                if 'Python :: 3' in version_control & python3counter == 0:
                    python3counter += 1
                    count3master += 1
                else:
                    pass

        count_final = [round((count2master / len(list_of_all_packages)) * 10),
                       round((count3master / len(list_of_all_packages)) * 10)]

        # count_final = {'Python 2.x.x': count2master/len(list_of_all_packages), 'Python 3.x.x': count3master/len(list_of_all_packages)}
        # plt.bar(range(len(count_final)), count_final.values(), align='center')
        # plt.xticks(range(len(count_final)), count_final.keys())
        self.print_graphics(count_final[0], count_final[1])

    def print_graphics(self, python2, python3):
        count_python2 = ""
        count_python3 = ""

        for i in range(0, python2):
            count_python2 = count_python2 + "*"
        for i in range(0, python3):
            count_python3 = count_python3 + "*"
        print('\t\t\t |')
        print('Python 2.x.x |{} {}%'.format(count_python2, python2 * 10))
        print('\t\t\t |')
        print('\t\t\t |')
        print('Python 3.x.x |{} {}%'.format(count_python3, python3 * 10))
        print('\t\t\t |')
