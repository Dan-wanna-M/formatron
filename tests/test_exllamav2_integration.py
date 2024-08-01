from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache, ExLlamaV2Tokenizer
from exllamav2.generator import ExLlamaV2DynamicGenerator, ExLlamaV2Sampler

from formatter import FormatterBuilder
from integrations.exllamav2 import create_formatter_filter


def test_exllamav2_integration(snapshot):
    model_dir = "local_assets/Llama-3-8B-exl2/"
    config = ExLlamaV2Config(model_dir)
    model = ExLlamaV2(config)
    cache = ExLlamaV2Cache(model, max_seq_len = 65536, lazy = True)
    model.load_autosplit(cache, progress = True)
    tokenizer = ExLlamaV2Tokenizer(config)
    f = FormatterBuilder()
    f.append_line(" Hello, Exllamav2!")
    exllama_filter = create_formatter_filter(model, tokenizer, f)
    generator = ExLlamaV2DynamicGenerator(
        model=model,
        cache=cache,
        tokenizer=tokenizer,
    )
    output = generator.generate(
        prompt="Five good reasons to adopt a cat:",
        max_new_tokens=200,
        add_bos=True,
        filters=[exllama_filter]
    )
    snapshot.assert_match(output)