from __future__ import annotations

from typing import TYPE_CHECKING, Any, NotRequired, TypedDict, TypeVar, Unpack

from qtpy import QtCore, QtWidgets

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

T = TypeVar("T", bound=QtWidgets.QCheckBox)


class BindQCheckBoxProps(TypedDict):
    tristate: NotRequired[Observable[bool]]

    # Signals
    on_check_state_change: NotRequired[
        Observable[Callable[[QtCore.Qt.CheckState], Any]]
    ]


def bind_qcheckbox(
    ref: Ref[T],
    lifecycle: LifeCycle[T],
    **props: Unpack[BindQCheckBoxProps],
):
    if "tristate" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["tristate"])),
            unpack(QtWidgets.QCheckBox.setTristate),
        )
    if "on_check_state_change" in props:
        bind_signal(
            lifecycle,
            ref,
            lambda w: w.checkStateChanged,
            props["on_check_state_change"],
        )


class QCheckBoxProps(
    BindQCheckBoxProps, BindQAbstractButtonProps, BindQWidgetProps, TypedDict
):
    ref: NotRequired[Ref[QtWidgets.QCheckBox]]


def QCheckBox(**props: Unpack[QCheckBoxProps]) -> Callable[[], QtWidgets.QCheckBox]:  # noqa: N802
    ref = Ref[QtWidgets.QCheckBox]()
    adapter = with_ref(lambda: QtWidgets.QCheckBox(), ref, props.get("ref"))
    lc = LifeCycle(ref)
    bind_qwidget(ref, lc, **extract_typeddict(BindQWidgetProps, props))
    bind_qabstract_button(ref, lc, **extract_typeddict(BindQAbstractButtonProps, props))
    bind_qcheckbox(ref, lc, **extract_typeddict(BindQCheckBoxProps, props))
    return adapter
