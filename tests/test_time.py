from unittest import mock

import pytest
from hamcrest import assert_that, close_to, equal_to

from nanos.time import Timer


@pytest.fixture
def timer() -> Timer:
    timer_instance = Timer()
    timer_instance.start = 123.456789
    timer_instance.end = 987.654321
    return timer_instance


class TestTimer:
    def test__repr(self, timer: Timer) -> None:
        expected_repr = "<Timer [start=123.456789, end=987.654321]>"
        assert_that(repr(timer), equal_to(expected_repr))

    @pytest.mark.parametrize(
        "precision, expected_verbose",
        [
            (3, "0:14:24.198"),
            (2, "0:14:24.20"),
            (1, "0:14:24.2"),
        ],
    )
    def test__verbose(self, timer: Timer, precision, expected_verbose) -> None:
        timer.precision = precision
        assert_that(timer.verbose(), equal_to(expected_verbose))

    @pytest.mark.parametrize(
        "start, end, expected_elapsed",
        [
            (None, None, 0.0),
            (None, 1, 0.0),
            (2.14, 3.15, 1.01),
            (2.14, None, 121.316789),
        ],
    )
    def test__elapsed(self, start: float | None, end: float | None, expected_elapsed: float):
        with mock.patch("nanos.time.time") as patched_time:
            timer = Timer()
            timer.start = start
            timer.end = end
            patched_time.time.return_value = 123.456789
            assert_that(timer.elapsed, close_to(expected_elapsed, 0.01))

    def test__context_manager(self) -> None:
        time_return_value = 123.456789
        with mock.patch("nanos.time.time") as patched_time:
            patched_time.time.return_value = time_return_value
            with Timer() as t:
                ...

        assert_that(t.start, equal_to(time_return_value))
        assert_that(t.end, equal_to(time_return_value))
        assert_that(patched_time.time.call_count, equal_to(2))

    def test__str(self, timer: Timer) -> None:
        with mock.patch.object(timer, "verbose", return_value="foo"):
            assert_that(str(timer), equal_to("foo"))
            timer.verbose.assert_called_once()
