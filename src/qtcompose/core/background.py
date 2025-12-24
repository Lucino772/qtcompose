from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Generic, NotRequired, TypedDict, TypeVar

from qtpy import QtCore

from qtcompose.rx import Subject
from qtcompose.utils import qt_to_background

if TYPE_CHECKING:
    from collections.abc import Callable

    from qtcompose.core import LifeCycle
    from qtcompose.rx import Observable

T = TypeVar("T")
U = TypeVar("U", bound=QtCore.QObject)


def Background(  # noqa: N802
    lifecycle: LifeCycle[U], func: Observable[Callable[[], T]]
) -> Observable[BackgroundState]:
    result = Subject[BackgroundState]({"is_loading": True})

    schedule: Callable[[], None] | None = None

    def _update(function: Callable[[], T]) -> None:
        nonlocal schedule
        schedule = partial(_schedule, result, function)

    lifecycle.subscribe(func, _update)
    lifecycle.on_mount(lambda _: schedule() if schedule else None)

    return result


class BackgroundState(TypedDict, Generic[T]):
    is_loading: bool
    value: NotRequired[T]
    error: NotRequired[Exception]


def _schedule(state: Subject[BackgroundState], func: Callable[[], T]):
    state.push({"is_loading": True})
    QtCore.QTimer.singleShot(
        500, partial(qt_to_background, partial(_execute, state, func))
    )


def _execute(state: Subject[BackgroundState], func: Callable[[], T]):
    state.push({"is_loading": True})
    try:
        val = func()
    except Exception as err:  # noqa: BLE001
        state.push({"is_loading": False, "error": err})
    else:
        state.push({"is_loading": False, "value": val})
