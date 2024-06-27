import collections
import decimal
import json
import types
import typing

import schemas.schema
from grammar_generators.grammar_generator import GrammarGenerator


class JsonGenerator(GrammarGenerator):
    _space_nonterminal = r"(\u0020|\u000A|\u000D|\u0009)*"

    _grammar_header = rf"""
    integer ::= #"-?(0|[1-9]\d*)";
    number ::= #"-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?";
    string ::= #'"([^\\\\"\x00-\x1f]|\\\\["\\\\bfnrt/]|\\\\u[0-9A-Fa-f]{{4}})*"';
    boolean ::= "true"|"false";
    null ::= "null";
    array ::= array_begin (json_value (comma json_value)*)? array_end;
    object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
    json_value ::= number|string|boolean|null|array|object;
    comma ::= #"{_space_nonterminal},{_space_nonterminal}";
    colon ::= #"{_space_nonterminal}:{_space_nonterminal}";
    object_begin ::= #"{{{_space_nonterminal}";
    object_end ::= #"{_space_nonterminal}}}";
    array_begin ::= #"[{_space_nonterminal}";
    array_end ::= #"{_space_nonterminal}]";
    """
    _type_to_nonterminals = []

    @classmethod
    def register_generate_nonterminal_def(cls, generate_nonterminal_def):
        cls._type_to_nonterminals.append(generate_nonterminal_def)

    @classmethod
    def _register_all_predefined_types(cls):
        def schema(current: typing.Type, nonterminal: str):
            if isinstance(current, type) and not isinstance(current, types.GenericAlias) \
                    and issubclass(current, schemas.schema.Schema):
                line = [f"{nonterminal} ::= ", "object_begin "]
                result = []
                fields = []
                for field, field_info in current.fields().items():
                    field_name = f"{nonterminal}_{field}"
                    fields.append(f"'{field}' colon {field_name}")
                    result.append((field_info, field_name))
                line.append(" comma ".join(fields))
                line.append(" object_end;\n")
                return "".join(line), result
            return None

        def field_info(current: typing.Type, nonterminal: str):
            if isinstance(current, schemas.schema.FieldInfo):
                if current.required:
                    return "", [(current.annotation, nonterminal)]
                else:
                    new_nonterminal = f"{nonterminal}_required"
                    return f"{nonterminal} ::= {new_nonterminal}?;\n", [(current.annotation, new_nonterminal)]
            return None

        def builtin_list(current: typing.Type, nonterminal: str):
            original = typing.get_origin(current)
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
                return "", [(current.__supertype__, nonterminal)]

        cls.register_generate_nonterminal_def(builtin_simple_types)
        cls.register_generate_nonterminal_def(schema)
        cls.register_generate_nonterminal_def(field_info)
        cls.register_generate_nonterminal_def(builtin_tuple)
        cls.register_generate_nonterminal_def(builtin_literal)
        cls.register_generate_nonterminal_def(builtin_union)
        cls.register_generate_nonterminal_def(builtin_list)
        cls.register_generate_nonterminal_def(builtin_dict)

    # Definitions of various non-terminal type handlers (e.g., schema, field_info, builtin_list, etc.)
    # should be added here in a similar manner as the previous implementation.

    def generate(self, schema: typing.Type[schemas.schema.Schema], start_nonterminal: str = "start") -> str:
        result = [self._grammar_header]
        nonterminals = set()
        stack = [(schema, start_nonterminal)]
        while stack:
            (current, nonterminal) = stack.pop()
            for i in self._type_to_nonterminals:
                value = i(current, nonterminal)
                if value is not None:
                    line, to_stack = value
                    result.append(line)
                    stack.extend(to_stack)
                    nonterminals.add(nonterminal)
                    break
            else:
                raise TypeError(f"{type(current)} from {nonterminal} is not supported in json_generators!")
        return "".join(result)

    def match(self, input_str: str) -> tuple[str, typing.Any]:
        # Ensure the input string starts with '{' after stripping leading whitespace
        input_str = input_str.lstrip()
        assert input_str.startswith('{'), "Input string must start with '{'."

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

        # The position now points to the character after the last '}', so we slice to position
        json_str = input_str[:position]
        remaining_str = input_str[position:]
        # Use Python's json library to parse the JSON string
        decoded_json = json.loads(json_str)
        # Return the unparsed remainder of the string and the decoded JSON object
        return remaining_str, decoded_json
