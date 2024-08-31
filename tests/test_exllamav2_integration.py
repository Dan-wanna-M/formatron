from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache, ExLlamaV2Tokenizer
from exllamav2.generator import ExLlamaV2DynamicGenerator

from formatron.formatter import FormatterBuilder
from formatron.integrations.exllamav2 import create_formatter_filter


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


def test_exllamav2_utf_8(snapshot):
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
