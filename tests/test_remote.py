from pypixplore.remote import Index
import pytest
import requests


class Tests:
    @pytest.fixture(autouse=True)
    def index(self):
        return Index()

    def test_get_json(self, index):
        for package in ['pandas', 'numpy', 'tinydb']:
            obj = index._get_JSON(package)
            assert isinstance(obj, dict)
            assert 'info' in obj
            assert 'name' in obj['info']

    def test_cache_update(self, index):
        assert len(index.cache.all()) > 0

    def test_rank_of_packages_by_recent_release(self):
        aa = Index().rank_of_packages_by_recent_release(size = 100)
        assert len(aa) == 100
        aaa = Index().rank_of_packages_by_recent_release(size = 50)
        
    def test_package_info(self):
        ind = Index()
        result = ind.package_info("numpy")
        assert isinstance(result, tuple)


    def test_releases(self, index):
         for package_name in ['pandas', 'numpy', 'tinydb']:
             assert len(index.get_latest_releases(package_name)) > 0


    def test_get_popularity(self, index):
        assert isinstance(index.get_popularity('numpy'), dict)
        assert len(index.get_popularity('numpy')) > 0

    def test_get_git_number(self, index):
        with pytest.raises(AttributeError):
            index.get_git_number()

        with pytest.raises(AttributeError):
            index.get_git_number(of='forks')

    def test_get_github_repo_by_name(self, index):

        assert isinstance(index.get_github_repo_by_name('https://github.com/JoaoCarabetta/pypixplorer'), str)

        assert 'https://api.github.com/repos/' in index.get_github_repo_by_name('https://github.com/JoaoCarabetta/pypixplorer')

        with pytest.raises(AttributeError):
            index.get_github_repo_by_name(7)

    def test_get_len_request(self, index):

        with pytest.raises(AttributeError):
            index.get_github_repo_by_name(7)

        assert isinstance(index.get_len_request(requests.get('https://api.github.com/repos/fccoelho/pypixplorer/forks'))
                          , int)

        assert index.get_len_request(requests.get('https://api.github.com/repos/fccoelhsdfo/pypixsddasfplorer/forks')) is None


    def test_get_github_repo_by_search(self, index):

        with pytest.raises(AttributeError):
            index.get_github_repo_by_name(7)

        assert isinstance(index.get_github_repo_by_search('numpy'), str)

