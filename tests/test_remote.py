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
        assert len(aaa) == 50

    def test_releases(self, index):
         for package_name in ['pandas', 'numpy', 'tinydb']:
            assert len(index.get_releases(package_name)) > 0


    def test_get_popularity(self, index):
        assert isinstance(index.get_popularity('numpy'), dict)
        assert len(index.get_popularity('numpy')) > 0