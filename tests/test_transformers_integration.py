from formatron.integrations.transformers import create_formatter_logits_processor_list
from formatron.formatter import FormatterBuilder
from transformers import GPT2LMHeadModel
import transformers


def test_transformers_integration(snapshot):
    f = FormatterBuilder()
    f.append_line("Hello, Huggingface!")
    model = GPT2LMHeadModel.from_pretrained("openai-community/gpt2")
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        "openai-community/gpt2")
    # Remove the annoying warning
    model.generation_config.pad_token_id = tokenizer.eos_token_id
    logits_processor = create_formatter_logits_processor_list(tokenizer, f)
    inputs = tokenizer(["I am GPT2. "], return_tensors="pt")
    snapshot.assert_match(
        tokenizer.batch_decode(model.generate(**inputs, max_new_tokens=100, logits_processor=logits_processor)))


def test_transformers_batched_inference(snapshot):
    f = FormatterBuilder()
    f.append_line("Hello, Huggingface!")
    f3 = FormatterBuilder()
    f3.append_line("Hello, Huggingface! Hello, Huggingface!")
    model = GPT2LMHeadModel.from_pretrained("openai-community/gpt2")
    tokenizer = transformers.AutoTokenizer.from_pretrained("openai-community/gpt2",
                                                           padding_side='left')
    tokenizer.pad_token = tokenizer.eos_token  # Needed for padding
    model.generation_config.pad_token_id = tokenizer.pad_token_id
    logits_processor = create_formatter_logits_processor_list(tokenizer, [
                                                              f, f, f3])
    inputs = tokenizer(["I am GPT2. ", "I am another GPT2. ", "I am yet another GPT2. "], return_tensors="pt",
                       padding=True)
    snapshot.assert_match(
        tokenizer.batch_decode(model.generate(**inputs, max_new_tokens=100, logits_processor=logits_processor)))
    # Special tokens are not skipped for debugging purpose. In application, you probably want to skip.


def test_transformers_sparse_formatters(snapshot):
    f = FormatterBuilder()
    f.append_line("Hello, Huggingface!")
    model = GPT2LMHeadModel.from_pretrained("openai-community/gpt2")
    tokenizer = transformers.AutoTokenizer.from_pretrained("openai-community/gpt2",
                                                           padding_side='left')
    tokenizer.pad_token = tokenizer.eos_token
    model.generation_config.pad_token_id = tokenizer.pad_token_id
    
    # Create a sparse array of formatter builders
    sparse_formatters = [None, f, None, f, None]
    
    logits_processor = create_formatter_logits_processor_list(tokenizer, sparse_formatters)
    
    inputs = tokenizer(["I am GPT2. ", "I am another GPT2. ", "I am a third GPT2. ", "I am a fourth GPT2. ", "I am a fifth GPT2. "], 
                       return_tensors="pt", padding=True)
    
    outputs = model.generate(**inputs, max_new_tokens=100, logits_processor=logits_processor)
    
    snapshot.assert_match(tokenizer.batch_decode(outputs))


def test_transformers_text_generation_pipeline(snapshot):
    f = FormatterBuilder()
    f.append_line("Hello, Huggingface!")
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        "openai-community/gpt2")
    logits_processor = create_formatter_logits_processor_list(tokenizer, f)
    pipeline = transformers.TextGenerationPipeline(
        model=transformers.GPT2LMHeadModel.from_pretrained(
            "openai-community/gpt2"),
        tokenizer=tokenizer,
        logits_processor=logits_processor)
    snapshot.assert_match(pipeline("I am GPT2. ", max_new_tokens=100)[0])
