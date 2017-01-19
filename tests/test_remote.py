from pypixplore.remote import *
import pytest

class Tests:
    @pytest.fixture(autouse=True)
    def index(self):
        return Index()

    def test_get_json(self, index):
        obj = index._get_JSON('pandas')
        assert isinstance(obj, dict)
