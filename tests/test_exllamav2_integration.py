from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache, ExLlamaV2Tokenizer
from exllamav2.generator import ExLlamaV2DynamicGenerator
import formatron.schemas.json_schema
from formatron.formatter import FormatterBuilder
from formatron.integrations.exllamav2 import create_formatter_filter
from exllamav2.generator import ExLlamaV2Sampler
import kbnf
import torch
import gc
from formatron.integrations.exllamav2 import create_engine_vocabulary, FormatterFilter

def test_exllamav2_integration(snapshot):
    model_dir = "local_assets/Meta-Llama-3-8B-Instruct-32k/"
    config = ExLlamaV2Config(model_dir)
    model = ExLlamaV2(config)
    cache = ExLlamaV2Cache(model, max_seq_len=4096, lazy=True)
    model.load_autosplit(cache, progress=True)
    tokenizer = ExLlamaV2Tokenizer(config)
    f = FormatterBuilder()
    f.append_line("Hello, Exllamav2!")
    exllama_filter = create_formatter_filter(model, tokenizer, f)
    generator = ExLlamaV2DynamicGenerator(
        model=model,
        cache=cache,
        tokenizer=tokenizer,
    )
    output = generator.generate(
        prompt="Hello, cats! ",
        max_new_tokens=200,
        add_bos=True,
        filters=[exllama_filter]
    )
    snapshot.assert_match(output)
    del model
    del generator
    del cache
    del exllama_filter
    torch.cuda.empty_cache()
    gc.collect()

def test_exllamav2_json_schema(snapshot):
    model_dir = "local_assets/Meta-Llama-3-8B-Instruct-32k/"
    config = ExLlamaV2Config(model_dir)
    model = ExLlamaV2(config)
    cache = ExLlamaV2Cache(model, max_seq_len=4096, lazy=True)
    model.load_autosplit(cache, progress=True)
    tokenizer = ExLlamaV2Tokenizer(config)
    f = FormatterBuilder()
    json_schema = {
        "$id": "https://example.com/person",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "emotion": {
                "type": "string",
                "enum": ["happy", "sad", "angry", "disgusted", "amused"]
            }
        },
        "required": [
            "emotion"
        ]
    }
    schema = formatron.schemas.json_schema.create_schema(json_schema)
    f.append_line(f"{f.json(schema, capture_name='json')}")
    vocab = create_engine_vocabulary(tokenizer, None)
    config = kbnf.Config()
    config.regex_config.min_tokens_required_for_eager_regex_cache = None
    f = f.build(vocab, lambda tokens: tokenizer.decode(torch.tensor(tokens)), config)
    exllama_filter = FormatterFilter(model, tokenizer, f)
    tokens = tokenizer.encode('{"emotion":"angry",}').squeeze()
    for token in tokens:
        print(token)
        print(tokenizer.decode(token.unsqueeze(0)))
        print(498 in exllama_filter._formatter.get_allowed_tokens_since_last_computation())
        try:
            exllama_filter.feed(token)
            exllama_filter._formatter.compute_allowed_tokens()
        except Exception as e:
            print(e)
            file = open("engine.txt", "w")
            file.write(str(exllama_filter._formatter))
            file.close()
            return
    exllama_filter.reset()
    generator = ExLlamaV2DynamicGenerator(
        model=model,
        cache=cache,
        tokenizer=tokenizer,
    )
    settings = ExLlamaV2Sampler.Settings()
    settings.temperature = 5.0
    settings.top_p = 0.95
    output = generator.generate(
        prompt="Using the given JSON schema, give me an emotion from the following text: \nUgggghhh, why do you have to be such a jerk!",
        max_new_tokens=200,
        add_bos=True,
        filters=[exllama_filter],
        gen_settings=settings
    )
    snapshot.assert_match(output)
    del model
    del generator
    del cache
    del exllama_filter
    torch.cuda.empty_cache()
    gc.collect()


def test_exllamav2_utf_8(snapshot):
    gc.collect()
    model_dir = "local_assets/Meta-Llama-3-8B-Instruct-32k/"
    config = ExLlamaV2Config(model_dir)
    model = ExLlamaV2(config)
    cache = ExLlamaV2Cache(model, max_seq_len=4096, lazy=True)
    model.load_autosplit(cache, progress=True)
    tokenizer = ExLlamaV2Tokenizer(config)

    f = FormatterBuilder()
    f.append_line("你好，土豆！")
    exllama_filter = create_formatter_filter(model, tokenizer, f)
    generator = ExLlamaV2DynamicGenerator(
        model=model,
        cache=cache,
        tokenizer=tokenizer,
    )
    output = generator.generate(
        prompt="Hello, cats! ",
        max_new_tokens=200,
        add_bos=True,
        filters=[exllama_filter]
    )
    snapshot.assert_match(output)
    del model
    del generator
    del cache
    del exllama_filter
    torch.cuda.empty_cache()
    gc.collect()


def test_exllamav2_batched_inference(snapshot):
    model_dir = "local_assets/Meta-Llama-3-8B-Instruct-32k/"
    config = ExLlamaV2Config(model_dir)
    model = ExLlamaV2(config)
    cache = ExLlamaV2Cache(model, max_seq_len=4096, lazy=True)
    model.load_autosplit(cache, progress=True)
    tokenizer = ExLlamaV2Tokenizer(config)
    f = FormatterBuilder()
    f.append_line("Hello, Exllamav2!")
    exllama_filter = create_formatter_filter(model, tokenizer, f)
    exllama_filter2 = create_formatter_filter(model, tokenizer, f)
    generator = ExLlamaV2DynamicGenerator(
        model=model,
        cache=cache,
        tokenizer=tokenizer,
    )
    output = generator.generate(
        prompt=["Hello, cats! ", "Hello, dogs! "],
        max_new_tokens=200,
        add_bos=True,
        filters=[[exllama_filter], [exllama_filter2]]
    )
    snapshot.assert_match(output)
    del model
    del generator
    del cache
    del exllama_filter
    torch.cuda.empty_cache()
    gc.collect()
