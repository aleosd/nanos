import datetime


def days_after_now(
    days_num: int = 1, tz: datetime.tzinfo | None = datetime.timezone.utc
) -> datetime.datetime:
    """
    Returns a datetime object representing the date that is `days_num` days after now.

    By default, `days_num` is 1, so the function will return tomorrow's date by default.
    The timezone is set to `datetime.timezone.utc` by default.

    Parameters
    ----------
    days_num : int, optional
        The number of days after now. Defaults to 1.
    tz : datetime.tzinfo, optional
        The timezone to use. Defaults to :class:`datetime.timezone.utc`.

    Returns
    -------
    datetime.datetime
        The date that is `days_num` days after now.
    """
    return datetime.datetime.now(tz=tz) + datetime.timedelta(days=days_num)


def tomorrow(tz: datetime.tzinfo | None = datetime.timezone.utc) -> datetime.datetime:
    return days_after_now(tz=tz)


def days_before_now(
    days_num: int = 1, tz: datetime.tzinfo | None = datetime.timezone.utc
) -> datetime.datetime:
    return days_after_now(-days_num, tz=tz)


def yesterday(tz: datetime.tzinfo | None = datetime.timezone.utc) -> datetime.datetime:
    return days_before_now(tz=tz)


def yesterday_start(tz: datetime.tzinfo | None = datetime.timezone.utc) -> datetime.datetime:
    return datetime.datetime.combine(yesterday(tz=tz), datetime.datetime.min.time()).replace(
        tzinfo=tz
    )


def yesterday_end(tz: datetime.tzinfo | None = datetime.timezone.utc) -> datetime.datetime:
    return datetime.datetime.combine(yesterday(tz=tz), datetime.datetime.max.time()).replace(
        tzinfo=tz
    )


def today_eod(tz: datetime.tzinfo = datetime.timezone.utc) -> datetime.datetime:
    today = datetime.datetime.now().date()
    return datetime.datetime.combine(today, datetime.datetime.max.time()).replace(tzinfo=tz)
