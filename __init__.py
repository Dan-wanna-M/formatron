import typing

import schemas.pydantic
from pydantic import BaseModel, Field, PositiveInt


class Test(schemas.pydantic.ClassSchema):
    a: typing.Annotated[str, "boy"]
    b: int
    c: bool
    d: float
    e: None


print(Test.fields())


@schemas.pydantic.callable_schema
def foo(a: typing.Annotated[int, "boy"], b: typing.Annotated[int, Field(gt=10)] = 2):
    return a + b


print(foo(1))
print(foo.fields())
