from pypixplore.local import InstalledPackages
import pytest


@pytest.fixture()
def localpacks():
    return InstalledPackages


class Tests:
    @pytest.fixture(autouse=True)
    def localpacks(self):
        return InstalledPackages()

    def test_list_installed(self, localpacks):
        assert isinstance(localpacks.installed, list)

    def test_upgradeable(self, localpacks):
        if localpacks.upgradeable():
            assert isinstance(localpacks.upgradeable(), list)
            assert isinstance(localpacks.upgradeable()[0], str)
