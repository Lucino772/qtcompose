from __future__ import annotations

from typing import TYPE_CHECKING, Any, NotRequired, TypedDict, TypeVar, Unpack

from qtpy import QtCore, QtGui, QtWidgets

from qtcompose.core import LifeCycle, Ref, bind_signal
from qtcompose.rx import fn
from qtcompose.utils import unpack

if TYPE_CHECKING:
    from collections.abc import Callable

    from qtcompose.rx import Observable


T = TypeVar("T", bound=QtWidgets.QAbstractButton)


class BindQAbstractButtonProps(TypedDict):
    auto_exclusive: NotRequired[Observable[bool]]
    auto_repeat: NotRequired[Observable[bool]]
    auto_repeat_delay: NotRequired[Observable[int]]
    auto_repeat_interval: NotRequired[Observable[int]]
    checkable: NotRequired[Observable[bool]]
    checked: NotRequired[Observable[bool]]
    down: NotRequired[Observable[bool]]
    icon: NotRequired[Observable[QtGui.QIcon]]
    icon_size: NotRequired[Observable[QtCore.QSize]]
    shortcut: NotRequired[Observable[QtGui.QKeySequence]]
    text: NotRequired[Observable[str]]

    # Signals
    on_click: NotRequired[Observable[Callable[[bool], Any]]]
    on_press: NotRequired[Observable[Callable[[], Any]]]
    on_release: NotRequired[Observable[Callable[[], Any]]]
    on_toggle: NotRequired[Observable[Callable[[bool], Any]]]


def bind_qabstract_button(
    ref: Ref[T],
    lifecycle: LifeCycle[T],
    **props: Unpack[BindQAbstractButtonProps],
):
    if "auto_exclusive" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["auto_exclusive"])),
            unpack(QtWidgets.QAbstractButton.setAutoExclusive),
        )
    if "auto_repeat" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["auto_repeat"])),
            unpack(QtWidgets.QAbstractButton.setAutoRepeat),
        )
    if "auto_repeat_delay" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["auto_repeat_delay"])),
            unpack(QtWidgets.QAbstractButton.setAutoRepeatDelay),
        )
    if "auto_repeat_interval" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["auto_repeat_interval"])),
            unpack(QtWidgets.QAbstractButton.setAutoRepeatInterval),
        )
    if "checkable" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["checkable"])),
            unpack(QtWidgets.QAbstractButton.setCheckable),
        )
    if "checked" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["checked"])),
            unpack(QtWidgets.QAbstractButton.setChecked),
        )
    if "down" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["down"])),
            unpack(QtWidgets.QAbstractButton.setDown),
        )
    if "icon" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["icon"])),
            unpack(QtWidgets.QAbstractButton.setIcon),
        )
    if "icon_size" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["icon_size"])),
            unpack(QtWidgets.QAbstractButton.setIconSize),
        )
    if "shortcut" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["shortcut"])),
            unpack(QtWidgets.QAbstractButton.setShortcut),
        )
    if "text" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["text"])),
            unpack(QtWidgets.QAbstractButton.setText),
        )
    if "on_click" in props:
        bind_signal(lifecycle, ref, lambda w: w.clicked, props["on_click"])
    if "on_press" in props:
        bind_signal(lifecycle, ref, lambda w: w.pressed, props["on_press"])
    if "on_release" in props:
        bind_signal(lifecycle, ref, lambda w: w.released, props["on_release"])
    if "on_toggle" in props:
        bind_signal(lifecycle, ref, lambda w: w.toggled, props["on_toggle"])
