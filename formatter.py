import abc
import textwrap
import typing

import kbnf
from kbnf import AcceptTokenResult, Engine

import grammar_generators.grammar_generator
import schemas.schema
from matcher import Matcher, LiteralMatcher, RegexMatcher, ChoiceMatcher


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

    @property
    @abc.abstractmethod
    def captures(self) -> dict[str, typing.Any]:
        pass

    @abc.abstractmethod
    def reset(self) -> None:
        pass


class Formatter(FormatterBase):

    def __init__(self, matchers: list[Matcher], engine: kbnf.Engine,
                 decode_callback: typing.Callable[[list[int]], str], grammar_str: str):
        self._matchers = matchers
        self._engine = engine
        self._token_ids = []
        self._decode_callback = decode_callback
        self._grammar_str = grammar_str
        self._captures = {}

    @property
    def grammar_str(self):
        return self._grammar_str

    def accept_token(self, token_id: int):
        result = self._engine.try_accept_new_token(token_id)
        self._token_ids.append(token_id)
        if result == AcceptTokenResult.Finished:
            output = self._decode_callback(self._token_ids)
            self.on_completion(output)
        return result

    def compute_allowed_tokens(self) -> None:
        self._engine.compute_allowed_token_ids()

    def mask_logits(self, logits) -> typing.Any:
        return self._engine.mask_logits(logits)

    def is_completed(self) -> bool:
        return self._engine.is_finished()

    def on_completion(self, generated_output: str) -> None:
        print(self._matchers)
        print(self._token_ids)

        for matcher in self._matchers:
            generated_output, captured = matcher.match(generated_output)
            if matcher.capture_name:
                self._captures[matcher.capture_name] = captured

    @property
    def captures(self) -> dict[str, typing.Any] | None:
        return self._captures

    def reset(self) -> None:
        self._captures.clear()
        self._engine.reset()
        self._token_ids.clear()


class FormatterBuilder:
    _formatter_builder_counter = 0

    def __init__(self):
        self._counter = 0
        self._main_rule = []
        self._rules = []
        self._capture_names = set()
        self._nonterminal_to_matcher = {}
        self._matchers = []
        self.instance_id = self._formatter_builder_counter
        self.__class__._formatter_builder_counter += 1

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

        def append_literal(end):
            if last < end:
                literal = string[last:end]
                self._main_rule.append(repr(literal))
                self._matchers.append(LiteralMatcher(literal))

        for (i, char) in enumerate(string):
            if char == "$":
                if state != "escaped":
                    state = "dollar"
                else:
                    state = "normal"
            elif state == "dollar":
                if char == "{":
                    append_literal(i - 1)
                    last = i + 1
                    state = "left_bracket"
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
        append_literal(len(string))

    def _create_nonterminal(self, capture_name: typing.Optional[str], name: str) -> str:
        if capture_name is not None:
            self._assert_capture_name_valid(capture_name)
            self._capture_names.add(capture_name)
            nonterminal = f"__{name}_{capture_name}_{self.instance_id}"
        else:
            nonterminal = f"__{name}_{self._counter}_{self.instance_id}"
            self._counter += 1
        return nonterminal

    def choose(self, *matchers: Matcher | str, capture_name: str = None):
        new_matchers = []
        for matcher in matchers:
            if isinstance(matcher, str):
                new_matchers.append(LiteralMatcher(matcher))
            else:
                new_matchers.append(matcher)
        return self._add_matcher(capture_name, "choice",
                                 lambda nonterminal: ChoiceMatcher(new_matchers, capture_name, nonterminal),
                                 lambda nonterminal:
                                 f"{nonterminal} ::= {' | '.join([i.kbnf_representation for i in new_matchers])};")

    def _add_matcher(self, capture_name: str, matcher_type: str, create_matcher: typing.Callable[[str], Matcher],
                     create_rule: typing.Callable[[str], str]):
        nonterminal = self._create_nonterminal(capture_name, matcher_type)
        self._nonterminal_to_matcher[nonterminal] = create_matcher(nonterminal)
        self._rules.append(create_rule(nonterminal))
        return self._nonterminal_to_matcher[nonterminal]

    def regex(self, regex: str, *, capture_name: str = None) -> str:
        return self._add_matcher(capture_name, "regex",
                                 lambda nonterminal: RegexMatcher(regex, capture_name, nonterminal),
                                 lambda nonterminal: f"{nonterminal} ::= #{repr(regex)};")

    def schema(self, schema: typing.Type[schemas.schema.Schema],
               grammar_generator: grammar_generators.grammar_generator.GrammarGenerator, *, capture_name: str = None):
        return self._add_matcher(capture_name, "schema",
                                 lambda nonterminal: grammar_generator.get_matcher(nonterminal, capture_name),
                                 lambda nonterminal: grammar_generator.generate(schema, nonterminal))

    def str(self, *, stop: typing.Union[str, list[str]] = None,
            not_contain: typing.Union[str, list[str], None] = None,
            capture_name: typing.Optional[str] = None):
        stop = [stop] if isinstance(stop, str) else stop or []
        not_contain = [not_contain] if isinstance(not_contain, str) else not_contain or []
        if not stop and not not_contain:
            capture_regex = ".*"
            get_excepted = None
            get_nonterminal_regex = lambda _: "#'.*'"
        else:
            capture_regex = f".*?(?:{'|'.join(map(repr, stop + not_contain))})"
            get_excepted = lambda nonterminal: f"{nonterminal}_excepted"
            end = f"({'|'.join(map(repr, stop))})" if stop else ""
            get_nonterminal_regex = lambda nonterminal: f"except!({get_excepted(nonterminal)}){end}"
        nonterminal = self._create_nonterminal(capture_name, "str")
        if get_excepted:
            self._rules.append(f"{get_excepted(nonterminal)} ::= {' | '.join(map(repr, stop + not_contain))};")
        self._rules.append(f"{nonterminal} ::= {get_nonterminal_regex(nonterminal)};")
        self._nonterminal_to_matcher[nonterminal] = RegexMatcher(capture_regex, capture_name, nonterminal)
        return self._nonterminal_to_matcher[nonterminal]

    def build(self, vocabulary: kbnf.Vocabulary, decode_callback: typing.Callable[[list[int]], str]):
        self._rules.append(f"start ::= {' '.join(self._main_rule)};")
        grammar_str = "\n".join(self._rules)
        engine = Engine(grammar_str, vocabulary)
        f = Formatter(self._matchers, engine, decode_callback, grammar_str)
        return f
