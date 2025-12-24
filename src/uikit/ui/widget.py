from __future__ import annotations

from typing import TYPE_CHECKING, Any, NotRequired, TypedDict, Unpack

from qtpy import QtCore, QtGui, QtWidgets

from uikit.core import LifeCycle, Ref, bind_signal, with_ref
from uikit.rx import fn
from uikit.utils import extract_typeddict, unpack

if TYPE_CHECKING:
    from collections.abc import Callable

    from uikit.rx import Observable


class BindQWidgetProps(TypedDict):
    attributes: NotRequired[Observable[dict[QtCore.Qt.WidgetAttribute, bool]]]
    accept_drops: NotRequired[Observable[bool]]
    accessible_description: NotRequired[Observable[str]]
    accessible_name: NotRequired[Observable[str]]
    auto_fill_background: NotRequired[Observable[bool]]
    base_size: NotRequired[Observable[QtCore.QSize]]
    context_menu_policy: NotRequired[Observable[QtCore.Qt.ContextMenuPolicy]]
    cursor: NotRequired[
        Observable[QtGui.QCursor | QtCore.Qt.CursorShape | QtGui.QPixmap | None]
    ]
    enabled: NotRequired[Observable[bool]]
    focus: NotRequired[Observable[bool]]
    focus_policy: NotRequired[Observable[QtCore.Qt.FocusPolicy]]
    font: NotRequired[Observable[QtGui.QFont]]
    height: NotRequired[Observable[int]]
    input_method_hints: NotRequired[Observable[QtCore.Qt.InputMethodHint]]
    locale: NotRequired[Observable[QtCore.QLocale | None]]
    layout: NotRequired[Observable[Callable[[], QtWidgets.QLayout]]]
    maximum_height: NotRequired[Observable[int]]
    maximum_size: NotRequired[Observable[QtCore.QSize]]
    maximum_width: NotRequired[Observable[int]]
    minimum_height: NotRequired[Observable[int]]
    minimum_size: NotRequired[Observable[QtCore.QSize]]
    minimum_width: NotRequired[Observable[int]]
    mouse_tracking: NotRequired[Observable[bool]]
    object_name: NotRequired[Observable[str]]
    parent: NotRequired[Observable[QtWidgets.QWidget]]
    properties: NotRequired[Observable[dict[str, Any]]]
    size: NotRequired[Observable[QtCore.QSize]]
    size_policy: NotRequired[Observable[QtWidgets.QSizePolicy]]
    status_tip: NotRequired[Observable[str]]
    stylesheet: NotRequired[Observable[str]]
    tablet_tracking: NotRequired[Observable[bool]]
    tooltip: NotRequired[Observable[str]]
    visible: NotRequired[Observable[bool]]
    width: NotRequired[Observable[int]]

    # Events
    on_destroy: NotRequired[Observable[Callable[[QtWidgets.QWidget], Any]]]


def bind_qwidget(
    ref: Ref[QtWidgets.QWidget],
    lifecycle: LifeCycle[QtWidgets.QWidget],
    **props: Unpack[BindQWidgetProps],
):
    if "attributes" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["attributes"])),
            unpack(_update_attributes),
        )
    if "accept_drops" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["accept_drops"])),
            unpack(QtWidgets.QWidget.setAcceptDrops),
        )
    if "accessible_description" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["accessible_description"])),
            unpack(QtWidgets.QWidget.setAccessibleDescription),
        )
    if "accessible_name" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["accessible_name"])),
            unpack(QtWidgets.QWidget.setAccessibleName),
        )
    if "auto_fill_background" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["auto_fill_background"])),
            unpack(QtWidgets.QWidget.setAutoFillBackground),
        )
    if "base_size" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["base_size"])),
            unpack(QtWidgets.QWidget.setBaseSize),
        )
    if "context_menu_policy" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["context_menu_policy"])),
            unpack(QtWidgets.QWidget.setContextMenuPolicy),
        )
    if "cursor" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["cursor"])),
            unpack(
                lambda widget, cursor: (
                    widget.setCursor(cursor)
                    if cursor is not None
                    else widget.unsetCursor()
                )
            ),
        )
    if "enabled" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["enabled"])),
            unpack(QtWidgets.QWidget.setEnabled),
        )
    if "focus" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["focus"])),
            unpack(
                lambda widget, focus: (
                    widget.setFocus() if focus is True else widget.clearFocus()
                )
            ),
        )
    if "focus_policy" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["focus_policy"])),
            unpack(QtWidgets.QWidget.setFocusPolicy),
        )
    if "font" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["font"])),
            unpack(QtWidgets.QWidget.setFont),
        )
    if "height" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["height"])),
            unpack(QtWidgets.QWidget.setFixedHeight),
        )
    if "input_method_hints" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["input_method_hints"])),
            unpack(QtWidgets.QWidget.setInputMethodHints),
        )
    if "locale" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["locale"])),
            unpack(
                lambda widget, locale: (
                    widget.setLocale(locale)
                    if locale is not None
                    else widget.unsetLocale()
                )
            ),
        )
    if "layout" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["layout"])),
            unpack(lambda widget, layout: widget.setLayout(layout())),
        )
    if "maximum_height" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["maximum_height"])),
            unpack(QtWidgets.QWidget.setMaximumHeight),
        )
    if "maximum_size" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["maximum_size"])),
            unpack(QtWidgets.QWidget.setMaximumSize),
        )
    if "maximum_width" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["maximum_width"])),
            unpack(QtWidgets.QWidget.setMaximumWidth),
        )
    if "minimum_height" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["minimum_height"])),
            unpack(QtWidgets.QWidget.setMinimumHeight),
        )
    if "minimum_size" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["minimum_size"])),
            unpack(QtWidgets.QWidget.setMinimumSize),
        )
    if "minimum_width" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["minimum_width"])),
            unpack(QtWidgets.QWidget.setMinimumWidth),
        )
    if "mouse_tracking" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["mouse_tracking"])),
            unpack(QtWidgets.QWidget.setMouseTracking),
        )
    if "object_name" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["object_name"])),
            unpack(QtWidgets.QWidget.setObjectName),
        )
    if "parent" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["parent"])),
            unpack(QtWidgets.QWidget.setParent),
        )
    if "properties" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["properties"])),
            unpack(_update_properties),
        )
    if "size" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["size"])),
            unpack(QtWidgets.QWidget.setFixedSize),
        )
    if "size_policy" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["size_policy"])),
            unpack(QtWidgets.QWidget.setSizePolicy),
        )
    if "status_tip" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["status_tip"])),
            unpack(QtWidgets.QWidget.setStatusTip),
        )
    if "stylesheet" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["stylesheet"])),
            unpack(_update_stylesheet),
        )
    if "tablet_tracking" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["tablet_tracking"])),
            unpack(QtWidgets.QWidget.setTabletTracking),
        )
    if "tooltip" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["tooltip"])),
            unpack(QtWidgets.QWidget.setToolTip),
        )
    if "visible" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["visible"])),
            unpack(QtWidgets.QWidget.setVisible),
        )
    if "width" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["width"])),
            unpack(QtWidgets.QWidget.setFixedWidth),
        )
    if "on_destroy" in props:
        bind_signal(lifecycle, ref, lambda w: w.destroyed, props["on_destroy"])


class QWidgetProps(BindQWidgetProps, TypedDict):
    ref: NotRequired[Ref[QtWidgets.QWidget]]


def QWidget(**props: Unpack[QWidgetProps]):  # noqa: N802
    ref = Ref[QtWidgets.QWidget]()
    adapter = with_ref(lambda: QtWidgets.QWidget(), ref, props.get("ref"))
    lc = LifeCycle(ref)
    bind_qwidget(ref, lc, **extract_typeddict(BindQWidgetProps, props))
    return adapter


def _update_attributes(
    widget: QtWidgets.QWidget, attrs: dict[QtCore.Qt.WidgetAttribute, bool]
) -> None:
    for key, value in attrs.items():
        widget.setAttribute(key, value)


def _update_properties(widget: QtWidgets.QWidget, properties: dict[str, Any]) -> None:
    property_names: set[str] = {str(p) for p in widget.dynamicPropertyNames()}
    properties_to_unset = property_names.difference(properties.keys())
    for _property in properties_to_unset:
        widget.setProperty(_property, None)
    for _property, value in properties.items():
        widget.setProperty(_property, value)


def _update_stylesheet(widget: QtWidgets.QWidget, stylesheet: str) -> None:
    widget.setStyleSheet(stylesheet)
    widget.style().unpolish(widget)
    widget.style().polish(widget)
