import inspect
import typing

import pydantic.fields
from pydantic_core._pydantic_core import PydanticUndefined

import schemas.schema
from pydantic import BaseModel, validate_call, ConfigDict, Field


class FieldInfo(schemas.schema.FieldInfo):
    __slots__ = ("_field",)

    def __init__(self, field: pydantic.fields.FieldInfo):
        self._field = field

    @property
    def annotation(self) -> typing.Type[typing.Any] | None:
        return self._field.annotation

    @property
    def required(self) -> bool:
        return self._field.is_required()

    def __repr__(self):
        return repr(self._field)

    def __str__(self):
        return str(self._field)


class ClassSchema(BaseModel, schemas.schema.Schema):
    __cached_fields__ = None

    @classmethod
    def fields(cls) -> typing.Dict[str, typing.Any]:
        if cls.__cached_fields__ is not None:
            return cls.__cached_fields__
        cls.__cached_fields__ = {k: FieldInfo(v) for k, v in cls.model_fields.items()}
        return cls.__cached_fields__


CallableT = typing.TypeVar('CallableT', bound=typing.Callable)


def callable_schema(func: CallableT, /, *, config: ConfigDict = None, validate_return: bool = False) -> CallableT:
    pydantic_wrapper = validate_call(config=config, validate_return=validate_return)(func)
    signature = inspect.signature(func, eval_str=True)
    fields = {}
    for k, p in signature.parameters.items():
        if isinstance(p.default, pydantic.fields.FieldInfo):
            fields[k] = p.default
            continue
        default = PydanticUndefined
        if p.default is not inspect.Signature.empty:
            default = p.default
        actual_type = p.annotation
        metadata = []
        if typing.get_origin(p.annotation) is typing.Annotated:
            actual_type, *meta = typing.get_args(p.annotation)
            fieldinfo = None
            for i in meta:
                if isinstance(i, pydantic.fields.FieldInfo):
                    fieldinfo = i
                else:
                    metadata.append(i)
            if fieldinfo is not None:
                fields[k] = fieldinfo
                fields[k].default = default
                fields[k].annotation = actual_type
                fields[k].metadata.extend(metadata)
                continue
        fields[k] = Field(default)
        fields[k].annotation = actual_type
        fields[k].metadata.extend(metadata)
    for k in fields:
        fields[k] = FieldInfo(fields[k])
    _class = type(
        f'{func.__qualname__}PydanticSchema',
        (schemas.schema.Schema,),
        {
            "_func": pydantic_wrapper,
            'fields': lambda: fields,
            '__new__': lambda cls, *args, **kwargs: pydantic_wrapper(*args, **kwargs),
            '__call__': lambda *args, **kwargs: pydantic_wrapper(*args, **kwargs)  # make duck typer happy
        }
    )
    return _class
