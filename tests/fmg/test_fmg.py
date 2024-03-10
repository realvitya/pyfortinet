"""Test of human API"""
import pytest
from pyfortinet import FMG, FMGSettings
from pyfortinet.fmg_api.common import F


@pytest.mark.usefixtures("fmg")
class TestObjectsOnLab:
    def test_get_adom_list(self, fmg):
        result = fmg.get_adom_list(F(name__like="root"))  # root filter
        assert result == ["root"]

    def test_get_adom_list_with_or_filters(self, fmg):
        result = fmg.get_adom_list(F(name__like="root") | F(name__like="rootp"))
        assert result == ["root", "rootp"]

    def test_get_adom_list_with_three_filters(self, fmg):
        result = fmg.get_adom_list(F(name__like="root") | (F(name__like="rootp") | F(name="others")))
        assert result == ["others", "root", "rootp"]

    def test_get_adom_list_with_three_filters2(self, fmg):
        result = fmg.get_adom_list(F(name__like="root") + (F(name__like="rootp") + F(name="others")))
        assert result == ["others", "root", "rootp"]

    def test_get_adom_list_with_complex_filter(self, fmg):
        result = fmg.get_adom_list(
            (F(name__like="root") + (F(name__like="rootp") + F(name="others")) & F(state=1))
        )
        assert result == ["others", "root", "rootp"]
