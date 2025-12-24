from __future__ import annotations

from functools import partial
from typing import (
    TYPE_CHECKING,
    Generic,
    TypeVar,
    TypeVarTuple,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from qtcompose.rx._types import Disposable, Observable, Observer, Subscriber

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")
Ts = TypeVarTuple("Ts")


def map_(func: Callable[[T], U]) -> Callable[[Observable[T]], Observable[U]]:
    def _operator(obs: Observable[T]) -> Observable[U]:
        def _subscribe(other: Observer[U]) -> Disposable:
            return obs.subscribe(lambda val: other.push(func(val)))

        return _Observable(_subscribe)

    return _operator


def if_(func: Callable[[T], bool]) -> Callable[[Observable[T]], Observable[T]]:
    def _operator(obs: Observable[T]) -> Observable[T]:
        def _subscribe(other: Observer[T]) -> Disposable:
            return obs.subscribe(
                lambda val: other.push(val) if func(val) is True else None
            )

        return _Observable(_subscribe)

    return _operator


def is_not_none() -> Callable[[Observable[T | None]], Observable[T]]:
    def _operator(obs: Observable[T | None]) -> Observable[T]:
        def _subscribe(other: Observer[T]) -> Disposable:
            return obs.subscribe(
                lambda val: other.push(val) if val is not None else None
            )

        return _Observable(_subscribe)

    return _operator


def as_tuple() -> Callable[[Observable[T]], Observable[tuple[T]]]:
    return map_(lambda v: (v,))


def combine(
    other: Observable[U],
) -> Callable[[Observable[tuple[*Ts]]], Observable[tuple[*Ts, U]]]:
    def _operator(observable: Observable[tuple[*Ts]]) -> Observable[tuple[*Ts, U]]:
        values = {}

        def _update(observer: Observer[tuple[*Ts]], **kwargs) -> None:
            nonlocal values
            values.update(kwargs)

            if ("first" not in values) or ("second" not in values):
                return

            if isinstance(values["first"], tuple):
                observer.push((*values["first"], values["second"]))  # type: ignore
            else:
                observer.push((values["first"], values["second"]))  # type: ignore

        def _subscribe(observer: Observer[tuple]) -> Disposable:
            _updater = partial(_update, observer)
            return _CompositeDisposable(
                [
                    observable.subscribe(lambda v: _updater(first=v)),
                    other.subscribe(lambda v: _updater(second=v)),
                ]
            )

        return _Observable(_subscribe)

    return _operator


def start_with(value: T) -> Callable[[Observable[T]], Observable[T]]:
    def _operator(observable: Observable[T]) -> Observable[T]:
        def _subscribe(other: Observer[T]) -> Disposable:
            other.push(value)
            return observable.subscribe(other.push)

        return _Observable(_subscribe)

    return _operator


def for_(
    func: Callable[[T], U],
) -> Callable[[Observable[Iterable[T]]], Observable[Iterable[U]]]:
    return map_(lambda items: [func(item) for item in items])


class _Observable(Generic[T]):
    def __init__(self, subscribe: Subscriber[T]) -> None:
        self.__subscribe = subscribe

    def apply(self, func: Callable[[Observable[T]], Observable[U]]) -> Observable[U]:
        return func(self)

    def __or__(self, func: Callable[[Observable[T]], Observable[U]]) -> Observable[U]:
        return self.apply(func)

    def subscribe(self, func: Callable[[T], None]) -> Disposable:
        return self.__subscribe(_CallbackObserver(func))


class _CallbackObserver(Generic[T]):
    def __init__(self, func: Callable[[T], None]) -> None:
        self.__func = func

    def push(self, val: T) -> None:
        self.__func(val)


class _CompositeDisposable:
    def __init__(self, disposables: list[Disposable]) -> None:
        self.__disposables = disposables

    def dispose(self) -> None:
        for disposable in self.__disposables:
            disposable.dispose()
