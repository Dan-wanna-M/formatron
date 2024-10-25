"""
This module contains the Schema abstract class and FieldInfo abstract class.
"""
import abc
from dataclasses import dataclass
import typing


class FieldInfo(abc.ABC):
    """
    An abstract field info that describes a data field in a schema.
    """
    @property
    @abc.abstractmethod
    def annotation(self) -> typing.Type[typing.Any] | None:
        """
        Get the type annotation of the field.
        """
        pass

    @property
    @abc.abstractmethod
    def required(self) -> bool:
        """
        Check if the field is required for the schema.
        """
        pass

class TypeWithMetadata:
    """
    A type with metadata.
    """
    def __init__(self, type: typing.Type[typing.Any], metadata: dict[str, typing.Any]|None):
        self._type = type
        self._metadata = metadata

    @property
    def type(self) -> typing.Type[typing.Any]:
        """
        Get the type of the type with metadata.
        """
        return self._type

    @property
    def metadata(self) -> dict[str, typing.Any]|None:
        """
        Get the metadata of the type with metadata.
        """
        return self._metadata

class Schema(abc.ABC):
    """
    An abstract schema that describes some data.
    """
    @classmethod
    @abc.abstractmethod
    def fields(cls) -> dict[str, FieldInfo]:
        """
        Get the fields of the schema.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def from_json(cls, json: str) -> "Schema":
        """
        Create a schema from a JSON string.
        """
        pass

@dataclass
class SubstringOf:
    """
    A metadata class that indicates that the field is a substring of the given string.
    """
    substring_of: str
