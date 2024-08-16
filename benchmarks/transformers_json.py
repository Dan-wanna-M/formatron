import json
from timeit import timeit

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from utils import Order
from grammar_generators.json_generator import JsonGenerator
from integrations.transformers import create_formatter_logits_processor_list, FormattersLogitsProcessor
from test_grammar_gen import LinkedList
from utils import BenchResult, Context, Address, log
from formatron.formatter import FormatterBuilder


def get_llama3_8b_tokenizer_and_model():
    model = AutoModelForCausalLM.from_pretrained("NurtureAI/Meta-Llama-3-8B-Instruct-32k",
                                                 device_map="cuda",
                                                 torch_dtype=torch.bfloat16,
                                                 attn_implementation="flash_attention_2")
    tokenizer = AutoTokenizer.from_pretrained("NurtureAI/Meta-Llama-3-8B-Instruct-32k")
    model.generation_config.pad_token_id = tokenizer.eos_token_id
    return model, tokenizer

def get_address_schema():
    f = FormatterBuilder()
    f.append_line(f"{f.schema(Address, JsonGenerator(), capture_name='json')}")
    return create_formatter_logits_processor_list(tokenizer, f)

def get_linkedlist_schema():
    f = FormatterBuilder()
    f.append_line(f"{f.schema(LinkedList, JsonGenerator(), capture_name='json')}")
    return create_formatter_logits_processor_list(tokenizer, f)

def get_order_schema():
    f = FormatterBuilder()
    f.append_line(f"{f.schema(Order, JsonGenerator(), capture_name='json')}")
    return create_formatter_logits_processor_list(tokenizer, f)

def execute():
    prompts = [
        f"{system_prompt}{inputs[context.index]}<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
    ]
    prompts = tokenizer(prompts, return_tensors='pt').to(model.device)
    input_len = prompts.input_ids.shape[-1]
    context.index+=1
    outputs = model.generate(**prompts, logits_processor=logits_processor,
                             max_new_tokens=max_new_tokens)
    context.tokens += outputs.shape[-1]-input_len
    l = logits_processor
    if l and isinstance(l[0], FormattersLogitsProcessor):
        l[0].reset()

def warm_up(f):
    f()
    context.index = 0
    context.tokens = 0

def bench(result:BenchResult, context:Context,func, bench_name:str, f):
    context.index = 0
    context.tokens = 0
    result.s1 = (timeit(func, setup=lambda: warm_up(func), number=len(inputs)))
    result.t1 = context.tokens
    context.index = 0
    context.tokens = 0
    logits_processor.clear()
    result.s2 = (timeit(func, number=len(inputs)))
    result.t2 = context.tokens
    log(bench_name, result, f)

if __name__ == "__main__":
    system_prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

    You are a helpful AI assistant for information extraction.<|eot_id|><|start_header_id|>user<|end_header_id|>

    Extract information into json format: """


    data = BenchResult(0, 0, 0, 0)
    context = Context(0, 0)
    with open("transformers_json.txt", "w") as f:
        model, tokenizer = get_llama3_8b_tokenizer_and_model()
        with torch.no_grad():
            model.eval()
            max_new_tokens = 50
            inputs = json.load(open("address.json"))["sentences"]
            logits_processor = get_address_schema()
            bench(data,context,execute, "address_json", f)
            inputs = json.load(open("linkedlist.json"))["sentences"]
            logits_processor = get_linkedlist_schema()
            max_new_tokens = 200
            bench(data,context,execute, "linkedlist_json", f)
            inputs = json.load(open("orders.json"))["orders"]
            logits_processor = get_order_schema()
            bench(data, context, execute, "order_json", f)