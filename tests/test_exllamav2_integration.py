from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache, ExLlamaV2Tokenizer


def test_exllamav2_integration(snapshot):
    model_dir = "local_assets/Llama-3-8B-exl2/"
    config = ExLlamaV2Config(model_dir)
    model = ExLlamaV2(config)
    cache = ExLlamaV2Cache(model, max_seq_len = 65536, lazy = True)
    model.load_autosplit(cache, progress = True)
    tokenizer = ExLlamaV2Tokenizer(config)
    snapshot.assert_match("Test")