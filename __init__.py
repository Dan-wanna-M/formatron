import decimal
import ipaddress
import typing
import ipaddress
import schemas.pydantic
from pydantic import BaseModel, Field, PositiveInt

from grammar_generators.json_generator import JsonAsKbnf


class IPv4Address:
    pass


new_int = typing.NewType("new_int", int)
vector = list[int]


class Test(schemas.pydantic.ClassSchema):
    a: typing.Annotated[str, Field("OK"), "114":514, Field("OK2")]
    b: int = 1
    c: typing.Literal["114'\"", "514", True, typing.Literal["1919", "810"]]
    e: tuple[typing.List[float], decimal.Decimal, typing.Dict, dict[str, typing.Any]]
    f: typing.Union[bool, int, typing.Any, new_int, vector]


print(Test.fields()['f'])
print(JsonAsKbnf().generate(Test))


@schemas.pydantic.callable_schema
def foo(a: int, b: typing.Annotated[int, Field(gt=10), "1124"] = 2):
    return a + b


print(foo(1))
print(foo.fields()['a'])
assert typing.get_origin(typing.List[int]) is list
