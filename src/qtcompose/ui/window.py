from __future__ import annotations

from typing import TYPE_CHECKING, NotRequired, TypedDict, Unpack

from qtpy import QtGui, QtWidgets

from qtcompose.core import LifeCycle, Ref, with_ref
from qtcompose.rx import fn
from qtcompose.ui.widget import BindQWidgetProps
from qtcompose.utils import unpack

if TYPE_CHECKING:
    from collections.abc import Callable

    from qtcompose.rx import Observable


class QMainWindowProps(BindQWidgetProps, TypedDict):
    ref: NotRequired[Ref[QtWidgets.QMainWindow]]
    title: NotRequired[Observable[str]]
    icon: NotRequired[Observable[QtGui.QIcon]]
    children: NotRequired[Observable[Callable[[], QtWidgets.QWidget]]]


def QMainWindow(**props: Unpack[QMainWindowProps]):  # noqa: N802
    ref = Ref[QtWidgets.QMainWindow]()
    adapter = with_ref(lambda: QtWidgets.QMainWindow(), ref, props.get("ref"))
    lc = LifeCycle(ref)
    if "title" in props:
        lc.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["title"])),
            unpack(QtWidgets.QMainWindow.setWindowTitle),
        )
    if "icon" in props:
        lc.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["icon"])),
            unpack(QtWidgets.QMainWindow.setWindowIcon),
        )
    if "children" in props:
        lc.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["children"])),
            unpack(_update_children),
        )

    return adapter


def _update_children(
    widget: QtWidgets.QMainWindow, children: Callable[[], QtWidgets.QWidget]
):
    current = widget.takeCentralWidget()
    if current is not None:
        current.deleteLater()

    if children is not None:
        widget.setCentralWidget(children())
