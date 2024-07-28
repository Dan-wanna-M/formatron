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
        :param schema: The schema to generate a grammar for.
        :param start_nonterminal: The start nonterminal of the grammar.
        :return: The generated KBNF grammar string.
        """
        pass

    @abc.abstractmethod
    def get_extractor(self, nonterminal: str, capture_name: typing.Optional[str],
                      to_object: typing.Callable[[str, ], schemas.schema.Schema]) -> extractor.Extractor:
        """
        Get an extractor for this grammar generator.
        :param nonterminal: The nonterminal representing the extractor.
        :param capture_name: The capture name of the extractor, or `None` if the extractor does not capture.
        :param to_object: A callable to convert the extracted string to a schema instance.
        :return: The extractor.
        """
        pass
