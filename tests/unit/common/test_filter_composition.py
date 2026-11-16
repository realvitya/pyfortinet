"""Filter composition must preserve predicates and grouping."""

import operator

import pytest

from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.firewall import Address
from tests.unit.conftest import resolve


@pytest.mark.parametrize("combine, symbol", [(operator.and_, "&&"), (operator.or_, "||")])
def test_combining_list_with_complex_filter_preserves_both_sides(client, post, combine, symbol):
    left = combine(F(name="first"), F(name="second"))
    right = (F(comment="a") | F(comment="b")) & F(type="ipmask")
    original = left.generate()
    expected = [original, symbol, right.generate()]
    combined = combine(left, right)
    assert combined.generate() == expected
    assert left.generate() == original
    post.return_value = {"data": []}
    resolve(client.get(Address, filters=combined))
    assert post.call_args.kwargs["request"]["params"][0]["filter"] == expected


@pytest.mark.parametrize("combine", [operator.and_, operator.or_])
def test_implicit_or_preserves_explicit_grouping(combine):
    left = F(name="first") + F(name="second")
    right = combine(F(comment="a"), F(type="ipmask"))
    expected = [left.generate(), right.generate()]
    assert (left + right).generate() == expected
