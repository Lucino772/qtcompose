from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, NotRequired, TypedDict, Unpack
from uuid import uuid4

from qtpy import QtCore, QtWidgets

from uikit.core import LifeCycle, Ref, with_ref
from uikit.rx import fn
from uikit.utils import extract_typeddict, unpack

if TYPE_CHECKING:
    from collections.abc import Callable, Collection

    from uikit.rx import Observable


class QBoxLayoutItem:
    @dataclass
    class Spacing:
        spacing: int
        key: str = field(default_factory=lambda: str(uuid4()))

    @dataclass
    class Stretch:
        stretch: int | None = None
        key: str = field(default_factory=lambda: str(uuid4()))

    @dataclass
    class Child:
        component: Callable[[], QtWidgets.QWidget]
        stretch: int | None = None
        alignment: QtCore.Qt.AlignmentFlag = field(
            default_factory=lambda: QtCore.Qt.AlignmentFlag(0)
        )
        key: str = field(default_factory=lambda: str(uuid4()))


class BindQBoxLayoutProps(TypedDict):
    # From QtWidgets.QLayout
    alignment: NotRequired[Observable[QtCore.Qt.AlignmentFlag]]
    margins: NotRequired[Observable[QtCore.QMargins]]
    size_constraint: NotRequired[Observable[QtWidgets.QBoxLayout.SizeConstraint]]
    spacing: NotRequired[Observable[int]]

    # From QtWidgets.QBoxLayout
    direction: Observable[QtWidgets.QBoxLayout.Direction]
    children: NotRequired[
        Observable[
            Collection[
                QBoxLayoutItem.Spacing | QBoxLayoutItem.Stretch | QBoxLayoutItem.Child
            ]
        ]
    ]


def bind_qboxlayout(
    ref: Ref[QtWidgets.QBoxLayout],
    lifecycle: LifeCycle[QtWidgets.QBoxLayout],
    **props: Unpack[BindQBoxLayoutProps],
):
    if "alignment" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["alignment"])),
            unpack(QtWidgets.QBoxLayout.setAlignment),
        )
    if "margins" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["margins"])),
            unpack(QtWidgets.QBoxLayout.setContentsMargins),
        )
    if "spacing" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["spacing"])),
            unpack(QtWidgets.QBoxLayout.setSpacing),
        )

    if "size_constraint" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["size_constraint"])),
            unpack(QtWidgets.QBoxLayout.setSizeConstraint),
        )
    if "direction" in props:
        lifecycle.subscribe(
            fn.pipe(ref, fn.as_tuple(), fn.combine(props["direction"])),
            unpack(QtWidgets.QBoxLayout.setDirection),
        )
    if "children" in props:
        _bind_children(lifecycle, ref, props["children"])


def _bind_children(
    lifecycle: LifeCycle[QtWidgets.QBoxLayout],
    ref: Ref[QtWidgets.QBoxLayout],
    children: Observable[
        Collection[
            QBoxLayoutItem.Spacing | QBoxLayoutItem.Stretch | QBoxLayoutItem.Child
        ]
    ],
):
    previous_children: Collection[
        QBoxLayoutItem.Spacing | QBoxLayoutItem.Stretch | QBoxLayoutItem.Child
    ] = []

    def _updater(
        layout: QtWidgets.QBoxLayout,
        children: Collection[
            QBoxLayoutItem.Spacing | QBoxLayoutItem.Stretch | QBoxLayoutItem.Child
        ],
    ):
        nonlocal previous_children

        item_to_key: dict[str, QtWidgets.QLayoutItem] = {}
        for child in previous_children:
            item_to_key[child.key] = layout.takeAt(0)

        previous_children = children

        current_keys = {item.key for item in children}
        for key, item in item_to_key.items():
            if key not in current_keys:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                layout.removeItem(item)

        for idx, child in enumerate(children):
            prev = item_to_key.get(child.key)
            if prev is not None:
                layout.insertItem(min(idx, layout.count()), prev)
            elif isinstance(child, QBoxLayoutItem.Spacing):
                layout.insertSpacing(min(idx, layout.count()), child.spacing)
            elif isinstance(child, QBoxLayoutItem.Stretch):
                if child.stretch is not None:
                    layout.insertStretch(min(idx, layout.count()), child.stretch)
                else:
                    layout.insertStretch(min(idx, layout.count()))
            elif child.stretch is not None:
                layout.insertWidget(
                    min(idx, layout.count()),
                    child.component(),
                    stretch=child.stretch,
                    alignment=child.alignment,
                )
            else:
                layout.insertWidget(
                    min(idx, layout.count()),
                    child.component(),
                    alignment=child.alignment,
                )

    lifecycle.subscribe(
        fn.pipe(
            ref,
            fn.as_tuple(),
            fn.combine(children),
        ),
        unpack(_updater),
    )


class QBoxLayoutProps(BindQBoxLayoutProps, TypedDict):
    ref: NotRequired[Ref[QtWidgets.QBoxLayout]]


def QBoxLayout(**props: Unpack[QBoxLayoutProps]):  # noqa: N802
    ref = Ref[QtWidgets.QBoxLayout]()
    adapter = with_ref(
        lambda: QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.LeftToRight),
        ref,
        props.get("ref"),
    )
    lc = LifeCycle(ref)
    bind_qboxlayout(ref, lc, **extract_typeddict(BindQBoxLayoutProps, props))
    return adapter


class QVBoxLayoutProps(BindQBoxLayoutProps, TypedDict):
    ref: NotRequired[Ref[QtWidgets.QBoxLayout]]
    direction: NotRequired[Observable[QtWidgets.QBoxLayout.Direction]]


def QVBoxLayout(**props: Unpack[QVBoxLayoutProps]):  # noqa: N802
    ref = Ref[QtWidgets.QBoxLayout]()
    adapter = with_ref(
        lambda: QtWidgets.QVBoxLayout(),
        ref,
        props.get("ref"),
    )
    lc = LifeCycle(ref)
    bind_qboxlayout(ref, lc, **extract_typeddict(BindQBoxLayoutProps, props))
    return adapter


class QHBoxLayoutProps(BindQBoxLayoutProps, TypedDict):
    ref: NotRequired[Ref[QtWidgets.QBoxLayout]]
    direction: NotRequired[Observable[QtWidgets.QBoxLayout.Direction]]


def QHBoxLayout(**props: Unpack[QHBoxLayoutProps]):  # noqa: N802
    ref = Ref[QtWidgets.QBoxLayout]()
    adapter = with_ref(
        lambda: QtWidgets.QHBoxLayout(),
        ref,
        props.get("ref"),
    )
    lc = LifeCycle(ref)
    bind_qboxlayout(ref, lc, **extract_typeddict(BindQBoxLayoutProps, props))
    return adapter
