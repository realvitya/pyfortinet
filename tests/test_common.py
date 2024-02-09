"""Test offline classes and functions"""
import pytest

from pyfortinet import FMGResponse
from pyfortinet.fmg_api.common import F


class TestFilters:
    def test_simple_filter(self):
        f = F(name="test_address").generate()
        assert f == ["name", "==", "test_address"]

    def test_negate_filter(self):
        f = (~F(name="test_address")).generate()
        assert f == ["!", "name", "==", "test_address"]

    def test_filter_with_more_values(self):
        f = F(member__in=["abc", "def", "ghi"]).generate()
        assert f == ["member", "in", "abc", "def", "ghi"]

    def test_filter_with_implicit_or(self):
        f = (F(name="test_address") + F(name="test2_address")).generate()
        assert f == [["name", "==", "test_address"], ["name", "==", "test2_address"]]

    def test_explicit_or_filters(self):
        f = (F(name="test_address") | F(name="prod_address")).generate()
        assert f == [["name", "==", "test_address"], "||", ["name", "==", "prod_address"]]

    def test_multiple_filters(self):
        f = (F(name="acceptance_address") | F(name="test_address") | F(name="prod_address")).generate()
        assert f == [
            [["name", "==", "acceptance_address"], "||", ["name", "==", "test_address"]],
            "||",
            ["name", "==", "prod_address"],
        ]

    def test_filters_with_parentheses(self):
        f = (F(name="acceptance_address") | (F(name="test_address") | F(name="prod_address"))).generate()
        assert f == [
            ["name", "==", "acceptance_address"],
            "||",
            [["name", "==", "test_address"], "||", ["name", "==", "prod_address"]],
        ]

    def test_filters_with_parentheses2(self):
        f = ((F(name="acceptance_address") | F(name="test_address")) & F(state=1)).generate()
        assert f == [
            [["name", "==", "acceptance_address"], "||", ["name", "==", "test_address"]],
            "&&",
            ["state", "==", 1],
        ]

    def test_and_filters(self):
        f = (F(name__like="test%") & F(interface="port1")).generate()
        assert f == [["name", "like", "test%"], "&&", ["interface", "==", "port1"]]

    def test_complex_filter(self):
        f = ((F(name="root") + F(name="rootp")) & (F(status=1) + F(status=2))).generate()
        assert f == [
            [["name", "==", "root"], ["name", "==", "rootp"]],
            "&&",
            [["status", "==", 1], ["status", "==", 2]],
        ]

    def test_first_good(self):
        response = FMGResponse(data={"data": ["response1", "response2"]})
        assert response.first() == "response1"

    def test_first_empty(self):
        response = FMGResponse()
        assert response.first() is None
