from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache, ExLlamaV2Tokenizer
from exllamav2.generator import ExLlamaV2DynamicGenerator, ExLlamaV2Sampler
from formatron.formatter import FormatterBuilder
from formatron.integrations.exllamav2 import create_formatter_filter
from formatron.schemas.pydantic import ClassSchema
from typing import Optional, List, Union, Literal
from typing import Dict, Type

model_dir = "local_assets/Mistral-7B-instruct-v0.3-exl2"
config = ExLlamaV2Config(model_dir)
model = ExLlamaV2(config)
cache = ExLlamaV2Cache(model, max_seq_len=4096, lazy=True)
model.load_autosplit(cache, progress=True)
tokenizer = ExLlamaV2Tokenizer(config)

generator = ExLlamaV2DynamicGenerator(
    model=model,
    cache=cache,
    tokenizer=tokenizer,
)

class Address(ClassSchema):
    street: str
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str
    

class Weather(ClassSchema):
    temperature: int


class ToolCalling(ClassSchema):
    """ The format to call one or multiple tools """
    functions_calling: List[Union[Address, Weather]] = []


def f_get_filter():
    f = FormatterBuilder()
    spaces = f.regex(r'\s*')
    f.append_line(f"{spaces}{f.json(ToolCalling, capture_name='json')}{spaces}")
    exllama_filter = create_formatter_filter(
        generator.model, generator.tokenizer, f)
    return exllama_filter

output = generator.generate(
    prompt="What is Wall Street's address?\n",
    max_new_tokens=200,
    add_bos=True,
    filters=[f_get_filter()],
)

print(output)
print(repr(output))