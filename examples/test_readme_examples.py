def test_readme_example():
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


def test_readme_example2():
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


def test_readme_example3():
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


def test_readme_example4():
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


def test_readme_example5():
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

def test_readme_example6():
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

def test_readme_example7():
    from formatron.integrations.transformers import create_formatter_logits_processor_list
    from formatron.formatter import FormatterBuilder
    from transformers import AutoModelForCausalLM
    import transformers
    import torch

    torch.manual_seed(520)
    model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct",
                                                 device_map="cuda",
                                                 torch_dtype=torch.float16)
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        "microsoft/Phi-3-mini-128k-instruct")

    f = FormatterBuilder()
    f.append_line(f"{f.substr('The quick brown fox jumps over the lazy dog.', capture_name='animal')}")
    logits_processor = create_formatter_logits_processor_list(tokenizer, f)
    inputs = tokenizer(["""<|system|>
You are a helpful assistant.<|end|>
<|user|>What animal is mentioned in the phrase "The quick brown fox jumps over the lazy dog"?<|end|>
<|assistant|>The animal mentioned in the phrase is the """], return_tensors="pt").to("cuda")
    output = tokenizer.batch_decode(model.generate(**inputs, top_p=0.5, temperature=1,
                                                   max_new_tokens=100, logits_processor=logits_processor))
    print(output)
    print(logits_processor[0].formatters_captures)
    # possible output:
    # [{'animal': 'fox'}]

def test_readme_example8():
    from formatron.schemas.pydantic import ClassSchema
    from formatron.integrations.transformers import create_formatter_logits_processor_list
    from formatron.schemas.schema import SubstringOf
    from formatron.formatter import FormatterBuilder
    from transformers import AutoModelForCausalLM
    import transformers
    import torch
    import typing
    from pydantic import Field

    class Person(ClassSchema):
        name: typing.Annotated[str, Field(..., substring_of="Alice Bob Charlie David Eve"), SubstringOf("Alice Bob Charlie David Eve")]
        age: int

    torch.manual_seed(520)
    model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct",
                                                 device_map="cuda",
                                                 torch_dtype=torch.float16)
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        "microsoft/Phi-3-mini-128k-instruct")

    f = FormatterBuilder()
    f.append_line(f"{f.json(Person, capture_name='json')}")
    logits_processor = create_formatter_logits_processor_list(tokenizer, f)
    inputs = tokenizer(["""<|system|>
You are a helpful assistant.<|end|>
<|user|>Extract information from this sentence into json: Bob is 32 years old.<|end|>
<|assistant|>```"""], return_tensors="pt").to("cuda")
    print(tokenizer.batch_decode(model.generate(**inputs, top_p=0.5, temperature=1,
                                                max_new_tokens=100, logits_processor=logits_processor)))
    print(logits_processor[0].formatters_captures)
    # possible output:
    # [{'json': {'name': 'Bob', 'age': 32}}]

def test_readme_example9():
    from formatron.schemas import json_schema
    from formatron.integrations.transformers import create_formatter_logits_processor_list
    from formatron.formatter import FormatterBuilder
    from transformers import AutoModelForCausalLM
    import transformers
    import torch

    schema = {
        "$id": "https://example.com/animal.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "animal": {
                "type": "string",
                "substring_of": "The quick brown fox jumps over the lazy dog."
            }
        },
        "required": ["animal"]
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
<|user|>What animal is mentioned in the phrase "The quick brown fox jumps over the lazy dog"?<|end|>
<|assistant|>The animal mentioned in the phrase is the """], return_tensors="pt").to("cuda")
    output = tokenizer.batch_decode(model.generate(**inputs, top_p=0.5, temperature=1,
                                                   max_new_tokens=100, logits_processor=logits_processor))
    print(output)
    print(logits_processor[0].formatters_captures)
    # possible output:
    # [{'json': {'animal': 'fox'}}]


test_readme_example()
test_readme_example2()
test_readme_example3()
test_readme_example4()
test_readme_example5()
test_readme_example6()
test_readme_example7()
test_readme_example8()
test_readme_example9()
