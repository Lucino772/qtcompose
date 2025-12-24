from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any, TypeAlias, TypeVar, overload

from uikit.rx._types import Observable

T = TypeVar("T")
U = TypeVar("U")

T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")
T7 = TypeVar("T7")
T8 = TypeVar("T8")
T9 = TypeVar("T9")

_Operator: TypeAlias = Callable[[Observable[T]], Observable[U]]


@overload
def pipe(
    source: Observable[T1],
    a: _Operator[T1, T2],
    /,
) -> Observable[T2]: ...


@overload
def pipe(
    source: Observable[T1],
    a: _Operator[T1, T2],
    b: _Operator[T2, T3],
    /,
) -> Observable[T3]: ...


@overload
def pipe(
    source: Observable[T1],
    a: _Operator[T1, T2],
    b: _Operator[T2, T3],
    c: _Operator[T3, T4],
    /,
) -> Observable[T4]: ...


@overload
def pipe(
    source: Observable[T1],
    a: _Operator[T1, T2],
    b: _Operator[T2, T3],
    c: _Operator[T3, T4],
    d: _Operator[T4, T5],
    /,
) -> Observable[T5]: ...


@overload
def pipe(
    source: Observable[T1],
    a: _Operator[T1, T2],
    b: _Operator[T2, T3],
    c: _Operator[T3, T4],
    d: _Operator[T4, T5],
    e: _Operator[T5, T6],
    /,
) -> Observable[T6]: ...


@overload
def pipe(
    source: Observable[T1],
    a: _Operator[T1, T2],
    b: _Operator[T2, T3],
    c: _Operator[T3, T4],
    d: _Operator[T4, T5],
    e: _Operator[T5, T6],
    f: _Operator[T6, T7],
    /,
) -> Observable[T7]: ...


@overload
def pipe(
    source: Observable[T1],
    a: _Operator[T1, T2],
    b: _Operator[T2, T3],
    c: _Operator[T3, T4],
    d: _Operator[T4, T5],
    e: _Operator[T5, T6],
    f: _Operator[T6, T7],
    g: _Operator[T7, T8],
    /,
) -> Observable[T8]: ...


@overload
def pipe(
    source: Observable[T1],
    a: _Operator[T1, T2],
    b: _Operator[T2, T3],
    c: _Operator[T3, T4],
    d: _Operator[T4, T5],
    e: _Operator[T5, T6],
    f: _Operator[T6, T7],
    g: _Operator[T7, T8],
    h: _Operator[T8, T9],
    /,
) -> Observable[T9]: ...


def pipe(source: Observable[Any], *operators: _Operator[Any, Any]) -> Observable[Any]:
    return functools.reduce(lambda obs, operator: operator(obs), operators, source)
