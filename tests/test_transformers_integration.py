from transformers import LogitsProcessorList, GPT2LMHeadModel

from formatter import FormatterBuilder
from integrations.transformers import create_engine_vocabulary, FormattersLogitsProcessor
import transformers


def test_transformers_integration(snapshot):
    f = FormatterBuilder()
    f.append_line(f"Hello, Huggingface!")
    model = GPT2LMHeadModel.from_pretrained("openai-community/gpt2")
    tokenizer = transformers.AutoTokenizer.from_pretrained("openai-community/gpt2")
    vocab = create_engine_vocabulary(tokenizer)
    f = f.build(vocab, lambda tokens: tokenizer.decode(tokens))
    logits_processor = LogitsProcessorList([FormattersLogitsProcessor([f], tokenizer.eos_token_id)])
    inputs = tokenizer.encode("I am GPT2. ", return_tensors="pt")
    snapshot.assert_match(
        tokenizer.decode(list(model.generate(inputs, max_new_tokens=100, logits_processor=logits_processor))[0]))
