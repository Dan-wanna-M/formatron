"""
This module defines the GrammarGenerator abstract base class.
"""
import abc
import typing

import extractor
import schemas


class GrammarGenerator(abc.ABC):
    """
    An abstract KBNF grammar generator that enables converting from a schema to a KBNF grammar
    and converting from a string adhering to the grammar back to a schema instance.
    """
    @abc.abstractmethod
    def generate(self, schema: typing.Type[schemas.schema.Schema], start_nonterminal: str) -> str:
        """
        Generate a KBNF grammar string from a schema.

        Args:
            schema: The schema to generate a grammar for.
            start_nonterminal: The start nonterminal of the grammar.

        Returns:
            The KBNF grammar string.
        """

    @abc.abstractmethod
    def get_extractor(self, nonterminal: str, capture_name: typing.Optional[str],
                      to_object: typing.Callable[[str, ], schemas.schema.Schema]) -> extractor.Extractor:
        """
        Get an extractor for this grammar generator.

        Args:
            nonterminal: The nonterminal representing the extractor.
            capture_name: The capture name of the extractor, or `None` if the extractor does not capture.
            to_object: A callable to convert the extracted string to a schema instance.

        Returns:
            The extractor.
        """
