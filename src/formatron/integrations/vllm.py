import typing

import kbnf
from transformers import PreTrainedTokenizerBase
from vllm import LLM

from config import EngineGenerationConfig
from formatter import Formatter, FormatterBuilder
from integrations._utils import get_original_whitespace_characters


def create_engine_vocabulary(llm:LLM)->kbnf.Vocabulary:
    tokenizer = llm.get_tokenizer()
    vocab = tokenizer.get_vocab()
    new_vocab = get_original_whitespace_characters(tokenizer, vocab)
    return kbnf.Vocabulary({v: kbnf.Token(k.encode("utf-8")) for k, v in new_vocab.items()},
                           {v: k for k, v in new_vocab.items()})

def create_formatter_logits_processor(llm:LLM,
                                      formatter_builder: FormatterBuilder,
                                      config:EngineGenerationConfig = None) -> "FormatterLogitsProcessor":
    """
    Create a formatter logits processor.
    """
    vocab = create_engine_vocabulary(llm)
    tokenizer = llm.get_tokenizer()
    formatter = formatter_builder.build(vocab, lambda tokens:tokenizer.decode(tokens))
    return FormatterLogitsProcessor(formatter, tokenizer.eos_token_id, config)

class FormatterLogitsProcessor:
    """
    Logit processor that uses formatters to mask batch logits.
    """

    def __init__(self, formatter: Formatter, eos_token_id: int,
                 config: EngineGenerationConfig = None):
        self._formatter = formatter
        self._eos_token_id = eos_token_id
        self._last_input_id_length = None
        if config is None:
            config = EngineGenerationConfig()
        self.config = config

    def __call__(self, prompt, generated_tokens, logits):
        if self._last_input_id_length is None:  # First iteration
            self._last_input_id_length = len(generated_tokens)
            if self.config.reset_on_completion and self._formatter.is_completed():
                self._formatter.reset()
            if self.config.read_prompt:
                for token in prompt:
                    self._formatter.accept_token(token)
        else:
            assert len(generated_tokens) == self._last_input_id_length + 1, ("One iteration in generation loop"
                                                                          " must add exactly one token.")
            self._last_input_id_length += 1
            input_id = generated_tokens[-1]
            if input_id != self._eos_token_id:
                self._formatter.accept_token(input_id)
        if self._formatter.is_completed():
            logits[:] = float("-inf")
            logits[self._eos_token_id] = 0.0
            return logits
        self._formatter.compute_allowed_tokens()
        logits = self._formatter.mask_logits(logits)
        return logits