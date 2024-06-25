import collections.abc
from typing import Any, Type

from pydantic import typing

import schemas.schema


class FieldInfo(schemas.schema.FieldInfo):
    __slots__ = ("_annotation",)

    def __init__(self, annotation: typing.Type):
        self._annotation = annotation

    @property
    def annotation(self) -> typing.Type[typing.Any] | None:
        return self._annotation

    def required(self) -> bool:
        return True


def _infer_type(value: Any) -> Type[Any]:
    """Infer the type of given value."""
    if isinstance(value, collections.abc.Mapping):
        return infer_mapping(value)
    elif isinstance(value, collections.abc.Sequence) and not isinstance(value, str):
        # Handle sequences with possibly heterogeneous elements
        if value:
            element_types = {type(v) for v in value}
            if len(element_types) == 1:
                return collections.abc.Sequence[next(iter(element_types))]
            else:
                union_type = typing.Union[tuple(element_types)]
                return collections.abc.Sequence[union_type]
        else:
            return collections.Sequence[Any]
    else:
        return type(value)


def infer_mapping(mapping: collections.abc.Mapping[str, Any]) -> typing.Type[schemas.schema.Schema]:
    """Recursively infer a schema from a mapping."""
    field_infos = {}
    for key, value in mapping.items():
        inferred_type = _infer_type(value)
        field_infos[key] = FieldInfo(inferred_type)
    _class = type(f"Mapping_{id(mapping)}", (schemas.schema.Schema,), {"fields": lambda: field_infos})
    return _class
