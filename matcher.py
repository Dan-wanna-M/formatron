import abc
import re
import typing


class Matcher(abc.ABC):
    def __init__(self, capture_name: typing.Optional[str] = None):
        self.capture_name = capture_name

    @abc.abstractmethod
    def match(self, input_str: str) -> typing.Optional[tuple[str, typing.Any]]:
        pass

    @property
    @abc.abstractmethod
    def kbnf_representation(self) -> str:
        pass

    def __str__(self):
        return f"${{{self.kbnf_representation}}}"


class LiteralMatcher(Matcher):

    def __init__(self, literal: str):
        super().__init__(None)
        self.literal = literal

    def match(self, input_str: str) -> typing.Optional[tuple[str, typing.Any]]:
        pos = input_str.find(self.literal)
        if pos == -1:
            return None
        return input_str[pos + len(self.literal):], self.literal

    @property
    def kbnf_representation(self) -> str:
        return repr(self.literal)


class RegexMatcher(Matcher):

    def __init__(self, regex: str, capture_name: str, nonterminal: str):
        super().__init__(capture_name)
        self.regex = re.compile(regex)
        self._nonterminal = nonterminal

    def match(self, input_str: str) -> typing.Optional[tuple[str, typing.Any]]:
        matched = self.regex.match(input_str)
        if not matched:
            return None
        return input_str[matched.span()[1]:], matched

    @property
    def kbnf_representation(self) -> str:
        return self._nonterminal


class ChoiceMatcher(Matcher):
    def __init__(self, choices: typing.Iterable[Matcher], capture_name: str, nonterminal: str):
        super().__init__(capture_name)
        self.choices = choices
        self._nonterminal = nonterminal

    def match(self, input_str: str) -> typing.Optional[tuple[str, typing.Any]]:
        for choice in self.choices:
            matched = choice.match(input_str)
            if matched:
                return matched
        return None

    @property
    def kbnf_representation(self) -> str:
        return self._nonterminal
