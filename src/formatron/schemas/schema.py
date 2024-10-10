"""
This module contains the Schema abstract class and FieldInfo abstract class.
"""
import abc
import typing


class FieldInfo(abc.ABC):
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
    def __init__(self, type: typing.Type[typing.Any], metadata: dict[str, typing.Any]|None):
        self._type = type
        self._metadata = metadata

    @property
    def type(self) -> typing.Type[typing.Any]:
        return self._type

    @property
    def metadata(self) -> dict[str, typing.Any]|None:
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
