"""
This module integrates the vllm library by providing convenience utilities.
"""
import collections.abc
import typing

import kbnf
from vllm import LLM

from config import EngineGenerationConfig
from formatter import Formatter, FormatterBuilder
from integrations._utils import get_original_characters


class FormattersLogitsProcessor:
    """
    Logit processor that uses formatters to mask batch logits.
    """

    def __init__(self, formatters: typing.Sequence[Formatter], eos_token_id: int,
                 configs: typing.Sequence[EngineGenerationConfig] = None):
        self._formatters = formatters
        self._eos_token_id = eos_token_id
        self._last_input_id_length = 0
        if configs is None:
            configs = [EngineGenerationConfig() for _ in formatters]
        assert len(configs) == len(formatters), \
            f"Number of formatters({len(formatters)}) must match number of configs({len(configs)})"
        self._configs = configs
        self._iter = zip(self._formatters, self._configs)
        self._debug_counter = 0

    @property
    def formatters_captures(self) -> list[dict[str, typing.Any]]:
        return [f.captures for f in self._formatters]

    def reset(self)->None:
        for f in self._formatters:
            f.reset()
        self._to_next_batch_step()
        self._last_input_id_length = 0

    def _to_next_batch_step(self):
        self._iter = zip(self._formatters, self._configs)
        self._debug_counter = 0

    def __call__(self, prompt, generated_tokens, logits):
        result = next(self._iter, None)
        if result is None and len(generated_tokens) == self._last_input_id_length:
            # We exhausted all formatters but still have sequences to process in this batch
            raise ValueError(f"Batch size {self._debug_counter} "
                             f"is greater than number of formatters({len(self._formatters)})!")
        if len(generated_tokens) == 0:  # First iteration
            self._debug_counter += 1
            formatter, config = result
            if config.reset_at_beginning and formatter.is_completed():
                formatter.reset()
            if config.read_prompt:
                for token in prompt:
                    formatter.accept_token(token)
        elif len(generated_tokens) == self._last_input_id_length + 1:  # to next batch step
            assert result is None, (f"Batch size {self._debug_counter} "
                                    f"is less than number of formatters({len(self._formatters)})!")
            self._to_next_batch_step()
            result = next(self._iter)
            self._last_input_id_length += 1
        formatter, _ = result
        while formatter.is_completed():
            formatter, _ = next(self._iter)
        if len(generated_tokens) != 0:  # accept new token
            input_id = generated_tokens[-1]
            if input_id != self._eos_token_id:
                formatter.accept_token(input_id)

        if formatter.is_completed():
            logits[:] = float("-inf")
            logits[self._eos_token_id] = 1000
            return logits
        formatter.compute_allowed_tokens()
        logits = formatter.mask_logits(logits)
        return logits


def create_engine_vocabulary(llm: LLM) -> kbnf.Vocabulary:
    """
    Create a vocabulary for the KBNF engine.
    """
    tokenizer = llm.get_tokenizer()
    vocab = tokenizer.get_vocab()
    new_vocab = get_original_characters(vocab)
    return kbnf.Vocabulary({v: kbnf.Token(k) for k, v in new_vocab.items()}, {
        v:k for k,v in vocab.items()})


def create_formatters_logits_processor(llm: LLM,
                                       formatter_builders: typing.Sequence[FormatterBuilder] | FormatterBuilder,
                                       configs: typing.Sequence[EngineGenerationConfig] = None) \
        -> FormattersLogitsProcessor:
    """
    Create a formatter logits processor.
    """
    tokenizer = llm.get_tokenizer()
    vocab = create_engine_vocabulary(llm)
    if not isinstance(formatter_builders, collections.abc.Sequence):
        formatter_builders = [formatter_builders]
    formatters = [i.build(vocab, lambda tokens: tokenizer.decode(tokens)) for i in formatter_builders]
    return FormattersLogitsProcessor(formatters, tokenizer.eos_token_id, configs)