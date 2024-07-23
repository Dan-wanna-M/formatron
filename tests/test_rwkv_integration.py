import rwkv
from rwkv.model import RWKV

from integrations.RWKV import PIPELINE


def test_rwkv_integration(snapshot):
    model = RWKV("assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = PIPELINE(model, "rwkv_vocab_v20230424", grammar_str="start ::= '一个' start|'\\n\\n';")
    snapshot.assert_match(pipeline.generate("你是一个一个一个一个一个"))