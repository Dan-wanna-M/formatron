import gc
import torch
from vllm import LLM, SamplingParams

from formatron.formatter import FormatterBuilder
from formatron.integrations.vllm import create_formatters_logits_processor


def test_vllm_integration(snapshot):
    prompts = [
        "Hello, my name is",
        "The future of AI is",
    ]
    llm = LLM(model="openai-community/gpt2")
    f = FormatterBuilder()
    f.append_line("definitely vllm!")
    f2 = FormatterBuilder()
    f2.append_line("强大的【VLLM】！！！")
    logits_processor = create_formatters_logits_processor(llm, [f, f2])
    sampling_params = SamplingParams(max_tokens=50,temperature=0.8,skip_special_tokens=False, top_p=0.95, logits_processors=[logits_processor])
    # Generate texts from the prompts. The output is a list of RequestOutput objects
    # that contain the prompt, generated text, and other information.
    outputs = llm.generate(prompts, sampling_params, )
    # Print the outputs.
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        snapshot.assert_match(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
    # Clean up GPU memory
    del llm
    torch.cuda.empty_cache()
    gc.collect()


def test_vllm_integration_sparse(snapshot):
    prompts = [
        "The first prompt is",
        "The second prompt is",
        "The third prompt is",
        "The fourth prompt is",
    ]
    llm = LLM(model="openai-community/gpt2")
    
    f1 = FormatterBuilder()
    f1.append_line("formatted with vllm!")
    
    f3 = FormatterBuilder()
    f3.append_line("also formatted but is slightly longer!")
    
    # Create a sparse array of formatter builders
    sparse_formatters = [f1, None, f3, None]
    
    logits_processor = create_formatters_logits_processor(llm, sparse_formatters)
    sampling_params = SamplingParams(max_tokens=50, temperature=0, skip_special_tokens=False, top_p=0.1, logits_processors=[logits_processor])
    
    outputs = llm.generate(prompts, sampling_params)
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        snapshot.assert_match(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

