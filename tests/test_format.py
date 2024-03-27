import pytest
from hamcrest import assert_that, equal_to

from nanos import fmt


@pytest.mark.parametrize(
    "size_bytes, precision, expected_format",
    [
        (0, 1, "0.0 B"),
        (0, 0, "0 B"),
        (1, 1, "1.0 B"),
        (1023, 1, "1023.0 B"),
        (1024, 1, "1.0 KiB"),
        (1050, 2, "1.03 KiB"),
        (1050, 1, "1.0 KiB"),
        (1050, 0, "1 KiB"),
        (1050**9, 1, "1283.2 YiB"),
    ],
)
def test__size(size_bytes: int, precision: int, expected_format: str) -> None:
    assert_that(fmt.size(size_bytes, precision), equal_to(expected_format))
