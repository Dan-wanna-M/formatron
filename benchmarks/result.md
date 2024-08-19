# Benchmark
This benchmark is far from comprehensive and more benchmarks will be added in the
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

| model           | schema          | constrained(with warm-up) / tps | unconstrained / tps | overhead per token / ms |
|-----------------|-----------------|---------------------------------|---------------------|-------------------------|
| Llama3-8B(bf16) | address_json    | 40.82                           | 41.94               | 0.65                    |
| Llama3-8B(bf16) | linkedlist_json | 40.56                           | 41.85               | 0.76                    |
| Llama3-8B(bf16) | order_json      | 40.05                           | 41.46               | 0.84                    |
| Llama2-7B(fp16) | address_json    | 46.57                           | 47.53               | 0.44                    |
| Llama2-7B(fp16) | linkedlist_json | 46.51                           | 47.54               | 0.46                    |
| Llama2-7B(fp16) | order_json      | 45.71                           | 46.68               | 0.46                    |
## Exllamav2
Default exllamav2 setting are used. The inferior performance of exllamav2 integration
can be attributed to the fact that `Exllamav2Filter` requires the implementation to return
a set of allowed tokens, and constructing a large set is very slow in Python.

| model                  | schema          | constrained(with warm-up) / tps | unconstrained / tps | overhead per token / ms |
|------------------------|-----------------|---------------------------------|---------------------|-------------------------|
| Llama3-8B(6.0bpw-exl2) | address_json    | 81.76                           | 91.94               | 1.36                    |
| Llama3-8B(6.0bpw-exl2) | linkedlist_json | 73.73                           | 92.93               | 2.82                    |
| Llama3-8B(6.0bpw-exl2) | order_json      | 79.11                           | 93.47               | 1.96                    |
| Llama2-7B(4.0bpw-exl2) | address_json    | 123.71                          | 133.38              | 0.55                    |
| Llama2-7B(4.0bpw-exl2) | linkedlist_json | 80.05                           | 132.20              | 4.90                    |
| Llama2-7B(4.0bpw-exl2) | order_json      | 117.28                          | 129.65              | 0.82                    |

## Transformers
Default transformers setting with flash attention v2 enabled.

| model           | schema          | constrained(with warm-up) / tps | unconstrained / tps | overhead per token / ms |
|-----------------|-----------------|---------------------------------|---------------------|-------------------------|
| Llama3-8B(bf16) | address_json    | 37.39                           | 38.71               | 0.91                    |
| Llama3-8B(bf16) | linkedlist_json | 37.25                           | 38.65               | 0.98                    |
| Llama3-8B(bf16) | order_json      | 36.73                           | 38.11               | 0.99                    |
| Llama2-7B(fp16) | address_json    | 41.30                           | 42.14               | 0.48                    |
| Llama2-7B(fp16) | linkedlist_json | 40.75                           | 41.91               | 0.68                    |
| Llama2-7B(fp16) | order_json      | 39.70                           | 40.41               | 0.44                    |