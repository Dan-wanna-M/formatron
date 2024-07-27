import abc
import typing

import matcher
import schemas


class GrammarGenerator(abc.ABC):
    @abc.abstractmethod
    def generate(self, schema: typing.Type, start_nonterminal: str) -> str:
        pass

    @abc.abstractmethod
    def get_matcher(self, nonterminal: str, capture_name: typing.Optional[str],
                    to_object: typing.Callable[[str, ], schemas.schema.Schema]) -> matcher.Matcher:
        pass
