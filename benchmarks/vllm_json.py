import json
import typing
from timeit import timeit

from formatron.grammar_generators.json_generator import JsonGenerator
from vllm import LLM, SamplingParams

from utils import Order, log
from utils import LinkedList
from utils import BenchResult, Context
from utils import Address
from formatter import FormatterBuilder
from integrations.vllm import create_formatters_logits_processor, FormattersLogitsProcessor

def execute():
    prompts = [
        f"{system_prompt}{inputs[context.index]}<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
    ]
    context.index+=1
    outputs = llm.generate(prompts, sampling_params)
    context.tokens += len(outputs[0].outputs[0].token_ids)

    l = sampling_params.logits_processors
    if l and isinstance(l[0], FormattersLogitsProcessor):
        l[0].reset()


def get_vllm_address():
    f = FormatterBuilder()
    f.append_line(f"```json\n{f.schema(Address, JsonGenerator(), capture_name='json')}```")
    logits_processor = create_formatters_logits_processor(llm, [f])
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95,max_tokens=100, logits_processors=[logits_processor])
    return sampling_params

def get_vllm_linkedlist():
    f = FormatterBuilder()
    f.append_line(f"```json\n{f.schema(LinkedList, JsonGenerator(), capture_name='json')}```")
    logits_processor = create_formatters_logits_processor(llm, [f])
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=100, logits_processors=[logits_processor])
    return sampling_params

def get_vllm_order():
    f = FormatterBuilder()
    f.append_line(f"```json\n{f.schema(Order, JsonGenerator(), capture_name='json')}```")
    logits_processor = create_formatters_logits_processor(llm, [f])
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=256, logits_processors=[logits_processor])
    return sampling_params

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
    sampling_params.logits_processors = []
    result.s2 = (timeit(func, number=len(inputs)))
    result.t2 = context.tokens
    log(bench_name, result, f)

if __name__ == "__main__":
    system_prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

    You are a helpful AI assistant for information extraction.<|eot_id|><|start_header_id|>user<|end_header_id|>

    Extract information into json format: """
    llm = LLM(model="NurtureAI/Meta-Llama-3-8B-Instruct-32k", max_model_len=4096)
    sampling_params = get_vllm_address()
    data = BenchResult(0, 0, 0, 0)
    context = Context(0, 0)
    inputs = json.load(open("address.json"))["sentences"]
    with open("vllm_json_bench.txt", "w") as f:
        bench(data, context,execute, "vllm_address", f)
        sampling_params = get_vllm_linkedlist()
        inputs = json.load(open("linkedlist.json"))["sentences"]
        bench(data, context, execute, "linkedlist", f)
        sampling_params = get_vllm_order()
        inputs = json.load(open("orders.json"))["orders"]
        bench(data, context, execute, "orders", f)