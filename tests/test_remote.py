from pypixplore.remote import Index
import pytest


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

    def test_get_forks(self, index):
        assert isinstance(index.get_number_forks('pandas'), int)

    def test_get_stars(self, index):
        assert isinstance(index.get_number_stars('PySUS'), int)

    def test_get_watchers(self, index):
        assert isinstance(index.get_number_watchers('numpy'), int)
