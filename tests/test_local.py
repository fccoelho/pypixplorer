import os
os.system('echo %cd%')

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
        assert isinstance(localpacks.list_installed(), list)
        assert len(localpacks.list_installed()) > 0

    def test_upgradeable(self, localpacks):
        if localpacks.upgradeable() is not None:
            assert isinstance(localpacks.upgradeable(), list)
            assert isinstance(localpacks.upgradeable()[0], dict)
            assert isinstance(localpacks.upgradeable()[0]['Python Requirement'], str)

    def test_upgradeable_with_non_existing_package(self, localpacks):
        assert localpacks.upgradeable('abshfjsk') is None

    def test_upgradeable_with_specific_packages(self, localpacks):
        if localpacks.upgradeable('pandas', 'numpy') is not None:
            assert isinstance(localpacks.upgradeable('pandas', 'numpy'), list)
            assert isinstance(localpacks.upgradeable('pandas', 'numpy')[0], dict)
            assert isinstance(localpacks.upgradeable('pandas', 'numpy')[0]['Python Requirement'], str)

    def test_upgrade_specific_package(self, localpacks):
        assert localpacks.upgrade('pandas') is None

    def test_get_dependencies(self, localpacks):
        assert isinstance(localpacks.get_dependencies("pip"), dict)
        assert isinstance(localpacks.get_dependencies("JSON_dependencies"), str)
