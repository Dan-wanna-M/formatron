import numpy as np
from rwkv.model import RWKV

import grammar_generators.json_generator
import integrations.RWKV
import schemas.pydantic
from formatter import FormatterBuilder
from schemas.dict_inference import infer_mapping


class Test(schemas.pydantic.ClassSchema):
    name: str
    weight: float
    color: str


def test_formatter(snapshot):
    FormatterBuilder._formatter_builder_counter = 0
    f = FormatterBuilder()
    f.append_line(f"Today, I want to eat {f.choose('railroad', 'orange', 'banana', capture_name='food')}")
    f.append_str(f"My food's ID is {f.choose(f.regex('[0-9]+'), f.regex('[a-z]+'), capture_name='ID')}.\n")
    f.append_multiline_str(f"""
                            What's more, indentations
                            are handled
                            appropriately.""")
    f.append_line(
        f"My weight is 14.4kg and my color is pink. This is my personal info json: {f.schema(Test, grammar_generators.json_generator.JsonGenerator(), capture_name='json')}")
    model = RWKV("assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    np.random.seed(42)
    snapshot.assert_match(pipeline.formatter.grammar_str)
    snapshot.assert_match(
        pipeline.generate("My name is Van. ", token_count=256, args=integrations.RWKV.PIPELINE_ARGS(top_p=0.5)))
    snapshot.assert_match(pipeline.formatter.captures)

def test_formatter_str(snapshot):
    FormatterBuilder._formatter_builder_counter = 0
    f = FormatterBuilder()
    f.append_line(f"{f.str(stop=['.'])}")
    model = RWKV("assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    np.random.seed(42)
    snapshot.assert_match(pipeline.formatter.grammar_str)
    snapshot.assert_match(
        pipeline.generate("My name is Van. ", token_count=256, args=integrations.RWKV.PIPELINE_ARGS(top_p=0.5)))
    snapshot.assert_match(pipeline.formatter.captures)

def test_formatter_dict_inference(snapshot):
    FormatterBuilder._formatter_builder_counter = 0
    f = FormatterBuilder()
    f.append_line(
        f"{f.schema(infer_mapping({'name': 'xxx', 'gender': 'xxx'}), grammar_generators.json_generator.JsonGenerator(), capture_name='json')}")
    model = RWKV("assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    np.random.seed(42)
    snapshot.assert_match(pipeline.formatter.grammar_str)
    snapshot.assert_match(
        pipeline.generate("This is a random json: ", token_count=256, args=integrations.RWKV.PIPELINE_ARGS(top_p=0.5)))
    snapshot.assert_match(pipeline.formatter.captures)


def test_formatter_callable_schema(snapshot):
    @schemas.pydantic.callable_schema
    def add(a: int, b: int, /, *, c: int):
        return a + b + c

    FormatterBuilder._formatter_builder_counter = 0
    f = FormatterBuilder()
    f.append_line(
        f"{f.schema(add, grammar_generators.json_generator.JsonGenerator(), capture_name='json')}")
    model = RWKV("assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    np.random.seed(42)
    snapshot.assert_match(pipeline.formatter.grammar_str)
    snapshot.assert_match(
        pipeline.generate("This is a random json: ", token_count=256, args=integrations.RWKV.PIPELINE_ARGS(top_p=0.5)))
    snapshot.assert_match(pipeline.formatter.captures)