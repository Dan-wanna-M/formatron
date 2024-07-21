import abc
import typing

import matcher
import schemas.schema


class GrammarGenerator(abc.ABC):
    @abc.abstractmethod
    def generate(self, schema: typing.Type, start_nonterminal: str) -> str:
        pass

    @abc.abstractmethod
    def get_matcher(self, nonterminal:str, capture_name: typing.Optional[str]) -> matcher.Matcher:
        pass
