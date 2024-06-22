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

    def annotation(self) -> typing.Type[typing.Any] | None:
        return self._field.annotation


class ClassSchema(BaseModel, schemas.schema.Schema):
    __fields__ = None

    @classmethod
    def fields(cls) -> typing.Dict[str, typing.Any]:
        if cls.__fields__ is not None:
            return cls.__fields__
        cls.__fields__ = {k: FieldInfo(v) for k, v in cls.model_fields}
        return cls.__fields__


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
        if typing.get_origin(p.annotation) is typing.Annotated:
            actual_type, *meta = typing.get_args(p.annotation)
            fieldinfo = None
            for i in meta:
                if isinstance(i, pydantic.fields.FieldInfo):
                    if fieldinfo is not None:
                        raise TypeError(f"Function {func}'s parameter {k}'s"
                                        f" annotation contains more than one pydantic.Field()!")
                    fieldinfo = i
            if fieldinfo is not None:
                fields[k] = fieldinfo
                fields[k].default = default
                fields[k].annotation = actual_type
                continue
        fields[k] = Field(default)
        fields[k].annotation = actual_type
    _class = type(
        'FuncSchema',
        (schemas.schema.Schema,),
        {
            "_func": pydantic_wrapper,
            'fields': lambda: fields,
            '__new__': lambda cls, *args, **kwargs: pydantic_wrapper(*args, **kwargs),
            '__call__': lambda *args, **kwargs: pydantic_wrapper(*args, **kwargs)  # make duck typer happy
        }
    )
    return _class
