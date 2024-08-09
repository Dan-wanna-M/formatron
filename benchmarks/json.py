from timeit import timeit

from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache, ExLlamaV2Tokenizer
from exllamav2.generator import ExLlamaV2DynamicGenerator
from typing import Optional

from formatron.formatter import FormatterBuilder
from formatron.grammar_generators.json_generator import JsonGenerator
from formatron.integrations.exllamav2 import create_formatter_filter

from formatron.schemas.pydantic import ClassSchema


class Address(ClassSchema):
    street: str
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str


def create_exllamav2_6bpw_llama3_8b():
    model_dir = "../tests/local_assets/Llama-3-8B-exl2/"
    config = ExLlamaV2Config(model_dir)
    model = ExLlamaV2(config)
    cache = ExLlamaV2Cache(model, max_seq_len=65536, lazy=True)
    model.load_autosplit(cache, progress=True)
    tokenizer = ExLlamaV2Tokenizer(config)
    f = FormatterBuilder()
    f.append_line(f"{f.schema(Address, JsonGenerator(), capture_name='json')}")
    exllama_filter = create_formatter_filter(model, tokenizer, f)
    generator = ExLlamaV2DynamicGenerator(
        model=model,
        cache=cache,
        tokenizer=tokenizer,
    )
    return generator, exllama_filter


def test_address_exllamav2():
    prompt = f"""{system_prompt}I live in 5033 Broccoli street, Houston, Texas, the United States with postal\
 code 66004<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
    output = generator.generate(
        prompt=prompt,
        max_new_tokens=200,
        add_bos=False,
        filters=[exllama_filter]
    )


if __name__ == '__main__':
    system_prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful AI assistant for information extraction<|eot_id|><|start_header_id|>user<|end_header_id|>

Extract information into json format: """
    generator, exllama_filter = create_exllamav2_6bpw_llama3_8b()
    print(f"Test_address_exllamav2: {timeit(test_address_exllamav2, number=1000, globals=globals())/1000} seconds")
