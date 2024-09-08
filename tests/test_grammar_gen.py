import decimal
import json
import typing

from pydantic import Field
from referencing import Registry, Resource

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

def test_recursive_binary_tree_schema(snapshot):
    binary_tree_schema = {
        "$id": "https://example.com/binary-tree.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "value": {"type": "number"},
            "left": {"$ref": "#"},
            "right": {"$ref": "#"}
        },
        "required": ["value"]
    }
    schema = json_schema.create_schema(binary_tree_schema)
    result = JsonExtractor("start", None, schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)

def test_recursive_linked_list_schema(snapshot):
    linked_list_schema = {
        "$id": "https://example.com/linked-list.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "value": {"type": "integer"},
            "next": {
                "$ref": "#"
            }
        },
        "required": ["value"]
    }
    schema = json_schema.create_schema(linked_list_schema)
    result = JsonExtractor("start", None, schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)

def test_schema_with_reference(snapshot):
    schema1 = {
        "$id": "https://example.com/person.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "address": {"$ref": "https://example.com/address.json"}
        },
        "required": ["name", "age", "address"]
    }

    schema2 = {
        "$id": "https://example.com/address.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "street": {"type": "string"},
            "city": {"type": "string"},
            "country": {"type": "string"}
        },
        "required": ["street", "city", "country"]
    }

    combined_schema = json_schema.create_schema(schema1, Resource.from_contents(schema2) @ Registry())
    result = JsonExtractor("start", None, combined_schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)

def test_schema_with_anchor_reference(snapshot):
    schema = {
        "$id": "https://example.com/schemas/main.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "mainProperty": {"type": "string"},
            "referencedObject": {"$ref": "#referenced"},
            "referencedObject2": {"$ref": "#/$defs/referenced"}
        },
        "required": ["mainProperty", "referencedObject", "referencedObject2"],
        "$defs": {
            "referenced": {
                "$anchor": "referenced",
                "type": "object",
                "properties": {
                    "subProperty": {"type": "integer"}
                },
                "required": ["subProperty"]
            }
        }
    }

    combined_schema = json_schema.create_schema(schema)
    result = JsonExtractor("start", None, combined_schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)

def test_schema_with_embedded_schema(snapshot):
    schema = {
        "$id": "https://example.com/schemas/parent.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "parentProperty": {"type": "string"},
            "embeddedObject": {
                "$id": "https://example.com/schemas/embedded.json",
                "type": "object",
                "properties": {
                    "embeddedProperty": {"type": "integer"}
                },
                "required": ["embeddedProperty"]
            }
        },
        "required": ["parentProperty", "embeddedObject"]
    }
    schema_with_reference = {
        "$id": "https://example.com/schemas/referencing.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "referencedEmbedded": {"$ref": "https://example.com/schemas/embedded.json"}
        },
        "required": ["referencedEmbedded"]
    }

    # Combine both schemas
    combined_schema = json_schema.create_schema(schema_with_reference, Resource.from_contents(schema) @ Registry())
    result = JsonExtractor("start", None, combined_schema, lambda x: x).kbnf_definition
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

def test_schema_with_dynamic_ref(snapshot):
    schema = {
        "$id": "https://example.com/tree",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$dynamicAnchor": "node",
        "type": "object",
        "properties": {
            "data": {"type": "string"},
            "children": {
                "type": "array",
                "items": {"$dynamicRef": "#node"}
            }
        }
    }

    extended_schema = {
        "$id": "https://example.com/extended-tree",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$ref": "https://example.com/tree",
        "$dynamicAnchor": "node",
        "properties": {
            "data": {"type": "string"},
            "children": {
                "type": "array",
                "items": {"$dynamicRef": "#node"}
            },
            "metadata": {"type": "string"}
        }
    }

    combined_schema = json_schema.create_schema(extended_schema, Resource.from_contents(schema) @ Registry())
    
    result = JsonExtractor("start", None, combined_schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)
