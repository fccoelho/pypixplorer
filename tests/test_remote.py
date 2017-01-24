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
        aa = Index().rank_of_packages_by_recent_release()
    def test_get_releases(self,index):
        assert len(index.get_releases('pandas')) > 0
        assert len(aa) == 100