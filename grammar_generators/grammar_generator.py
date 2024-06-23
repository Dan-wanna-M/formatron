import abc
import schemas.schema


class GrammarGenerator(abc.ABC):
    @abc.abstractmethod
    def generate(self, schema: schemas.schema.Schema) -> str:
        pass
