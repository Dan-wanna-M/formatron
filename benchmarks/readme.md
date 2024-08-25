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
```
lm-format-enforcer==0.10.6
outlines==0.0.46
```

## vllm
Default vllm setting are used. Version: `0.5.3-post1`.

| model           | schema          | Formatron overhead per token(with warm-up) / ms | lm format enforcer overhead(with warm-up) per token / ms |
|-----------------|-----------------|-------------------------------------------------|----------------------------------------------------------|
| Llama3-8B(bf16) | address_json    | 0.59                                            | 2.31                                                     |
| Llama3-8B(bf16) | linkedlist_json | 0.66                                            | 0.26                                                     |
| Llama3-8B(bf16) | order_json      | 0.64                                            | 0.92                                                     |
| Llama2-7B(fp16) | address_json    | 0.33                                            | 0.33                                                     |
| Llama2-7B(fp16) | linkedlist_json | 0.45                                            | 0.36                                                     |
| Llama2-7B(fp16) | order_json      | 0.40                                            | 0.34                                                     |
## Exllamav2
Default exllamav2 setting are used. Version: `0.1.9`.

Note that the current `lm-format-enforcer` integration on `exllamav2` is [bugged](https://github.com/noamgat/lm-format-enforcer/issues/134),
crippling its performance significantly.

| model           | schema          | Formatron overhead per token(with warm-up) / ms | lm format enforcer overhead(with warm-up) per token / ms |
|-----------------|-----------------|-------------------------------------------------|----------------------------------------------------------|
| Llama3-8B(bf16) | address_json    | 2.83                                            | 11.7                                                     |
| Llama3-8B(bf16) | linkedlist_json | 0.85                                            | 25.7                                                     |
| Llama3-8B(bf16) | order_json      | 0.68                                            | 18.2                                                     |
| Llama2-7B(fp16) | address_json    | 0.96                                            | 7.98                                                     |
| Llama2-7B(fp16) | linkedlist_json | 0.41                                            | 6.4                                                      |
| Llama2-7B(fp16) | order_json      | 0.23                                            | 5.24                                                     |

## Transformers
Default transformers setting with flash attention v2 enabled. Version: `4.43.2`.

Note that `outlines` logits processor huggingface integration [does not work](https://github.com/outlines-dev/outlines/issues/1115) and their
wrapper over huggingface does not provide a way to measure token per second. Their own benchmark
only measures the total time taken.

| model           | schema          | Formatron overhead per token(with warm-up) / ms | lm format enforcer overhead(with warm-up) per token / ms | outlines overhead(with warm-up) per token / ms |
|-----------------|-----------------|-------------------------------------------------|----------------------------------------------------------|------------------------------------------------|
| Llama3-8B(bf16) | address_json    | 0.65                                            | 9.3                                                      | N/A                                            |
| Llama3-8B(bf16) | linkedlist_json | 0.70                                            | 3.5                                                      | N/A                                            |
| Llama3-8B(bf16) | order_json      | 0.69                                            | 6.1                                                      | N/A                                            |
| Llama2-7B(fp16) | address_json    | 0.41                                            | 1.4                                                      | N/A                                            |
| Llama2-7B(fp16) | linkedlist_json | 0.54                                            | 0.58                                                     | N/A                                            |
| Llama2-7B(fp16) | order_json      | 0.44                                            | 0.96                                                     | N/A                                            |
