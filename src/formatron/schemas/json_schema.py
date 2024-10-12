"""
This module contains utilities for creating schemas from JSON schemas.
"""

import collections
import collections.abc
import copy
import json
from urllib.parse import urldefrag, urljoin
import frozendict
import jsonschema.validators
from pydantic import typing
import jsonschema
from formatron import schemas
from referencing import Registry, Resource

class FieldInfo(schemas.schema.FieldInfo):
    __slots__ = ("_annotation",)

    def __init__(self, annotation: typing.Type, required:bool):
        """
        Initialize the field information.

        Args:
            annotation: The type annotation of the field.
        """
        self._annotation = annotation
        self._required = required

    @property
    def annotation(self) -> typing.Type[typing.Any] | None:
        """
        Get the type annotation of the field.
        """
        return self._annotation

    @property
    def required(self) -> bool:
        """
        Check if the field is required for the schema.
        """
        return self._required
    
_counter = 0

def create_schema(schema: dict[str, typing.Any], registry=Registry()) -> schemas.schema.Schema:
    """
    Create a Schema object from a JSON schema object.

    This function takes a JSON schema and converts it into a Schema object that can be used
    for data validation and serialization. Currently, only the following JSON Schema features are supported:

    - `type` keyword
    - `minLength, maxLength, pattern` keywords for string type
    - `minimum, maximum, exclusiveMinimum, exclusiveMaximum` keywords for number type and integer type
    - `items` keyword
      - optionally with `minItems`, `maxItems`, `prefixItems` constraints
    - `properties` keyword
      - Due to implementation limitations, we always assume `additionalProperties` is false.
    - `enum` and `const` keyword
      - This includes advanced enum types such as array and object.
      - Note that if both `enum`(or `const`) and `type` are present, `type` will be ignored.
    - `required` keyword
    - `anyOf` keyword
      - This currently does not support factoring out common parts of the subschemas(like https://json-schema.org/understanding-json-schema/reference/combining#factoringschemas)
    - Schema references ($ref and $dynamicRef)
      - Hence, all types of schema identifications(`$defs`, `$id`, `$anchor`, `$dynamicAnchor`) are supported.
      - This includes recursive schema references.
        - Recursive array references(like \[\[\[\[...\]\]\]\]) are not supported yet.
      - Due to implementation limitations, duplicate constraint keywords in both referrers and referents are not allowed.
        - This bound is expected to be loosened in future versions of Formatron where "easily mergeable" constraint keywords will be merged.    
        
    Requirements:
    - The input schema must be a valid JSON Schema according to the JSON Schema Draft 2020-12 standard
    - The root schema's type must be exactly "object" or "array" or both
    - The schema must have a valid '$id' and '$schema' fields
    - All references must be resolvable within the given schema and registry

    Args:
        schema: A dictionary representing a valid JSON schema. 
        registry: A Registry object containing additional schema definitions. 
                                       Defaults to an empty Registry.

    Returns:
        schemas.schema.Schema: A Schema object representing the input JSON schema.

    Raises:
        jsonschema.exceptions.ValidationError: If the input schema is not a valid JSON Schema.
        ValueError: If there are issues with schema references, constraints or requirements.
    """
    registry = copy.deepcopy(registry)
    schema = copy.deepcopy(schema)
    _validate_json_schema(schema)
    registry = Resource.from_contents(schema) @ registry
    json_schema_id_to_schema = {}
    memo = set()
    _recursive_resolve_reference(schema["$id"], schema, registry, memo)
    memo.clear()
    _merge_referenced_schema(schema,memo)
    result = _convert_json_schema_to_our_schema(schema,json_schema_id_to_schema)
    return result

def _resolve_new_url(uri: str, ref: str) -> str:
    """
    Adapted from https://github.com/python-jsonschema/referencing/blob/main/referencing/_core.py#L667.
    """
    if not ref.startswith("#"):
        uri, _ = urldefrag(urljoin(uri, ref))
    return uri

def _validate_json_schema(schema: dict[str, typing.Any]) -> None:
    if "type" in schema:
        root_type = schema["type"]
        if isinstance(root_type, str):
            if root_type not in ["object", "array"]:
                raise ValueError("Root schema type must be 'object' or 'array'")
        elif isinstance(root_type, list):
            if not set(root_type).issubset({"object", "array"}):
                raise ValueError("Root schema type must be 'object', 'array', or both")
        else:
            raise ValueError("Invalid 'type' specification in root schema")
    jsonschema.validate(instance=schema, schema=jsonschema.validators.Draft202012Validator.META_SCHEMA)

def _convert_json_schema_to_our_schema(schema: dict[str, typing.Any], json_schema_id_to_schema: dict[int, typing.Type])->typing.Type:
    """
    Recursively handle all types needed to fully determine the type of a schema
    """
    schema_id = id(schema)
    if schema_id in json_schema_id_to_schema: # Circular reference
        return json_schema_id_to_schema[schema_id]
    if isinstance(schema, dict):
        _inferred_type = _infer_type(schema, json_schema_id_to_schema)
        if "properties" in schema:
            fields = _extract_fields_from_object_type(json_schema_id_to_schema[schema_id])
            properties = schema["properties"]
            required = schema.get("required", [])
            for _property in properties:
                fields[_property] = FieldInfo(_convert_json_schema_to_our_schema(properties[_property], json_schema_id_to_schema), required=_property in required)
        return _inferred_type
    
def _extract_fields_from_object_type(object_type:typing.Type):
    args = typing.get_args(object_type)
    for arg in args:
        if isinstance(arg, type) and issubclass(arg, schemas.schema.Schema):
            return arg.fields()
    return object_type.fields()

def _handle_anyOf(schema: dict[str, typing.Any], json_schema_id_to_schema: dict[int, typing.Type]) -> typing.Type:
    allowed_keys = {"anyOf", "$id", "$schema"}
    assert set(schema.keys()).issubset(allowed_keys), "Only 'anyOf', '$id', and '$schema' are allowed when 'anyOf' is present"
    new_list = []
    for item in schema["anyOf"]:
        new_list.append(_convert_json_schema_to_our_schema(item, json_schema_id_to_schema))
    return typing.Union[tuple(new_list)]

def _infer_type(schema: dict[str, typing.Any], json_schema_id_to_schema: dict[int, typing.Type]) -> typing.Type[typing.Any | None]:
    """
    Infer more specific types.
    """
    if "anyOf" in schema:
        return _handle_anyOf(schema, json_schema_id_to_schema)
    obtained_type = _obtain_type(schema, json_schema_id_to_schema)
    if obtained_type is None:
        obtained_type = typing.Union[str, float, int, bool, None, list[typing.Any]]
    args = typing.get_args(obtained_type)
    if not args:
        args = [obtained_type]
    else:
        args = list(args)
    for i, arg in enumerate(args):
        if arg is object:
            args[i] = _create_custom_type(schema, json_schema_id_to_schema)
        elif arg is list:
            args[i] = _handle_list_metadata(obtained_type, schema, json_schema_id_to_schema)
        elif arg is str:
            args[i] = _handle_str_with_metadata(schema)
        elif arg is int or arg is float:
            args[i] = _handle_numeric_with_metadata(schema, arg)
    if typing.get_origin(obtained_type) is typing.Union:
        obtained_type = typing.Union[tuple(args)]
    elif typing.get_origin(obtained_type) is typing.Literal:
        obtained_type = typing.Literal[tuple(args)]
    else:
        obtained_type = args[0]
    json_schema_id_to_schema[id(schema)] = obtained_type
    return obtained_type

def _get_literal(schema: dict[str, typing.Any]) -> typing.Any:
    if "enum" in schema and "const" in schema:
        raise ValueError("JSON schema cannot contain both 'enum' and 'const' keywords")
    return tuple(schema["enum"]) if "enum" in schema else schema.get("const")

def _handle_literal(literal: typing.Any, obtained_type: typing.Type, schema: dict[str, typing.Any], json_schema_id_to_schema: dict[int, typing.Type]) -> typing.Type:
    # TODO: validate literal against obtained_type
    if not isinstance(literal, tuple):
        literal = (literal,)
    literal = frozendict.deepfreeze(literal)
    literal_type = typing.Literal[literal]
    return literal_type

def _handle_str_with_metadata(schema: dict[str, typing.Any]) -> typing.Type:
    """
    Handle string type with metadata such as maxLength, minLength, and pattern.
    """
    metadata = {}
    if "maxLength" in schema:
        metadata["max_length"] = schema["maxLength"]
    if "minLength" in schema:
        metadata["min_length"] = schema["minLength"]
    if "pattern" in schema:
        metadata["pattern"] = schema["pattern"]
    
    if metadata:
        return schemas.schema.TypeWithMetadata(str, metadata)
    return str

def _handle_numeric_with_metadata(schema: dict[str, typing.Any], numeric_type: typing.Type) -> typing.Type:
    """
    Handle numeric types (int or float) with metadata such as minimum, maximum, exclusiveMinimum, and exclusiveMaximum.
    """
    metadata = {}
    if "minimum" in schema:
        metadata["ge"] = schema["minimum"]
    if "maximum" in schema:
        metadata["le"] = schema["maximum"]
    if "exclusiveMinimum" in schema:
        metadata["gt"] = schema["exclusiveMinimum"]
    if "exclusiveMaximum" in schema:
        metadata["lt"] = schema["exclusiveMaximum"]
    
    if metadata:
        return schemas.schema.TypeWithMetadata(numeric_type, metadata)
    return numeric_type



def _create_custom_type(schema: dict[str, typing.Any], json_schema_id_to_schema: dict[int, typing.Type]) -> typing.Type:
    global _counter
    fields = {}
    new_type = type(f"__json_schema_{_counter}", (schemas.schema.Schema,), {
        "from_json": classmethod(lambda cls, x: json.loads(x)),
        "fields": classmethod(lambda cls: fields)
    })
    _counter += 1
    json_schema_id_to_schema[id(schema)] = new_type
    return new_type

def _handle_list_metadata(obtained_type: typing.Type, schema: dict[str, typing.Any], json_schema_id_to_schema: dict[int, typing.Type]) -> typing.Type:
    """
    Handle cases where the obtained type is a list
    """
    metadata = {}
    if "minItems" in schema:
        metadata["min_length"] = schema["minItems"]
    if "maxItems" in schema:
        metadata["max_length"] = schema["maxItems"]
    if "prefixItems" in schema:
        metadata["prefix_items"] = tuple(_convert_json_schema_to_our_schema(i, json_schema_id_to_schema) for i in schema["prefixItems"])
    item_type = typing.Any
    if "items" in schema:
        if schema["items"] == False:
            metadata["additional_items"] = False
        else:
            item_type = _convert_json_schema_to_our_schema(schema["items"], json_schema_id_to_schema)
            if item_type is None:
                item_type = typing.Any
    if metadata:
        if "additional_items" not in metadata:
            metadata["additional_items"] = True
        return schemas.schema.TypeWithMetadata(list, metadata)
    return list[item_type]


def _obtain_type(schema: dict[str, typing.Any], json_schema_id_to_schema:dict[int, typing.Type]) -> typing.Type[typing.Any|None]:
    """
    Directly obtain type information from this schema's type keyword.
    """
    if "type" not in schema:
        obtained_type = None
    else:
        json_type = schema["type"]
        if json_type == "string":
            obtained_type = str
        elif json_type == "number":
            obtained_type = float
        elif json_type == "integer":
            obtained_type = int
        elif json_type == "boolean":
            obtained_type = bool
        elif json_type == "null":
            obtained_type = type(None)
        elif json_type == "array":
            obtained_type = list
        elif json_type == "object":
            obtained_type = object
        elif isinstance(json_type, collections.abc.Sequence):
            new_list = []
            for item in json_type:
                new_schema = schema.copy()
                new_schema["type"] = item
                new_list.append(_obtain_type(new_schema, json_schema_id_to_schema))
            obtained_type = typing.Union[tuple(new_list)]
        else:
            raise TypeError(f"Unsupported type in json schema: {json_type}")
    literal = _get_literal(schema)
    if literal is not None:
        return _handle_literal(literal, obtained_type, schema, json_schema_id_to_schema)
    return obtained_type





def _merge_referenced_schema(schema: dict[str, typing.Any], memo: set[int]):
    keys = ["$ref", "$dynamicRef"]
    if id(schema) in memo: # Circular reference
        return None
    if isinstance(schema, list):
        memo.add(id(schema))
        for item in schema:
            _merge_referenced_schema(item, memo)
    elif isinstance(schema, dict):
        memo.add(id(schema))
        for key in keys:
            if key in schema:
                _merge_referenced_schema(schema[key], memo) # ensure no unmerged references
                for ref_key, ref_value in schema[key].items():
                    _merge_key(schema, ref_key, ref_value)
                del schema[key]
        for key, value in schema.items():
            _merge_referenced_schema(value, memo)

def _merge_key(schema:dict[str, typing.Any], ref_key:str, reference_value:typing.Any):
    if ref_key not in schema:
        schema[ref_key] = reference_value
        return None
    if schema[ref_key] is reference_value:
        return None
    if isinstance(schema[ref_key], dict) and isinstance(reference_value, dict):
        for new_ref_key, new_ref_value in reference_value.items():
            _merge_key(schema[ref_key], new_ref_key, new_ref_value)
        return None
    if ref_key in ("$id", "$schema"):
        # For $id and $schema, keep the original value
        return None
    if isinstance(schema[ref_key], (str, int, float, bool)) and isinstance(reference_value, (str, int, float, bool)):
        if schema[ref_key] == reference_value:
            return None
    raise ValueError(f"Duplicate keys in schema referenced by {ref_key} in JSON schema: {schema} is not supported")
    

def _recursive_resolve_reference(base_uri: str, schema: typing.Any, registry: Registry, memo: set[int]):
    if id(schema) in memo:
        return schema
    memo.add(id(schema))
    if isinstance(schema, list):
        new_list = []
        for item in schema:
            new_list.append(_recursive_resolve_reference(base_uri, item, registry, memo))
        schema.clear()
        schema.extend(new_list)
    if isinstance(schema, dict):
        if "$id" in schema:
            base_uri = _resolve_new_url(base_uri, schema["$id"])
        resolver = registry.resolver(base_uri)
        keys = ["$ref", "$dynamicRef"]
        for key in keys:
            if key in schema:
                _resolve_reference(schema, key, resolver)
        for key, value in schema.items():
            _recursive_resolve_reference(base_uri, value, registry, memo)
    return schema

def _resolve_reference(schema: dict[str, typing.Any], key: str, resolver: typing.Any):
    resolved = resolver.lookup(schema[key])
    if resolved.contents is schema:
        raise ValueError(f"Circular self reference detected in JSON schema: {schema}")
    schema[key] = resolved.contents