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
        assert isinstance(localpacks.package_status('pip'), tuple)
        assert localpacks.package_status('@ab') is None

    def test_show(self, localpacks):
        assert localpacks.show('pip') == 0
        assert localpacks.show('numkdkdpy') == 1