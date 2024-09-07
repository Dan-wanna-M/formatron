import decimal
import json
import typing

from pydantic import Field

from formatron.formats.json import JsonExtractor
from formatron.schemas import json_schema
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
    result = JsonExtractor("start", None,Test,lambda x:x).kbnf_definition
    snapshot.assert_match(result)

def test_json_schema(snapshot):
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.com/random-schema.json",
        "type": ["object", "number"],
        "properties": {
            "name": {
                "type": ["string", "number"],
                "description": "The name of the item"
            },
            "price": {
                "type": "number",
                "minimum": 0,
                "description": "The price of the item"
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": ["string", "number"]
                },
                "minItems": 1,
                "uniqueItems": True,
                "description": "Tags associated with the item"
            },
            "inStock": {
                "type": "boolean",
                "description": "Whether the item is in stock"
            },
            "category": {
                "type": ["string","integer", "number", "null"],
                "enum": ["electronics", 114, 514.1, None, ['114', 514, 514.1, True], {"a":1, "b":2.3}],
                "description": "The category of the item"
            },
            "sku": {
                "type": "string",
                "const": "ITEM-001",
                "description": "The stock keeping unit (SKU) of the item"
            }
        },
        "required": ["name", "price", "category", "sku"]
    }
    schema = json_schema.create_schema(schema)
    result = JsonExtractor("start", None,schema,lambda x:x).kbnf_definition
    snapshot.assert_match(result)


def test_pydantic_class_linked_list(snapshot):
    result = JsonExtractor("start", None,LinkedList,lambda x:x).kbnf_definition
    snapshot.assert_match(result)


def test_pydantic_callable(snapshot):
    @formatron.schemas.pydantic.callable_schema
    def foo(a: int, b: typing.Annotated[int, Field(gt=10), "1124"] = 2):
        return a + b

    result = JsonExtractor("start", None,foo,lambda x:x).kbnf_definition
    snapshot.assert_match(result)


def test_infer_mapping(snapshot):
    result = JsonExtractor("start", None,infer_mapping(json.loads("""
    {
      "mode": "xx",
      "title": "xx",
      "queries": ["xx", 2, true],
      "related_queries": [{"foo":514}, "xx", "xx"],
      "concepts": ["xx", "xx", "xx"],
      "urls": ["xx", "xx", "xx"]
    }
    """)),lambda x:x).kbnf_definition
    snapshot.assert_match(result)
