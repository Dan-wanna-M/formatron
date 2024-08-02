from vllm import LLM, SamplingParams

from formatter import FormatterBuilder
from integrations.vllm import create_formatters_logits_processor


def test_vllm_integration(snapshot):
    prompts = [
        "Hello, my name is",
        "The future of AI is",
    ]
    llm = LLM(model="openai-community/gpt2")
    f = FormatterBuilder()
    f.append_line("definitely vllm!")
    f2 = FormatterBuilder()
    f2.append_line("vllm for sure!")
    logits_processor = create_formatters_logits_processor(llm, [f, f2])
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95, logits_processors=[logits_processor])
    # Generate texts from the prompts. The output is a list of RequestOutput objects
    # that contain the prompt, generated text, and other information.
    outputs = llm.generate(prompts, sampling_params)
    # Print the outputs.
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        snapshot.assert_match(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")