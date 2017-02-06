from pypixplore.remote import Index
import pytest
import requests


class Tests:
    @pytest.fixture(autouse=True)
    def index(self):
        return Index()

    def test_get_json(self, index):
        for package in ['pandas', 'pip', 'ratelimit']:
            obj = index._get_JSON(package)
            assert isinstance(obj, dict)
            assert 'info' in obj
            assert 'name' in obj['info']

    def test_cache_update(self, index):
        assert len(index.cache) > 0

    def test_rank_of_packages_by_recent_release(self):
        a = Index().rank_of_packages_by_recent_release(time_days = 150, list_size = 20, rank_size= 20)
        assert len(a) == 20

    def test_count_releases(self):
        a = Index().count_releases(Index()._get_JSON('Pandas'), 150)
        assert isinstance(a, int)
        
    def test_package_info(self):
        ind = Index()
        result = ind.package_info("pip")
        assert isinstance(result, tuple)
        assert isinstance(result[0], str)
        assert isinstance(result[1], str)


    def test_releases(self, index):
         for package_name in ['pip', 'asciitree', 'ratelimit']:
             assert len(index.get_latest_releases(package_name)) > 0


    def test_get_popularity(self, index):
        assert isinstance(index.get_downloads('pip'), dict)
        assert len(index.get_downloads('pip')) > 0

    def test_get_git_number(self, index):
        with pytest.raises(AttributeError):
            index.get_git_stats()

        with pytest.raises(AttributeError):
            index.get_git_stats(of='forks')

        assert isinstance(index.get_git_stats(of='forks', package_name='ARCCSSive'), int)

        assert index.get_git_stats(of='forks', package_name='pandas') is None

    def test_release_series(self, index):

        assert isinstance(index.release_series('pip'), list)

        assert len(index.release_series('pip')) > 0

    def test_get_github_repo_by_name(self, index):

        assert isinstance(index.get_github_repo_by_name('https://github.com/JoaoCarabetta/pypixplorer'), str)

        assert 'https://api.github.com/repos/' in index.get_github_repo_by_name('https://github.com/JoaoCarabetta/pypixplorer')

        with pytest.raises(AttributeError):
            index.get_github_repo_by_name(7)

    def test_get_len_request(self, index):

        with pytest.raises(AttributeError):
            index.get_github_repo_by_name(7)

        assert isinstance(
            index.get_len_response(requests.get('https://api.github.com/repos/fccoelho/pypixplorer/forks'))
            , int)

        assert index.get_len_response(
            requests.get('https://api.github.com/repos/fccoelhsdfo/pypixsddasfplorer/forks')) is None

    def test_concurrent_downloads(self, index):
        out = index.get_multiple_JSONs(['asciitree', 'ratelimit', 'pip', 'pipdeptree'])
        assert isinstance(out, dict)
        assert isinstance(out['pip'], dict)

    def test_concurrent_downloads_100_pkgs(self, index):
        l = index.client.list_packages()
        out = index.get_multiple_JSONs(l[:100])
        assert isinstance(out, dict)
        assert isinstance(out.get(l[5]), dict)

    def test_print_graphics(self, index):
        out = index.print_graphics(2, 3)
        assert "**" in out and "***" in out

    def test_how_many_packages_version_py(self, index):
        out = index.how_many_packages_version_py(n_sample=150)
        assert isinstance(out, list)
        assert out[0] > 0
        assert out[1] > 0
