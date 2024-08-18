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
| Llama3-8B(bf16) | address_json    | 41.10                           | 41.97               | 0.50                    |
| Llama3-8B(bf16) | linkedlist_json | 40.80                           | 41.91               | 0.65                    |
| Llama3-8B(bf16) | order_json      | 40.24                           | 41.52               | 0.77                    |
| Llama2-7B(fp16) | address_json    | 46.92                           | 47.69               | 0.34                    |
| Llama2-7B(fp16) | linkedlist_json | 46.80                           | 47.71               | 0.41                    |
| Llama2-7B(fp16) | order_json      | 45.96                           | 46.84               | 0.41                    |
## Exllamav2
Default exllamav2 setting are used.

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

The mysterious performance drop in huggingface integration is very interesting. 
The same implementation in `mask_logits` just appears to vastly inefficient.

| model           | schema          | constrained(with warm-up) / tps | unconstrained / tps | overhead per token / ms |
|-----------------|-----------------|---------------------------------|---------------------|-------------------------|
| Llama3-8B(bf16) | address_json    | 37.42                           | 38.76               | 0.91                    |
| Llama3-8B(bf16) | linkedlist_json | 37.14                           | 38.72               | 1.09                    |
| Llama3-8B(bf16) | order_json      | 36.79                           | 38.16               | 0.97                    |
| Llama2-7B(fp16) | address_json    | 41.34                           | 42.22               | 0.50                    |
| Llama2-7B(fp16) | linkedlist_json | 40.97                           | 42.00               | 0.60                    |
| Llama2-7B(fp16) | order_json      | 39.74                           | 40.60               | 0.54                    |