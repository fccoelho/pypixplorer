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
        aa = Index().rank_of_packages_by_recent_release(list_size = 20, rank_size= 10)
        assert len(aa) == 10
        
    def test_package_info(self):
        ind = Index()
        result = ind.package_info("numpy")
        assert isinstance(result, tuple)


    def test_releases(self, index):
         for package_name in ['pandas', 'numpy', 'tinydb']:
             assert len(index.get_latest_releases(package_name)) > 0


    def test_get_popularity(self, index):
        assert isinstance(index.get_downloads('numpy'), dict)
        assert len(index.get_downloads('numpy')) > 0

    def test_get_git_number(self, index):
        with pytest.raises(AttributeError):
            index.get_git_number()

        with pytest.raises(AttributeError):
            index.get_git_number(of='forks')

        assert isinstance(index.get_git_number(of='forks', package_name='ARCCSSive'), int)

        assert index.get_git_number(of='forks', package_name='pandas') is None

    def test_release_series(self, index):

        assert isinstance(index.release_series('numpy'), list)

        assert len(index.release_series('numpy')) > 0

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

    def test_concurrent_downloads(self, index):
        out = index.get_multiple_JSONs(['pandas', 'numpy', 'pip', 'sympy'])
        assert isinstance(out, dict)
        assert isinstance(out['pip'], dict)

    def test_concurrent_downloads_big(self, index):
        l = index.client.list_packages()
        out = index.get_multiple_JSONs(l)
        assert isinstance(out, dict)
        assert isinstance(out['pip'], dict)
