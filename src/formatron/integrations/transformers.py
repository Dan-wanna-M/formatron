import typing

import kbnf
import torch
from transformers import LogitsProcessor, PreTrainedTokenizerBase

from formatter import Formatter


def _get_original_whitespace_characters(tokenizer, vocab, chars) -> typing.Dict[str, int]:
    old_char_to_new_char = {}
    for char in chars:
        char_ids = tokenizer.encode(char)
        if len(char_ids) != 1:
            continue
        char_id = char_ids[0]
        char_token = next(filter(lambda x: x[1] == char_id, vocab.items()))[0]
        if char_token != char:
            old_char_to_new_char[char_token] = char
    new_vocab = {}
    for k in vocab:
        new_k = k
        for char in old_char_to_new_char:
            new_k = new_k.replace(char, old_char_to_new_char[char])
        new_vocab[new_k] = vocab[k]
    return new_vocab


def create_engine_vocabulary(tokenizer: PreTrainedTokenizerBase) -> kbnf.Vocabulary:
    """
    Create a vocabulary for the KBNF engine.
    :param tokenizer: The tokenizer.
    :return: The vocabulary.
    """
    vocab = tokenizer.get_vocab()
    new_vocab = _get_original_whitespace_characters(tokenizer, vocab, [" ", "\n", "\t", '\n\n'])
    return kbnf.Vocabulary({v: kbnf.Token(k.encode("utf-8")) for k, v in new_vocab.items()},
                           {v: k for k, v in new_vocab.items()})


class FormattersLogitsProcessor(LogitsProcessor):
    """
    Logit processor that uses formatters to mask batch logits.
    """

    def __init__(self, formatters: typing.Sequence[Formatter], eos_token_id: int):
        self._formatters = formatters
        self._eos_token_id = eos_token_id
        self._last_input_id_length = None

    def __call__(self, input_ids, scores):
        assert input_ids.shape[0] == len(self._formatters), (f"Number of formatters({len(self._formatters)})"
                                                             f" must match batch size({input_ids.shape[0]})")

        if self._last_input_id_length is None:
            self._last_input_id_length = input_ids.shape[1]
            for formatter in self._formatters:
                formatter.reset()
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
