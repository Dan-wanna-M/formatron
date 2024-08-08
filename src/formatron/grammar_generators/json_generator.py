"""
The module defines the `JsonGenerator` class, a KBNF grammar generator for JSON format.
"""
import collections
import decimal
import types
import typing

import extractor
import schemas.schema
from grammar_generators.grammar_generator import GrammarGenerator

__all__ = ["JsonGenerator"]


class JsonGenerator(GrammarGenerator):
    """
    A KBNF grammar generator for JSON format.

    Currently, the following data types are supported:

    - bool
    - int
    - float
    - string
    - NoneType
    - typing.Any
    - Subclasses of collections.abc.Mapping[str,T] and typing.Mapping[str,T] where T is a supported type,
    - Subclasses of collections.abc.Sequence[T] and typing.Sequence[T] where T is a supported type.
    - tuple[T1,T2,...] where T1,T2,... are supported types. The order, type and number of elements will be preserved.
    - typing.Literal[x1,x2,...] where x1, x2, ... are instances of int, string, bool or NoneType, or another typing.Literal[y1,y2,...]
    - typing.Union[T1,T2,...] where T1,T2,... are supported types.
    - schemas.Schema where all its fields' data types are supported. Recursive schema definitions are supported as well.
    """
    _space_nonterminal = "(\\u0020|\\u000A|\\u000D|\\u0009)*"

    _grammar_header = rf"""integer ::= #"-?(0|[1-9]\\d*)";
number ::= #"-?(0|[1-9]\\d*)(\\.\\d+)?([eE][+-]?\\d+)?";
string ::= #'"([^\\\\"\u0000-\u001f]|\\\\["\\\\bfnrt/]|\\\\u[0-9A-Fa-f]{{4}})*"';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"{_space_nonterminal},{_space_nonterminal}";
colon ::= #"{_space_nonterminal}:{_space_nonterminal}";
object_begin ::= #"\\{{{_space_nonterminal}";
object_end ::= #"{_space_nonterminal}\\}}";
array_begin ::= #"\\[{_space_nonterminal}";
array_end ::= #"{_space_nonterminal}\\]";
"""
    _type_to_nonterminals = []

    @classmethod
    def register_generate_nonterminal_def(
            cls,
            generate_nonterminal_def: typing.Callable[
                [typing.Type, str],
                typing.Optional[typing.Tuple[str,
                                             typing.List[typing.Tuple[typing.Type, str]]]]]) -> None:
        """
        Register a callable to generate nonterminal definition from a type.
        The callable returns (nonterminal_definition, [(sub_type, sub_nonterminal), ...])
        if the type is supported by this callable, otherwise None.
        [(sub_type, sub_nonterminal), ...] are the types and nonterminals used in nonterminal_definition that may need
        to be generated in the grammar too.

        Args:
            generate_nonterminal_def: A callable to generate nonterminal definition from a type.
        """
        cls._type_to_nonterminals.append(generate_nonterminal_def)

    @classmethod
    def _register_all_predefined_types(cls):
        def schema(current: typing.Type, nonterminal: str):
            if isinstance(current, type) and not isinstance(current, types.GenericAlias) \
                    and issubclass(current, schemas.schema.Schema):
                line = [f"{nonterminal} ::= ", "object_begin "]
                result = []
                fields = []
                for field, _field_info in current.fields().items():
                    field_name = f"{nonterminal}_{field}"
                    fields.append(f"'\"{field}\"' colon {field_name}")
                    result.append((_field_info, field_name))
                line.append(" comma ".join(fields))
                line.append(" object_end;\n")
                return "".join(line), result
            return None

        def field_info(current: typing.Type, nonterminal: str):
            if isinstance(current, schemas.schema.FieldInfo):
                if current.required:
                    return "", [(current.annotation, nonterminal)]
                new_nonterminal = f"{nonterminal}_required"
                return f"{nonterminal} ::= {new_nonterminal}?;\n", [(current.annotation, new_nonterminal)]
            return None

        def builtin_list(current: typing.Type, nonterminal: str):
            original = typing.get_origin(current)
            if original is None:
                original = current
            if original is typing.Sequence or isinstance(original, type) \
                    and issubclass(original, collections.abc.Sequence):
                new_nonterminal = f"{nonterminal}_value"
                annotation = typing.get_args(current)
                if not annotation:
                    annotation = typing.Any
                else:
                    annotation = annotation[0]
                return f"{nonterminal} ::= array_begin ({new_nonterminal} (comma {new_nonterminal})*)? array_end;\n", \
                    [(annotation, new_nonterminal)]
            return None

        def builtin_dict(current: typing.Type, nonterminal: str):
            original = typing.get_origin(current)
            if original is None:
                original = current
            if original is typing.Mapping or isinstance(original, type) and issubclass(original,
                                                                                       collections.abc.Mapping):
                new_nonterminal = f"{nonterminal}_value"
                args = typing.get_args(current)
                if not args:
                    value = typing.Any
                else:
                    assert issubclass(args[0], str), f"{args[0]} is not string!"
                    value = args[1]
                return f"{nonterminal} ::=" \
                       f" object_begin (string colon {new_nonterminal} (comma string colon {new_nonterminal})*)?" \
                       f" object_end;\n", \
                    [(value, new_nonterminal)]
            return None

        def builtin_tuple(current: typing.Type, nonterminal: str):
            if typing.get_origin(current) is tuple or isinstance(current, type) and issubclass(current, tuple):
                args = typing.get_args(current)
                new_nonterminals = []
                result = []
                for i, arg in enumerate(args):
                    result.append(arg)
                    new_nonterminals.append(f"{nonterminal}_{i}")
                return f"{nonterminal} ::=array_begin {' comma '.join(new_nonterminals)} array_end;\n", \
                    zip(result, new_nonterminals)

        def builtin_union(current: typing.Type, nonterminal: str):
            if typing.get_origin(current) is typing.Union:
                args = typing.get_args(current)
                assert args, f"{current} from {nonterminal} cannot be an empty union!"
                new_nonterminals = []
                result = []
                for i, arg in enumerate(args):
                    result.append(arg)
                    new_nonterminals.append(f"{nonterminal}_{i}")
                return f"{nonterminal} ::= {' | '.join(new_nonterminals)};\n", zip(result, new_nonterminals)

        def builtin_literal(current: typing.Type, nonterminal: str):
            if typing.get_origin(current) is typing.Literal:
                args = typing.get_args(current)
                assert args, f"{current} from {nonterminal} cannot be an empty literal!"
                new_nonterminals = []
                result = []
                for i, arg in enumerate(args):
                    if isinstance(arg, str):
                        new_nonterminals.append(f"{repr(arg)}")
                    elif isinstance(arg, bool):
                        new_nonterminals.append(f"'{str(arg)}'")
                    elif isinstance(arg, int):
                        new_nonterminals.append(f"'{str(arg)}'")
                    elif arg is None:
                        new_nonterminals.append("null")
                    else:
                        new_nonterminal = f"{nonterminal}_{i}"
                        result.append((arg, new_nonterminal))
                        new_nonterminals.append(new_nonterminal)
                return f"{nonterminal} ::= {' | '.join(new_nonterminals)};\n", result

        def builtin_simple_types(current: typing.Type, nonterminal: str):
            if isinstance(current, type) and issubclass(current, bool):
                return f"{nonterminal} ::= boolean;\n", []
            elif isinstance(current, type) and issubclass(current, int):
                return f"{nonterminal} ::= integer;\n", []
            elif isinstance(current, type) and issubclass(current, float):
                return f"{nonterminal} ::= number;\n", []
            elif isinstance(current, type) and issubclass(current, decimal.Decimal):
                return f"{nonterminal} ::= number;\n", []
            elif isinstance(current, type) and issubclass(current, str):
                return f"{nonterminal} ::= string;\n", []
            elif isinstance(current, type) and issubclass(current, type(None)):
                return f"{nonterminal} ::= null;\n", []
            elif current is typing.Any:
                return f"{nonterminal} ::= json_value;\n", []
            elif type(current) is typing.NewType:
                current: typing.NewType
                return "", [(current.__supertype__, nonterminal)]

        cls.register_generate_nonterminal_def(builtin_simple_types)
        cls.register_generate_nonterminal_def(schema)
        cls.register_generate_nonterminal_def(field_info)
        cls.register_generate_nonterminal_def(builtin_tuple)
        cls.register_generate_nonterminal_def(builtin_literal)
        cls.register_generate_nonterminal_def(builtin_union)
        cls.register_generate_nonterminal_def(builtin_list)
        cls.register_generate_nonterminal_def(builtin_dict)

    def generate(self, schema: typing.Type[schemas.schema.Schema], start_nonterminal: str = "start") -> str:
        """
        Generate a KBNF grammar string from a schema for JSON format.

        Args:
            schema: The schema to generate a grammar for.
            start_nonterminal: The start nonterminal of the grammar. Default is "start".

        Returns:
            The generated KBNF grammar string.
        """
        type_id_to_nonterminal = {
            id(int): "integer",
            id(float): "number",
            id(str): "string",
            id(bool): "boolean",
            id(type(None)): "null",
            id(list): "array",
            id(dict): "object",
        }
        result = [self._grammar_header]
        nonterminals = set()
        stack = [(schema, start_nonterminal)]
        while stack:
            (current, nonterminal) = stack.pop()
            type_id = id(current)
            if type_id in type_id_to_nonterminal:
                line = f"{nonterminal} ::= {type_id_to_nonterminal[type_id]};\n"
                result.append(line)
                continue
            type_id_to_nonterminal[type_id] = nonterminal
            for i in self._type_to_nonterminals:
                value = i(current, nonterminal)
                if value is not None:
                    line, to_stack = value
                    result.append(line)
                    stack.extend(to_stack)
                    nonterminals.add(nonterminal)
                    break
            else:
                raise TypeError(f"{current} from {nonterminal} is not supported in json_generators!")
        return "".join(result)

    def get_extractor(self, nonterminal: str, capture_name: typing.Optional[str],
                      to_object: typing.Callable[[str, ], schemas.schema.Schema]) -> extractor.Extractor:
        return JsonExtractor(nonterminal, capture_name, to_object)


class JsonExtractor(extractor.Extractor):
    """
    An extractor that loads json data to an object from a string.
    """
    def __init__(self, nonterminal: str, capture_name: typing.Optional[str],
                 to_object: typing.Callable[[str, ], schemas.schema.Schema]):
        """
        Create an extractor.

        Args:
            nonterminal: The nonterminal representing the extractor.
            capture_name: The capture name of the extractor, or `None` if the extractor does not capture.
            to_object: A callable to convert the extracted string to a schema instance.
        """
        super().__init__(capture_name)
        self._nonterminal = nonterminal
        self._to_object = to_object

    @property
    def kbnf_representation(self) -> str:
        return self._nonterminal

    def extract(self, input_str: str) -> typing.Optional[tuple[str, schemas.schema.Schema]]:
        """
        Extract a schema instance from a string.

        Args:
            input_str: The input string to extract from.

        Returns:
            A tuple of the remaining string and the extracted schema instance, or `None` if extraction failed.
        """

        # Ensure the input string starts with '{' after stripping leading whitespace
        input_str = input_str.lstrip()
        if not input_str.startswith('{'):
            return None

        # Variables to track the balance of brackets and the position in the string
        bracket_count = 0
        position = 0

        # Iterate over the string to find where the JSON object ends
        for char in input_str:
            if char == '{':
                bracket_count += 1
            elif char == '}':
                bracket_count -= 1

            # Move to the next character
            position += 1

            # If brackets are balanced, stop processing
            if bracket_count == 0:
                break
        else:
            return None
        # The position now points to the character after the last '}', so we slice to position
        json_str = input_str[:position]
        remaining_str = input_str[position:]
        # Return the unparsed remainder of the string and the decoded JSON object
        return remaining_str, self._to_object(json_str)


JsonGenerator._register_all_predefined_types()
