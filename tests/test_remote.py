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

    def test_cache_update(self, index):
        assert len(index.cache.all()) > 0
