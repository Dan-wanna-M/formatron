# Benchmark

More benchmarks will be added in the
near future.

## Benchmark Setting

CPU: AMD EPYC 7513 32-Core Processor

GPU: NVIDIA RTX A5000

## Schemas

To summarize, `address` is a plain JSON schema, `linkedlist` is recursive,
and `order` is a JSON schema that includes other nested schemas.
You can find their definitions in `utils.py`.

## Why warm up?

`formatron` uses lazy caching,
so the first run is typically about 15% slower than subsequent runs.
Performing a warm-up run allows us to better measure latency under realistic workloads,
where a few schemas are created but many requests are made.

We also plan to add the "first-run" benchmark, which will measure the time taken from
schema creation to the first run ends.

## Other libraries' version

```txt
kbnf==0.3.10
lm-format-enforcer==0.10.6
outlines==0.0.46
vllm==0.6.0
exllamav2==0.2.1
transformers==4.43.2
```

## vllm

Default vllm setting are used. Outlines's whitespace pattern is aligned to lm-format-enforcer's and formatron's.

| model           | schema          | Formatron overhead per token(with warm-up) / ms | lm format enforcer overhead(with warm-up) per token / ms | outlines overhead(with warm-up) per token / ms |
|-----------------|-----------------|-------------------------------------------------|----------------------------------------------------------|------------------------------------------------|
| Llama3-8B(bf16) | address_json    | 0.10                                            | 1.84                                                     | 0.17                                          |
| Llama3-8B(bf16) | linkedlist_json | 0.10                                            | 0.28                                                     | N/A                                            |
| Llama3-8B(bf16) | order_json      | 0.06                                            | 0.61                                                     | 0.10                                           |
| Llama2-7B(fp16) | address_json    | 0.13                                            | 0.47                                                     | 0.13                                           |
| Llama2-7B(fp16) | linkedlist_json | 0.23                                            | 0.51                                                     | N/A                                            |
| Llama2-7B(fp16) | order_json      | 0.00                                            | 0.46                                                     | 0.03                                           |

## Exllamav2

Default exllamav2 setting are used.

Note that the current `lm-format-enforcer` integration on `exllamav2` is [bugged](https://github.com/noamgat/lm-format-enforcer/issues/134),
crippling its performance significantly. Also, `outlines` exllamav2 integration [has not been merged yet](https://github.com/outlines-dev/outlines/issues/1009).

| model           | schema          | Formatron overhead per token(with warm-up) / ms | lm format enforcer overhead(with warm-up) per token / ms | outlines overhead(with warm-up) per token / ms |
|-----------------|-----------------|-------------------------------------------------|----------------------------------------------------------|:-----------------------------------------------|
| Llama3-8B(bf16) | address_json    | 1.46                                            | 5.81                                                     | N/A                                            |
| Llama3-8B(bf16) | linkedlist_json | 0.81                                            | 16.65                                                     | N/A                                            |
| Llama3-8B(bf16) | order_json      | 0.44                                            | 10.62                                                     | N/A                                            |
| Llama2-7B(fp16) | address_json    | 0.75                                            | 7.28                                                     | N/A                                            |
| Llama2-7B(fp16) | linkedlist_json | 0.41                                            | 6.18                                                      | N/A                                            |
| Llama2-7B(fp16) | order_json      | 0.17                                            | 4.77                                                     | N/A                                            |

## Transformers

Default transformers setting with flash attention v2 enabled.

Note that `outlines` logits processor huggingface integration in the latest published version(`0.0.46`) [does not work](https://github.com/outlines-dev/outlines/issues/1115) and their wrapper over huggingface does not provide a way to measure token per second. Their own benchmark only measures the total time taken.

| model           | schema          | Formatron overhead per token(with warm-up) / ms | lm format enforcer overhead(with warm-up) per token / ms | outlines overhead(with warm-up) per token / ms |
|-----------------|-----------------|-------------------------------------------------|----------------------------------------------------------|------------------------------------------------|
| Llama3-8B(bf16) | address_json    | 0.30                                            | 10.14                                                      | N/A                                            |
| Llama3-8B(bf16) | linkedlist_json | 0.32                                            | 3.65                                                      | N/A                                            |
| Llama3-8B(bf16) | order_json      | 0.29                                            | 6.31                                                      | N/A                                            |
| Llama2-7B(fp16) | address_json    | 0.40                                            | 2.41                                                      | N/A                                            |
| Llama2-7B(fp16) | linkedlist_json | 0.44                                            | 0.77                                                     | N/A                                            |
| Llama2-7B(fp16) | order_json      | 0.43                                            | 1.22                                                     | N/A                                            |
