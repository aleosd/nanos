from unittest import mock

import pytest

import nanos

DUMMY_OBJ = mock.Mock()
DUMMY_OBJ.id = 42


@pytest.mark.parametrize(
    "data,expected_idfy",
    [
        ({"id": "a"}, {"a": {"id": "a"}}),
        ([{"id": "a"}], {"a": {"id": "a"}}),
        ([], {}),
        ([{"id": "a"}, {"id": "b"}], {"a": {"id": "a"}, "b": {"id": "b"}}),
        (DUMMY_OBJ, {42: DUMMY_OBJ}),
    ],
)
def test_idfy(data, expected_idfy):
    assert nanos.data.idfy(data) == expected_idfy
