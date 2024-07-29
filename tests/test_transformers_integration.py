from transformers import LogitsProcessorList, GPT2LMHeadModel

from formatter import FormatterBuilder
from integrations.transformers import create_formatter_logits_processor_list, FormattersLogitsProcessor
import transformers


def test_transformers_integration(snapshot):
    f = FormatterBuilder()
    f.append_line(f"Hello, Huggingface!")
    model = GPT2LMHeadModel.from_pretrained("openai-community/gpt2")
    tokenizer = transformers.AutoTokenizer.from_pretrained("openai-community/gpt2")
    model.generation_config.pad_token_id = tokenizer.eos_token_id
    logits_processor = create_formatter_logits_processor_list(tokenizer, f)
    inputs = tokenizer(["I am GPT2. "], return_tensors="pt")
    snapshot.assert_match(
        tokenizer.batch_decode(model.generate(**inputs, max_new_tokens=100, logits_processor=logits_processor)))


def test_transformers_text_generation_pipeline(snapshot):
    f = FormatterBuilder()
    f.append_line(f"Hello, Huggingface!")
    tokenizer = transformers.AutoTokenizer.from_pretrained("openai-community/gpt2")
    logits_processor = create_formatter_logits_processor_list(tokenizer, f)
    pipeline = transformers.TextGenerationPipeline(
        model=transformers.GPT2LMHeadModel.from_pretrained("openai-community/gpt2"),
        tokenizer=tokenizer,
        logits_processor=logits_processor)
    snapshot.assert_match(pipeline("I am GPT2. ", max_new_tokens=100)[0])
