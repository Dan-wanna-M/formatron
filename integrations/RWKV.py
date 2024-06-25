import kbnf
import numpy as np
import rwkv.utils
import rwkv.rwkv_tokenizer
import torch
from kbnf import AcceptTokenResult, Token
from torch.nn import functional as F
import schemas.schema
from config import EngineGenerationConfig


class PIPELINE_ARGS(rwkv.utils.PIPELINE_ARGS):
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


class PIPELINE(rwkv.utils.PIPELINE):
    def __init__(self, model, WORD_NAME, grammar_str=None):
        super().__init__(model, WORD_NAME)
        assert WORD_NAME == 'rwkv_vocab_v20230424', "Only world vocabulary is supported!"
        if grammar_str is not None:
            vocabulary = kbnf.Vocabulary({k: Token(v) for k, v in self.tokenizer.idx2token.items()},
                                         {k: v.decode("UTF-8", errors="replace") for k, v in
                                          self.tokenizer.idx2token.items()})
            self.engine = kbnf.Engine(grammar_str, vocabulary)
        else:
            self.engine = None

    def generate(self, ctx, token_count=100, args=PIPELINE_ARGS(), callback=None, state=None):
        all_tokens = []
        out_last = 0
        out_str = ''
        occurrence = {}
        for i in range(token_count):
            # forward & adjust prob.
            tokens = self.encode(ctx) if i == 0 else [token]
            engine_result = None
            if self.engine is not None:
                engine = self.engine
                if i == 0 and args.engine_gen_config.read_prompt:
                    for token in tokens:
                        engine.try_accept_new_token(token)
            while len(tokens) > 0:
                out, state = self.model.forward(tokens[:args.chunk_len], state)
                tokens = tokens[args.chunk_len:]
            if engine_result == AcceptTokenResult.Finished:
                break
            for n in args.token_ban:
                out[n] = -float('inf')
            for n in occurrence:
                out[n] -= (args.alpha_presence + occurrence[n] * args.alpha_frequency)
            if self.engine is not None:
                engine = self.engine
                engine.compute_allowed_token_ids()
                out = out[:len(self.tokenizer.idx2token) + 1]  # account for the padding `0` token
                out = engine.mask_logits(out)
                # out = torch.where(out == float('-inf'), torch.tensor(-1e38), out)
            # sampler
            token = self.sample_logits(out, temperature=args.temperature, top_p=args.top_p, top_k=args.top_k)
            if self.engine is not None:
                engine = self.engine
                result = engine.try_accept_new_token(token)
                if result == AcceptTokenResult.Finished:
                    if args.engine_gen_config.reset_on_completion:
                        engine.reset()
                    break
            if token in args.token_stop:
                break
            all_tokens += [token]
            for xxx in occurrence:
                occurrence[xxx] *= args.alpha_decay

            ttt = self.decode([token])
            www = 1
            if ttt in ' \t0123456789':
                www = 0
            # elif ttt in '\r\n,.;?!"\':+-*/=#@$%^&_`~|<>\\()[]{}，。；“”：？！（）【】':
            #     www = 0.5
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
        return out_str
