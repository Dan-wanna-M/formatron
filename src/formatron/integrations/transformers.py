"""
This module integrates the transformers library by providing convenience utilities.
"""
import collections
import typing

import kbnf
from config import EngineGenerationConfig
from formatter import Formatter, FormatterBuilder
from integrations._utils import get_original_characters
from transformers import LogitsProcessor, PreTrainedTokenizerBase, LogitsProcessorList


def create_engine_vocabulary(tokenizer: PreTrainedTokenizerBase) -> kbnf.Vocabulary:
    """
    Create a vocabulary for the KBNF engine.
    """
    vocab = tokenizer.get_vocab()
    new_vocab = get_original_characters(vocab)
    return kbnf.Vocabulary({v: kbnf.Token(k) for k, v in new_vocab.items()},
                           {v: k for k, v in vocab.items()})


def create_formatter_logits_processor(tokenizer: PreTrainedTokenizerBase,
                                      formatter_builders: typing.Sequence[FormatterBuilder] | FormatterBuilder,
                                      configs: typing.Sequence[EngineGenerationConfig] = None) -> LogitsProcessor:
    """
    Create a formatter logits processor.
    """
    vocab = create_engine_vocabulary(tokenizer)
    if not isinstance(formatter_builders, collections.abc.Sequence):
        formatter_builders = [formatter_builders]
    formatters = [i.build(vocab, lambda tokens: tokenizer.decode(tokens)) for i in formatter_builders]
    return FormattersLogitsProcessor(formatters, tokenizer.eos_token_id, configs)


def create_formatter_logits_processor_list(tokenizer: PreTrainedTokenizerBase,
                                           formatter_builders: typing.Sequence[FormatterBuilder] | FormatterBuilder,
                                           configs: typing.Sequence[EngineGenerationConfig] = None) \
        -> LogitsProcessorList:
    """
    Create a formatter logits processor list.
    """
    return LogitsProcessorList([create_formatter_logits_processor(tokenizer,
                                                                  formatter_builders, configs)])


class FormattersLogitsProcessor(LogitsProcessor):
    """
    Logit processor that uses formatters to mask batch logits.
    """

    def __init__(self, formatters: typing.Sequence[Formatter], eos_token_id: int,
                 configs: typing.Sequence[EngineGenerationConfig] = None):
        self._formatters = formatters
        self._eos_token_id = eos_token_id
        self._last_input_id_length = None
        if configs is None:
            configs = [EngineGenerationConfig() for _ in formatters]
        assert len(configs) == len(formatters), \
            f"Number of formatters({len(formatters)}) must match number of configs({len(configs)})"
        self.configs = configs

    @property
    def formatters_captures(self)->list[dict[str,typing.Any]]:
        return [f.captures for f in self._formatters]

    def __call__(self, input_ids, scores):
        assert input_ids.shape[0] == len(self._formatters), (f"Number of formatters({len(self._formatters)})"
                                                             f" must match batch size({input_ids.shape[0]})")
        if self._last_input_id_length is None:  # First iteration
            self._last_input_id_length = input_ids.shape[1]
            for formatter, config, prompt in zip(self._formatters, self.configs, input_ids):
                if config.reset_at_beginning and formatter.is_completed():
                    formatter.reset()
                if config.read_prompt:
                    for token in prompt:
                        formatter.accept_token(token)
        else:
            assert input_ids.shape[1] == self._last_input_id_length + 1, ("One iteration in generation loop"
                                                                          " must add exactly one token.")
            self._last_input_id_length += 1
            for formatter, input_id in zip(self._formatters, input_ids[:, -1]):
                if input_id != self._eos_token_id:
                    formatter.accept_token(input_id)

        for i, formatter in enumerate(self._formatters):
            if formatter.is_completed():
                scores[i, :] = float("-inf")
                scores[i, self._eos_token_id] = 0.0
                continue
            formatter.compute_allowed_tokens()
            score = scores[i, :]
            new_score = formatter.mask_logits(score)

            if score is not new_score:  # Avoid unnecessary copy
                scores[i, :] = new_score
        return scores
