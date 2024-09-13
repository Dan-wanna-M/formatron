<p align='center'>
<image src="logo.svg">
</p>

[![PyPI](https://img.shields.io/pypi/v/formatron.svg)](https://pypi.python.org/pypi/formatron)

Formatron allows users to control the output format of language models
with minimal overhead. It is lightweight, user-friendly,
and seamlessly integrates into existing codebases and frameworks.

## Installation

`pip install formatron`

## Features

- **🔗 Popular Library Integrations**: Supports transformers, exllamav2, vllm and RWKV.
- **🔌 Plugins, not wrappers**:
Instead of wrapping third-party libraries in large, cumbersome classes,
Formatron offers convenient, clean plugins for different libraries.
- **💡 Library, not framework**:
Instead of unifying everything into a bulky framework,
Formatron is a flexible library that can be embedded anywhere.
- **✍️ Fluent Formatting**: Describe your format as easily as writing natural language.
- **📜 Regex and CFG Support**:
Effortlessly interleave regular expressions and context-free grammars (CFG) in formats.
- **⚙️ Efficient JSON Generation**: Feature-complete JSON generation based on Pydantic models or json schemas.
- **📤 Batched Inference**:
Freely specify different formats for each sequence in one batch!
- **🚀 Minimal Runtime Overhead**:
With Leo optimization, a specialized compacting algorithm,
and CFG caches across generations, Earley algorithm implemented in Rust is
aymptotically and practically the fastest algorithm.
- **🔧 Customizable**: Everything is configurable, including schema generation,
grammar generation, and post-generation processing (such as function calls).

## Comparison to other libraries

| Capability                                   | Formatron                          | [LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer)                           | [Guidance](https://github.com/guidance-ai/guidance) | [Outlines](https://github.com/outlines-dev/outlines)                                    | [LMQL](https://github.com/eth-sri/lmql)                                                         |
|:---------------------------------------------|------------------------------------|:----------------------------------------------------------------------------------------------|:----------------------------------------------------|:----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| Regular Expressions                          | ✅                                  | ✅                                                                                             | ✅                                                   | ✅                                                                                       | 🟡([preview feature](https://lmql.ai/docs/language/constraints.html#regex-constraints-preview)) |
| Efficient Regex-constrained Generation       | ✅                                  | 🟡([performance issues still exist](https://github.com/noamgat/lm-format-enforcer/issues/36)) | ❌                                                   | 🟡([scalablity currently suffers](https://github.com/outlines-dev/outlines/issues/680)) | ❌                                                                                               |
| Context Free Grammars(CFG)                   | ✅                                  | ❌                                                                                             | ✅                                                   | 🟡([some bugs exist](https://github.com/outlines-dev/outlines/issues/959))              | ❌                                                                                               |
| Efficient CFG-constrained Generation         | ✅                                  | ❌                                                                                             | ❌                                                   | ❌                                                                                       | ❌                                                                                               |
| Custom Format Extractor                      | 🟡([some limitations exist](#ast)) | ❌                                                                                             | ✅                                                   | ✅                                                                                       | ✅                                                                                               |
| JSON Schema                                  | ✅([indirectly](#json-schema))      | ✅                                                                                             | ✅                                                   | ✅                                                                                       | ❌                                                                                               |
| Function Call From Callable                  | ✅                                  | ❌                                                                                             | ✅                                                   | ✅                                                                                       | ✅                                                                                               |
| Interleave Python control flow in generation | ❌                                  | ❌                                                                                             | ✅                                                   | ❌                                                                                       | ✅                                                                                               |
| Batched Generation                           | ✅                                  | ✅                                                                                             | ❌                                                   | ✅                                                                                       | ❌                                                                                               |
| Beam Search                                  | ❌                                  | ✅                                                                                             | ❌                                                   | ✅                                                                                       | ✅                                                                                               |
| Integrates into existing pipelines           | ✅                                  | ✅                                                                                             | ❌                                                   | 🟡([some integrations crash](https://github.com/outlines-dev/outlines/issues/1115))     | ❌                                                                                               |
| Optional JSON Fields                         | ✅                                  | ✅                                                                                             | ❌                                                   | ❌                                                                                       | ❌                                                                                               |
| LLM Controls JSON field whitespaces          | ✅                                  | ✅                                                                                             | ❌                                                   | ✅                                                                                       | ❌                                                                                               |
| LLM Controls JSON field orderings            | ❌                                  | ✅                                                                                             | ❌                                                   | ❌                                                                                       | ❌                                                                                               |
| JSON Schema with recursive classes           | ✅                                  | ✅                                                                                             | ❌                                                   | ❌                                                                                       | ❌                                                                                               |

Feel free to open up an [issue](https://github.com/Dan-wanna-M/formatron/issues) if something is missing or incorrect!

## Examples

### Regex-constrained Generation

```python
import torch
from formatron.integrations.transformers import create_formatter_logits_processor_list
from formatron.formatter import FormatterBuilder
from transformers import AutoModelForCausalLM
import transformers
torch.manual_seed(514)
model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct",
                                                device_map="cuda",
                                                torch_dtype=torch.float16)
tokenizer = transformers.AutoTokenizer.from_pretrained(
    "microsoft/Phi-3-mini-128k-instruct")

f = FormatterBuilder()
digit = f.regex('([1-9][0-9]*)', capture_name='digit')
f.append_line(f"My favorite integer is {digit}.")
f.append_str(f"I think integer {digit} is also very interesting.")
logits_processor = create_formatter_logits_processor_list(tokenizer, f)
inputs = tokenizer(["""<|system|>
You are a helpful assistant.<|end|>
<|user|>Which integer is your favourite?<|end|>
<|assistant|>"""], return_tensors="pt").to("cuda")
print(tokenizer.batch_decode(model.generate(**inputs, top_p=0.5, temperature=1,
                                            max_new_tokens=100, logits_processor=logits_processor)))
print(logits_processor[0].formatters_captures)
# possible output:
# [{'digit': [<re.Match object; span=(0, 2), match='42'>, <re.Match object; span=(0, 2), match='42'>]}]
```

Note that only
[Rust regex's syntax](https://docs.rs/regex/latest/regex/#syntax) is supported, which notably
does not include arbitrary lookaheads.

### Json Generation

#### Pydantic Model

```python
import torch
from formatron.integrations.transformers import create_formatter_logits_processor_list
from formatron.formatter import FormatterBuilder
from transformers import AutoModelForCausalLM
import transformers
from formatron.schemas.dict_inference import infer_mapping
torch.manual_seed(520)
model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct",
                                                device_map="cuda",
                                                torch_dtype=torch.float16)
tokenizer = transformers.AutoTokenizer.from_pretrained(
    "microsoft/Phi-3-mini-128k-instruct")

f = FormatterBuilder()
schema = infer_mapping({"name": "foo", "age": 28})
f.append_line(f"{f.json(schema, capture_name='json')}")
logits_processor = create_formatter_logits_processor_list(tokenizer, f)
inputs = tokenizer(["""<|system|>
You are a helpful assistant.<|end|>
<|user|>I am 周明瑞. My age is 24. Extract information from this sentence into json.<|end|>
<|assistant|>"""], return_tensors="pt").to("cuda")
print(tokenizer.batch_decode(model.generate(**inputs, top_p=0.5, temperature=1,
                                            max_new_tokens=100, logits_processor=logits_processor)))
print(logits_processor[0].formatters_captures)
# possible output:
# [{'json': {'name': '周明瑞', 'age': 34}}]
```

#### Json Example

```python
from formatron.schemas.pydantic import ClassSchema
from formatron.integrations.transformers import create_formatter_logits_processor_list
from formatron.formatter import FormatterBuilder
from transformers import AutoModelForCausalLM
import transformers
import torch

class Goods(ClassSchema):
    name: str
    price: float
    remaining: int

torch.manual_seed(520)
model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct",
                                                device_map="cuda",
                                                torch_dtype=torch.float16)
tokenizer = transformers.AutoTokenizer.from_pretrained(
    "microsoft/Phi-3-mini-128k-instruct")

f = FormatterBuilder()
schema = Goods
f.append_line(f"{f.json(schema, capture_name='json')}")
logits_processor = create_formatter_logits_processor_list(tokenizer, f)
inputs = tokenizer(["""<|system|>
You are a helpful assistant.<|end|>
<|user|>We have 14 apples left with each price 14.4$. Extract information from this sentence into json.<|end|>
<|assistant|>"""], return_tensors="pt").to("cuda")
print(tokenizer.batch_decode(model.generate(**inputs, top_p=0.5, temperature=1,
                                            max_new_tokens=100, logits_processor=logits_processor)))
print(logits_processor[0].formatters_captures)
# possible output:
# [{'json': Goods(name='apples', price=14.4, remaining=14)}]
```

### Batched Inference

```python
import transformers
from transformers import GPT2LMHeadModel

from formatron.formatter import FormatterBuilder
from formatron.integrations.transformers import create_formatter_logits_processor_list
f = FormatterBuilder()
f.append_line(f"Hello, Huggingface!")
f3 = FormatterBuilder()
f3.append_line("Hello, Huggingface! Hello, Huggingface!")
model = GPT2LMHeadModel.from_pretrained("openai-community/gpt2")
tokenizer = transformers.AutoTokenizer.from_pretrained("openai-community/gpt2",
                                                       padding_side='left')
tokenizer.pad_token = tokenizer.eos_token  # Needed for padding
model.generation_config.pad_token_id = tokenizer.pad_token_id
logits_processor = create_formatter_logits_processor_list(tokenizer, [f, f, f3])
inputs = tokenizer(["I am GPT2. ", "I am another GPT2. ", "I am yet another GPT2. "], return_tensors="pt",
                   padding=True)
print(tokenizer.batch_decode(model.generate(**inputs,
                                            max_new_tokens=100,
                                            logits_processor=logits_processor),
                             skip_special_tokens=True))
```

### Function Calls

```python
import torch
from formatron import schemas
from formatron.formatter import FormatterBuilder
from transformers import AutoModelForCausalLM
import transformers
from formatron.integrations.transformers import create_formatter_logits_processor_list

@schemas.pydantic.callable_schema
def add(a: int, b: int, /, *, c: int):
    return a + b + c

model = AutoModelForCausalLM.from_pretrained("NurtureAI/Meta-Llama-3-8B-Instruct-32k",
                                                device_map="cuda",
                                                torch_dtype=torch.float16)
tokenizer = transformers.AutoTokenizer.from_pretrained(
    "NurtureAI/Meta-Llama-3-8B-Instruct-32k")
inputs = tokenizer(["""<|system|>
You are a helpful assistant.<|end|>
<|user|>a is 1, b is 6 and c is 7. Generate a json containing them.<|end|>
<|assistant|>"""], return_tensors="pt").to("cuda")
f = FormatterBuilder()
f.append_line(f"{f.json(add, capture_name='json')}")
logits_processor = create_formatter_logits_processor_list(tokenizer, f)
print(tokenizer.batch_decode(model.generate(**inputs, top_p=0.5, temperature=1,
                                            max_new_tokens=100, logits_processor=logits_processor)))
print(logits_processor[0].formatters_captures)
# possible output:
# [{'json': 14}]
```

### CFG-Constrained generation

Context free grammars use [kbnf's syntax](https://docs.rs/kbnf/latest/kbnf/#kbnf-grammar) which is a variant of EBNF.
Since formatron uses [kbnf](https://github.com/Dan-wanna-M/kbnf?tab=readme-ov-file#features) under the hood, all kbnf's claims on performance hold.

```python
import torch
from formatron.formatter import FormatterBuilder
from transformers import AutoModelForCausalLM
import transformers
from formatron.integrations.transformers import create_formatter_logits_processor_list
from formatron.extractor import NonterminalExtractor
import typing

class ArithmeticExpressionExtractor(NonterminalExtractor):
    def __init__(self, nonterminal: str, capture_name: typing.Optional[str] = None):
        super().__init__(nonterminal, capture_name)

    def extract(self, input_str: str) -> typing.Optional[tuple[str, typing.Any]]:
        i = 0
        left_bracket = 0
        while i < len(input_str):
            if input_str[i].isdigit() or input_str[i] in "+-*/.":
                i += 1
                continue
            if input_str[i] == "(":
                i += 1
                left_bracket += 1
                continue
            if input_str[i] == ")":
                i += 1
                left_bracket -= 1
                continue
            else:
                break
        if left_bracket != 0:
            return None
        return input_str[i:], input_str[:i]

    @property
    def kbnf_definition(self) -> str:
        return  """
expression ::=  term { ("+" | "-") term };
term       ::= factor { ("*" | "/") factor };
factor     ::= number | "(" expression ")";
number     ::= #"[0-9]+(\\\\.[0-9]+)?";
""".replace("expression", self.nonterminal)

model = AutoModelForCausalLM.from_pretrained("NurtureAI/Meta-Llama-3-8B-Instruct-32k",
                                                device_map="cuda",
                                                torch_dtype=torch.float16)
tokenizer = transformers.AutoTokenizer.from_pretrained(
    "NurtureAI/Meta-Llama-3-8B-Instruct-32k")
inputs = tokenizer(["""<|system|>
    You are a helpful assistant.<|end|>
    <|user|>Repeat it: ((32+43)*114)<|end|>
    <|assistant|>((32+43)*114)<|end|>
    <|user|>Repeat it: ((32+43)*(114-514))<|end|>
    <|assistant|>"""], return_tensors="pt").to("cuda")
f = FormatterBuilder()
f.append_line(
    f"{f.extractor(lambda nonterminal: ArithmeticExpressionExtractor(nonterminal, 'json'))}")
logits_processor = create_formatter_logits_processor_list(tokenizer, f)
print(tokenizer.batch_decode(model.generate(**inputs, top_p=0.5, temperature=1,
                                            max_new_tokens=100, logits_processor=logits_processor)))
print(logits_processor[0].formatters_captures)
# possible output: [{'json': '(((32+43)*(114-514)))*1.5'}]
```

### Json Schema

Starting from `0.4.0`, Formatron supports some basic json schemas natively.

```python
from formatron.schemas import json_schema
from formatron.integrations.transformers import create_formatter_logits_processor_list
from formatron.formatter import FormatterBuilder
from transformers import AutoModelForCausalLM
import transformers
import torch

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
torch.manual_seed(520)
model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct",
                                                device_map="cuda",
                                                torch_dtype=torch.float16)
tokenizer = transformers.AutoTokenizer.from_pretrained(
    "microsoft/Phi-3-mini-128k-instruct")

f = FormatterBuilder()
f.append_line(f"{f.json(schema, capture_name='json')}")
logits_processor = create_formatter_logits_processor_list(tokenizer, f)
inputs = tokenizer(["""<|system|>
You are a helpful assistant.<|end|>
<|user|>Extract information from this sentence into json: my name is Genov and I am 28 years old.<|end|>
<|assistant|>```"""], return_tensors="pt").to("cuda")
print(tokenizer.batch_decode(model.generate(**inputs, top_p=0.5, temperature=1,
                                            max_new_tokens=100, logits_processor=logits_processor)))
print(logits_processor[0].formatters_captures)
# possible output:
# [{'json': {'name': 'Genov', 'age': 28}}]
```

### Integrations

Check out integration examples in the [tests](https://github.com/Dan-wanna-M/formatron/tree/master/tests) directory.
You may also want to check the minimum compatible version in [pyproject.toml](https://github.com/Dan-wanna-M/formatron/blob/master/pyproject.toml).

## API Reference

Check out the API reference [here](https://dan-wanna-m.github.io/formatron/).

## Benchmark

Check out the benchmark [here](benchmarks/readme.md).

## What Formatron Won't Do

### Implement an End-to-End Inference Pipeline

Every library related to large language models(LLM) must consider that LLMs
are rapidly evolving. Many libraries, such as Guidance, Outlines, and LMQL,
address this by offering their own end-to-end inference pipelines,
which are constantly updated to incorporate the latest techniques.

Formatron, however, takes a different approach.
Rather than providing a full-fledged inference pipeline,
Formatron focuses on being modular and easily embeddable into existing
and future pipelines.
While this may require users to write a bit more code initially,
it makes maintaining and updating the pipeline painless in the long run.

## What Formatron Can't Do Now

### Support OpenAI or in general API-based LLM solutions

They don't support efficient logits masking per token, nullifying most benefits
of constrained decoding.

### Semantic Validation

Although constrained decoding can enforce certain formats
in generated text, they cannot guarantee that the output aligns
with the users' intention. In other words, if the model is inadequate
or the prompt is poorly written, it's possible to generate well-formatted
but meaningless output.

### Context-Sensitive Validation

Unfortunately, many formats require context-sensitive validation.
For example, two keys in a JSON object must not be equal to each other.
Unlike CFGs, there is no efficient, generic algorithm to validate
such constraints. However, for a specific format, it is possible to validate
them efficiently with a specialized algorithm. In a future release,
Formatron will support context-sensitive validation for popular formats like JSON.

### Abstract Syntax Tree (AST) Construction<a id='ast'></a>

Formatron uses an Earley recognizer rather than a parser under the hood.
This approach allows for more efficient generation and validation
but also means that the AST of a given format is not available.
In most cases, this is not a problem,
as it is usually possible to extract the format from the generated string
using simple algorithms and then parse it with an existing parser.
However, in some cases, obtaining the AST might be necessary.
In a future release, Formatron will support AST construction.

### Process batch logits in parallel

While it is *technically possible* to process batch logits in parallel CPU threads
since Formatron uses Rust internally, most frameworks sequentially
call Formatron's plugin for each logits in a batch. Altering
this behaviour requires a breaking change to the frameworks' API or letting
Formatron take over the control flow. Both options imply
substantial work.
