"""
This module integrates the RWKV library by providing convenience utilities.
"""
import kbnf
import rwkv.utils
from kbnf import Token

from formatron.config import EngineGenerationConfig
from formatron.formatter import FormatterBuilder


class PIPELINE_ARGS(rwkv.utils.PIPELINE_ARGS):
    """
    A wrapper for the arguments of the pipeline of RWKV.
    """

    def __init__(self,
                 temperature=1.0,
                 top_p=0.2,
                 top_k=0,
                 alpha_frequency=0.2,
                 alpha_presence=0.2,
                 alpha_decay=0.996,
                 token_ban=[],
                 token_stop=[],
                 chunk_len=256,
                 engine_gen_config=EngineGenerationConfig()):
        super().__init__(temperature, top_p, top_k, alpha_frequency, alpha_presence, alpha_decay, token_ban, token_stop,
                         chunk_len)
        self.engine_gen_config = engine_gen_config


def create_engine_vocabulary(WORD_NAME: str, tokenizer) -> kbnf.Vocabulary:  # NOSONAR
    """
    Create a vocabulary for the KBNF engine.
    """
    assert WORD_NAME == 'rwkv_vocab_v20230424', "Only world vocabulary is supported!"
    return kbnf.Vocabulary({k: Token(v) for k, v in tokenizer.idx2token.items()},
                           {k: v.decode("UTF-8", errors="replace") for k, v in
                            tokenizer.idx2token.items()})


class PIPELINE(rwkv.utils.PIPELINE):  # NOSONAR
    """
    A wrapper for the pipeline of RWKV.
    """

    def __init__(self, model, WORD_NAME, formatter_builder: FormatterBuilder = None):  # NOSONAR
        super().__init__(model, WORD_NAME)
        vocabulary = create_engine_vocabulary(WORD_NAME, self.tokenizer)
        formatter = formatter_builder.build(vocabulary, lambda tokens: self.tokenizer.decode(tokens))
        if formatter is not None:
            self.formatter = formatter
        else:
            self.formatter = None

    def generate(self, ctx, token_count=100, args=PIPELINE_ARGS(), callback=None, state=None):
        all_tokens = []
        out_last = 0
        out_str = ''
        occurrence = {}
        if args.engine_gen_config.reset_at_beginning and self.formatter and self.formatter.is_completed():
            self.formatter.reset()
        for i in range(token_count):
            # forward & adjust prob.
            tokens = self.encode(ctx) if i == 0 else [token]
            if self.formatter is not None:
                if i == 0 and args.engine_gen_config.read_prompt:
                    for token in tokens:
                        self.formatter.accept_token(token)
            while len(tokens) > 0:
                out, state = self.model.forward(tokens[:args.chunk_len], state)
                tokens = tokens[args.chunk_len:]
            if self.formatter and self.formatter.is_completed():
                break
            for n in args.token_ban:
                out[n] = -float('inf')
            for n in occurrence:
                out[n] -= (args.alpha_presence + occurrence[n] * args.alpha_frequency)
            if self.formatter is not None:
                formatter = self.formatter
                formatter.compute_allowed_tokens()
                out = out[:len(self.tokenizer.idx2token) + 1]  # account for the padding `0` token
                out = formatter.mask_logits(out)
            # sampler
            token = self.sample_logits(out, temperature=args.temperature, top_p=args.top_p, top_k=args.top_k)
            if self.formatter:
                self.formatter.accept_token(token)
            if token in args.token_stop:
                break
            all_tokens += [token]
            for xxx in occurrence:
                occurrence[xxx] *= args.alpha_decay

            ttt = self.decode([token])
            www = 1
            if ttt in ' \t0123456789':
                www = 0
            if token not in occurrence:
                occurrence[token] = www
            else:
                occurrence[token] += www
            # print(occurrence) # debug

            # output
            tmp = self.decode(all_tokens[out_last:])
            if '\ufffd' not in tmp:  # is valid utf-8 string?
                if callback:
                    callback(tmp)
                out_str += tmp
                out_last = i + 1
            if self.formatter and self.formatter.is_completed():
                break
        return out_str
