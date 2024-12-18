"""
This module contains the RegexExtractor class, which is used to extract data using a regular expression.
"""
import re
import typing
from formatron.extractor import NonterminalExtractor


class RegexExtractor(NonterminalExtractor):
    """
    An extractor that extracts a string using a regular expression.
    """

    def __init__(self, regex: str, capture_name: str, nonterminal: str):
        """
        Initialize the regex extractor.

        Args:
            regex: The regular expression for extraction.
            capture_name: The name of the capture, or `None` if the extractor does not capture.
            nonterminal: The nonterminal representing the extractor.
        """
        super().__init__(nonterminal, capture_name)
        self._regex = re.compile(regex)

    def extract(self, input_str: str) -> typing.Optional[tuple[str, re.Match | None]]:
        """
        Extract the string using the regular expression.
        Specifically, the first match(if any) of the regex pattern in the input string is returned. 

        Args:
            input_str: The input string.
        Returns:
            The remaining string and the extracted `re.Match` object, or `None` if the extraction failed.
        """
        matched = self._regex.match(input_str)
        if not matched:
            return None
        return input_str[matched.span()[1]:], matched

    @property
    def kbnf_definition(self) -> str:
        return f"{self.nonterminal} ::= #{repr(self._regex.pattern)};"
    

class RegexComplementExtractor(NonterminalExtractor):
    """
    An extractor that extracts data by matching a regex complement.
    """

    def __init__(self, regex: str, capture_name: str, nonterminal: str):
        """
        Initialize the regex complement extractor.
        """
        super().__init__(nonterminal, capture_name)
        self._regex = re.compile(regex)

    def extract(self, input_str: str) -> typing.Optional[tuple[str, str]]:
        """
        Extract the data by matching a regex complement.

        Specifically, the string until the first character in the first match of the regex is extracted if there is a match,
        or the entire string is extracted if there is no match.
        """
        matched = self._regex.search(input_str)
        if not matched:
            return "", input_str
        return input_str[matched.span()[0]:], input_str[:matched.span()[0]]

    @property
    def kbnf_definition(self) -> str:
        return f"{self.nonterminal} ::= #ex{repr(self._regex.pattern)};"