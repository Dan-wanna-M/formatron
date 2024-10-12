"""
The module defines the `JsonExtractor` class, which is used to extract data from a string in JSON format.
"""
import collections
import decimal
import types
import typing

from frozendict import frozendict

from formatron import extractor, schemas

__all__ = ["JsonExtractor"]

SPACE_NONTERMINAL = "[ \t\n\r]*"

GRAMMAR_HEADER = rf"""integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'"([^\\\\"\u0000-\u001f]|\\\\["\\\\bfnrt/]|\\\\u[0-9A-Fa-f]{{4}})*"';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"{SPACE_NONTERMINAL},{SPACE_NONTERMINAL}";
colon ::= #"{SPACE_NONTERMINAL}:{SPACE_NONTERMINAL}";
object_begin ::= #"\\{{{SPACE_NONTERMINAL}";
object_end ::= #"{SPACE_NONTERMINAL}\\}}";
array_begin ::= #"\\[{SPACE_NONTERMINAL}";
array_end ::= #"{SPACE_NONTERMINAL}\\]";
"""
_type_to_nonterminals = []


def register_generate_nonterminal_def(
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
    _type_to_nonterminals.append(generate_nonterminal_def)


def _register_all_predefined_types():
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
            annotation = current.annotation
            if current.required:
                return "", [(annotation, nonterminal)]
            new_nonterminal = f"{nonterminal}_required"
            return f"{nonterminal} ::= {new_nonterminal}?;\n", [(annotation, new_nonterminal)]
        return None

    def string_metadata(current: typing.Type, nonterminal: str):
        min_length = current.metadata.get("min_length")
        max_length = current.metadata.get("max_length")
        pattern = current.metadata.get("pattern")
        if pattern:
            assert not (min_length or max_length), "pattern is mutually exclusive with min_length and max_length"
        repetition_map = {
            (True, False): f"{{{min_length},}}",
            (False, True): f"{{0,{max_length}}}",
            (True, True): f"{{{min_length},{max_length}}}"
        }
        repetition = repetition_map.get((min_length is not None, max_length is not None))
        if repetition is not None:
            return fr"""{nonterminal} ::= #'"([^\\\\"\u0000-\u001f]|\\\\["\\\\bfnrt/]|\\\\u[0-9A-Fa-f]{{4}}){repetition}"';
""", []
        if pattern is not None:
            pattern = pattern.replace("'", "\\'")
            return f"""{nonterminal} ::= #'"{pattern}"';\n""", []
    
    def number_metadata(current: typing.Type, nonterminal: str):
        gt = current.metadata.get("gt")
        ge = current.metadata.get("ge")
        lt = current.metadata.get("lt")
        le = current.metadata.get("le")
        
        prefix_map = {
            (gt, 0): "",
            (ge, 0): "0|",
            (lt, 0): "-",
            (le, 0): "0|-",
        }
        
        for (condition, value), prefix in prefix_map.items():
            if condition is not None and condition == value:
                if issubclass(current.type, int):
                    return f"""{nonterminal} ::= #'{prefix}[1-9][0-9]*';\n""", []
                elif issubclass(current.type, float):
                    return f"""{nonterminal} ::= #'{prefix}[1-9][0-9]*(\\.[0-9]+)?([eE][+-]?[0-9]+)?';\n""", []
        
        raise ValueError(f"{current.type.__name__} metadata {current.metadata} is not supported in json_generators!")
    
    def sequence_metadata(current: typing.Type, nonterminal: str):
        min_items = current.metadata.get("min_length")
        max_items = current.metadata.get("max_length")
        prefix_items = current.metadata.get("prefix_items")
        additional_items = current.metadata.get("additional_items")
        if max_items is not None and prefix_items is not None and max_items <= len(prefix_items): # truncate prefix items
            prefix_items = prefix_items[:max_items+1]
        if prefix_items:
            if not min_items: # json schema defaults to 0
                min_items = 0
            if not additional_items:
                if min_items > len(prefix_items):
                    raise ValueError(f"min_items {min_items} is greater than the number of prefix_items {len(prefix_items)} and additional_items is not allowed")
                max_items = len(prefix_items)
        if min_items is not None or max_items is not None: # prefix items will set min
            new_nonterminal = f"{nonterminal}_item"
            ebnf_rules = []
            if min_items is None:
                min_items = 0
            if min_items == 0 and max_items is None and prefix_items is None: # no special handling needed
                return "", [(current.type, new_nonterminal)]
            prefix_items_nonterminals = [f"{new_nonterminal}_{i}" for i in range(len(prefix_items))] if prefix_items else []
            prefix_items_parts = [] # contains the sequence of nonterminals for prefix items from min_items to len(prefix_items)
            if prefix_items is not None:
                for i in range(max(min_items,1), len(prefix_items)+1):
                    prefix_items_parts.append(prefix_items_nonterminals[:i])
                if min_items == 0:
                    ebnf_rules.append(f"{nonterminal} ::= array_begin array_end;")
            if max_items is None: # unbounded
                if not prefix_items:
                    min_items_part = ' comma '.join([new_nonterminal] * (min_items - 1))
                    ebnf_rules.append(f"{nonterminal} ::= array_begin {min_items_part} comma {new_nonterminal}+ array_end;")
                elif len(prefix_items_parts) >= min_items:
                    for prefix_items_part in prefix_items_parts:
                        prefix_items_part = ' comma '.join(prefix_items_part)
                    ebnf_rules.append(f"{nonterminal} ::= array_begin {prefix_items_part} (comma {new_nonterminal})* array_end;")
                else:
                    min_items_part = ' comma '.join([new_nonterminal] * (min_items - len(prefix_items_nonterminals)-1))
                    if  min_items_part:
                        min_items_part = "comma " + min_items_part
                    prefix_items_part = ' comma '.join(prefix_items_nonterminals)
                    ebnf_rules.append(f"{nonterminal} ::= array_begin {prefix_items_part} {min_items_part} comma {new_nonterminal}+ array_end;")
            elif min_items == 0 and not prefix_items:
                for i in range(min_items, max_items + 1):
                    items = ' comma '.join([new_nonterminal] * i)
                    ebnf_rules.append(f"{nonterminal} ::= array_begin {items} array_end;")
            else:
                prefix_items_num = len(prefix_items_nonterminals)
                if prefix_items:
                    for prefix_items_part in prefix_items_parts:
                        prefix_items_part = ' comma '.join(prefix_items_part)
                        ebnf_rules.append(f"{nonterminal} ::= array_begin {prefix_items_part} array_end;")
                min_items_part = ' comma '.join([new_nonterminal] * (min_items - prefix_items_num))
                prefix_items_part = ' comma '.join(prefix_items_nonterminals)
                if min_items_part and prefix_items_part:
                    ebnf_rules.append(f"{nonterminal}_min ::= {prefix_items_part} comma {min_items_part};")
                elif min_items_part:
                    ebnf_rules.append(f"{nonterminal}_min ::= {min_items_part};")
                elif prefix_items_part:
                    ebnf_rules.append(f"{nonterminal}_min ::= {prefix_items_part};")
                common = max(min_items, prefix_items_num)
                for i in range(1, max_items + 1 - common):
                    items = ' comma '.join([new_nonterminal] * i)
                    ebnf_rules.append(f"{nonterminal} ::= array_begin {nonterminal}_min comma {items} array_end;")  
            # Handle the item type
            args = typing.get_args(current.type)
            if args:
                item_type = args[0]
            else:
                # If args is empty, default to Any
                item_type = typing.Any
            if prefix_items:
                return "\n".join(ebnf_rules) + "\n", list(zip(prefix_items, prefix_items_nonterminals)) + [(item_type, new_nonterminal)]
            return "\n".join(ebnf_rules) + "\n", [(item_type, new_nonterminal)]
        return None
    
    def is_sequence_like(current: typing.Type) -> bool:
        """
        Check if the given type is sequence-like.

        This function returns True for:
        - typing.Sequence
        - typing.List
        - typing.Tuple
        - Any subclass of collections.abc.Sequence
        - list
        - tuple

        Args:
            current: The type to check.

        Returns:
            bool: True if the type is sequence-like, False otherwise.
        """
        original = typing.get_origin(current)
        if original is None:
            original = current
        return (
            original is typing.Sequence or
            original is typing.List or
            original is typing.Tuple or
            (isinstance(original, type) and (issubclass(original, collections.abc.Sequence) or
            issubclass(original, list) or
            issubclass(original, tuple)))
        )

    def metadata(current: typing.Type, nonterminal: str):
        if isinstance(current, schemas.schema.TypeWithMetadata):
            original = typing.get_origin(current.type)
            if original is None:
                original = current.type
            if not current.metadata:
                return "", [(current.type, nonterminal)]
            if isinstance(current.type, type) and issubclass(current.type, str):
                return string_metadata(current, nonterminal)
            elif isinstance(current.type, type) and issubclass(current.type, (int, float)):
                return number_metadata(current, nonterminal)
            elif is_sequence_like(original):
                return sequence_metadata(current, nonterminal)
        return None

    def builtin_sequence(current: typing.Type, nonterminal: str):
        original = typing.get_origin(current)
        if original is None:
            original = current
        if is_sequence_like(original):
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
                assert issubclass(
                    args[0], str), f"{args[0]} is not string!"
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
            new_items = []
            result = []
            for i, arg in enumerate(args):
                if isinstance(arg, str):
                    new_items.append(f'"\\"{repr(arg)[1:-1]}\\""')
                elif isinstance(arg, bool):
                    new_items.append(f'"{str(arg).lower()}"')
                elif isinstance(arg, int):
                    new_items.append(f'"{str(arg)}"')
                elif isinstance(arg, float):
                    new_items.append(f'"{str(arg)}"')
                elif arg is None:
                    new_items.append("null")
                elif isinstance(arg, tuple):
                    for j,item in enumerate(arg):
                        new_nonterminal = f"{nonterminal}_{i}_{j}"
                        result.append((typing.Literal[item], new_nonterminal))
                    new_item = f"(array_begin {' comma '.join(map(lambda x:x[1], result))} array_end)"
                    new_items.append(new_item)
                elif isinstance(arg, frozendict):
                    for key, value in arg.items():
                        new_nonterminal = f"{nonterminal}_{i}_{key}"
                        result.append((typing.Literal[value], new_nonterminal))
                    new_item = f"object_begin {' comma '.join(map(lambda x:x[1], result))} object_end"
                    new_items.append(new_item)
                else:
                    new_nonterminal = f"{nonterminal}_{i}"
                    result.append((arg, new_nonterminal))
                    new_items.append(new_nonterminal)
            return f"{nonterminal} ::= {' | '.join(new_items)};\n", result

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
        elif isinstance(current, typing.NewType):
            current: typing.NewType
            return "", [(current.__supertype__, nonterminal)]

    register_generate_nonterminal_def(builtin_simple_types)
    register_generate_nonterminal_def(schema)
    register_generate_nonterminal_def(field_info)
    register_generate_nonterminal_def(metadata)
    register_generate_nonterminal_def(builtin_tuple)
    register_generate_nonterminal_def(builtin_literal)
    register_generate_nonterminal_def(builtin_union)
    register_generate_nonterminal_def(builtin_sequence)
    register_generate_nonterminal_def(builtin_dict)

def _generate_kbnf_grammar(schema: schemas.schema.Schema|collections.abc.Sequence, start_nonterminal: str) -> str:
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
        id(typing.Any): "json_value",
    }
    result = [GRAMMAR_HEADER]
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
        for i in _type_to_nonterminals:
            value = i(current, nonterminal)
            if value is not None:
                line, to_stack = value
                result.append(line)
                stack.extend(to_stack)
                nonterminals.add(nonterminal)
                break
        else:
            raise TypeError(
                f"{current} from {nonterminal} is not supported in json_generators!")
    return "".join(result)


class JsonExtractor(extractor.NonterminalExtractor):
    """
    An extractor that loads json data to an object from a string.
    """

    def __init__(self, nonterminal: str, capture_name: typing.Optional[str], schema: schemas.schema.Schema|collections.abc.Sequence,
                 to_object: typing.Callable[[str], schemas.schema.Schema]):
        """
        Create a json extractor from a given schema or a list of supported types.

        Currently, the following data types are supported:

        - bool
        - int
          - positive int
          - negative int
          - nonnegative int
          - nonpositive int
        - float
          - positive float
          - negative float
          - nonnegative float
          - nonpositive float
        - str
          - optionally with min_length, max_length and pattern constraints
            - length is measured in UTF-8 character number after json parsing
            - *Warning*: too large difference between min_length and max_length can lead to enormous memory consumption!
            - pattern is mutually exclusive with min_length and max_length
            - pattern will be compiled to a regular expression so all caveats of regular expressions apply
            - pattern currently is automatically anchored at both ends
            - the generated json could be invalid if the pattern allows invalid content between the json string's quotes.
              - for example, `pattern=".*"` will allow '\"' to appear in the json string which is forbidden by JSON standard.
        - NoneType
        - typing.Any
        - Subclasses of collections.abc.Mapping[str,T] and typing.Mapping[str,T] where T is a supported type,
        - Subclasses of collections.abc.Sequence[T] and typing.Sequence[T] where T is a supported type.
          - optionally with `minItems`, `maxItems`, `prefixItems` constraints
          - *Warning*: too large difference between minItems and maxItems can lead to very slow performance!
          - *Warning*: By json schema definition, prefixItems by default allows additional items and missing items in the prefixItems, which may not be the desired behavior and can lead to very slow performance if prefixItems is long!
        - tuple[T1,T2,...] where T1,T2,... are supported types. The order, type and number of elements will be preserved.
        - typing.Literal[x1,x2,...] where x1, x2, ... are instances of int, string, bool or NoneType, or another typing.Literal[y1,y2,...]
        - typing.Union[T1,T2,...] where T1,T2,... are supported types.
        - schemas.Schema where all its fields' data types are supported. Recursive schema definitions are supported as well.
          - *Warning*: while not required field is supported, they can lead to very slow performance and/or enormous memory consumption if there are too many of them!
        Args:
            nonterminal: The nonterminal representing the extractor.
            capture_name: The capture name of the extractor, or `None` if the extractor does not capture.
            to_object: A callable to convert the extracted string to a schema instance.
        """
        super().__init__(nonterminal, capture_name)
        self._to_object = to_object
        self._rule_str = _generate_kbnf_grammar(schema, self.nonterminal)
    def extract(self, input_str: str) -> typing.Optional[tuple[str, schemas.schema.Schema]]:
        """
        Extract a schema instance from a string.

        Args:
            input_str: The input string to extract from.

        Returns:
            A tuple of the remaining string and the extracted schema instance, or `None` if extraction failed.
        """

        # Ensure the input string starts with '{' or '[' after stripping leading whitespace
        input_str = input_str.lstrip()
        if not input_str.startswith(('{', '[')):
            return None

        # Variables to track the balance of brackets and the position in the string
        bracket_count = 0
        position = 0
        in_string = False
        escape_next = False
        start_char = input_str[0]
        end_char = '}' if start_char == '{' else ']'

        # Iterate over the string to find where the JSON object or array ends
        for char in input_str:
            if not in_string:
                if char == start_char:
                    bracket_count += 1
                elif char == end_char:
                    bracket_count -= 1
                elif char == '"':
                    in_string = True
            else:
                if char == '"' and not escape_next:
                    in_string = False
                elif char == '\\':
                    escape_next = not escape_next
                else:
                    escape_next = False

            # Move to the next character
            position += 1

            # If brackets are balanced and we're not in a string, stop processing
            if bracket_count == 0 and not in_string:
                break
        else:
            return None
        # The position now points to the character after the last '}', so we slice to position
        json_str = input_str[:position]
        remaining_str = input_str[position:]
        # Return the unparsed remainder of the string and the decoded JSON object
        return remaining_str, self._to_object(json_str)

    @property
    def kbnf_definition(self):
        return self._rule_str


_register_all_predefined_types()
