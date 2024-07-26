import decimal
import json
import os
import sys
import typing

import rwkv
from rwkv.model import RWKV
from rwkv.rwkv_tokenizer import TRIE_TOKENIZER

import integrations.RWKV
from pydantic import Field

import grammar_generators.json_generator
import schemas.pydantic
from formatter import FormatterBuilder
from schemas.dict_inference import infer_mapping

new_int = typing.NewType("new_int", int)
vector = list[int]


class Test(schemas.pydantic.ClassSchema):
    name: str
    weight: float
    color: str


def test_formatter(snapshot):
    f = FormatterBuilder()
    f.append_line(f"Today, I want to eat {f.choose('railroad', 'orange', 'banana', capture_name='food')}")
    f.append_str(f"My food's ID is {f.choose(f.regex('[0-9]+'), f.regex('[a-z]+'), capture_name='ID')}.\n")
    f.append_multiline_str(f"""
                            What's more, indentations
                            are handled
                            appropriately.""")
    f.append_line(
        f"Let me give you a random json: {f.schema(Test, grammar_generators.json_generator.JsonGenerator(), capture_name='json')}")
    model = RWKV("assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
    pipeline = integrations.RWKV.PIPELINE(model, "rwkv_vocab_v20230424", f)
    snapshot.assert_match(pipeline.formatter.grammar_str)
    snapshot.assert_match(pipeline.generate("My name is Van. ", args=integrations.RWKV.PIPELINE_ARGS(top_p=0)))
    snapshot.assert_match(pipeline.formatter.captures)
