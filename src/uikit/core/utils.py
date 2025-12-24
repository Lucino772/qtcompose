from collections.abc import Callable
from typing import Any, TypeVar

from qtpy import QtCore

from uikit.core import LifeCycle, Ref
from uikit.rx import Observable, fn

T = TypeVar("T")
T_widget = TypeVar("T_widget", bound=QtCore.QObject)


def bind_signal(
    lifecycle: LifeCycle[T_widget],
    ref: Ref[T_widget],
    get_signal: Callable[[T_widget], QtCore.SignalInstance],  # type: ignore
    callback: Observable[Callable[..., Any]],
):
    signal_conn: QtCore.QMetaObject.Connection | None = None

    def _signal_updater(signal: QtCore.SignalInstance, value: Callable[..., Any]):  # type: ignore
        nonlocal signal_conn
        if signal_conn is not None:
            signal.disconnect(signal_conn)
        signal_conn = signal.connect(value)

    lifecycle.subscribe(
        fn.pipe(
            ref,
            fn.map_(get_signal),
            fn.as_tuple(),
            fn.combine(callback),
        ),
        lambda val: _signal_updater(val[0], val[1]),
    )


def with_ref(factory: Callable[[], T], /, *refs: Ref[T] | None) -> Callable[[], T]:
    def _factory() -> T:
        obj = factory()
        for ref in refs:
            if ref is not None:
                ref.push(obj)
        return obj

    return _factory
