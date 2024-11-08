import datetime
from unittest import mock

import pytest
from hamcrest import assert_that, equal_to

from nanos import dt


@pytest.fixture
def mocked_datetime():
    with mock.patch("nanos.dt.datetime") as m:
        m.timedelta = datetime.timedelta
        yield m


@pytest.mark.parametrize(
    "fake_now, days_num, expected_result",
    [
        (
            datetime.datetime(2023, 2, 2, 14, 15, 2, 999888),
            1,
            datetime.datetime(2023, 2, 3, 14, 15, 2, 999888),
        ),
        (
            datetime.datetime(2023, 2, 2, 14, 15, 2, 999888),
            2,
            datetime.datetime(2023, 2, 4, 14, 15, 2, 999888),
        ),
        (
            datetime.datetime(2023, 2, 2, 14, 15, 2, 999888),
            0,
            datetime.datetime(2023, 2, 2, 14, 15, 2, 999888),
        ),
    ],
)
def test__days_after_now__days_num(mocked_datetime, fake_now, days_num, expected_result):
    # given
    mocked_datetime.datetime.now.return_value = fake_now

    # when
    days_after_now = dt.days_after_now(days_num)

    # then
    assert_that(days_after_now, equal_to(expected_result))


@pytest.mark.parametrize(
    "fake_now, tz, expected_result",
    [
        (
            datetime.datetime(2023, 2, 2, 14, 15, 2, 999888),
            datetime.timezone.utc,
            datetime.datetime(2023, 2, 3, 14, 15, 2, 999888),
        ),
        (
            datetime.datetime(2023, 2, 2, 14, 15, 2, 999888),
            None,
            datetime.datetime(2023, 2, 4, 14, 15, 2, 999888),
        ),
    ],
)
def test__days_after_now__tz(mocked_datetime, fake_now, tz, expected_result):
    # given
    mocked_datetime.datetime.now.return_value = fake_now

    # when
    _ = dt.days_after_now(tz=tz)

    # then
    mocked_datetime.datetime.now.assert_called_once_with(tz=tz)


def test__days_after_now__default_args(mocked_datetime):
    # arrange
    fake_now = datetime.datetime(2023, 2, 2, 14, 15, 2, 999888)
    mocked_datetime.datetime.now.return_value = fake_now
    expected_result = datetime.datetime(2023, 2, 3, 14, 15, 2, 999888)

    # when
    result = dt.days_after_now()

    # then
    assert_that(result, equal_to(expected_result))
    mocked_datetime.datetime.now.assert_called_once_with(tz=datetime.timezone.utc)


def test__yesterday_start__default_tz():
    # arrange
    yesterday_dt = datetime.datetime(2023, 2, 2, 14, 15, 2, 999888, tzinfo=datetime.timezone.utc)
    expected_result = datetime.datetime(2023, 2, 2, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)

    # when
    with mock.patch("nanos.dt.yesterday") as m:
        m.return_value = yesterday_dt
        result = dt.yesterday_start()

    # then
    m.assert_called_once_with(tz=datetime.timezone.utc)
    assert_that(result, equal_to(expected_result))


def test__yesterday_start__no_tz():
    # arrange
    yesterday_dt = datetime.datetime(2023, 2, 2, 14, 15, 2, 999888)
    expected_result = datetime.datetime(2023, 2, 2, 0, 0, 0, 0)

    # when
    with mock.patch("nanos.dt.yesterday") as m:
        m.return_value = yesterday_dt
        result = dt.yesterday_start(tz=None)

    # then
    m.assert_called_once_with(tz=None)
    assert_that(result, equal_to(expected_result))


def test__yesterday_end():
    # arrange
    yesterday_dt = datetime.datetime(2023, 2, 2, 14, 15, 2, 999888, tzinfo=datetime.timezone.utc)
    expected_result = datetime.datetime(
        2023, 2, 2, 23, 59, 59, 999999, tzinfo=datetime.timezone.utc
    )

    # when
    with mock.patch("nanos.dt.yesterday") as m:
        m.return_value = yesterday_dt
        result = dt.yesterday_end()

    # then
    m.assert_called_once_with(tz=datetime.timezone.utc)
    assert_that(result, equal_to(expected_result))
