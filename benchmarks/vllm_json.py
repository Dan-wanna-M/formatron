import gc
import time
from timeit import timeit
import torch
from lmformatenforcer.integrations.vllm import build_vllm_logits_processor
from vllm import LLM, SamplingParams
from vllm.distributed import destroy_model_parallel, destroy_distributed_environment

from formatron.formatter import FormatterBuilder
from formatron.integrations.vllm import create_formatters_logits_processor, FormattersLogitsProcessor
from utils import Address
from utils import BenchResult, Context
from utils import LinkedList
from utils import Order, log
from utils import address_lfe, linked_list_lfe, order_lfe
from utils import load_address, load_linkedlist, load_orders
from outlines.integrations.vllm import JSONLogitsProcessor


def execute():
    prompts = [
        f"{system_prompt}{inputs[context.index]}{tail}",
    ]
    context.index += 1
    outputs = llm.generate(prompts, sampling_params)
    context.tokens += len(outputs[0].outputs[0].token_ids)
    # print(repr(outputs[0].outputs[0].text))
    logits_processor = sampling_params.logits_processors
    if logits_processor and isinstance(logits_processor[0], FormattersLogitsProcessor):
        # print(logits_processor[0]._formatters[0]._token_ids)
        logits_processor[0].reset()



def formatron_vllm_address():
    f = FormatterBuilder()
    f.append_str(f"{f.json(Address, capture_name='json')}")
    logits_processor = create_formatters_logits_processor(llm, [f])
    sampling_params = SamplingParams(
        temperature=1, top_p=0.5, max_tokens=100, logits_processors=[logits_processor])
    return sampling_params


def lfe_vllm_address():
    logits_processor = build_vllm_logits_processor(llm, address_lfe)
    sampling_params = SamplingParams(
        temperature=1, top_p=0.5, max_tokens=100, logits_processors=[logits_processor])
    return sampling_params


def outlines_address():
    logits_processor = JSONLogitsProcessor(Address, llm, whitespace_pattern=r"[ \t\n\r]*")
    sampling_params = SamplingParams(
        temperature=1, top_p=0.5, max_tokens=100, logits_processors=[logits_processor])
    return sampling_params


def formatron_vllm_linkedlist():
    f = FormatterBuilder()
    f.append_str(
        f"{f.json(LinkedList, capture_name='json')}")
    logits_processor = create_formatters_logits_processor(llm, [f])
    sampling_params = SamplingParams(
        temperature=1, top_p=0.5, max_tokens=100, logits_processors=[logits_processor])
    return sampling_params


def lfe_vllm_linkedlist():
    logits_processor = build_vllm_logits_processor(llm, linked_list_lfe)
    sampling_params = SamplingParams(
        temperature=1, top_p=0.5, max_tokens=100, logits_processors=[logits_processor])
    return sampling_params


def formatron_vllm_order():
    f = FormatterBuilder()
    f.append_str(f"{f.json(Order, capture_name='json')}")
    logits_processor = create_formatters_logits_processor(llm, [f])
    sampling_params = SamplingParams(
        temperature=1, top_p=0.5, max_tokens=350, logits_processors=[logits_processor])
    return sampling_params


def lfe_vllm_order():
    logits_processor = build_vllm_logits_processor(llm, order_lfe)
    sampling_params = SamplingParams(
        temperature=1, top_p=0.5, max_tokens=350, logits_processors=[logits_processor])
    return sampling_params


def outlines_order():
    logits_processor = JSONLogitsProcessor(Order, llm, whitespace_pattern=r"[ \t\n\r]*")
    sampling_params = SamplingParams(
        temperature=1, top_p=0.5, max_tokens=350, logits_processors=[logits_processor])
    return sampling_params


def warm_up(f):
    f()
    context.index = 0
    context.tokens = 0


def bench(result: BenchResult, context: Context, func, bench_name: str, f):
    context.index = 0
    context.tokens = 0
    result.s1 = (timeit(func, setup=lambda: warm_up(func), number=len(inputs)))
    result.t1 = context.tokens
    context.index = 0
    context.tokens = 0
    sampling_params.logits_processors = []
    result.s2 = (timeit(func, number=len(inputs)))
    result.t2 = context.tokens
    log(bench_name, result, f)


if __name__ == "__main__":
    data = BenchResult(0, 0, 0, 0)
    context = Context(0, 0)
    with open("vllm_json_bench.txt", "w") as f:
        system_prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

                You are a helpful AI assistant for information extraction.<|eot_id|><|start_header_id|>user<|end_header_id|>

                Extract information into json format: """
        tail = "<|eot_id|><|start_header_id|>assistant<|end_header_id|>```\n"
        llm = LLM(model="NurtureAI/Meta-Llama-3-8B-Instruct-32k",
                  max_model_len=4096)
        # --------------------------------------------------------------------------------------------------------------
        inputs = load_address()
        sampling_params = formatron_vllm_address()
        bench(data, context, execute, "formatron_llama3_8b_address", f)
        sampling_params = lfe_vllm_address()
        bench(data, context, execute, "lm_format_enforcer_llama3_8b_address", f)
        sampling_params = outlines_address()
        bench(data, context, execute, "outlines_llama3_8b_address", f)
        # --------------------------------------------------------------------------------------------------------------
        sampling_params = formatron_vllm_linkedlist()
        inputs = load_linkedlist()
        bench(data, context, execute, "formatron_llama3_8b_linkedlist", f)
        sampling_params = lfe_vllm_linkedlist()
        bench(data, context, execute, "lm_format_enforcer_llama3_8b_linkedlist", f)
        # --------------------------------------------------------------------------------------------------------------
        sampling_params = formatron_vllm_order()
        inputs = load_orders()
        bench(data, context, execute, "formatron_llama3_8b_orders", f)
        sampling_params = lfe_vllm_order()
        bench(data, context, execute, "lm_format_enforcer_llama3_8b_order", f)
        sampling_params = outlines_order()
        bench(data, context, execute, "outlines_llama3_8b_order", f)
        # --------------------------------------------------------------------------------------------------------------
        destroy_model_parallel()
        destroy_distributed_environment()
        del llm.llm_engine.model_executor
        del llm
        gc.collect()
        torch.cuda.empty_cache()
        system_prompt = """[INST]
            You are a helpful AI assistant for information extraction.

            Extract information into json format: """
        tail = "[/INST]```\n"
        llm = LLM(model="mistralai/Mistral-7B-Instruct-v0.3",
                  max_model_len=4096)
        # --------------------------------------------------------------------------------------------------------------
        inputs = load_address()
        sampling_params = formatron_vllm_address()
        bench(data, context, execute, "formatron_llama2_7b_address", f)
        sampling_params = lfe_vllm_address()
        bench(data, context, execute, "lm_format_enforcer_llama2_7b_address", f)
        sampling_params = outlines_address()
        bench(data, context, execute, "outlines_llama2_7b_address", f)
        # --------------------------------------------------------------------------------------------------------------
        sampling_params = formatron_vllm_linkedlist()
        inputs = load_linkedlist()
        bench(data, context, execute, "formatron_llama2_7b_linkedlist", f)
        sampling_params = lfe_vllm_linkedlist()
        bench(data, context, execute, "lm_format_enforcer_llama2_7b_linkedlist", f)
        # --------------------------------------------------------------------------------------------------------------
        sampling_params = formatron_vllm_order()
        inputs = load_orders()
        bench(data, context, execute, "formatron_llama2_7b_orders", f)
        sampling_params = lfe_vllm_order()
        bench(data, context, execute, "lm_format_enforcer_llama2_7b_orders", f)
        sampling_params = outlines_order()
        bench(data, context, execute, "outlines_llama2_7b_order", f)
