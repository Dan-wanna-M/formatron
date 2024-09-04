"""
Extractors for extracting data from generated strings.
"""
import abc
import typing

from general_sam import GeneralSam
__all__ = ["Extractor", "ChoiceExtractor", "NonterminalExtractor"]

class Extractor(abc.ABC):
    """
    An abstract extractor that extracts data from a string and offers its KBNF rules definition.
    """

    def __init__(self, capture_name: typing.Optional[str] = None):
        """
        Initialize an extractor.
        Args:
            capture_name: The name of the capture, or `None` if the extractor does not capture.
        """
        self._capture_name = capture_name

    @property
    def capture_name(self) -> typing.Optional[str]:
        """
        Get the name of the capture, or `None` if the extractor does not capture.
        """
        return self._capture_name

    @abc.abstractmethod
    def extract(self, input_str: str) -> typing.Optional[tuple[str, typing.Any]]:
        """
        Extract data from the input string, or `None` if the extraction failed.
        Args:
            input_str: The input string.
        Returns:
            The remaining string and the extracted data, or `None` if the extraction failed.
        """

    @property
    @abc.abstractmethod
    def kbnf_reference(self) -> str:
        """
        Get the KBNF reference of the extractor in the generated grammar of a Formatter.
        Check Formatter.kbnf_definition for the difference between kbnf_reference and kbnf_definition.
        """

    def __str__(self):
        return f"${{{self.kbnf_reference}}}"

    @property
    @abc.abstractmethod
    def kbnf_definition(self) -> str:
        """
        Get the KBNF definition of the extractor in the generated grammar of a Formatter.

        The difference between kbnf_reference and kbnf_definition is that kbnf_reference is how the extractor is referenced in other rules,
        while kbnf_definition is the definition of the extractor itself, similar to a C header file. If kbnf_reference does not need extra definition,
        you can just return an empty string.
        """


class NonterminalExtractor(Extractor):
    """
    An extractor that extracts data corresponding to a nonterminal.
    """

    def __init__(self, nonterminal: str, capture_name: typing.Optional[str] = None):
        """
        Initialize the nonterminal extractor.
        """
        super().__init__(capture_name)
        if capture_name is None:
            self._nonterminal = nonterminal
        else:
            self._nonterminal = f"{nonterminal}_{capture_name}"

    @property
    def nonterminal(self) -> str:
        """
        Get the nonterminal of the extractor.
        """
        return self._nonterminal

    @property
    def kbnf_reference(self) -> str:
        return self._nonterminal


class LiteralExtractor(Extractor):
    """
    An extractor that extracts a literal string.
    """

    def __init__(self, literal: str):
        """
        Initialize the literal extractor. It never captures since capturing a literal is redundant.

        Args:
            literal: The literal string to extract.
        """
        super().__init__(None)
        self._literal = literal

    def extract(self, input_str: str) -> typing.Optional[tuple[str, str]]:
        """
        Extract the literal from the input string, or `None` if the literal is not found.
        """
        pos = input_str.find(self._literal)
        if pos == -1:
            return None
        return input_str[pos + len(self._literal):], self._literal

    @property
    def kbnf_reference(self) -> str:
        return repr(self._literal)

    @property
    def kbnf_definition(self) -> str:
        return ""


class ChoiceExtractor(NonterminalExtractor):
    """
    An extractor that uses multiple extractors to extract data. It stops at the first succeeding extractor.
    """

    def __init__(self, choices: typing.Iterable[Extractor], capture_name: str, nonterminal: str):
        """
        Initialize the choice extractor.

        Args:
            choices: The extractors to choose from. The order determines the extractors' priority.
            capture_name: The name of the capture, or `None` if the extractor does not capture.
            nonterminal: The nonterminal representing the extractor.
        """
        super().__init__(nonterminal, capture_name)
        self._choices = choices

    def extract(self, input_str: str) -> typing.Optional[tuple[str, typing.Any]]:
        """
        Extract data from the input string using the first succeeding extractor.

        Args:
            input_str: The input string.
        Returns:
            The remaining string and the extracted data, or `None` if all extractors failed.
        """
        for choice in self._choices:
            matched = choice.extract(input_str)
            if matched:
                return matched
        return None

    @property
    def kbnf_definition(self) -> str:
        return f"{self.nonterminal} ::= {' | '.join([i.kbnf_reference for i in self._choices])};"
    

class SubstringExtractor(NonterminalExtractor):
    """
    An extractor that extracts a substring of a given string from the input string.
    """

    def __init__(self, string: str, capture_name: str, nonterminal: str, *, extract_empty_substring: bool = False):
        """
        Initialize the substring extractor.
        Args:
            string: The string to extract.
            capture_name: The name of the capture, or `None` if the extractor does not capture.
            extract_empty_substring: Whether to extract empty substring as a valid substring.
        """
        super().__init__(nonterminal, capture_name)
        self._suffix_automaton = GeneralSam.from_bytes(string.encode("UTF-8"))
        self._string = string
        self.extract_empty_substring = extract_empty_substring

    def extract(self, input_str: str) -> typing.Optional[tuple[str, str]]:
        """
        Extract the longest substring of a given string from the input string. 
        If extract_empty_substring is True, empty string is always a valid substring, so the returned string could be empty and `None` will never be returned.
        Otherwise, empty string is not a valid substring,
        so the returned string could not be empty and `None` will be returned if the input string does not contain the given string.
        """
        current_state = self._suffix_automaton.get_root_state()
        longest_match = 0
        for char in input_str:
            current_state.feed_bytes(char.encode('utf-8'))
            if current_state.is_nil():
                break
            longest_match += 1
        
        if longest_match > 0 or self.extract_empty_substring:
            extracted = input_str[:longest_match]
            remaining = input_str[longest_match:]
            return remaining, extracted
        return None
    
    @property
    def kbnf_definition(self) -> str:
        return f"{self.nonterminal} ::= #substrs{repr(self._string)};"