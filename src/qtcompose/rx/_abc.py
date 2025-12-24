from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

    from qtcompose.rx._types import Disposable, Observable

T = TypeVar("T")
U = TypeVar("U")


class ObservableBase(Generic[T]):
    def __init__(self) -> None:
        self._subscribers: list[Callable[[T], None]] = []

    def apply(self, func: Callable[[Observable[T]], Observable[U]]) -> Observable[U]:
        return func(self)

    def __or__(self, func: Callable[[Observable[T]], Observable[U]]) -> Observable[U]:
        return self.apply(func)

    def subscribe(self, func: Callable[[T], None]) -> Disposable:
        self._subscribers.append(func)
        return _FuncDisposable(lambda: self._subscribers.remove(func))


class _FuncDisposable:
    def __init__(self, func: Callable[[], None]) -> None:
        self.__func = func
        self.__disposed = False

    def dispose(self) -> None:
        if self.__disposed:
            return

        self.__func()
        self.__disposed = True
