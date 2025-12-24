from __future__ import annotations

import functools
from functools import partial
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from qtpy import QtCore

from qtcompose.rx import Observable, Subject, fn
from qtcompose.utils import qt_ensure_ui_thread, unpack

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from qtcompose.rx import Disposable

T = TypeVar("T")
U = TypeVar("U")

T_widget = TypeVar("T_widget", bound=QtCore.QObject)


class LifeCycle(Generic[T_widget]):
    def __init__(self, ref: Ref[T_widget]) -> None:
        self.__subscriptions = [ref.subscribe(self._bind)]
        self.__mounted_callbacks: list[
            Callable[[T_widget], Callable[[], Any] | None]
        ] = []

    def subscribe(
        self,
        source: Observable[T],
        func: Callable[[T], Any],
        *,
        ensure_ui_thread: bool = True,
    ) -> None:
        # TODO: Add lazy option (subscribe only when mounted)
        _func = func if ensure_ui_thread is False else qt_ensure_ui_thread(func)
        self.__subscriptions.append(source.subscribe(_func))

    def on_mount(self, func: Callable[[T_widget], Callable[[], Any] | None]):
        self.__mounted_callbacks.append(func)

    def _bind(self, widget: T_widget | None) -> None:
        if widget is None:
            return

        def _cleanup(
            subscriptions: list[Disposable], callbacks: list[Callable[[], Any]]
        ):
            for sub in subscriptions:
                sub.dispose()
            for callback in callbacks:
                callback()

        unmount_callbacks = [
            func
            for callback in self.__mounted_callbacks
            if (func := callback(widget)) is not None
        ]

        # TODO: Initialize all subscriptions
        widget.destroyed.connect(
            partial(_cleanup, self.__subscriptions, unmount_callbacks)
        )


class Ref(Generic[T]):
    def __init__(self) -> None:
        self.__subject = Subject[T | None](None)

    def apply(self, func: Callable[[Observable[T]], Observable[U]]) -> Observable[U]:
        return self.__subject.apply(fn.is_not_none()).apply(func)

    def __or__(self, func: Callable[[Observable[T]], Observable[U]]) -> Observable[U]:
        return self.apply(func)

    def subscribe(self, func: Callable[[T], None]) -> Disposable:
        return self.__subject.apply(fn.is_not_none()).subscribe(func)

    def push(self, val: T) -> None:
        return self.__subject.push(val)


def Fallback(data: Observable[T], fallback: U) -> Observable[T | U]:  # noqa: N802
    return fn.pipe(data, fn.start_with(fallback))


def For(items: Observable[Iterable[T]], render: Callable[[T], U]):  # noqa: N802
    return fn.pipe(items, fn.for_(render))


def Map(data: Observable[T], render: Callable[[T], U]):  # noqa: N802
    return fn.pipe(data, fn.map_(render))


def Merge(  # noqa: N802
    *items: Observable[Iterable[T]] | Iterable[Observable[T]],
):
    observable = Subject[list[T]]([])
    return functools.reduce(
        lambda prev, current: fn.pipe(
            prev,
            fn.as_tuple(),
            fn.combine(current),
            fn.map_(unpack(lambda a, b: [*a, *b])),
        ),
        [_process_merge_item(item) for item in items],
        observable,
    )


def _process_merge_item(
    item: Observable[Iterable[T]] | Iterable[Observable[T]],
):
    observable = Subject[list[T]]([])

    if isinstance(item, Observable):
        return fn.pipe(
            observable,
            fn.as_tuple(),
            fn.combine(item),
            fn.map_(unpack(lambda a, b: [*a, *b])),
        )

    return functools.reduce(
        lambda prev, current: fn.pipe(
            prev,
            fn.as_tuple(),
            fn.combine(current),
            fn.map_(unpack(lambda a, b: [*a, b])),
        ),
        item,
        observable,
    )
