import decimal
import json
import os
import sys
import typing

import rwkv
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
    a: typing.Annotated[str, Field("OK"), "114":514, Field("OK2")]
    b: int = 1
    c: typing.Literal["114'\"", "514", True, typing.Literal["1919", "810"]]
    e: tuple[typing.List[float], str, decimal.Decimal, typing.Dict, dict[str, typing.Any]]
    f: typing.Union[bool, int, typing.Any, new_int, vector]


def test_formatter(snapshot):
    f = FormatterBuilder()
    f.append_line(f"This is a number: {f.regex('[0-9]+')}")
    f.append_str(f"This is a json: "
                 f"{f.schema(Test, grammar_generators.json_generator.JsonGenerator(), capture_name='json')}\n")
    f.append_multiline_str(f"""Multiple indentations
                                are handled
                                    correctly. This is a random sentence: {f.str(stop=".")}""")
    rwkv_world_series_vocab_name = "rwkv_vocab_v20230424"
    tokenizer = TRIE_TOKENIZER("assets/rwkv_vocab_v20230424.txt")
    vocabulary = integrations.RWKV.create_engine_vocabulary(rwkv_world_series_vocab_name, tokenizer)
    snapshot.assert_match(f.build(vocabulary, lambda tokens: tokenizer.decode(tokens)).grammar_str)
