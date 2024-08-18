import gc
import json
from timeit import timeit

import torch
from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache, ExLlamaV2Tokenizer
from exllamav2.generator import ExLlamaV2DynamicGenerator, ExLlamaV2Sampler
from formatron.formatter import FormatterBuilder
from formatron.grammar_generators.json_generator import JsonGenerator
from formatron.integrations.exllamav2 import create_formatter_filter

from utils import Order
from test_grammar_gen import LinkedList
from utils import Address, BenchResult, Context, log


def create_exllamav2_6bpw_llama3_8b():
    model_dir = "../tests/local_assets/Llama-3-8B-exl2/"
    config = ExLlamaV2Config(model_dir)
    model = ExLlamaV2(config)
    cache = ExLlamaV2Cache(model, max_seq_len=65536, lazy=True)
    model.load_autosplit(cache, progress=True)
    tokenizer = ExLlamaV2Tokenizer(config)
    generator = ExLlamaV2DynamicGenerator(
        model=model,
        cache=cache,
        tokenizer=tokenizer,
    )
    return generator

def create_exllamav2_4bpw_llama2_7b():
    model_dir = "../tests/local_assets/Llama-2-7b-chat-hf-4.0-bpw-exl2/"
    config = ExLlamaV2Config(model_dir)
    model = ExLlamaV2(config)
    cache = ExLlamaV2Cache(model, max_seq_len=65536, lazy=True)
    model.load_autosplit(cache, progress=True)
    tokenizer = ExLlamaV2Tokenizer(config)
    generator = ExLlamaV2DynamicGenerator(
        model=model,
        cache=cache,
        tokenizer=tokenizer,
    )
    return generator

def get_address_filter():
    f = FormatterBuilder()
    f.append_line(f"{f.schema(Address, JsonGenerator(), capture_name='json')}")
    exllama_filter = create_formatter_filter(generator.model, generator.tokenizer, f)
    return exllama_filter

def get_linkedlist_filter():
    f = FormatterBuilder()
    f.append_line(f"{f.schema(LinkedList, JsonGenerator(), capture_name='json')}")
    exllama_filter = create_formatter_filter(generator.model, generator.tokenizer, f)
    return exllama_filter

def get_order_filter():
    f = FormatterBuilder()
    f.append_line(f"{f.schema(Order, JsonGenerator(), capture_name='json')}")
    exllama_filter = create_formatter_filter(generator.model, generator.tokenizer, f)
    return exllama_filter


def execute():
    prompt = f"""{system_prompt}{inputs[context.index]}<|eot_id|><|start_header_id|>assistant<|end_header_id|> Sure! Here is the json: """
    output = generator.generate(
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        gen_settings=settings,
        decode_special_tokens=True,
        add_bos=False,
        filters=context.filters,
        completion_only=True,
    )
    context.index += 1
    if context.filters:
        context.tokens += len(context.filters[0]._formatter._token_ids)
    else:
        assert not output.endswith(generator.tokenizer.eos_token), "Something is wrong"
        context.tokens += max_new_tokens

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
    context.filters = None
    settings.disallow_tokens(generator.tokenizer, [generator.tokenizer.eos_token_id])
    result.s2 = (timeit(func, number=len(inputs)))
    result.t2 = context.tokens
    log(bench_name, result, f)


if __name__ == '__main__':
    system_prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful AI assistant for information extraction<|eot_id|><|start_header_id|>user<|end_header_id|>

Extract information into json format: """
    data = BenchResult(0, 0, 0, 0)
    context = Context(0, 0)
    with open("exllamav2_json.txt", "w") as f:
        generator = create_exllamav2_6bpw_llama3_8b()
        settings = ExLlamaV2Sampler.Settings()
        inputs = json.load(open("address.json"))["sentences"]
        context.filters = [get_address_filter()]
        max_new_tokens = 100
        bench(data, context, execute, "llama3_8b_6pw_exl2_address_json_exllamav2", f)
        settings = ExLlamaV2Sampler.Settings()
        context.filters = [get_linkedlist_filter()]
        inputs = json.load(open("linkedlist.json"))["sentences"]
        max_new_tokens = 32
        bench(data, context, execute, "llama3_8b_6pw_exl2_linkedlist_json_exllamav2", f)
        settings = ExLlamaV2Sampler.Settings()
        context.filters = [get_order_filter()]
        inputs = json.load(open("orders.json"))["orders"]
        max_new_tokens = 160
        bench(data, context, execute, "llama3_8b_6pw_exl2_orders_json_exllamav2", f)
        del generator
        gc.collect()
        torch.cuda.empty_cache()
        generator = create_exllamav2_4bpw_llama2_7b()
        settings = ExLlamaV2Sampler.Settings()
        inputs = json.load(open("address.json"))["sentences"]
        context.filters = [get_address_filter()]
        max_new_tokens = 120
        bench(data, context, execute, "llama2_7b_4pw_exl2_address_json_exllamav2", f)
        settings = ExLlamaV2Sampler.Settings()
        context.filters = [get_linkedlist_filter()]
        inputs = json.load(open("linkedlist.json"))["sentences"]
        max_new_tokens = 15
        bench(data, context, execute, "llama2_7b_4pw_exl2_linkedlist_json_exllamav2", f)
        settings = ExLlamaV2Sampler.Settings()
        context.filters = [get_order_filter()]
        inputs = json.load(open("orders.json"))["orders"]
        max_new_tokens = 160
        bench(data, context, execute, "llama2_7b_4pw_exl2_orders_json_exllamav2", f)