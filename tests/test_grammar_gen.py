import decimal
import json
import typing

from pydantic import Field

import grammar_generators.json_generator
import schemas.pydantic
from schemas.dict_inference import infer_mapping

new_int = typing.NewType("new_int", int)
vector = list[int]


class Test(schemas.pydantic.ClassSchema):
    a: typing.Annotated[str, Field("OK"), "114":514, Field("OK2")]
    b: int = 1
    c: typing.Literal["114'\"", "514", True, typing.Literal["1919", "810"]]
    e: tuple[typing.List[float], str, decimal.Decimal, typing.Dict, dict[str, typing.Any]]
    f: typing.Union[bool, int, typing.Any, new_int, vector]


def test_pydantic_class(snapshot):
    """Testing the API for /me"""
    result = grammar_generators.json_generator.JsonGenerator().generate(Test)
    snapshot.assert_match(result)


def test_infer_mapping(snapshot):
    result = grammar_generators.json_generator.JsonGenerator().generate(infer_mapping(json.loads("""
    {
      "mode": "xx",
      "title": "xx",
      "queries": ["xx", 2, true],
      "related_queries": [{"114":514}, "xx", "xx"],
      "concepts": ["xx", "xx", "xx"],
      "urls": ["xx", "xx", "xx"]
    }
    """)))
    snapshot.assert_match(result)
