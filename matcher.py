import abc
import re
import typing


class Matcher(abc.ABC):
    def __init__(self, capture_name: typing.Optional[str] = None):
        self.capture_name = capture_name

    @abc.abstractmethod
    def match(self, input_str: str) -> tuple[str, typing.Any]:
        pass

    @abc.abstractmethod
    def _to_str(self) -> str:
        pass

    def __str__(self):
        return f"${{{self._to_str()}}}"


class LiteralMatcher(Matcher):

    def __init__(self, literal: str):
        super().__init__(literal)
        self.literal = literal

    def match(self, input_str: str) -> tuple[str, typing.Any]:
        pos = input_str.find(self.literal)
        assert pos != -1
        return input_str[pos + len(self.literal):], self.literal

    def _to_str(self) -> str:
        return self.literal


class RegexMatcher(Matcher):

    def __init__(self, regex: str, capture_name: str, nonterminal: str):
        super().__init__(capture_name)
        self.regex = re.compile(regex)
        self.nonterminal = nonterminal

    def match(self, input_str: str) -> tuple[str, typing.Any]:
        matched = self.regex.match(input_str)
        return input_str[matched.lastindex + 1:], matched.groups()

    def _to_str(self) -> str:
        return self.nonterminal
