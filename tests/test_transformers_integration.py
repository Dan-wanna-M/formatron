import torch
import transformers
from formatron.schemas.pydantic import ClassSchema
from transformers import GPT2LMHeadModel, AutoModelForCausalLM

from formatter import FormatterBuilder
from grammar_generators.json_generator import JsonGenerator
from integrations.transformers import create_formatter_logits_processor_list
from schemas.dict_inference import infer_mapping


def test_transformers_integration(snapshot):
    f = FormatterBuilder()
    f.append_line(f"Hello, Huggingface!")
    model = GPT2LMHeadModel.from_pretrained("openai-community/gpt2")
    tokenizer = transformers.AutoTokenizer.from_pretrained("openai-community/gpt2")
    model.generation_config.pad_token_id = tokenizer.eos_token_id  # Remove the annoying warning
    logits_processor = create_formatter_logits_processor_list(tokenizer, f)
    inputs = tokenizer(["I am GPT2. "], return_tensors="pt")
    snapshot.assert_match(
        tokenizer.batch_decode(model.generate(**inputs, max_new_tokens=100, logits_processor=logits_processor)))


def test_readme_example(snapshot):
    torch.manual_seed(514)
    model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct",
                                                 device_map="cuda",
                                                 torch_dtype=torch.float16)
    tokenizer = transformers.AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct")

    f = FormatterBuilder()
    digit = f.regex('([1-9][0-9]*)', capture_name='digit')
    f.append_line(f"My favorite integer is {digit}.")
    f.append_str(f"I think integer {digit} is also very interesting.")
    logits_processor = create_formatter_logits_processor_list(tokenizer, f)
    inputs = tokenizer(["""<|system|>
You are a helpful assistant.<|end|>
<|user|>Which integer is your favourite?<|end|>
<|assistant|>"""], return_tensors="pt").to("cuda")
    print(tokenizer.batch_decode(model.generate(**inputs,top_p=0.5, temperature=1,
                                              max_new_tokens=100, logits_processor=logits_processor)))
    print(logits_processor[0].formatters_captures)
    # possible output:
    # [{'digit': [<re.Match object; span=(0, 2), match='42'>, <re.Match object; span=(0, 2), match='42'>]}]

def test_readme_example2(snapshot):
    torch.manual_seed(520)
    model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct",
                                                 device_map="cuda",
                                                 torch_dtype=torch.float16)
    tokenizer = transformers.AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct")

    f = FormatterBuilder()
    schema = infer_mapping({"name":"foo", "age": 28})
    f.append_line(f"{f.str(not_contain='{')}{f.schema(schema, JsonGenerator(), capture_name='json')}")
    logits_processor = create_formatter_logits_processor_list(tokenizer, f)
    inputs = tokenizer(["""<|system|>
You are a helpful assistant.<|end|>
<|user|>I am 周明瑞. My age is 24. Extract information from this sentence into json.<|end|>
<|assistant|>"""], return_tensors="pt").to("cuda")
    print(tokenizer.batch_decode(model.generate(**inputs,top_p=0.5, temperature=1,
                                              max_new_tokens=100, logits_processor=logits_processor)))
    print(logits_processor[0].formatters_captures)
    # possible output:
    # [{'json': {'name': '周明瑞', 'age': 34}}]


def test_readme_example3(snapshot):
    class Goods(ClassSchema):
        name:str
        price:float
        remaining:int

    torch.manual_seed(520)
    model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct",
                                                 device_map="cuda",
                                                 torch_dtype=torch.float16)
    tokenizer = transformers.AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct")

    f = FormatterBuilder()
    schema = Goods
    f.append_line(f"{f.schema(schema, JsonGenerator(), capture_name='json')}")
    logits_processor = create_formatter_logits_processor_list(tokenizer, f)
    inputs = tokenizer(["""<|system|>
You are a helpful assistant.<|end|>
<|user|>We have 14 apples left with each price 14.4$. Extract information from this sentence into json.<|end|>
<|assistant|>"""], return_tensors="pt").to("cuda")
    print(tokenizer.batch_decode(model.generate(**inputs,top_p=0.5, temperature=1,
                                              max_new_tokens=100, logits_processor=logits_processor)))
    print(logits_processor[0].formatters_captures)
    # possible output:
    # [{'json': Goods(name='apples', price=14.4, remaining=14)}]


def test_transformers_batched_inference(snapshot):
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
    snapshot.assert_match(
        tokenizer.batch_decode(model.generate(**inputs, max_new_tokens=100, logits_processor=logits_processor)))
    # Special tokens are not skipped for debugging purpose. In application, you probably want to skip.


def test_transformers_text_generation_pipeline(snapshot):
    f = FormatterBuilder()
    f.append_line(f"Hello, Huggingface!")
    tokenizer = transformers.AutoTokenizer.from_pretrained("openai-community/gpt2")
    logits_processor = create_formatter_logits_processor_list(tokenizer, f)
    pipeline = transformers.TextGenerationPipeline(
        model=transformers.GPT2LMHeadModel.from_pretrained("openai-community/gpt2"),
        tokenizer=tokenizer,
        logits_processor=logits_processor)
    snapshot.assert_match(pipeline("I am GPT2. ", max_new_tokens=100)[0])
