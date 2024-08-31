from rwkv.model import RWKV

from formatron.formatter import FormatterBuilder
from formatron.integrations.RWKV import PIPELINE


def test_rwkv_integration(snapshot):
    model = RWKV("assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    f = FormatterBuilder()
    f.append_line(f"Hello, RWKV!")
    pipeline = PIPELINE(model, "rwkv_vocab_v20230424", f)
    snapshot.assert_match(pipeline.generate("你好！"))
    snapshot.assert_match(pipeline.generate("你好！"))