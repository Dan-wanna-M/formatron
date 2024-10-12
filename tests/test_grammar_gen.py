import decimal
import json
import typing

from pydantic import Field, NegativeFloat, NegativeInt, NonNegativeFloat, NonNegativeInt, NonPositiveFloat, NonPositiveInt, PositiveFloat, PositiveInt
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

def test_pydantic_string_constraints(snapshot):
    class StringConstraints(formatron.schemas.pydantic.ClassSchema):
        min_length_str: typing.Annotated[str, Field(min_length=3)]
        max_length_str: typing.Annotated[str, Field(max_length=10)]
        pattern_str: typing.Annotated[str, Field(pattern=r'^[a-zA-Z0-9]+$')]
        combined_str: typing.Annotated[str, Field(min_length=2, max_length=5)]

    result = JsonExtractor("start", None, StringConstraints, lambda x: x).kbnf_definition
    snapshot.assert_match(result)

def test_pydantic_integer_constraints(snapshot):
    class IntegerConstraints(formatron.schemas.pydantic.ClassSchema):
        gt_int: typing.Annotated[int, Field(gt=0)]
        ge_int: typing.Annotated[int, Field(ge=0)]
        lt_int: typing.Annotated[int, Field(lt=0)]
        le_int: typing.Annotated[int, Field(le=0)]
        positive_int: PositiveInt
        negative_int: NegativeInt
        nonnegative_int: NonNegativeInt
        nonpositive_int: NonPositiveInt

    result = JsonExtractor("start", None, IntegerConstraints, lambda x: x).kbnf_definition
    snapshot.assert_match(result)

def test_pydantic_float_constraints(snapshot):
    class FloatConstraints(formatron.schemas.pydantic.ClassSchema):
        gt_float: typing.Annotated[float, Field(gt=0.0)]
        ge_float: typing.Annotated[float, Field(ge=0.0)]
        lt_float: typing.Annotated[float, Field(lt=0.0)]
        le_float: typing.Annotated[float, Field(le=0.0)]
        positive_float: PositiveFloat
        negative_float: NegativeFloat
        nonnegative_float: NonNegativeFloat
        nonpositive_float: NonPositiveFloat

    result = JsonExtractor("start", None, FloatConstraints, lambda x: x).kbnf_definition
    snapshot.assert_match(result)

def test_pydantic_sequence_constraints(snapshot):
    class SequenceConstraints(formatron.schemas.pydantic.ClassSchema):
        min_2_list: typing.Annotated[typing.List[int], Field(min_length=2)]
        max_5_list: typing.Annotated[typing.List[str], Field(max_length=5)]
        min_1_max_3_list: typing.Annotated[typing.List[float], Field(min_length=1, max_length=3)]
        min_2_tuple: typing.Annotated[typing.Tuple[int, ...], Field(min_length=2)]
        max_5_tuple: typing.Annotated[typing.Tuple[str, ...], Field(max_length=5)]
        min_1_max_3_tuple: typing.Annotated[typing.Tuple[float, ...], Field(min_length=1, max_length=3)]
        empty_list: typing.Annotated[typing.List[typing.Any], Field(min_length=0)]

    result = JsonExtractor("start", None, SequenceConstraints, lambda x: x).kbnf_definition
    snapshot.assert_match(result)


def test_json_schema_integer_constraints(snapshot):
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.com/integer-constraints-schema.json",
        "type": "object",
        "properties": {
            "gt_int": {
                "type": "integer",
                "exclusiveMinimum": 0
            },
            "ge_int": {
                "type": "integer",
                "minimum": 0
            },
            "lt_int": {
                "type": "integer",
                "exclusiveMaximum": 0
            },
            "le_int": {
                "type": "integer",
                "maximum": 0
            },
        },
        "required": ["gt_int", "ge_int", "lt_int", "le_int"]
    }
    schema = json_schema.create_schema(schema)
    result = JsonExtractor("start", None, schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)

def test_json_schema_number_constraints(snapshot):
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.com/number-constraints-schema.json",
        "type": "object",
        "properties": {
            "gt_number": {
                "type": "number",
                "exclusiveMinimum": 0
            },
            "ge_number": {
                "type": "number",
                "minimum": 0
            },
            "lt_number": {
                "type": "number",
                "exclusiveMaximum": 0
            },
            "le_number": {
                "type": "number",
                "maximum": 0
            },
        },
        "required": ["gt_number", "ge_number", "lt_number", "le_number"]
    }
    schema = json_schema.create_schema(schema)
    result = JsonExtractor("start", None, schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)

def test_json_schema_array_min_max_items_constraints(snapshot):
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.com/array-constraints-schema.json",
        "type": "object",
        "properties": {
            "min_items_array": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 2
            },
            "max_items_array": {
                "type": "array",
                "items": {"type": "number"},
                "maxItems": 3
            },
            "min_max_items_array": {
                "type": "array",
                "items": {"type": "boolean"},
                "minItems": 1,
                "maxItems": 4
            },
        },
        "required": ["min_items_array", "max_items_array", "min_max_items_array"]
    }
    schema = json_schema.create_schema(schema)
    result = JsonExtractor("start", None, schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)

def test_json_schema_array_prefix_items(snapshot):
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.com/prefix-items-schema.json",
        "type": "object",
        "properties": {
            "2_5_prefix_items": {
                "type": "array",
                "prefixItems": [
                    {"type": "string"},
                    {"type": "number"},
                    {"type": "boolean"}
                ],
                "items": False,
                "minItems": 2,
                "maxItems": 5
            },
            "1_4_prefix_items": {
                "type": "array",
                "prefixItems": [
                    {"type": "string"},
                    {"type": "number"}
                ],
                "items": {"type": "boolean"},
                "minItems": 1,
                "maxItems": 4
            },
            "3__prefix_items": {
                "type": "array",
                "prefixItems": [
                    {"type": "string"},
                    {"type": "number"}
                ],
                "minItems": 3,
            },
            "0_4_prefix_items": {
                "type": "array",
                "prefixItems": [{"type": "string"}],
                "maxItems": 4
            },
            "simple_prefix_items": {
                "type": "array",
                "prefixItems": [{"type": "string"}],
            }
        },
        "required": ["2_5_prefix_items", "1_4_prefix_items", "3__prefix_items", "0_4_prefix_items", "simple_prefix_items"]
    }
    schema = json_schema.create_schema(schema)
    result = JsonExtractor("start", None, schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)


def test_json_schema(snapshot):
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.com/random-schema.json",
        "type": "object",
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

def test_schema_with_reference_to_number(snapshot):
    schema = {
        "$id": "https://example.com/schemas/number-reference.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "mainProperty": {"type": "string"},
            "numberReference": {"$ref": "#/$defs/numberDef"}
        },
        "required": ["mainProperty", "numberReference"],
        "$defs": {
            "numberDef": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
            }
        }
    }

    combined_schema = json_schema.create_schema(schema)
    result = JsonExtractor("start", None, combined_schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)


def test_schema_with_top_level_array(snapshot):
    schema = {
        "$id": "https://example.com/schemas/top-level-array.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "active": {"type": "boolean"}
            },
            "required": ["id", "name"]
        },
        "minItems": 1
    }

    combined_schema = json_schema.create_schema(schema)
    result = JsonExtractor("start", None, combined_schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)

def test_schema_with_union_array_object(snapshot):
    schema = {
        "$id": "https://example.com/schemas/union-array-object.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": ["array", "object"],
        "items": {
            "type": "string"
        },
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        },
        "required": ["name"]
    }

    combined_schema = json_schema.create_schema(schema)
    result = JsonExtractor("start", None, combined_schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)

def test_schema_with_top_level_anyOf(snapshot):
    schema = {
        "$id": "https://example.com/schemas/top-level-anyOf.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "anyOf": [
            {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"}
                },
                "required": ["name", "age"]
            },
            {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            {
                "type": "string"
            }
        ]
    }

    combined_schema = json_schema.create_schema(schema)
    result = JsonExtractor("start", None, combined_schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)

def test_schema_with_string_metadata(snapshot):
    schema = {
        "$id": "https://example.com/schemas/string-with-metadata.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "username": {
                "type": "string",
                "minLength": 3,
                "maxLength": 20,
            },
            "email": {
                "type": "string",
                "minLength": 3
            },
            "description": {
                "type": "string",
                "maxLength": 200
            },
            "password": {
                "type": "string",
                "pattern": ".*[A-Za-z].*"
            }
        },
        "required": ["username", "email", "description", "password"]
    }

    combined_schema = json_schema.create_schema(schema)
    result = JsonExtractor("start", None, combined_schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)


def test_schema_with_anyOf_inside_array(snapshot):
    schema = {
        "$id": "https://example.com/schemas/anyOf-inside-array.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "anyOf": [
                        {"type": "string"},
                        {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "value": {"type": "number"}
                            },
                            "required": ["name", "value"]
                        },
                        {"type": "boolean"}
                    ]
                }
            }
        },
        "required": ["items"]
    }

    combined_schema = json_schema.create_schema(schema)
    result = JsonExtractor("start", None, combined_schema, lambda x: x).kbnf_definition
    snapshot.assert_match(result)


def test_pydantic_class_linked_list(snapshot):
    result = JsonExtractor("start", None,LinkedList,lambda x:x).kbnf_definition
    snapshot.assert_match(result)


def test_pydantic_callable(snapshot):
    @formatron.schemas.pydantic.callable_schema
    def foo(a: int, b: typing.Annotated[int, "1124"] = 2):
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
