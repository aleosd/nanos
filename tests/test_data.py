from unittest import mock

import pytest
from hamcrest import assert_that, equal_to

import nanos

DUMMY_OBJ = mock.Mock()
DUMMY_OBJ.id = 42


def dummy_generator():
    for number in range(1, 3):
        yield {"id": number, "field": str(number)}


@pytest.mark.parametrize(
    "data,expected_idfy",
    [
        ({"id": "a"}, {"a": {"id": "a"}}),
        ([{"id": "a"}], {"a": {"id": "a"}}),
        ([], {}),
        ([{"id": "a"}, {"id": "b"}], {"a": {"id": "a"}, "b": {"id": "b"}}),
        (DUMMY_OBJ, {42: DUMMY_OBJ}),
        (dummy_generator(), {1: {"id": 1, "field": "1"}, 2: {"id": 2, "field": "2"}}),
    ],
)
def test_idfy(data, expected_idfy):
    assert nanos.data.idfy(data) == expected_idfy


@pytest.mark.parametrize(
    "input_obj, expected_output",
    [
        ([], None),
        (0, 0),
        (1, 1),
        ((), ()),
        ("", None),
        ({}, None),
        (["a"], ["a"]),
        ([""], None),
        (["", None, [], {}], None),
        (["foo", ""], ["foo"]),
        ({"foo": "bar"}, {"foo": "bar"}),
        ({"foo": ""}, None),
        ({"foo": "", "bar": [1, 2, ""], "baz": ["", ""]}, {"bar": [1, 2]}),
    ],
)
def test__remove_empty_members__default_empty(input_obj, expected_output):
    assert_that(nanos.data.remove_empty_members(input_obj), equal_to(expected_output))
