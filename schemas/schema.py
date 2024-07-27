import abc
import typing


class FieldInfo(abc.ABC):
    @property
    @abc.abstractmethod
    def annotation(self) -> typing.Type[typing.Any] | None:
        pass

    @property
    @abc.abstractmethod
    def required(self) -> bool:
        pass


class Schema(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def fields(cls) -> dict[str, FieldInfo]:
        pass

    @classmethod
    @abc.abstractmethod
    def from_json(cls, json: str) -> "Schema":
        pass
