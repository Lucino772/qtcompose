from __future__ import annotations

from typing import TYPE_CHECKING, Any, NotRequired, TypedDict, TypeVar, Unpack

from qtpy import QtCore, QtGui, QtWidgets

from qtcompose.core import LifeCycle, Ref, bind_signal, with_ref
from qtcompose.rx import Observable, fn
from qtcompose.ui.buttons.abstract import (
    BindQAbstractButtonProps,
    bind_qabstract_button,
)
from qtcompose.ui.widget import BindQWidgetProps, bind_qwidget
from qtcompose.utils import extract_typeddict, unpack

if TYPE_CHECKING:
    from collections.abc import Callable

T = TypeVar("T", bound=QtWidgets.QToolButton)


class BindQToolButtonProps(TypedDict):
    arrow_type: NotRequired[Observable[QtCore.Qt.ArrowType]]
    auto_raise: NotRequired[Observable[bool]]
    popup_mode: NotRequired[Observable[QtWidgets.QToolButton.ToolButtonPopupMode]]
    tool_button_styles: NotRequired[Observable[QtCore.Qt.ToolButtonStyle]]

    # Signals
    on_trigger: NotRequired[Observable[Callable[[QtGui.QAction], Any]]]  # type: ignore


def bind_qtoolbutton(
    ref: Ref[T], lifecycle: LifeCycle[T], **props: Unpack[BindQToolButtonProps]
):
    if "arrow_type" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["arrow_type"])),
            unpack(QtWidgets.QToolButton.setArrowType),
        )
    if "auto_raise" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["auto_raise"])),
            unpack(QtWidgets.QToolButton.setAutoRaise),
        )
    if "popup_mode" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["popup_mode"])),
            unpack(QtWidgets.QToolButton.setPopupMode),
        )
    if "tool_button_styles" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["tool_button_styles"])),
            unpack(QtWidgets.QToolButton.setToolButtonStyle),
        )
    if "on_trigger" in props:
        bind_signal(lifecycle, ref, lambda w: w.triggered, props["on_trigger"])


class QToolButtonProps(
    BindQToolButtonProps, BindQAbstractButtonProps, BindQWidgetProps, TypedDict
):
    ref: Ref[QtWidgets.QToolButton]


def QToolButton(**props: Unpack[QToolButtonProps]):  # noqa: N802
    ref = Ref[QtWidgets.QToolButton]()
    adapter = with_ref(lambda: QtWidgets.QToolButton(), ref, props.get("ref"))

    lc = LifeCycle(ref)
    bind_qwidget(ref, lc, **extract_typeddict(BindQWidgetProps, props))
    bind_qabstract_button(ref, lc, **extract_typeddict(BindQAbstractButtonProps, props))
    bind_qtoolbutton(ref, lc, **extract_typeddict(BindQToolButtonProps, props))
    return adapter
