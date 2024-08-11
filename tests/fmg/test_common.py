"""Test offline classes and functions"""

import pytest
from pydantic import Field

from pyfortinet import FMGResponse, AsyncFMGResponse
from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.common import F, text_to_filter


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

    def test_explicit_and_filters(self):
        f = (F(name="test_address") & F(name="prod_address")).generate()
        assert f == [["name", "==", "test_address"], "&&", ["name", "==", "prod_address"]]

    def test_multiple_filters(self):
        f = (F(name="acceptance_address") | F(name="test_address") | F(name="prod_address")).generate()
        assert f == [
            ["name", "==", "acceptance_address"],
            "||",
            ["name", "==", "test_address"],
            "||",
            ["name", "==", "prod_address"],
        ]

    def test_multiple_filters2(self):
        f = (F(name="acceptance_address") | (F(name="test_address") | F(name="prod_address"))).generate()
        assert f == [
            ["name", "==", "acceptance_address"],
            "||",
            ["name", "==", "test_address"],
            "||",
            ["name", "==", "prod_address"],
        ]

    def test_multiple_filters3(self):
        f = (F(name="acceptance_address") & (F(name="test_address") & F(name="prod_address"))).generate()
        assert f == [
            ["name", "==", "acceptance_address"],
            "&&",
            ["name", "==", "test_address"],
            "&&",
            ["name", "==", "prod_address"],
        ]

    def test_empty_filter_handling(self):
        hosts = ["host1", "host2", "host3"]
        filters = F()  # initialize filters without any data
        for host in hosts:
            filters |= F(name=host)  # use the initialized filters object
        assert filters.generate() == [
            ["name", "==", "host1"],
            "||",
            ["name", "==", "host2"],
            "||",
            ["name", "==", "host3"],
        ]

    def test_filterlist_add(self):
        f = (
            (F(name="acceptance_address") + F(name="test_address") + F(name="prod_address"))
            + (F(name="acceptance_address") + F(name="test_address") + F(name="prod_address"))
        ).generate()
        assert f == [
            ["name", "==", "acceptance_address"],
            ["name", "==", "test_address"],
            ["name", "==", "prod_address"],
            ["name", "==", "acceptance_address"],
            ["name", "==", "test_address"],
            ["name", "==", "prod_address"],
        ]

    def test_f_to_complex(self):
        f = (
            F(name="test_address")
            + ((F(name="acceptance_address") | (F(name="test_address"))) & F(name="prod_address"))
        ).generate()
        assert f == [
            ["name", "==", "test_address"],
            [
                [["name", "==", "acceptance_address"], "||", ["name", "==", "test_address"]],
                "&&",
                ["name", "==", "prod_address"],
            ],
        ]

    def test_filterlist_add_with_complex(self):
        f = (
            (F(name="acceptance_address") + F(name="test_address") + F(name="prod_address"))
            + (F(name="acceptance_address") | F(name="test_address") + F(name="prod_address"))
        ).generate()
        assert f == [
            [["name", "==", "acceptance_address"], ["name", "==", "test_address"], ["name", "==", "prod_address"]],
            [
                ["name", "==", "acceptance_address"],
                "||",
                [["name", "==", "test_address"], ["name", "==", "prod_address"]],
            ],
        ]

    def test_filterlist_to_complex(self):
        f = (
            (F(name="acceptance_address") + F(name="test_address") + F(name="prod_address"))
            | (F(name="acceptance_address") + F(name="test_address") + F(name="prod_address"))
        ).generate()
        assert f == [
            [["name", "==", "acceptance_address"], ["name", "==", "test_address"], ["name", "==", "prod_address"]],
            "||",
            [["name", "==", "acceptance_address"], ["name", "==", "test_address"], ["name", "==", "prod_address"]],
        ]

    def test_filters_with_parentheses(self):
        f = (F(name="acceptance_address") & (F(name="test_address") | F(name="prod_address"))).generate()
        assert f == [
            ["name", "==", "acceptance_address"],
            "&&",
            [["name", "==", "test_address"], "||", ["name", "==", "prod_address"]],
        ]

    def test_filters_with_parentheses2(self):
        f = ((F(name="acceptance_address") | F(name="test_address")) & F(state=1)).generate()
        assert f == [
            [["name", "==", "acceptance_address"], "||", ["name", "==", "test_address"]],
            "&&",
            ["state", "==", 1],
        ]

    def test_filters_with_parentheses3(self):
        f = ((F(name="acceptance_address") | F(name="test_address")) & (F(state=1) | F(state=2))).generate()
        assert f == [
            [["name", "==", "acceptance_address"], "||", ["name", "==", "test_address"]],
            "&&",
            [["state", "==", 1], "||", ["state", "==", 2]],
        ]

    def test_filters_with_parentheses4(self):
        f = (
            (F(name="acceptance_address") | F(name="test_address")) & (F(state=1) | F(state=2))
            | (F(name="acceptance_address") | F(name="test_address")) & (F(state=1) | F(state=2))
        ).generate()
        assert f == [
            [
                [["name", "==", "acceptance_address"], "||", ["name", "==", "test_address"]],
                "&&",
                [["state", "==", 1], "||", ["state", "==", 2]],
            ],
            "||",
            [
                [["name", "==", "acceptance_address"], "||", ["name", "==", "test_address"]],
                "&&",
                [["state", "==", 1], "||", ["state", "==", 2]],
            ],
        ]

    def test_filters_with_parentheses5(self):
        f = (
            ((F(name="acceptance_address") | F(name="test_address")) & (F(state=1) | F(state=2)))
            & ((F(name="acceptance_address") | F(name="test_address")) & (F(state=1) | F(state=2)))
        ).generate()
        assert f == [
            [
                [["name", "==", "acceptance_address"], "||", ["name", "==", "test_address"]],
                "&&",
                [["state", "==", 1], "||", ["state", "==", 2]],
            ],
            "&&",
            [
                [["name", "==", "acceptance_address"], "||", ["name", "==", "test_address"]],
                "&&",
                [["state", "==", 1], "||", ["state", "==", 2]],
            ],
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

    def test_filter_with_separator(self):
        f = F(allow_routing="enable", _sep="-").generate()
        assert f == ["allow-routing", "==", "enable"]

    def test_filter_without_separator(self):
        f = F(allow_routing="enable").generate()
        assert f == ["allow_routing", "==", "enable"]

    def test_filter_with_sep_keep_first_(self):
        f = F(_image_base64="qweqweqwe", _sep="-").generate()
        assert f == ["_image-base64", "==", "qweqweqwe"]

    def test_filter_with_multiple_separator(self):
        f = F(_allow_routing_test="enable", _sep="-").generate()
        assert f == ["_allow-routing-test", "==", "enable"]

    def test_first_good(self):
        response = FMGResponse(data={"data": ["response1", "response2"]})
        assert response.first() == "response1"

    def test_first_empty(self):
        response = FMGResponse()
        assert response.first() is None

    def test_first_good_async(self):
        response = AsyncFMGResponse(data={"data": ["response1", "response2"]})
        assert response.first() == "response1"

    def test_first_empty_async(self):
        response = AsyncFMGResponse()
        assert response.first() is None

    def test_text_to_filter(self):
        assert text_to_filter("name like test%").generate() == ["name", "like", "test%"]
        assert text_to_filter("~name like host_%").generate() == ["!", "name", "like", "host_%"]
        assert text_to_filter("name eq host_1 and conf_status eq insync").generate() == [
            ["name", "==", "host_1"],
            "&&",
            ["conf_status", "==", "insync"],
        ]
        # `-` and ` ` also works
        assert text_to_filter("_image-base64 like test%").generate() == ["_image-base64", "like", "test%"]
        assert text_to_filter("scope member in fw1").generate() == ["scope member", "in", "fw1"]
        assert text_to_filter("name eq test-addr1, name eq test-addr2").generate() == [
            ["name", "==", "test-addr1"],
            ["name", "==", "test-addr2"],
        ]
        assert text_to_filter("name eq host_1 or conf_status eq insync or conf_status eq modified").generate() == [
            ["name", "==", "host_1"],
            "||",
            ["conf_status", "==", "insync"],
            "||",
            ["conf_status", "==", "modified"],
        ]
        assert text_to_filter("name eq host_1 or conf_status eq insync and conf_status eq modified").generate() == [
            ["name", "==", "host_1"],
            "||",
            [["conf_status", "==", "insync"], "&&", ["conf_status", "==", "modified"]],
        ]
        assert text_to_filter("(name eq host_1 or conf_status eq insync) and conf_status eq modified").generate() == [
            [
                ["name", "==", "host_1"],
                "||",
                ["conf_status", "==", "insync"],
            ],
            "&&",
            ["conf_status", "==", "modified"],
        ]
        assert text_to_filter("(name eq host_1 or conf_status eq insync)").generate() == [
            ["name", "==", "host_1"],
            "||",
            ["conf_status", "==", "insync"],
        ]
        assert text_to_filter("(name eq host_1 or conf_status eq insync) and conf_status eq modified").generate() == [
            [
                ["name", "==", "host_1"],
                "||",
                ["conf_status", "==", "insync"],
            ],
            "&&",
            ["conf_status", "==", "modified"],
        ]
        assert text_to_filter("(name eq host_1 and (conf_status eq insync or conf_status eq modified))").generate() == [
            ["name", "==", "host_1"],
            "&&",
            [["conf_status", "==", "insync"], "||", ["conf_status", "==", "modified"]],
        ]


class TestFMGObject:
    class TestObj(FMGObject):
        _url: str = "/something/{urlvar}/qwe"
        urlvar: str = Field(None, exclude=True)
        normal: str = None
        excluded: str = Field(None, exclude=True)
        ex_with_alias: str = Field(None, exclude=True, serialization_alias="ex-with-alias")
        excluded_empty: str = Field(None, exclude=True)

    def test_fmo_model_dump_for_filter(self):

        test = self.TestObj(urlvar="qwe", normal="normal", excluded="excluded", ex_with_alias="ex-with-alias")
        for_filter = test.model_dump_for_filter()
        assert for_filter == {"normal": "normal", "excluded": "excluded", "ex-with-alias": "ex-with-alias"}
