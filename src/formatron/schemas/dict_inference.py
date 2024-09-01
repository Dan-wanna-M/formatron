"""
This module contains utilities for inferring schemas from dictionaries.
"""
import collections.abc
import json
from typing import Any, Type

from pydantic import typing

from formatron import schemas


class FieldInfo(schemas.schema.FieldInfo):
    __slots__ = ("_annotation",)

    def __init__(self, annotation: typing.Type):
        """
        Initialize the field information.

        Args:
            annotation: The type annotation of the field.
        """
        self._annotation = annotation

    @property
    def annotation(self) -> typing.Type[typing.Any] | None:
        """
        Get the type annotation of the field.
        """
        return self._annotation

    @property
    def required(self) -> bool:
        """
        Check if the field is required for the schema.
        """
        return True


def _infer_type(value: Any) -> Type[Any]:
    if isinstance(value, collections.abc.Mapping):
        return infer_mapping(value)
    elif isinstance(value, collections.abc.Sequence) and not isinstance(value, str):
        # Handle sequences with possibly heterogeneous elements
        if not value:
            return collections.Sequence[Any]
        element_types = set()
        for element in value:
            element_type = type(element)
            # Check for dictionary
            original = typing.get_origin(element_type)
            if original is None:
                original = element_type
            if original is typing.Mapping or isinstance(original, type) and issubclass(original,
                                                                                       collections.abc.Mapping):
                element_types.add(infer_mapping(element))
            else:
                element_types.add(element_type)
        if len(element_types) == 1:
            return collections.abc.Sequence[next(iter(element_types))]
        union_type = typing.Union[tuple(element_types)]
        return collections.abc.Sequence[union_type]
    else:
        return type(value)


def infer_mapping(mapping: collections.abc.Mapping[str, Any]) -> typing.Type[schemas.schema.Schema]:
    """
    Recursively infer a schema from a mapping.

    Types that are specially handled:
        - collections.abc.Mapping: converted to a schema. Keys are converted to field names and corresponding value types are converted to field types.
        - collections.abc.Sequence with heterogeneous elements: all different element types are included in a union type.

    Other types are directly inferred from the type of the value with no special handling.
    """
    field_infos = {}
    for key, value in mapping.items():
        assert isinstance(key, str), f"Key must be a string, got {key} of type {type(key)}"
        assert key.isidentifier(), f"Key must be a valid identifier, got {key}"
        inferred_type = _infer_type(value)
        field_infos[key] = FieldInfo(inferred_type)
    _class = type(f"Mapping_{id(mapping)}", (schemas.schema.Schema,), {"fields": lambda: field_infos})
    _class.from_json = classmethod(lambda cls, json_str: json.loads(json_str))
    return _class
