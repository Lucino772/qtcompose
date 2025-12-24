from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, TypeAlias, TypeVar, runtime_checkable

T_co = TypeVar("T_co", covariant=True)
U_contra = TypeVar("U_contra", contravariant=True)
T = TypeVar("T")


@runtime_checkable
class Disposable(Protocol):
    def dispose(self) -> None: ...


@runtime_checkable
class Observable(Protocol[T_co]):
    def apply(
        self, func: Callable[[Observable[T_co]], Observable[U_contra]]
    ) -> Observable[U_contra]: ...

    def __or__(
        self, func: Callable[[Observable[T_co]], Observable[U_contra]]
    ) -> Observable[U_contra]: ...

    def subscribe(self, func: Callable[[T_co], None]) -> Disposable: ...


@runtime_checkable
class Observer(Protocol[U_contra]):
    def push(self, val: U_contra) -> None: ...


Subscriber: TypeAlias = Callable[[Observer[T]], Disposable]
