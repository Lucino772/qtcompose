from __future__ import annotations

from typing import TYPE_CHECKING, NotRequired, TypedDict, TypeVar, Unpack

from qtpy import QtWidgets

from qtcompose.core import LifeCycle, Ref, with_ref
from qtcompose.rx import fn
from qtcompose.ui.buttons.abstract import (
    BindQAbstractButtonProps,
    bind_qabstract_button,
)
from qtcompose.ui.widget import BindQWidgetProps, bind_qwidget
from qtcompose.utils import extract_typeddict, unpack

if TYPE_CHECKING:
    from collections.abc import Callable

    from qtcompose.rx import Observable

T = TypeVar("T", bound=QtWidgets.QPushButton)


class BindQPushButtonProps(TypedDict):
    auto_default: NotRequired[Observable[bool]]
    default: NotRequired[Observable[bool]]
    flat: NotRequired[Observable[bool]]


def bind_qpush_button(
    ref: Ref[T],
    lifecycle: LifeCycle[T],
    **props: Unpack[BindQPushButtonProps],
):
    if "auto_default" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["auto_default"])),
            unpack(QtWidgets.QPushButton.setAutoDefault),
        )
    if "default" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["default"])),
            unpack(QtWidgets.QPushButton.setDefault),
        )
    if "flat" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["flat"])),
            unpack(QtWidgets.QPushButton.setFlat),
        )


class QPushButtonProps(
    BindQPushButtonProps, BindQAbstractButtonProps, BindQWidgetProps, TypedDict
):
    ref: NotRequired[Ref[QtWidgets.QPushButton]]


def QPushButton(  # noqa: N802
    **props: Unpack[QPushButtonProps],
) -> Callable[[], QtWidgets.QPushButton]:
    ref = Ref[QtWidgets.QPushButton]()
    adapter = with_ref(lambda: QtWidgets.QPushButton(), ref, props.get("ref"))

    lc = LifeCycle(ref)
    bind_qwidget(ref, lc, **extract_typeddict(BindQWidgetProps, props))
    bind_qabstract_button(ref, lc, **extract_typeddict(BindQAbstractButtonProps, props))
    bind_qpush_button(ref, lc, **extract_typeddict(BindQPushButtonProps, props))
    return adapter
