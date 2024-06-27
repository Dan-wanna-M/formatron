import abc
import re
import textwrap
import typing

import grammar_generators.grammar_generator
import schemas.schema


class Matcher(abc.ABC):
    def __init__(self, capture_name: typing.Optional[str] = None):
        self.capture_name = capture_name

    @abc.abstractmethod
    def match(self, input_str: str) -> tuple[str, typing.Any]:
        pass


class LiteralMatcher(Matcher):

    def __init__(self, literal: str):
        super().__init__()
        self.literal = literal

    def match(self, input_str: str) -> tuple[str, typing.Any]:
        pos = input_str.find(self.literal)
        assert pos != -1
        return input_str[pos + len(self.literal):], self.literal


class RegexMatcher(Matcher):

    def __init__(self, regex: str, capture_name: str):
        super().__init__(capture_name)
        self.regex = re.compile(regex)

    def match(self, input_str: str) -> tuple[str, typing.Any]:
        matched = self.regex.match(input_str)
        return input_str[matched.lastindex + 1:], matched.groups()


class FormatterBase(abc.ABC):
    @abc.abstractmethod
    def accept_token(self, token_id: int):
        pass

    @abc.abstractmethod
    def compute_allowed_tokens(self) -> None:
        pass

    @abc.abstractmethod
    def mask_logits(self, logits) -> typing.Any:
        pass

    @abc.abstractmethod
    def is_completed(self) -> bool:
        pass

    @abc.abstractmethod
    def on_completion(self) -> None:
        pass

    @abc.abstractmethod
    def captures_iter(self) -> dict[str, typing.Any]:
        pass


class Formatter(FormatterBase):
    def __init__(self):
        self.counter = 0
        self.rules = []
        self.strings = []
        self.capture_names = set()
        self.matchers = []
        self.engine = None

    def _assert_capture_name_valid(self, capture_name: str):
        assert capture_name.isidentifier(), f"capture_name {capture_name} should only contains alphanumeric characters, " \
                                            f"underscores, and does not start with digits!"
        assert capture_name not in self.capture_names, f"capture_name {capture_name} is duplicated!"

    def append_line(self, line: str):
        self.append_str(line + '\n')

    def append_multiline_str(self, lines: str):
        first = lines.find('\n')
        self.append_str(lines[:first + 1] + textwrap.dedent(lines[first + 1:]))

    def append_str(self, string: str):
        escaped = False
        dollar = False
        left_bracket = False
        last = 0
        for (i, char) in enumerate(string):
            if char == "$":
                if not escaped:
                    dollar = True
                escaped = False
            elif dollar:
                if char == "{":
                    left_bracket = True
                    self.strings.append(repr(string[last:i - 1]))
                    self.matchers.append(LiteralMatcher(string[last:i - 1]))
                    last = i + 1
                dollar = False
            elif left_bracket and char == "}":
                left_bracket = False
                self.strings.append(string[last:i])
                self.matchers.append(LiteralMatcher(string[last:i]))
                last = i + 1
            elif char == "\\":
                escaped = True
            else:
                escaped = False
        if last < len(string):
            self.strings.append(repr(string[last:]))
            self.matchers.append(LiteralMatcher(string[last:]))

    def regex(self, regex: str, *, capture_name: str = None) -> str:
        if capture_name is not None:
            self._assert_capture_name_valid(capture_name)
            nonterminal = f"__regex_{capture_name}_{id(regex)}"
        else:
            nonterminal = f"__regex_{id(regex)}_{self.counter}"
            self.counter += 1
        self.matchers.append(RegexMatcher(regex, capture_name))
        self.rules.append(f"{nonterminal} ::= #{repr(regex)};")
        self.capture_names.add(nonterminal)
        return f"${{{nonterminal}}}"

    def schema(self, schema: schemas.schema.Schema,
               grammar_generator: grammar_generators.grammar_generator.GrammarGenerator, *, capture_name: str = None):
        if capture_name is not None:
            self._assert_capture_name_valid(capture_name)
            nonterminal = f"__schema_{capture_name}_{id(schema)}"
        else:
            nonterminal = f"__schema_{id(schema)}_{self.counter}"
            self.counter += 1
        self.rules.append(grammar_generator.generate(schema, nonterminal))
        self.matchers.append(grammar_generator)
        self.capture_names.add(nonterminal)
        # Repetitive header might slow down compilation time, but let's ignore it for now.
        return f"${{{nonterminal}}}"

    def str(self, *,
            stop: typing.Union[str, list[str]] = None, not_contain: typing.Union[str, list[str], None] = None,
            capture_name: str = None):
        if stop is None:
            stop = []
        if not_contain is None:
            not_contain = []
        if not stop and not not_contain:
            capture_regex = ".*"
            get_nonterminal_regex = lambda _: "#'.*'"
        else:
            capture_regex = f".*?(?:{'|'.join([repr(i) for i in stop + not_contain])})"
            get_excepted = lambda nonterminal: f"{nonterminal}_excepted"
            if stop:
                end = f"({' | '.join(repr(stop))})"
            else:
                end = ""
            get_nonterminal_regex = lambda nonterminal: f"except!({get_excepted(nonterminal)}){end}"
        if capture_name is not None:
            self._assert_capture_name_valid(capture_name)
            nonterminal = f"__str_{capture_name}_{id(capture_name)}"
        else:
            nonterminal = f"__str_{id(self)}_{self.counter}"
            self.counter += 1
        self.rules.append(f"{nonterminal} ::= f{get_nonterminal_regex(nonterminal)};")
        self.matchers.append(RegexMatcher(capture_regex,capture_name))
        return f"${{{nonterminal}}}"

    def build(self):
        self.rules.append(f"start ::= {' '.join(self.strings)};")
