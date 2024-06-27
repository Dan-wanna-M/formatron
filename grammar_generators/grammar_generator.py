import abc

import formatter
import schemas.schema


class GrammarGenerator(formatter.Matcher, abc.ABC):
    @abc.abstractmethod
    def generate(self, schema: schemas.schema.Schema, start_nonterminal:str) -> str:
        pass
