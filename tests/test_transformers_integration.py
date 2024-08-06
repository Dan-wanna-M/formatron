import transformers
from formatter import FormatterBuilder
from integrations.transformers import create_formatter_logits_processor_list
from schemas import dict_inference
from transformers import GPT2LMHeadModel, AutoModelForCausalLM

from grammar_generators.json_generator import JsonGenerator


def test_transformers_integration(snapshot):
    f = FormatterBuilder()
    f.append_line(f"Hello, Huggingface!")
    model = GPT2LMHeadModel.from_pretrained("openai-community/gpt2")
    tokenizer = transformers.AutoTokenizer.from_pretrained("openai-community/gpt2")
    model.generation_config.pad_token_id = tokenizer.eos_token_id  # Remove the annoying warning
    logits_processor = create_formatter_logits_processor_list(tokenizer, f)
    inputs = tokenizer(["I am GPT2. "], return_tensors="pt")
    snapshot.assert_match(
        tokenizer.batch_decode(model.generate(**inputs, max_new_tokens=100, logits_processor=logits_processor)))


def test_readme_example(snapshot):
    f = FormatterBuilder()
    digit = f.regex('([1-9][0-9]*)', capture_name='digit')
    f.append_line(f"My favorite numbers are {digit}, {digit}, and {digit}.")
    schema = dict_inference.infer_mapping({'name': 'xxx', 'age': 'xxx'})
    f.append_str(f"Here's my personal info: {f.schema(schema,JsonGenerator(), capture_name='info')}\n")
    f.append_multiline_str(f"""
    Today, I want to eat {f.choose('apple', 'orange', 'banana', capture_name='food')}.
        I also want to {f.str(stop='.')}
    """)
    model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
    tokenizer = transformers.AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
    model.generation_config.pad_token_id = tokenizer.eos_token_id  # Remove the annoying warning
    logits_processor = create_formatter_logits_processor_list(tokenizer, f)
    inputs = tokenizer(["I am Phi. "], return_tensors="pt")
    snapshot.assert_match(
        tokenizer.batch_decode(model.generate(**inputs, max_new_tokens=256, logits_processor=logits_processor)))


def test_transformers_batched_inference(snapshot):
    f = FormatterBuilder()
    f.append_line(f"Hello, Huggingface!")
    f3 = FormatterBuilder()
    f3.append_line("Hello, Huggingface! Hello, Huggingface!")
    model = GPT2LMHeadModel.from_pretrained("openai-community/gpt2")
    tokenizer = transformers.AutoTokenizer.from_pretrained("openai-community/gpt2",
                                                           padding_side='left')
    tokenizer.pad_token = tokenizer.eos_token  # Needed for padding
    model.generation_config.pad_token_id = tokenizer.pad_token_id
    logits_processor = create_formatter_logits_processor_list(tokenizer, [f, f, f3])
    inputs = tokenizer(["I am GPT2. ", "I am another GPT2. ", "I am yet another GPT2. "], return_tensors="pt",
                       padding=True)
    snapshot.assert_match(
        tokenizer.batch_decode(model.generate(**inputs, max_new_tokens=100, logits_processor=logits_processor)))
    # Special tokens are not skipped for debugging purpose. In application, you probably want to skip.


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
