"""
This module contains the Formatter class and its related classes.
"""
import abc
import collections
from json import JSONDecodeError
import json
import re
import textwrap
import typing
from copy import copy
import kbnf
from formatron.formats.json import JsonExtractor
from formatron.schemas.schema import Schema
from formatron.extractor import Extractor, LiteralExtractor, NonterminalExtractor, ChoiceExtractor, SubstringExtractor
from formatron.formats.regex import RegexExtractor



class FormatterBase(abc.ABC):
    """
    An abstract Formatter that enforces a format on the string generated by a language model. 
    """

    @abc.abstractmethod
    def accept_token(self, token_id: int) -> typing.Any:
        """
        Accept a token from the language model.
        Args:
            token_id: The token ID.
        Returns:
            The result of accepting the token.
        """

    @abc.abstractmethod
    def accept_bytes(self, _bytes: bytes):
        """
        Accept a bytes object from the language model.
        Args:
            _bytes: The bytes object.
        """

    @abc.abstractmethod
    def compute_allowed_tokens(self) -> None:
        """
        Compute the allowed tokens based on the current state.
        """

    @abc.abstractmethod
    def mask_logits(self, logits) -> typing.Any:
        """
        Mask the logits based on the current state.
        Args:
            logits: The logits to mask.
        Returns:
            The masked logits.
        """

    @abc.abstractmethod
    def get_allowed_tokens_since_last_computation(self) -> typing.Sequence[int]:
        """
        Get the allowed tokens since the last computation(in other words, the last call to `compute_allowed_tokens`).
        Returns:
            The allowed tokens.
        """

    @abc.abstractmethod
    def is_completed(self) -> bool:
        """
        Check if the generated string satisfies the format and hence the generation is completed.
        """

    @abc.abstractmethod
    def _on_completion(self, generated_output: str) -> None:
        """
        Perform actions when the generation is completed.
        """

    @property
    @abc.abstractmethod
    def captures(self) -> dict[str, typing.Any|None]:
        """
        Get the captures from the generated string. 
        """

    @abc.abstractmethod
    def reset(self) -> None:
        """
        Reset the formatter to the initial state.
        """


class Formatter(FormatterBase):
    """
    A Formatter that enforces a format on the string generated by a language model. It is designed to compose
    multiple extractors in a sequential, unambiguous, greedy manner. Check out the Formatter.captures property docs for more details.
    If you need more complex extraction logic, you need to implement your own Extractor.
    """

    def __init__(self, extractors: list[Extractor], engine: kbnf.Engine,
                 decode_callback: typing.Callable[[list[int]], str], grammar_str: str):
        """
        Initialize the formatter.
        Args:
            extractors: The matchers to extract data from the generated string.
            engine: The KBNF engine to enforce the format.
            decode_callback: The callback to decode the token IDs to a string.
            grammar_str: The KBNF grammar string.
        """
        self._extractors = extractors
        self._engine = engine
        self._token_ids = []
        self._decode_callback = decode_callback
        self._grammar_str = grammar_str
        self._captures = {}

    @property
    def grammar_str(self):
        """
        Get the KBNF grammar string.
        """
        return self._grammar_str

    def accept_token(self, token_id: int):
        result = self._engine.try_accept_new_token(token_id)
        self._token_ids.append(token_id)
        if result == kbnf.AcceptTokenResult.Finished:
            output = self._decode_callback(self._token_ids)
            self._on_completion(output)
        return result

    def accept_bytes(self, _bytes: bytes):
        self._engine.try_accept_new_bytes(_bytes)

    def compute_allowed_tokens(self) -> None:
        self._engine.compute_allowed_token_ids()

    def mask_logits(self, logits) -> typing.Any:
        return self._engine.mask_logits(logits)

    def get_allowed_tokens_since_last_computation(self) -> typing.Sequence[int]:
        return self._engine.get_allowed_token_ids_from_last_computation()

    def is_completed(self) -> bool:
        """
        Check if the generation is completed. This means the generation is ended by the engine.
        If the generation is ended by integration-specific stop conditions like `max_new_tokens`,
        the generation is not considered completed by this method.
        """
        return self._engine.is_finished()

    def _on_completion(self, generated_output: str) -> None:
        for matcher in self._extractors:
            result = matcher.extract(generated_output)
            if result is None:
                captured = None
            else:
                generated_output, captured = matcher.extract(generated_output)
            if matcher.capture_name:
                if matcher.capture_name in self._captures:
                    self._captures[matcher.capture_name] = [
                        self._captures[matcher.capture_name]]
                    self._captures[matcher.capture_name].append(captured)
                else:
                    self._captures[matcher.capture_name] = captured

    @property
    def captures(self) -> dict[str, typing.Any] | None:
        """
        Get the captures from the generated string. Note that the captures are only available for one extractor if:
        - The extractor has a capture name.
        - Formatter.is_completed() returns True.
        - The extractor successfully extracts the data.
          - This means the extractor identifies the correct string span to extract and whatever post-processing the extractor does on the extracted string is successful.
        
        Captures are obtained by calling `Extractor.extract` method on the generated string in the sequence of extractors appended to the formatter.
        Note that the previous extractors does not 'see' the semantics of the later extractors. For example,
        consider the following formatter:
        ```python
        f = FormatterBuilder()
        f.append_line(f"{f.regex('.*?', capture_name='a')}{f.regex('.*', capture_name='b')}")
        f = f.build()
        ```
        The `b` extractor will always corresponding to `None` because the `a` extractor will always extract the whole string.
        This behavior is different from what a typical regular expression engine would do! 
        """
        return self._captures

    def reset(self) -> None:
        self._captures.clear()
        self._engine.reset()
        self._token_ids.clear()

    def __str__(self):
        return (f"Formatter(engine={self._engine}, "
                f"captures={self._captures}, "
                f"extractors={len(self._extractors)}, "
                f"completed={self.is_completed()}, "
                f"token_ids={len(self._token_ids)})"
                f"grammar={self._grammar_str})")


class FormatterBuilder:
    """
    A builder for creating a Formatter.
    """
    _formatter_builder_counter = 0

    def __init__(self):
        """
        Initialize the formatter builder.
        """
        self._counter = 0
        self._main_rule = []
        self._rules = []
        self._capture_names = set()
        self._nonterminal_to_extractor = {}
        self._extractors = []
        self._instance_id = self.__class__._formatter_builder_counter
        self.__class__._formatter_builder_counter += 1


    def _assert_capture_name_valid(self, capture_name: str):
        assert capture_name.isidentifier(), (f"capture_name {capture_name}"
                                             f" should only contains alphanumeric characters, "
                                             f"underscores, and does not start with digits!")
        assert capture_name not in self._capture_names, f"capture_name {capture_name} is duplicated!"

    def append_line(self, line: str) -> None:
        """
        Append a line to the format. Specifically, a newline character is appended to the input.

        Note that if you need a literal `$`, you need to escape it by adding a backslash: `\\$`.
        """
        self.append_str(line + '\n')

    def append_multiline_str(self, lines: str) -> None:
        """
        Appends a multiline string to the format, preserving the first line's leading whitespaces
        and remove any common leading whitespaces from subsequent lines.

        Note that tabs and spaces are both treated as whitespace, but they are not equal:
        the lines " hello" and "\\thello" are considered to have no common leading whitespace.

        Entirely blank lines are normalized to a newline character.

        Note that if you need a literal `$`, you need to escape it by adding a backslash: `\\$`.
        """
        first = lines.find('\n')
        self.append_str(lines[:first + 1] + textwrap.dedent(lines[first + 1:]))

    def append_str(self, string: str) -> None:
        """
        Append a string to the format without any post-processing.

        Note that if you need a literal `$`, you need to escape it by adding a backslash: `\\$`.
        """
        state = "normal"
        last = 0

        def append_literal(end):
            if last < end:
                literal = string[last:end]
                self._main_rule.append(repr(literal))
                self._extractors.append(LiteralExtractor(literal))

        for i, char in enumerate(string):
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
                    self._extractors.append(
                        self._nonterminal_to_extractor[string[last:i]])
                    last = i + 1
            elif char == "\\":
                state = "escaped"
            else:
                state = "normal"
        append_literal(len(string))

    def _create_nonterminal(self, name: str) -> str:
        nonterminal = f"__{name}_{self._counter}_{self._instance_id}"
        self._counter += 1
        return nonterminal

    def _add_capture_name(self, extractor: NonterminalExtractor) -> None:
        if extractor.capture_name is None:
            return None
        self._assert_capture_name_valid(extractor.capture_name)
        self._capture_names.add(extractor.capture_name)

    def choose(self, *extractors: Extractor | str, capture_name: str = None) -> ChoiceExtractor:
        """
        Create a choice extractor.

        Check out the ChoiceExtractor docs for more details.
        Args:
            extractors: The extractors to choose from.
            capture_name: The capture name of the extractor, or `None` if the extractor does not capture.
        Returns:
            The choice extractor.
        """
        new_extractors = []
        for extractor in extractors:
            if isinstance(extractor, str):
                new_extractors.append(LiteralExtractor(extractor))
            else:
                new_extractors.append(extractor)
        return self._add_extractor("choice",
                                   lambda nonterminal: ChoiceExtractor(new_extractors, capture_name, nonterminal))

    def _add_extractor(self, extractor_type: str, create_extractor: typing.Callable[[str], Extractor]):
        nonterminal = self._create_nonterminal(extractor_type)
        extractor = create_extractor(nonterminal)
        if isinstance(extractor, NonterminalExtractor):
            self._add_capture_name(extractor)
            nonterminal = extractor.nonterminal
        self._nonterminal_to_extractor[nonterminal] = extractor
        self._rules.append(extractor.kbnf_definition)
        return extractor

    def extractor(self, create_extractor: typing.Callable[[str], Extractor]) -> Extractor:
        """
        Create a custom extractor.

        Args:
            create_extractor: callable with signature (extractor_nonterminal: str)->Extractor that create the extractor. extractor_nonterminal is the auto-generated nonterminal reference for the extractor.
            capture_name: The capture name of the extractor, or `None` if the extractor does not capture.
        """
        return self._add_extractor("extractor", create_extractor)

    def json(self, schema: typing.Type[Schema]|collections.abc.Sequence, *, capture_name: str = None) -> JsonExtractor:
        """
        Create a JSON extractor. Check out the JsonExtractor docs for more details.

        Args:
            schema: The schema for extraction.
            capture_name: The capture name of the extractor, or `None` if the extractor does not capture.
        Returns:
            The JSON extractor.
        """
        def to_json(_json: str):
            if isinstance(schema, type) and issubclass(schema, Schema):
                try:
                    return schema.from_json(_json)
                except JSONDecodeError:  # make ChoiceExtractor work appropriately
                    return None
            else:
                try:
                    return json.loads(_json)
                except JSONDecodeError:
                    return None
        return self._add_extractor("json",
                                   lambda nonterminal: JsonExtractor(nonterminal, capture_name,schema, to_json))

    def regex(self, regex: str, *, capture_name: str = None) -> RegexExtractor:
        """
        Create a regex extractor.

        Check out the RegexExtractor docs for more details.

        Args:
            regex: The regular expression for extraction.
            capture_name: The capture name of the extractor, or `None` if the extractor does not capture.
        Returns:
            The regex extractor.
        """
        return self._add_extractor("regex",
                                   lambda nonterminal: RegexExtractor(regex, capture_name, nonterminal))

    def str(self, *, stop: typing.Union[str, list[str]] = None,
            capture_name: typing.Optional[str] = None) -> Extractor:
        """
        Create a string extractor.

        The extractor will extract all text until(inclusive) one of the stop strings is encountered. 

        Args:
            stop: The strings for the extractors to stop at. They will be included in text generation and extraction.
            capture_name: The capture name of the extractor, or `None` if the extractor does not capture.
        Returns:
            The string extractor.
        """
        stop = [stop] if isinstance(stop, str) else stop or []
        if not stop:
            capture_regex = ".*"
        else:
            backslash = '\\'
            capture_regex = f".*?(?:{'|'.join([i.replace(backslash, backslash * 2) for i in map(re.escape, stop)])})"
        return self._add_extractor("str",
                                   lambda nonterminal: RegexExtractor(capture_regex, capture_name, nonterminal))
    
    def substr(self, string: str, *, capture_name: str = None, extract_empty_substring: bool = False) -> Extractor:
        """
        Create a substring extractor.

        The extractor will extract a substring of the input string.

        Args:
            string: The string to extract.
            capture_name: The capture name of the extractor, or `None` if the extractor does not capture.
            extract_empty_substring: Whether to extract an empty substring as a valid substring.
        Returns:
            The substring extractor.
        """
        return self._add_extractor("substr",
                                   lambda nonterminal: SubstringExtractor(string, capture_name, nonterminal,
                                                                           extract_empty_substring=extract_empty_substring))

    def build(self, vocabulary: kbnf.Vocabulary,
              decode: typing.Callable[[list[int]], str],
              engine_config: kbnf.Config = None) -> Formatter:
        """
        Build a formatter from the builder. The builder will not be consumed and can be used again.

        Args:
            vocabulary: The KBNF engine vocabulary for the formatter.
            decode: The callback to decode the token IDs to a string.
            engine_config: The KBNF engine configuration.
        Returns:
            The formatter.
        """
        assert len(
            self._main_rule) != 0, "An empty formatter builder cannot build!"
        rules = copy(self._rules)
        rules.append(f"start ::= {' '.join(self._main_rule)};")
        grammar_str = "\n".join(rules)
        engine = kbnf.Engine(grammar_str, vocabulary, engine_config)
        extractors = copy(self._extractors)
        f = Formatter(extractors, engine, decode, grammar_str)
        return f
