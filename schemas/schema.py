import abc
import typing


class FieldInfo(abc.ABC):
    @property
    @abc.abstractmethod
    def annotation(self) -> typing.Type[typing.Any]|None:
        pass


class Schema(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def fields(cls) -> typing.Dict[str, FieldInfo]:
        pass
