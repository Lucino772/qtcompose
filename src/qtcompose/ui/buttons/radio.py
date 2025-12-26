from __future__ import annotations

from typing import TYPE_CHECKING, NotRequired, TypedDict, Unpack

from qtpy import QtWidgets

from qtcompose.core import LifeCycle, Ref, with_ref
from qtcompose.ui.buttons.abstract import (
    BindQAbstractButtonProps,
    bind_qabstract_button,
)
from qtcompose.ui.widget import BindQWidgetProps, bind_qwidget
from qtcompose.utils import extract_typeddict

if TYPE_CHECKING:
    from collections.abc import Callable


class QRadioButtonProps(BindQAbstractButtonProps, TypedDict):
    ref: NotRequired[Ref[QtWidgets.QRadioButton]]


def QRadioButton(  # noqa: N802
    **props: Unpack[QRadioButtonProps],
) -> Callable[[], QtWidgets.QRadioButton]:
    ref = Ref[QtWidgets.QRadioButton]()
    adapter = with_ref(lambda: QtWidgets.QRadioButton(), ref, props.get("ref"))

    lc = LifeCycle(ref)
    bind_qwidget(ref, lc, **extract_typeddict(BindQWidgetProps, props))
    bind_qabstract_button(ref, lc, **extract_typeddict(BindQAbstractButtonProps, props))
    return adapter
