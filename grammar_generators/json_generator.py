import decimal
import typing

import grammar_generators.grammar_generator
import schemas.schema


class JsonAsKbnf(grammar_generators.grammar_generator.GrammarGenerator):
    _space_nonterminal: typing.ClassVar[str] = r"(\u0020|\u000A|\u000D|\u0009)*"
    _grammar_header: typing.ClassVar[str] = rf"""
integer ::= #"-?(0|[1-9]\d*)";
number ::= #"-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?";
string ::= #'"([^\\\\"\x00-\x1f]|\\\\["\\\\bfnrt/]|\\\\u[0-9A-Fa-f]{{4}})*"';
boolean ::= "true"|"false";
null ::= "null";
comma ::= #"{_space_nonterminal},{_space_nonterminal}";
colon ::= #"{_space_nonterminal}:{_space_nonterminal}";
object_begin ::= #"{{{_space_nonterminal}";
object_end ::= #"{_space_nonterminal}}}";
array_begin ::= #"[{_space_nonterminal}";
array_end ::= #"{_space_nonterminal}]";
"""
    _type_to_nonterminals = []

    @classmethod
    def register_generate_nonterminal_def(cls,
                                          generate_nonterminal_def: typing.Callable[[typing.Type, str],
                                          typing.Union[typing.Tuple[str, typing.Iterable[typing.Tuple[typing.Type, str]]], None]]):
        cls._type_to_nonterminals.append(generate_nonterminal_def)

    @classmethod
    def _register_all_predefined_types(cls):
        def schema(current: typing.Type, nonterminal: str):
            if isinstance(current, type) and issubclass(current, schemas.schema.Schema):
                line = [f"{nonterminal} ::= ", "object_begin "]
                result = []
                fields = []
                for field, field_info in current.fields().items():
                    field_name = f"{nonterminal}_{field}"
                    fields.append(f"'{field}' colon {field_name}")
                    result.append((field_info, field_name))
                line.append(" comma ".join(fields))
                line.append("object_end;\n")
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
            if typing.get_origin(current) is list or isinstance(current, type) and issubclass(current, list):
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
            if typing.get_origin(current) is dict or isinstance(current, type) and issubclass(current, dict):
                new_nonterminal = f"{nonterminal}_value"
                args = typing.get_args(current)
                if not args:
                    value = typing.Any
                else:
                    assert issubclass(args[0], str), f"{args[0]} is not string!"
                    value = args[1]
                return f"{nonterminal} ::=" \
                       f" object_begin (string colon {new_nonterminal} (comma string colon {new_nonterminal})*)? " \
                       f"object_end;\n", \
                    [(value, new_nonterminal)]
            return None

        def builtin_simple_types(current: typing.Type, nonterminal: str):
            if isinstance(current, type) and issubclass(current, int):
                return f"{nonterminal} ::= integer;\n", []
            elif isinstance(current, type) and issubclass(current, float):
                return f"{nonterminal} ::= number;\n", []
            elif isinstance(current, type) and issubclass(current, decimal.Decimal):
                return f"{nonterminal} ::= number;\n", []
            elif isinstance(current, type) and issubclass(current, str):
                return f"{nonterminal} ::= string;\n", []
            elif isinstance(current, type) and issubclass(current, type(None)):
                return f"{nonterminal} ::= null;\n", []
            elif isinstance(current, type) and issubclass(current, bool):
                return f"{nonterminal} ::= boolean;\n", []

        cls.register_generate_nonterminal_def(schema)
        cls.register_generate_nonterminal_def(field_info)
        cls.register_generate_nonterminal_def(builtin_list)
        cls.register_generate_nonterminal_def(builtin_dict)
        cls.register_generate_nonterminal_def(builtin_simple_types)

    def generate(self, schema: typing.Type[schemas.schema.Schema]) -> str:
        result = [JsonAsKbnf._grammar_header]
        nonterminals = set()
        stack = [(schema, f"{schema.__module__.replace('.', '_')}_{schema.__qualname__}")]
        while stack:
            (current, nonterminal) = stack.pop()
            for i in self.__class__._type_to_nonterminals:
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


JsonAsKbnf._register_all_predefined_types()
