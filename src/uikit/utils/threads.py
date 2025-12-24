from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Generic, ParamSpec

from qtpy.QtCore import (
    QMetaObject,
    QObject,
    QThreadPool,
    Signal,  # type: ignore
    Slot,  # type: ignore
)
from qtpy.QtWidgets import QApplication

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")


def qt_to_background(
    callback: Callable[[], None], thread_pool: QThreadPool | None = None
):
    if thread_pool is None:
        thread_pool = QThreadPool.globalInstance()

    thread_pool.start(callback)  # type: ignore


def qt_ensure_ui_thread(
    func: Callable[P, Any], *, parent: QObject | None = None
) -> Callable[P, Any]:
    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs):
        nonlocal parent
        if parent is None:
            parent = QApplication.instance()
        if parent is None:
            msg = "A instance of a Qt Application must exit or parent must be set manually"
            raise RuntimeError(msg)

        return _QtUiThreadFunc(parent, func, *args, **kwargs)()

    return _wrapper


class _QtUiThreadFunc(Generic[P], QObject):
    finished = Signal(object)

    def __init__(
        self, parent: QObject, func: Callable[P, Any], *args: P.args, **kwargs: P.kwargs
    ):
        super().__init__()
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

        self.moveToThread(parent.thread())
        self.setParent(parent)

    @Slot()  # type: ignore
    def execute(self):
        ret = self.__func(*self.__args, **self.__kwargs)
        self.finished.emit(ret)  # type: ignore

    def __call__(self) -> None:
        QMetaObject.invokeMethod(self, "execute")  # type: ignore
