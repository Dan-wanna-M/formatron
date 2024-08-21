"""
This module integrates the ExLlamaV2 library by providing convenience utilities.
"""
import typing
from copy import copy, deepcopy
import kbnf
import torch
from exllamav2 import ExLlamaV2Tokenizer, ExLlamaV2
from exllamav2.generator.base import ExLlamaV2Filter
from formatron.config import EngineGenerationConfig
from formatron.formatter import FormatterBase, FormatterBuilder
from formatron.integrations._utils import get_original_characters


def create_engine_vocabulary(tokenizer: ExLlamaV2Tokenizer) -> kbnf.Vocabulary:
    """
    Create a vocabulary for the KBNF engine.
    """
    assert hasattr(tokenizer.tokenizer_model, "vocab"), (f"tokenizer({tokenizer})"
                                                         f" with tokenizer_model({tokenizer.tokenizer_model})"
                                                         f" does not have vocab attribute!")
    vocab = {tokenizer.tokenizer_model.id_to_piece(i): i for i in range(tokenizer.tokenizer_model.vocab_size())}
    new_vocab = get_original_characters(vocab)
    return kbnf.Vocabulary({v: kbnf.Token(k) for k, v in new_vocab.items()},
                           {k: v for k, v in enumerate(vocab)})


def create_formatter_filter(model: ExLlamaV2, tokenizer: ExLlamaV2Tokenizer,
                            formatter_builder: FormatterBuilder,
                            engine_config: EngineGenerationConfig = None) -> ExLlamaV2Filter:
    """
    Create a formatter filter for the ExLlamaV2 engine.
    """
    vocab = create_engine_vocabulary(tokenizer)
    f = formatter_builder.build(vocab, lambda tokens: tokenizer.decode(torch.tensor(tokens)))
    return FormatterFilter(model, tokenizer, f, engine_config)


class FormatterFilter(ExLlamaV2Filter):
    """
    ExLlamaV2Filter that uses a formatter to mask logits.
    """

    def __init__(self, model, tokenizer, formatter: FormatterBase,
                 config: EngineGenerationConfig = None):
        super().__init__(model, tokenizer)
        self._formatter = formatter
        if config is None:
            config = EngineGenerationConfig()
        self._config = config
        self._pass_tokens = set()

    def clone(self, c=None) -> "FormatterFilter":
        if c is None:
            c = FormatterFilter.__new__(FormatterFilter)
        c.model = self.model
        c.tokenizer = self.tokenizer
        c.sequence_str = self.sequence_str
        c._formatter = copy(self._formatter)  # formatter does not have mutable public state anyway
        c._config = deepcopy(self._config)
        c._pass_tokens = self._pass_tokens
        return c

    def begin(self, prefix_str: str) -> None:
        if self._config.reset_at_beginning:
            self._formatter.reset()
        if self._config.read_prompt:
            prompt = prefix_str.encode("utf-8")
            self._formatter.accept_bytes(prompt)

    def reset(self)->None:
        self._formatter.reset()

    def feed(self, token: int):
        if self._formatter.is_completed():
            return None
        self._formatter.accept_token(token)

    def next(self) -> typing.Tuple[typing.Set[int], typing.Set[int]]:
        if self._formatter.is_completed():
            return {self.tokenizer.eos_token_id}, set()
        self._formatter.compute_allowed_tokens()
        self._pass_tokens.clear()
        self._pass_tokens.update(self._formatter.get_allowed_tokens_since_last_computation())
        return self._pass_tokens, set()

    @property
    def formatter_captures(self) -> dict[str, typing.Any]:
        return self._formatter.captures
