"""
This module integrates the transformers library by providing convenience utilities.
"""
import collections
import typing
import torch
import kbnf
from transformers import LogitsProcessor, PreTrainedTokenizerBase, LogitsProcessorList

from formatron.config import EngineGenerationConfig
from formatron.formatter import FormatterBuilder, FormatterBase
from formatron.integrations.utils import get_original_characters

__all__ = ["create_engine_vocabulary", "create_formatter_logits_processor", "create_formatter_logits_processor_list", "FormattersLogitsProcessor"]

def create_engine_vocabulary(tokenizer: PreTrainedTokenizerBase,
                             vocab_processors: typing.Optional[list[typing.Callable]] = None) -> kbnf.Vocabulary:
    """
    Create a vocabulary for the KBNF engine.
    Args:
        tokenizer: The tokenizer.
        vocab_processors: List of callables with signature (token_to_char: typing.Dict[bytes, bytes])->None.
            Callables can be used to "unmangle" encoded characters to original characters. If None, processors will be auto-detected.
    """
    vocab = tokenizer.get_vocab()
    new_vocab = get_original_characters(vocab, vocab_processors)
    return kbnf.Vocabulary({k: kbnf.Token(v) for k, v in new_vocab.items()},
                           {v: k for k, v in vocab.items()})


def create_formatter_logits_processor(tokenizer: PreTrainedTokenizerBase,
                                      formatter_builders: typing.Sequence[FormatterBuilder | None] | FormatterBuilder,
                                      configs: typing.Sequence[EngineGenerationConfig] = None,
                                      vocab_processors: typing.Optional[list[typing.Callable]] = None) -> LogitsProcessor:
    """
    Create a formatter logits processor.
    Args:
        tokenizer: The tokenizer.
        formatter_builders: The formatter builders.
        configs: The engine generation configurations.
        vocab_processors: List of callables with signature (token_to_char: typing.Dict[bytes, bytes])->None.
            Callables can be used to "unmangle" encoded characters to original characters. If None, processors will be auto-detected.
    """
    vocab = create_engine_vocabulary(tokenizer, vocab_processors)
    if not isinstance(formatter_builders, collections.abc.Sequence):
        formatter_builders = [formatter_builders]
    formatters = [i.build(vocab, lambda tokens: tokenizer.decode(tokens)) if i is not None else None
                  for i in formatter_builders]
    return FormattersLogitsProcessor(formatters, tokenizer.eos_token_id, configs)


def create_formatter_logits_processor_list(tokenizer: PreTrainedTokenizerBase,
                                           formatter_builders: typing.Sequence[FormatterBuilder | None] | FormatterBuilder,
                                           configs: typing.Sequence[EngineGenerationConfig] = None,
                                           vocab_processors: typing.Optional[list[typing.Callable]] = None) \
        -> LogitsProcessorList:
    """
    Create a formatter logits processor list.
    Args:
        tokenizer: The tokenizer.
        formatter_builders: The formatter builders.
        configs: The engine generation configurations.
        vocab_processors: List of callables with signature (token_to_char: typing.Dict[bytes, bytes])->None.
            Callables can be used to "unmangle" encoded characters to original characters. If None, processors will be auto-detected.
    """
    return LogitsProcessorList([create_formatter_logits_processor(tokenizer,
                                                                  formatter_builders, configs, vocab_processors)])


class FormattersLogitsProcessor(LogitsProcessor):
    """
    Logit processor that uses formatters to mask batch logits.
    """

    def __init__(self, formatters: typing.Sequence[FormatterBase | None], eos_token_id: int,
                 configs: typing.Sequence[EngineGenerationConfig] | None = None):
        self._formatters = formatters
        self._eos_token_id = eos_token_id
        self._last_input_id_length = None
        if configs is None:
            configs = [EngineGenerationConfig() for _ in formatters]
        assert len(configs) == len(formatters), \
            f"Number of formatters({len(formatters)}) must match number of configs({len(configs)})"
        self.configs = configs
        self._mask_logits_fn = FormattersLogitsProcessor._get_fastest_compatible_logits_mask_fn()
    
    @staticmethod
    def _get_fastest_compatible_logits_mask_fn():
        def default_mask_logits_fn(bit_masks, formatter, scores, i):
            scores[i, :] = formatter.mask_logits(scores[i, :])
        try:
            from kbnf.triton_logits_mask import mask_logits_inplace
            def fast_mask_logits_fn(bit_masks, formatter, scores, i):
                mask_logits_inplace(scores[i, :], bit_masks[i, :], [formatter._engine])
            return fast_mask_logits_fn
        except ImportError:
            return default_mask_logits_fn

    def reset(self) -> None:
        self._last_input_id_length = None
        for f in self._formatters:
            if f is not None:
                f.reset()

    @property
    def formatters_captures(self) -> list[dict[str, typing.Any] | None]:
        """
        Get the captures of the formatters. Each element in the list corresponds to the
        captures of the formatter at the same index. If the formatter is None, the element
        is None.
        """
        return [f.captures if f is not None else None for f in self._formatters]

    def is_completed(self) -> list[bool | None]:
        """
        Check if the formatters are completed. Each boolean in the list corresponds to the
        completion status of the formatter at the same index. If the formatter is None,
        the element is None.
        """
        return [f.is_completed() if f is not None else None for f in self._formatters]

    def __call__(self, input_ids, scores):
        assert input_ids.shape[0] == len(self._formatters), (f"Number of formatters({len(self._formatters)})"
                                                             f" must match batch size({input_ids.shape[0]})")
        if self._last_input_id_length is None:  # First iteration
            self._last_input_id_length = input_ids.shape[1]
            for formatter, config, prompt in zip(self._formatters, self.configs, input_ids):
                if formatter is None:
                    continue
                if config.reset_at_beginning:
                    formatter.reset()
                if config.read_prompt:
                    for token in prompt:
                        formatter.accept_token(token)
            self._bit_masks = torch.empty((scores.shape[0],
                                            (scores.shape[1]+31)//32), dtype=torch.int32, device='cpu', pin_memory=True)
        else:
            assert input_ids.shape[1] == self._last_input_id_length + 1, ("One iteration in generation loop"
                                                                          " must add exactly one token.")
            self._last_input_id_length += 1
            for formatter, input_id in zip(self._formatters, input_ids[:, -1]):
                if  formatter is not None and not formatter.is_completed():
                    formatter.accept_token(input_id)
        for i, formatter in enumerate(self._formatters):
            if formatter is None:
                continue
            if formatter.is_completed():
                scores[i, :] = float("-inf")
                scores[i, self._eos_token_id] = 0.0
                continue
            formatter.compute_allowed_tokens()
            self._mask_logits_fn(self._bit_masks, formatter, scores, i)
        return scores
