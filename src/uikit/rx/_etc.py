from __future__ import annotations

from typing import TypeVar

from uikit.rx import Observable, Subject

T = TypeVar("T")


def as_observable(value: Observable[T] | T) -> Observable[T]:
    if isinstance(value, Observable):
        return value
    return Subject(value)
