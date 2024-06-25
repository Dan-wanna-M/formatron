import decimal
import json
import typing
import rwkv.model
import rwkv.utils
from pydantic import Field

import schemas.pydantic
import grammar_generators.json_generator
from integrations.RWKV import PIPELINE
from schemas.dict_inference import infer_mapping


class IPv4Address:
    pass


new_int = typing.NewType("new_int", int)
vector = list[int]


class Test(schemas.pydantic.ClassSchema):
    a: typing.Annotated[str, Field("OK"), "114":514, Field("OK2")]
    b: int = 1
    c: typing.Literal["114'\"", "514", True, typing.Literal["1919", "810"]]
    e: tuple[typing.List[float],str, decimal.Decimal, typing.Dict, dict[str, typing.Any]]
    f: typing.Union[bool, int, typing.Any, new_int, vector]


class XiaolJSON(schemas.pydantic.ClassSchema):
    mode: str
    title: str
    queries: list[str]
    related_queries: list[str]
    concepts: list[str]
    urls: list[str]


print(grammar_generators.json_generator.generate(XiaolJSON))
print(grammar_generators.json_generator.generate(infer_mapping(json.loads("""
{
  "mode": "xx",
  "title": "xx",
  "queries": ["xx", "xx", "xx"],
  "related_queries": ["xx", "xx", "xx"],
  "concepts": ["xx", "xx", "xx"],
  "urls": ["xx", "xx", "xx"]
}
"""))))


@schemas.pydantic.callable_schema
def foo(a: int, b: typing.Annotated[int, Field(gt=10), "1124"] = 2):
    return a + b


print(foo(1))
print(foo.fields()['a'])
assert typing.get_origin(typing.List[int]) is list

model = rwkv.model.RWKV("assets/RWKV-5-World-0.4B-v2-20231113-ctx4096.pth", 'cuda fp16')
out, state = model.forward([187, 510, 1563, 310, 247], None)  # use 20B_tokenizer.json
print(out.detach().cpu().numpy())  # get logits
out, state = model.forward([187, 510], None)
out, state = model.forward([1563], state)  # RNN has state (use deepcopy if you want to clone it)
out, state = model.forward([310, 247], state)
print(out.detach().cpu().numpy())  # same result as above
pipeline = PIPELINE(model, "rwkv_vocab_v20230424", grammar_str="start ::= '一个' start|'\\n\\n';")
print(pipeline.generate("你是一个一个一个一个一个"))
print(pipeline.generate("你是一个一个一个一个一个"))