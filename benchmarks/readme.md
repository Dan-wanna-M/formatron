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
## vllm
Default vllm setting are used.

| model           | schema          | Formatron overhead per token(with warm-up) / ms | lm format enforcer overhead(with warm-up) per token / ms |
|-----------------|-----------------|-------------------------------------------------|----------------------------------------------------------|
| Llama3-8B(bf16) | address_json    | 0.59                                            | 2.31                                                     |
| Llama3-8B(bf16) | linkedlist_json | 0.66                                            | 0.26                                                     |
| Llama3-8B(bf16) | order_json      | 0.64                                            | 0.92                                                     |
| Llama2-7B(fp16) | address_json    | 0.33                                            | 0.33                                                     |
| Llama2-7B(fp16) | linkedlist_json | 0.45                                            | 0.36                                                     |
| Llama2-7B(fp16) | order_json      | 0.40                                            | 0.34                                                     |
## Exllamav2
Default exllamav2 setting are used. 
Quantization likely has some influence on json outputs and hence affects the performance.

| model                  | schema          | Formatron overhead per token(with warm-up) / ms | lm format enforcer overhead(with warm-up) per token / ms |
|------------------------|-----------------|-------------------------------------------------|----------------------------------------------------------|
| Llama3-8B(6.0bpw-exl2) | address_json    | 1.4                                             | 11.7                                                     |
| Llama3-8B(6.0bpw-exl2) | linkedlist_json | 5.4                                             | 9.1                                                      |
| Llama3-8B(6.0bpw-exl2) | order_json      | 3.4                                             | 12.1                                                     |
| Llama2-7B(4.0bpw-exl2) | address_json    | 1.2                                             | 0.73                                                     |
| Llama2-7B(4.0bpw-exl2) | linkedlist_json | 3.2                                             | 0.20                                                     |
| Llama2-7B(4.0bpw-exl2) | order_json      | 1.2                                             | 0.60                                                     |

## Transformers
Default transformers setting with flash attention v2 enabled.

| model           | schema          | Formatron overhead per token(with warm-up) / ms | lm format enforcer overhead(with warm-up) per token / ms |
|-----------------|-----------------|-------------------------------------------------|----------------------------------------------------------|
| Llama3-8B(bf16) | address_json    | 0.65                                            | 9.3                                                      |
| Llama3-8B(bf16) | linkedlist_json | 0.70                                            | 3.5                                                      |
| Llama3-8B(bf16) | order_json      | 0.69                                            | 6.1                                                      |
| Llama2-7B(fp16) | address_json    | 0.41                                            | 1.4                                                      |
| Llama2-7B(fp16) | linkedlist_json | 0.54                                            | 0.58                                                     |
| Llama2-7B(fp16) | order_json      | 0.44                                            | 0.96                                                     |
