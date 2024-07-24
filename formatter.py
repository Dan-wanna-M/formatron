import abc
import textwrap
import typing

import kbnf
from kbnf import AcceptTokenResult, Engine

import grammar_generators.grammar_generator
import schemas.schema
from matcher import Matcher, LiteralMatcher, RegexMatcher


class FormatterBase(abc.ABC):
    @abc.abstractmethod
    def accept_token(self, token_id: int) -> typing.Any:
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
    def on_completion(self, generated_output: str) -> None:
        pass

    @abc.abstractmethod
    def captures_iter(self) -> dict[str, typing.Any]:
        pass


class Formatter(FormatterBase):
    def __init__(self, matchers: list[Matcher], engine: kbnf.Engine,
                 decode_callback: typing.Callable[[list[int]], str], grammar_str: str):
        self._matchers = matchers
        self._engine = engine
        self._token_ids = []
        self._decode_callback = decode_callback
        self._grammar_str = grammar_str

    @property
    def grammar_str(self):
        return self._grammar_str

    def accept_token(self, token_id: int):
        result = self._engine.try_accept_new_token(token_id)
        self._token_ids.append(token_id)
        if result == AcceptTokenResult.Finished:
            output = self._decode_callback(self._token_ids)
            self.on_completion(output)

    def compute_allowed_tokens(self) -> None:
        self._engine.compute_allowed_token_ids()

    def mask_logits(self, logits) -> typing.Any:
        return self._engine.mask_logits(logits)

    def is_completed(self) -> bool:
        return self._engine.is_finished()

    def on_completion(self, generated_output: str) -> None:
        pass  # TODO

    def captures_iter(self) -> dict[str, typing.Any]:
        pass


class FormatterBuilder:
    def __init__(self):
        self._counter = 0
        self._main_rule = []
        self._rules = []
        self._capture_names = set()
        self._nonterminal_to_matcher = {}
        self._matchers = []

    def _assert_capture_name_valid(self, capture_name: str):
        assert capture_name.isidentifier(), f"capture_name {capture_name} should only contains alphanumeric characters, " \
                                            f"underscores, and does not start with digits!"
        assert capture_name not in self._capture_names, f"capture_name {capture_name} is duplicated!"

    def append_line(self, line: str):
        self.append_str(line + '\n')

    def append_multiline_str(self, lines: str):
        first = lines.find('\n')
        self.append_str(lines[:first + 1] + textwrap.dedent(lines[first + 1:]))

    def append_str(self, string: str):
        state = "normal"
        last = 0
        for (i, char) in enumerate(string):
            if char == "$":
                if state != "escaped":
                    state = "dollar"
                else:
                    state = "normal"
            elif state == "dollar":
                if char == "{":
                    state = "left_bracket"
                    self._main_rule.append(repr(string[last:i - 1]))
                    self._matchers.append(LiteralMatcher(string[last:i - 1]))
                    last = i + 1
                else:
                    state = "normal"
            elif state == "left_bracket":
                if char == "}":
                    state = "normal"
                    self._main_rule.append(string[last:i])
                    self._matchers.append(self._nonterminal_to_matcher[string[last:i]])
                    last = i + 1
            elif char == "\\":
                state = "escaped"
            else:
                state = "normal"
        if last < len(string):
            self._main_rule.append(repr(string[last:]))
            self._matchers.append(LiteralMatcher(string[last:]))

    def regex(self, regex: str, *, capture_name: str = None) -> str:
        if capture_name is not None:
            self._assert_capture_name_valid(capture_name)
            self._capture_names.add(capture_name)
            nonterminal = f"__regex_{capture_name}_{id(regex)}"
        else:
            nonterminal = f"__regex_{id(regex)}_{self._counter}"
            self._counter += 1
        self._nonterminal_to_matcher[nonterminal] = RegexMatcher(regex, capture_name, nonterminal)
        self._rules.append(f"{nonterminal} ::= #{repr(regex)};")
        return self._nonterminal_to_matcher[nonterminal]

    def schema(self, schema: typing.Type[schemas.schema.Schema],
               grammar_generator: grammar_generators.grammar_generator.GrammarGenerator, *, capture_name: str = None):
        if capture_name is not None:
            self._assert_capture_name_valid(capture_name)
            self._capture_names.add(capture_name)
            nonterminal = f"__schema_{capture_name}_{id(schema)}"
        else:
            nonterminal = f"__schema_{id(schema)}_{self._counter}"
            self._counter += 1
        self._rules.append(grammar_generator.generate(schema, nonterminal))
        self._nonterminal_to_matcher[nonterminal] = grammar_generator.get_matcher(nonterminal, capture_name)
        # Repetitive header might slow down compilation time, but let's ignore it for now.
        return self._nonterminal_to_matcher[nonterminal]

    def str(self, *,
            stop: typing.Union[str, list[str]] = None, not_contain: typing.Union[str, list[str], None] = None,
            capture_name: str = None):
        if stop is None:
            stop = []
        elif isinstance(stop, str):
            stop = [stop]
        if not_contain is None:
            not_contain = []
        elif isinstance(not_contain, str):
            not_contain = [not_contain]
        if not stop and not not_contain:
            capture_regex = ".*"
            get_excepted = None
            get_nonterminal_regex = lambda _: "#'.*'"
        else:
            capture_regex = f".*?(?:{'|'.join([repr(i) for i in stop + not_contain])})"
            get_excepted = lambda nonterminal: f"{nonterminal}_excepted"
            if stop:
                end = f"({' | '.join(repr(i) for i in stop)})"
            else:
                end = ""
            get_nonterminal_regex = lambda nonterminal: f"except!({get_excepted(nonterminal)}){end}"
        if capture_name is not None:
            self._assert_capture_name_valid(capture_name)
            self._capture_names.add(capture_name)
            nonterminal = f"__str_{capture_name}_{id(capture_name)}"
        else:
            nonterminal = f"__str_{id(self)}_{self._counter}"
            self._counter += 1
        if get_excepted is not None:
            self._rules.append(f"{get_excepted(nonterminal)} ::= {' | '.join(repr(i) for i in stop+not_contain)};")
        self._rules.append(f"{nonterminal} ::= {get_nonterminal_regex(nonterminal)};")
        self._nonterminal_to_matcher[nonterminal] = RegexMatcher(capture_regex, capture_name, nonterminal)
        return self._nonterminal_to_matcher[nonterminal]

    def build(self, vocabulary: kbnf.Vocabulary, decode_callback: typing.Callable[[list[int]], str]):
        self._rules.append(f"start ::= {' '.join(self._main_rule)};")
        grammar_str = "\n".join(self._rules)
        print(grammar_str)
        engine = Engine(grammar_str, vocabulary)
        f = Formatter(self._matchers, engine, decode_callback, grammar_str)
        return f
