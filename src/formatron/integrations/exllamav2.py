import typing
from copy import copy, deepcopy
import kbnf
import torch
from exllamav2 import ExLlamaV2Tokenizer, ExLlamaV2
from exllamav2.generator.base import ExLlamaV2Filter
from config import EngineGenerationConfig
from formatter import Formatter, FormatterBuilder
from integrations._utils import get_original_whitespace_characters


def create_engine_vocabulary(tokenizer: ExLlamaV2Tokenizer) -> kbnf.Vocabulary:
    """
    Create a vocabulary for the KBNF engine.
    :param tokenizer: The tokenizer.
    :return: The vocabulary.
    """
    assert hasattr(tokenizer.tokenizer_model, "vocab"), (f"tokenizer({tokenizer})"
                                                         f" with tokenizer_model({tokenizer.tokenizer_model})"
                                                         f" does not have vocab attribute!")
    vocab = tokenizer.get_id_to_piece_list(include_special_tokens=True)
    vocab = {v: i for i, v in enumerate(vocab)}
    vocab = get_original_whitespace_characters(tokenizer, vocab)
    return kbnf.Vocabulary({v: kbnf.Token(k.encode("utf-8")) for k, v in vocab.items()},
                           {v: k for k, v in vocab.items()})

def create_formatter_filter(model:ExLlamaV2,tokenizer: ExLlamaV2Tokenizer,
                            formatter_builder:FormatterBuilder,
                            engine_config:EngineGenerationConfig=None)->ExLlamaV2Filter:
    vocab = create_engine_vocabulary(tokenizer)
    f = formatter_builder.build(vocab, lambda tokens:tokenizer.decode(torch.tensor(tokens)))
    return FormatterFilter(model, tokenizer, f, engine_config)

class FormatterFilter(ExLlamaV2Filter):
    def __init__(self, model, tokenizer, formatter: Formatter,
                 config: EngineGenerationConfig = None):
        super().__init__(model, tokenizer)
        self._formatter = formatter
        if config is None:
            config = EngineGenerationConfig()
        self._config = config

    def clone(self, c=None) -> "FormatterFilter":
        if c is None:
            c = FormatterFilter.__new__(FormatterFilter)
        c.model = self.model
        c.tokenizer = self.tokenizer
        c.sequence_str = self.sequence_str
        c._formatter = copy(self._formatter)  # formatter does not have mutable public state anyway
        c._config = deepcopy(self._config)
        return c

    def begin(self, prefix_str: str) -> None:
        if self._config.reset_on_completion and self._formatter.is_completed():
            self._formatter.reset()
        if self._config.read_prompt:
            prompt = prefix_str.encode("utf-8")
            self._formatter.accept_bytes(prompt)

    def feed(self, token: int):
        self._formatter.accept_token(token)

    def next(self) -> typing.Tuple[typing.Set[int], typing.Set[int]]:
        pass_tokens = set()
        end_tokens = set()
        self._formatter.compute_allowed_tokens()
        pass_tokens.update(self._formatter.get_allowed_tokens_since_last_computation())
        end_tokens.update(self._formatter.get_tokens_to_finish_since_last_computation())
        return pass_tokens, end_tokens
