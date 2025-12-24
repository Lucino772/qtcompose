from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, cast

from qtcompose.rx._abc import ObservableBase

if TYPE_CHECKING:
    from collections.abc import Callable

    from qtcompose.rx._types import Disposable

T = TypeVar("T")


class Subject(ObservableBase[T]):
    def __init__(self, initial: T, /) -> None:
        super().__init__()

        self.__value = initial

    def subscribe(self, func: Callable[[T], None]) -> Disposable:
        func(self.__value)
        return super().subscribe(func)

    def push(self, val: T | Callable[[T], T]) -> None:
        if callable(val):
            self.__value = cast(T, val(self.__value))
        else:
            self.__value = cast(T, val)

        for subscriber in self._subscribers:
            subscriber(self.__value)
