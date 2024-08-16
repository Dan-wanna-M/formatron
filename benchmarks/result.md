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
| Llama3-8B(bf16) | address_json    | 40.85                           | 41.93               | 0.63                    |
| Llama3-8B(bf16) | linkedlist_json | 40.54                           | 41.83               | 0.76                    |
| Llama3-8B(bf16) | order_json      | 40.03                           | 41.45               | 0.86                    |
| Llama2-7B(fp16) | address_json    | 46.54                           | 47.51               | 0.44                    |
| Llama2-7B(fp16) | linkedlist_json | 46.50                           | 47.51               | 0.46                    |
| Llama2-7B(fp16) | order_json      | 45.69                           | 46.65               | 0.45                    |
## Exllamav2
Default exllamav2 setting are used.

| model                  | schema          | constrained(with warm-up) / tps | unconstrained / tps | overhead per token / ms |
|------------------------|-----------------|---------------------------------|---------------------|-------------------------|
| Llama3-8B(6.0bpw-exl2) | address_json    | 82.89                           | 84.38               | 0.21                    |
| Llama3-8B(6.0bpw-exl2) | linkedlist_json | 80.73                           | 88.09               | 1.03                    |
| Llama3-8B(6.0bpw-exl2) | order_json      | 84.08                           | 91.83               | 1.00                    |
## Transformers
Default transformers setting with flash attention v2 enabled.

The mysterious performance drop in huggingface integration is very interesting.

| model           | schema          | constrained(with warm-up) / tps | unconstrained / tps | overhead per token / ms |
|-----------------|-----------------|---------------------------------|---------------------|-------------------------|
| Llama3-8B(bf16) | address_json    | 27.73                           | 32.07               | 4.88                    |
| Llama3-8B(bf16) | linkedlist_json | 26.11                           | 32.13               | 7.17                    |
| Llama3-8B(bf16) | order_json      | 26.36                           | 31.66               | 6.35                    |
