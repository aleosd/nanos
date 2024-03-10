from __future__ import annotations

import datetime
import time
import typing as t


class Timer:
    def __init__(self) -> None:
        self.start: float | None = None
        self.end: float | None = None

    def __enter__(self) -> Timer:
        self.start = time.time()
        return self

    def __exit__(self, *args: t.Any) -> None:
        self.end = time.time()

    def __str__(self) -> str:
        return self.verbose()

    def __repr__(self) -> str:
        return self.verbose()

    def verbose(self) -> str:
        time_run = datetime.timedelta(seconds=self.elapsed)
        seconds = int(time_run.total_seconds())
        microseconds = time_run.total_seconds() - seconds
        result = f"{datetime.timedelta(seconds=seconds)}"
        if microseconds:
            result = f"{result}.{int(microseconds * 1000)}"
        return result

    @property
    def elapsed(self) -> float:
        assert self.start is not None, "Timer wasn't started"
        assert self.end is not None, "Timer hasn't finished yet"
        return self.end - self.start
