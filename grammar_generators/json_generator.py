import collections
import decimal
import types
import typing
from collections.abc import Sequence

import schemas.schema

_space_nonterminal: str = r"(\u0020|\u000A|\u000D|\u0009)*"
_grammar_header: str = rf"""
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


def register_generate_nonterminal_def(
                                      generate_nonterminal_def: typing.Callable[[typing.Type, str],
                                      typing.Union[tuple[
                                          str, typing.Iterable[tuple[typing.Type, str]]], None]]):
    _type_to_nonterminals.append(generate_nonterminal_def)


def _register_all_predefined_types():
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
                and issubclass(original, Sequence):
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
        if original is typing.Mapping or isinstance(original, type) and issubclass(original, collections.abc.Mapping):
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

    register_generate_nonterminal_def(schema)
    register_generate_nonterminal_def(field_info)
    register_generate_nonterminal_def(builtin_tuple)
    register_generate_nonterminal_def(builtin_literal)
    register_generate_nonterminal_def(builtin_union)
    register_generate_nonterminal_def(builtin_list)
    register_generate_nonterminal_def(builtin_dict)
    register_generate_nonterminal_def(builtin_simple_types)


def generate(schema: typing.Type[schemas.schema.Schema]) -> str:
    result = [_grammar_header]
    nonterminals = set()
    stack = [(schema, f"{schema.__module__.replace('.', '_')}_{schema.__qualname__}")]
    while stack:
        (current, nonterminal) = stack.pop()
        for i in _type_to_nonterminals:
            value = i(current, nonterminal)
            if value is not None:
                line, to_stack = value
                result.append(line)
                stack.extend(to_stack)
                nonterminals.add(nonterminal)
                break
        else:
            raise TypeError(f"{type(current)} from {nonterminal} is not supported in JsonToKbnf!")
    return "".join(result)


_register_all_predefined_types()
