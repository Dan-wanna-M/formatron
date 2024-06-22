import typing

import schemas.pydantic
from pydantic import BaseModel, Field, PositiveInt


class Test(schemas.pydantic.ClassSchema):
    a: typing.Annotated[str, Field("OK"), "114":514, Field("OK2")]
    b: int = 1
    c: bool
    d: float
    e: None


print(Test.fields()['b'].required)
print(Test.fields()['c'].required)


@schemas.pydantic.callable_schema
def foo(a: typing.Annotated[int, "boy"], b: typing.Annotated[int, Field(gt=10), "1124"] = 2):
    return a + b


print(foo(1))
print(foo)
