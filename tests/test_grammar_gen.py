import decimal
import json
import typing

from pydantic import Field

from formatron.formats.json import create_json_extractor
import formatron.schemas.pydantic
from formatron.schemas.dict_inference import infer_mapping

new_int = typing.NewType("new_int", int)
vector = list[int]


class Test(formatron.schemas.pydantic.ClassSchema):
    a: typing.Annotated[str, Field("OK"), "114":514, Field("OK2")]
    b: int = 1
    c: typing.Literal["114'\"", "514", True, typing.Literal["1919", "810"]]
    e: tuple[typing.List[float], str, decimal.Decimal,
             typing.Dict, dict[str, typing.Any]]
    f: typing.Union[bool, int, typing.Any, new_int, vector]


class LinkedList(formatron.schemas.pydantic.ClassSchema):
    value: int
    next: typing.Optional["LinkedList"]


def test_pydantic_class(snapshot):
    result = create_json_extractor(Test, "start").kbnf_definition
    snapshot.assert_match(result)


def test_pydantic_class_linked_list(snapshot):
    result = create_json_extractor(LinkedList, "start").kbnf_definition
    snapshot.assert_match(result)


def test_pydantic_callable(snapshot):
    @formatron.schemas.pydantic.callable_schema
    def foo(a: int, b: typing.Annotated[int, Field(gt=10), "1124"] = 2):
        return a + b

    result = create_json_extractor(foo, "start").kbnf_definition
    snapshot.assert_match(result)


def test_infer_mapping(snapshot):
    result = create_json_extractor(infer_mapping(json.loads("""
    {
      "mode": "xx",
      "title": "xx",
      "queries": ["xx", 2, true],
      "related_queries": [{"foo":514}, "xx", "xx"],
      "concepts": ["xx", "xx", "xx"],
      "urls": ["xx", "xx", "xx"]
    }
    """)), "start").kbnf_definition
    snapshot.assert_match(result)
