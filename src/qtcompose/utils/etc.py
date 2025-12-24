from __future__ import annotations

from functools import wraps
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Protocol,
    TypeVar,
    TypeVarTuple,
    cast,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping


class _AnyTypedDict(Protocol):
    __required_keys__: ClassVar[frozenset[str]]
    __optional_keys__: ClassVar[frozenset[str]]


T = TypeVar("T")
Ts = TypeVarTuple("Ts")
T_dict = TypeVar("T_dict", bound=_AnyTypedDict)


def unpack(func: Callable[[*Ts], T]) -> Callable[[tuple[*Ts]], T]:
    @wraps(func)
    def _wrapper(args: tuple[*Ts]) -> T:
        return func(*args)

    return _wrapper


def extract_typeddict(typ: type[T_dict], data: Mapping[Any, Any]) -> T_dict:
    _dict = {}
    for key in typ.__required_keys__:
        if key in data:
            _dict[key] = data[key]

    for key in typ.__optional_keys__:
        if key in data:
            _dict[key] = data[key]

    return cast(T_dict, _dict)
