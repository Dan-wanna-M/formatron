import gc
import json
from timeit import timeit

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from benchmarks.utils import load_address, load_linkedlist, load_orders, address_lfe, linked_list_lfe, order_lfe
from utils import Order
from grammar_generators.json_generator import JsonGenerator
from integrations.transformers import create_formatter_logits_processor_list, FormattersLogitsProcessor
from test_grammar_gen import LinkedList
from utils import BenchResult, Context, Address, log
from formatron.formatter import FormatterBuilder
from lmformatenforcer.integrations.transformers import build_transformers_prefix_allowed_tokens_fn

def get_llama3_8b_tokenizer_and_model():
    model = AutoModelForCausalLM.from_pretrained("NurtureAI/Meta-Llama-3-8B-Instruct-32k",
                                                 device_map="cuda",
                                                 torch_dtype=torch.bfloat16,
                                                 attn_implementation="flash_attention_2")
    tokenizer = AutoTokenizer.from_pretrained("NurtureAI/Meta-Llama-3-8B-Instruct-32k")
    model.generation_config.pad_token_id = tokenizer.eos_token_id
    return model, tokenizer

def get_llama2_7b_tokenizer_and_model():
    model = AutoModelForCausalLM.from_pretrained("togethercomputer/LLaMA-2-7B-32K",
                                                 device_map="cuda",
                                                 torch_dtype=torch.float16,
                                                 attn_implementation="flash_attention_2")
    tokenizer = AutoTokenizer.from_pretrained("togethercomputer/LLaMA-2-7B-32K")
    model.generation_config.pad_token_id = tokenizer.eos_token_id
    return model, tokenizer

def get_address_schema():
    f = FormatterBuilder()
    f.append_line(f"{f.schema(Address, JsonGenerator(), capture_name='json')}")
    return create_formatter_logits_processor_list(tokenizer, f)

def lfe_address_prefix():
    return build_transformers_prefix_allowed_tokens_fn(tokenizer, address_lfe)

def get_linkedlist_schema():
    f = FormatterBuilder()
    f.append_line(f"{f.schema(LinkedList, JsonGenerator(), capture_name='json')}")
    return create_formatter_logits_processor_list(tokenizer, f)

def lfe_linkedlist_prefix():
    return build_transformers_prefix_allowed_tokens_fn(tokenizer, linked_list_lfe)

def get_order_schema():
    f = FormatterBuilder()
    f.append_line(f"{f.schema(Order, JsonGenerator(), capture_name='json')}")
    return create_formatter_logits_processor_list(tokenizer, f)

def lfe_order_prefix():
    return build_transformers_prefix_allowed_tokens_fn(tokenizer, order_lfe)

def execute():
    prompts = [
        f"{system_prompt}{inputs[context.index]}{tail}",
    ]
    prompts = tokenizer(prompts, return_tensors='pt').to(model.device)
    input_len = prompts.input_ids.shape[-1]
    context.index+=1
    if logits_processor is not None:
        outputs = model.generate(**prompts, logits_processor=logits_processor,
                                 max_new_tokens=max_new_tokens)
    else:
        outputs = model.generate(**prompts, prefix_allowed_tokens_fn=prefix_fn,
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
    if logits_processor is not None:
        logits_processor.clear()
    else:
        global prefix_fn
        prefix_fn = None
    result.s2 = (timeit(func, number=len(inputs)))
    result.t2 = context.tokens
    log(bench_name, result, f)

if __name__ == "__main__":
    data = BenchResult(0, 0, 0, 0)
    context = Context(0, 0)
    with open("transformers_json.txt", "w") as f:
        with torch.no_grad():
            system_prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

            You are a helpful AI assistant for information extraction.<|eot_id|><|start_header_id|>user<|end_header_id|>

            Extract information into json format: """
            tail = "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
            model, tokenizer = get_llama3_8b_tokenizer_and_model()
            model.eval()
            max_new_tokens = 50
            inputs = load_address()
            prefix_fn = None
            logits_processor = get_address_schema()
            bench(data,context,execute, "formatron_llama3_8b_address_json", f)
            logits_processor = None
            prefix_fn = lfe_address_prefix()
            bench(data, context, execute, "lm_format_enforcer_llama3_8b_address_json", f)
            inputs = load_linkedlist()
            logits_processor = get_linkedlist_schema()
            max_new_tokens = 200
            bench(data,context,execute, "formatron_llama3_8b_linkedlist_json", f)
            logits_processor = None
            prefix_fn = lfe_linkedlist_prefix()
            bench(data, context, execute, "lm_format_enforcer_llama3_8b_linkedlist_json", f)
            inputs = load_orders()
            logits_processor = get_order_schema()
            bench(data, context, execute, "formatron_llama3_8b_order_json", f)
            logits_processor = None
            prefix_fn = lfe_order_prefix()
            bench(data, context, execute, "lm_format_enforcer_llama3_8b_order_json", f)
            system_prompt = """[INST]
                        You are a helpful AI assistant for information extraction.

                        Extract information into json format: """
            tail = "[/INST]"
            del model
            del tokenizer
            gc.collect()
            torch.cuda.empty_cache()
            model, tokenizer = get_llama2_7b_tokenizer_and_model()
            model.eval()
            max_new_tokens = 50
            inputs = load_address()
            logits_processor = get_address_schema()
            bench(data, context, execute, "formatron_llama2_7b_address_json", f)
            logits_processor = None
            prefix_fn = lfe_address_prefix()
            bench(data, context, execute, "lm_format_enforcer_llama2_7b_address_json", f)
            max_new_tokens = 30
            inputs = load_linkedlist()
            logits_processor = get_linkedlist_schema()
            max_new_tokens = 200
            bench(data, context, execute, "formatron_llama2_7b_linkedlist_json", f)
            logits_processor = None
            prefix_fn = lfe_linkedlist_prefix()
            bench(data, context, execute, "lm_format_enforcer_llama2_7b_linkedlist_json", f)
            inputs = load_orders()
            logits_processor = get_order_schema()
            bench(data, context, execute, "formatron_llama2_7b_order_json", f)
            logits_processor = None
            prefix_fn = lfe_order_prefix()
            bench(data, context, execute, "lm_format_enforcer_llama2_7b_order_json", f)