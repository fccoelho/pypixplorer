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
<<<<<<< HEAD
        assert isinstance(localpacks.installed, list)

    def test_upgradeable(self, localpacks):
        if localpacks.upgradeable():
            assert isinstance(localpacks.upgradeable(), list)
            assert isinstance(localpacks.upgradeable()[0], dict)
            assert isinstance(localpacks.upgradeable()[0]['Python Requirement'], str)
=======
        assert isinstance(localpacks.list_installed(), list)
        assert len(localpacks.list_installed()) > 0

    def test_get_dependencies(self, localpacks):
        assert isinstance(localpacks.get_dependencies("pip"), dict)
        assert isinstance(localpacks.get_dependencies("JSON_dependencies"), str)
>>>>>>> d87534a04c514091cf8f47dae9c33d4a78b2349c
