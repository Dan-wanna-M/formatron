from typing import Literal
from formatron.schemas import json_schema
from formatron.schemas.dict_inference import infer_mapping
from formatron.formatter import FormatterBuilder
import formatron.schemas.pydantic
import formatron.integrations.RWKV
from rwkv.model import RWKV
import numpy as np
import formatron



class Test(formatron.schemas.pydantic.ClassSchema):
    name: str
    weight: float
    color: str


def test_formatter(snapshot):
    FormatterBuilder._formatter_builder_counter = 0
    f = FormatterBuilder()
    a = f.choose('railroad', 'orange', 'banana', capture_name='food')
    f.append_line(
        f"Today, I want to eat {a}")
    f.append_str(
        f"My food's ID is {f.choose(f.regex('[0-9]+'), f.regex('[a-z]+'), capture_name='ID')}.\n")
    f.append_multiline_str("""
                            What's more, indentations
                            are handled
                            appropriately.""")
    f.append_line(
        f"My weight is 14.4kg and my color is pink. This is my personal info json: {f.json(Test, capture_name='json')}")
    model = RWKV(
        "assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = formatron.integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    np.random.seed(42)
    snapshot.assert_match(pipeline.formatter.grammar_str)
    snapshot.assert_match(
        pipeline.generate("My name is Van. ", token_count=256, args=formatron.integrations.RWKV.PIPELINE_ARGS(top_p=0.5)))
    snapshot.assert_match(pipeline.formatter.captures)


def test_formatter_str(snapshot):
    FormatterBuilder._formatter_builder_counter = 0
    f = FormatterBuilder()
    f.append_line(f"{f.str(stop=['.'])}")
    model = RWKV(
        "assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = formatron.integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    np.random.seed(42)
    snapshot.assert_match(pipeline.formatter.grammar_str)
    snapshot.assert_match(
        pipeline.generate("My name is Van. ", token_count=256, args=formatron.integrations.RWKV.PIPELINE_ARGS(top_p=0.5)))
    snapshot.assert_match(pipeline.formatter.captures)

def test_formatter_substr(snapshot):
    FormatterBuilder._formatter_builder_counter = 0
    f = FormatterBuilder()
    f.append_str(f"{f.substr('Name: Umbrella; Price: 114.514 dollars;', extract_empty_substring=True, capture_name='substr')}<eos>")
    model = RWKV(
        "assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = formatron.integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    np.random.seed(42)
    snapshot.assert_match(pipeline.formatter.grammar_str)
    snapshot.assert_match(pipeline.generate("Umbrella Price: 114.514 dollars. The price of the umbrella is",
                                             token_count=256, args=formatron.integrations.RWKV.PIPELINE_ARGS(top_p=0.5)))
    snapshot.assert_match(pipeline.formatter.captures)


def test_formatter_dict_inference(snapshot):
    FormatterBuilder._formatter_builder_counter = 0
    f = FormatterBuilder()
    f.append_line(
        f"{f.json(infer_mapping({'name': 'xxx', 'gender': 'xxx'}), capture_name='json')}")
    model = RWKV(
        "assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = formatron.integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    np.random.seed(42)
    snapshot.assert_match(pipeline.formatter.grammar_str)
    snapshot.assert_match(
        pipeline.generate("This is a random json: ", token_count=256, args=formatron.integrations.RWKV.PIPELINE_ARGS(top_p=0.5)))
    snapshot.assert_match(pipeline.formatter.captures)

def test_formatter_json_schema(snapshot):
    FormatterBuilder._formatter_builder_counter = 0
    f = FormatterBuilder()
    schema = {
        "$id": "https://example.com/person.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            },
            "age": {
                "type": "integer"
            }
        },
        "required": ["name", "age"]
    }
    schema = json_schema.create_schema(schema)
    f.append_line(
        f"{f.json(schema, capture_name='json')}")
    model = RWKV(
        "assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = formatron.integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    np.random.seed(42)
    snapshot.assert_match(
        pipeline.generate("This is a random json: ", token_count=256, args=formatron.integrations.RWKV.PIPELINE_ARGS(top_p=0.5)))
    snapshot.assert_match(pipeline.formatter.captures)
    snapshot.assert_match(pipeline.formatter.grammar_str)

def test_formatter_top_level_array_json_schema(snapshot):
    FormatterBuilder._formatter_builder_counter = 0
    f = FormatterBuilder()
    schema = {
        "$id": "https://example.com/array.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "active": {"type": "boolean"}
            },
            "required": ["id", "name"]
        },
        "minItems": 1,
        "maxItems": 5
    }
    schema = json_schema.create_schema(schema)
    f.append_line(f"{f.json(schema, capture_name='json')}")
    model = RWKV(
        "assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = formatron.integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    np.random.seed(42)
    snapshot.assert_match(pipeline.formatter.grammar_str)
    snapshot.assert_match(
        pipeline.generate("Generate a JSON array of users: ", token_count=256, args=formatron.integrations.RWKV.PIPELINE_ARGS(top_p=0.5)))
    snapshot.assert_match(pipeline.formatter.captures)


def test_formatter_callable_schema(snapshot):
    @formatron.schemas.pydantic.callable_schema
    def add(a: int, b: int, /, *, c: int):
        return a + b + c

    FormatterBuilder._formatter_builder_counter = 0
    f = FormatterBuilder()
    f.append_line(
        f"{f.json(add, capture_name='json')}")
    model = RWKV(
        "assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = formatron.integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    np.random.seed(42)
    snapshot.assert_match(pipeline.formatter.grammar_str)
    snapshot.assert_match(
        pipeline.generate("This is a random json: ", token_count=256, args=formatron.integrations.RWKV.PIPELINE_ARGS(top_p=0.5)))
    snapshot.assert_match(pipeline.formatter.captures)

def test_grammar_literal(snapshot):
    FormatterBuilder._formatter_builder_counter = 0
    f = FormatterBuilder()
    class A(formatron.schemas.pydantic.ClassSchema):
        a: Literal['114', '514']
    f.append_line(
        f"{f.json(A, capture_name='json')}")
    model = RWKV(
        "assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = formatron.integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    np.random.seed(42)
    snapshot.assert_match(pipeline.formatter.grammar_str)
    snapshot.assert_match(
        pipeline.generate("This is a random json: ", token_count=256, args=formatron.integrations.RWKV.PIPELINE_ARGS(top_p=0.5)))
    snapshot.assert_match(pipeline.formatter.captures)


def test_formatter_alternate_accept(snapshot):
    FormatterBuilder._formatter_builder_counter = 0
    f = FormatterBuilder()
    f.append_str(f"Name: {f.str(stop=[','], capture_name='name')}")
    f.append_str(f"Age: {f.regex('[0-9]+', capture_name='age')}")

    model = RWKV(
        "assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = formatron.integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    
    formatter = pipeline.formatter
    
    # Simulate alternating between accept_token and accept_bytes
    tokens = pipeline.tokenizer.encode("Name: John,")
    for token in tokens:
        formatter.accept_token(token)
    formatter.accept_bytes(b"Age: ")
    tokens = pipeline.tokenizer.encode("30")
    for token in tokens:
        formatter.accept_token(token)
    
    snapshot.assert_match(formatter.captures)

