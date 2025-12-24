from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, TypeAlias, TypeVar

T_co = TypeVar("T_co", covariant=True)
U_contra = TypeVar("U_contra", contravariant=True)
T = TypeVar("T")


class Disposable(Protocol):
    def dispose(self) -> None: ...


class Observable(Protocol[T_co]):
    def apply(
        self, func: Callable[[Observable[T_co]], Observable[U_contra]]
    ) -> Observable[U_contra]: ...

    def __or__(
        self, func: Callable[[Observable[T_co]], Observable[U_contra]]
    ) -> Observable[U_contra]: ...

    def subscribe(self, func: Callable[[T_co], None]) -> Disposable: ...


class Observer(Protocol[U_contra]):
    def push(self, val: U_contra) -> None: ...


Subscriber: TypeAlias = Callable[[Observer[T]], Disposable]
