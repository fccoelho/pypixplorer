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
        with pytest.raises(Exception) as excinfo:
            localpacks.get_dependencies("jghjjhd")
        assert """package {} not installed! or are you requesting dependencies of a standard library
            package? they don't have those!""".format("jghjjhd") in str(excinfo.value)

    def test_dependency_graph(self, localpacks):
        assert isinstance(localpacks.dependency_graph("pip"), str)
        assert isinstance(localpacks.sub_graph("pip"), dict)

    def test_package_status(self, localpacks):
        assert isinstance(localpacks.package_status('numpy'), tuple)
        assert localpacks.package_status('@ab') is None
