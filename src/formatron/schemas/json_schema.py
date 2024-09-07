"""
This module contains utilities for creating schemas from JSON schemas.
"""

import collections
import collections.abc
import copy
import inspect
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

def create_schema(schemas: dict[str, typing.Any]|typing.Iterable[dict[str, typing.Any]], registry=Registry()
                  ) -> schemas.schema.Schema|typing.Iterable[dict[str, typing.Any]]:
    """
    
    """
    if isinstance(schemas, dict):
        schemas = [schemas]
    resources = []
    for schema in schemas:
        _validate_json_schema(schema)
        resources.append(Resource.from_contents(schema))
    registry = resources @ registry
    json_schema_id_to_schema = {}
    memo = set()
    result = []
    for schema in resources:
        schema = schema.contents
        _recursive_resolve_reference(schema["$id"], schema, registry)
        _merge_referenced_schema(schema,memo)
        result.append(_convert_json_schema_to_our_schema(schema,json_schema_id_to_schema))
    if len(result) == 1:
        return result[0]
    return result

def _resolve_new_url(uri: str, ref: str) -> str:
    """
    Adapted from https://github.com/python-jsonschema/referencing/blob/main/referencing/_core.py#L667.
    """
    if not ref.startswith("#"):
        uri, _ = urldefrag(urljoin(uri, ref))
    return uri

def _validate_json_schema(schema: dict[str, typing.Any]) -> None:
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
    
def _infer_type(schema: dict[str, typing.Any], json_schema_id_to_schema: dict[int, typing.Type]) -> typing.Type[typing.Any | None]:
    """
    Infer more specific types.
    """
    obtained_type = _obtain_type(schema, json_schema_id_to_schema)
    args = typing.get_args(obtained_type)
    if obtained_type is None or obtained_type is object or object in args:
        return _create_custom_type(obtained_type, schema, json_schema_id_to_schema)
    if obtained_type is typing.List and "items" in schema:
        item_type = _convert_json_schema_to_our_schema(schema["items"], json_schema_id_to_schema)
        obtained_type = typing.List[item_type]
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

def _create_custom_type(obtained_type: typing.Type|None, schema: dict[str, typing.Any], json_schema_id_to_schema: dict[int, typing.Type]) -> typing.Type:
    global _counter
    fields = {}
    new_type = type(f"__json_schema_{_counter}", (schemas.schema.Schema,), {
        "from_json": classmethod(lambda cls, x: json.loads(x)),
        "fields": classmethod(lambda cls: fields)
    })
    _counter += 1
    
    if obtained_type is None:
        json_schema_id_to_schema[id(schema)] = typing.Union[str, float, int, bool, None, typing.List[typing.Any], new_type]
    elif object in typing.get_args(obtained_type):
        json_schema_id_to_schema[id(schema)] = typing.Union[tuple(item for item in typing.get_args(obtained_type) if item is not object)+(new_type,)]
    else:
        json_schema_id_to_schema[id(schema)] = obtained_type
    return json_schema_id_to_schema[id(schema)]


def _obtain_type(schema: dict[str, typing.Any], json_schema_id_to_schema:dict[int, typing.Type]) -> typing.Type[typing.Any|None]:
    """
    Directly obtain type information from this schema level.
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
            obtained_type = typing.List
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
    memo.add(id(schema))
    if isinstance(schema, list):
        for item in schema:
            _merge_referenced_schema(item, memo)
    elif isinstance(schema, dict):
        for key in keys:
            if key in schema:
                _merge_referenced_schema(schema[key], memo) # ensure no unmerged references
                for ref_key, ref_value in schema[key].items():
                    _merge_key(schema, ref_key, ref_value)
                    schema[ref_key] = ref_value
                del schema[key]
        for key, value in schema.items():
            if key not in keys:
                _merge_referenced_schema(value, memo)

def _merge_key(schema:dict[str, typing.Any], ref_key:str, reference_value:typing.Any):
    if ref_key not in schema:
        schema[ref_key] = reference_value
        return None
    if isinstance(schema[ref_key], dict) and isinstance(reference_value, dict):
        for new_ref_key, new_ref_value in reference_value.items():
            _merge_key(schema[ref_key], new_ref_key, new_ref_value)
        return None
    raise ValueError(f"Duplicate keys in schema referenced by {ref_key} in JSON schema: {schema} is not supported")
    

def _recursive_resolve_reference(base_uri: str, schema: typing.Any, registry: Registry):
    if isinstance(schema, list):
        new_list = []
        for item in schema:
            new_list.append(_recursive_resolve_reference(base_uri, item, registry))
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
            if key not in keys:
                _recursive_resolve_reference(base_uri, value, registry)
    return schema

def _resolve_reference(schema: dict[str, typing.Any], key: str, resolver: typing.Any):
    resolved = resolver.lookup(schema[key])
    if resolved.contents is schema:
        raise ValueError(f"Circular self reference detected in JSON schema: {schema}")
    schema[key] = resolved.contents