from __future__ import annotations

from typing import TYPE_CHECKING, NotRequired, TypedDict, TypeVar, Unpack

from qtpy import QtCore, QtGui, QtWidgets

from qtcompose.core import LifeCycle, Ref, with_ref
from qtcompose.rx import fn
from qtcompose.ui.widget import (
    BindQWidgetProps,
    bind_qwidget,
)
from qtcompose.utils import extract_typeddict, unpack

if TYPE_CHECKING:
    from collections.abc import Callable

    from qtcompose.rx import Observable

T_widget = TypeVar("T_widget", bound=QtWidgets.QLabel)


class BindQLabelProps(TypedDict):
    alignment: NotRequired[Observable[QtCore.Qt.AlignmentFlag]]
    indent: NotRequired[Observable[int]]
    margin: NotRequired[Observable[int]]
    open_external_links: NotRequired[Observable[bool]]
    pixmap: NotRequired[Observable[QtGui.QPixmap]]
    scaled_contents: NotRequired[Observable[bool]]
    text: NotRequired[Observable[str]]
    text_format: NotRequired[Observable[QtCore.Qt.TextFormat]]
    text_interaction_flags: NotRequired[Observable[QtCore.Qt.TextInteractionFlag]]
    word_wrap: NotRequired[Observable[bool]]


def bind_qlabel(
    ref: Ref[T_widget],
    lifecycle: LifeCycle[T_widget],
    **props: Unpack[BindQLabelProps],
):
    if "alignment" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["alignment"])),
            unpack(QtWidgets.QLabel.setAlignment),
        )
    if "indent" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["indent"])),
            unpack(QtWidgets.QLabel.setIndent),
        )
    if "margin" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["margin"])),
            unpack(QtWidgets.QLabel.setMargin),
        )
    if "open_external_links" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["open_external_links"])),
            unpack(QtWidgets.QLabel.setOpenExternalLinks),
        )
    if "pixmap" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["pixmap"])),
            unpack(QtWidgets.QLabel.setPixmap),
        )
    if "scaled_contents" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["scaled_contents"])),
            unpack(QtWidgets.QLabel.setScaledContents),
        )
    if "text" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["text"])),
            unpack(QtWidgets.QLabel.setText),
        )
    if "text_format" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["text_format"])),
            unpack(QtWidgets.QLabel.setTextFormat),
        )
    if "text_interaction_flags" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["text_interaction_flags"])),
            unpack(QtWidgets.QLabel.setTextInteractionFlags),
        )
    if "word_wrap" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["word_wrap"])),
            unpack(QtWidgets.QLabel.setWordWrap),
        )


class QLabelProps(BindQWidgetProps, BindQLabelProps, TypedDict):
    ref: NotRequired[Ref[QtWidgets.QLabel]]


def QLabel(**props: Unpack[QLabelProps]) -> Callable[[], QtWidgets.QLabel]:  # noqa: N802
    ref = Ref[QtWidgets.QLabel]()
    adapter = with_ref(lambda: QtWidgets.QLabel(), ref, props.get("ref"))

    lc = LifeCycle(ref)
    bind_qwidget(ref, lc, **extract_typeddict(BindQWidgetProps, props))
    bind_qlabel(ref, lc, **extract_typeddict(BindQLabelProps, props))
    return adapter
