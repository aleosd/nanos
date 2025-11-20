from __future__ import annotations

import datetime
import math
import time
import typing as t

DEFAULT_TIMER_PRECISION: t.Final = 2


class Timer:
    """
    Initializes a Timer instance with optional precision.

    Args:
        precision (int): The number of decimal places to use
            for displaying fractional seconds. Defaults to 2.

    Attributes:
        precision (int): Number of decimal places for time display.
        start (float | None): The start time in seconds since epoch, or None
            if not started.
        end (float | None): The end time in seconds since epoch, or None if
            still running.

    Examples:
        Basic synchronous usage with context manager::

            with Timer() as timer:
                time.sleep(1.5)
            print(f"Elapsed: {timer.elapsed}s")
            # Output: Elapsed: 1.5s
            print(timer.verbose())
            # Output: 0:00:01.50

        Asynchronous usage with aiohttp::

            async with Timer() as timer:
                async with aiohttp.ClientSession() as session:
                    response = await session.get('https://api.example.com/data')
                    data = await response.json()
            print(f"API call took: {timer.elapsed}s")

        Asynchronous usage with asyncio::

            async with Timer(precision=3) as timer:
                await asyncio.sleep(2.5)
                result = await some_async_function()
            print(f"Operation completed in {timer.verbose()}")
            # Output: Operation completed in 0:00:02.500

        Manual control without context manager::

            timer = Timer()
            timer.start = time.time()

            # Do some work
            time.sleep(0.5)

            timer.end = time.time()
            print(f"Work took: {timer.elapsed}s")

        Custom precision for high-resolution timing::

            with Timer(precision=4) as timer:
                fast_operation()
            print(timer.verbose())
            # Output: 0:00:00.0123

        Checking elapsed time while timer is still running::

            with Timer() as timer:
                time.sleep(1)
                print(f"After 1 second: {timer.elapsed}s")
                time.sleep(1)
                print(f"After 2 seconds: {timer.elapsed}s")
            print(f"Final: {timer.elapsed}s")

        Using timer in async loops::

            total_timer = Timer()
            total_timer.start = time.time()

            for item in items:
                async with Timer() as request_timer:
                    await process_item(item)
                print(f"Item processed in {request_timer.elapsed}s")

            total_timer.end = time.time()
            print(f"All items processed in {total_timer.verbose()}")

    Note:
        The timer uses ``time.time()`` which measures wall-clock time, not CPU time.
        For CPU time measurement, consider using ``time.process_time()`` or similar.
    """

    def __init__(self, precision: int = DEFAULT_TIMER_PRECISION) -> None:
        self.precision = precision
        self.start: float | None = None
        self.end: float | None = None

    def __enter__(self) -> Timer:
        self.start = time.time()
        return self

    def __exit__(self, *args: t.Any) -> None:
        self.end = time.time()

    # Async context manager methods
    async def __aenter__(self) -> Timer:
        self.start = time.time()
        return self

    async def __aexit__(self, *args: t.Any) -> None:
        self.end = time.time()

    def __str__(self) -> str:
        return self.verbose()

    def __repr__(self) -> str:
        return f"<Timer [start={self.start}, end={self.end}]>"

    def verbose(self) -> str:
        """
        Returns a formatted string representing the elapsed time with a precision
        specified by the Timer instance.

        The elapsed time is formatted as a string in the format of 'H:MM:SS.F',
        where 'H:MM:SS' is the hours, minutes, and seconds, and 'F' is the
        fractional seconds with a number of decimal places equal to the precision.

        Returns:
            str: The formatted elapsed time as a string.
        """
        fraction_seconds, whole_seconds = math.modf(self.elapsed)
        rounded_fraction = round(fraction_seconds, self.precision)
        if rounded_fraction >= 1:
            whole_seconds += 1
            formatted_fraction = "0" * self.precision
        elif fraction_seconds == 0:
            formatted_fraction = "0" * self.precision
        else:
            fraction = int(rounded_fraction * 10**self.precision)
            formatted_fraction = str(fraction).zfill(self.precision)
        return f"{datetime.timedelta(seconds=whole_seconds)}.{formatted_fraction}"

    @property
    def elapsed(self) -> float:
        """
        Calculates the elapsed time in seconds.

        This property computes the difference between the end time and the
        start time of the Timer. If the Timer has not been started, it returns
        0.0. If the Timer is running (i.e., the end time is not set), it uses
        the current time as the end time.

        Returns:
            float: The elapsed time in seconds.
        """
        if not self.start:
            return 0.0
        return (self.end or time.time()) - self.start
