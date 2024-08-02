![Logo](logo.svg)
---
Formatron allows users to control the output format of language models
with minimal overhead. It is lightweight, user-friendly,
and seamlessly integrates into existing codebases and frameworks.

## Features

- **🔗 Popular Library Integrations**: Supports transformers, exllamav2, vllm and RWKV.
- **🔌 Plugins, not wrappers**:
Instead of wrapping third-party libraries in large, cumbersome classes,
Formatron offers convenient, clean plugins for different libraries.
- **💡 Library, not framework**:
Instead of unifying everything into a bulky framework,
Formatron is a flexible library that can be embedded anywhere.
- **✍️ Fluent Formatting**: Describe your format as easily as writing natural language.
- **📜 Regex and CFG Support**:
Effortlessly interleave regular expressions and context-free grammars (CFG) in formats.
- **⚙️ Efficient JSON Generation**: Feature-complete JSON generation based on Pydantic models or json schemas.
- **📤 Batched Inference**: 
Freely specify different formats for each sequence in one batch!
- **🚀 Minimal Runtime Overhead**: 
With Leo optimization, a specialized compacting algorithm,
and CFG caches across generations, Earley algorithm implemented in Rust is
aymptotically and practically the fastest algorithms.
Here's a refined version of the bullet point:
- **🔧 Customizable**: Everything is configurable, including schema generation,
grammar generation, and post-generation processing (such as function calls).
## Comparison to other libraries

| Capability                                   | Formatron                                                                                | [LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer)                           | [Guidance](https://github.com/guidance-ai/guidance) | [Outlines](https://github.com/outlines-dev/outlines)                                    |
|:---------------------------------------------|------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------|:----------------------------------------------------|:----------------------------------------------------------------------------------------|
| Regular Expressions                          | ✅                                                                                        | ✅                                                                                             | ✅                                                   | ✅                                                                                       |
| Efficient Regex-constrained Generation       | ✅                                                                                        | 🟡([performance issues still exist](https://github.com/noamgat/lm-format-enforcer/issues/36)) | ❌                                                   | 🟡([scalablity currently suffers](https://github.com/outlines-dev/outlines/issues/680)) |
| Context Free Grammars(CFG)                   | ✅                                                                                        | ❌                                                                                             | ✅                                                   | 🟡([some bugs exists](https://github.com/outlines-dev/outlines/issues/959))             |
| Efficient CFG-constrained Generation         | ✅                                                                                        | ❌                                                                                             | ❌                                                   | ❌                                                                                       |
| Custom Format Extractor                      | 🟡([some limitations exist](#ast))                                                       | ❌                                                                                             | ✅                                                   | ✅                                                                                       |
| JSON Schema                                  | ✅([indirectly](https://docs.pydantic.dev/latest/integrations/datamodel_code_generator/)) | ✅                                                                                             | ✅                                                   | ✅                                                                                       |
| Function Call From Callable                  | ✅                                                                                        | ❌                                                                                             | ✅                                                   | ✅                                                                                       |
| Interleave Python control flow in generation | ❌                                                                                        | ❌                                                                                             | ✅                                                   | ❌                                                                                       |
| Batched Generation                           | ✅                                                                                        | ✅                                                                                             | ❌                                                   | ✅                                                                                       |
| Beam Search                                  | ❌                                                                                        | ✅                                                                                             | ❌                                                   | ✅                                                                                       |
| Integrates into existing pipelines           | ✅                                                                                        | ✅                                                                                             | ❌                                                   | ✅                                                                                       |
| Optional JSON Fields                         | ✅                                                                                        | ✅                                                                                             | ❌                                                   | ❌                                                                                       |
| LLM Controls JSON field whitespaces          | ✅                                                                                        | ✅                                                                                             | ❌                                                   | ❌                                                                                       |
| LLM Controls JSON field orderings            | ❌                                                                                        | ✅                                                                                             | ❌                                                   | ❌                                                                                       |
| JSON Schema with recursive classes           | ✅                                                                                        | ✅                                                                                             | ❌                                                   | ❌                                                                                       |

Feel free to open up an [issue](https://github.com/Dan-wanna-M/formatron/issues) if something is missing or incorrect!
## Examples
### Quick Start
TODO: make a fancy example that shows off all the powerful features of Formatron
### Function Calls
TODO: show how to call functions in Formatron
### Customize Schema Generation
TODO: show how to customize schema generation
### Customize Grammar Generation
TODO: show how to customize grammar generation
### Customize Post-Generation Processing
TODO: show how to customize post-generation processing
### Integrations
Check out integration examples in the `tests` directory.
## API Reference
Check out the API reference [here]().
## Benchmarks
TODO: show Formatron's speed against other libraries
Here's a refined version of the paragraph:

---

## What Formatron Won't Do
### Implement an End-to-End Inference Pipeline
Every library related to large language models(LLM) must consider that LLMs
are rapidly evolving. Many libraries, such as Guidance, Outlines, and LMQL,
address this by offering their own end-to-end inference pipelines,
which are constantly updated to incorporate the latest techniques. 

Formatron, however, takes a different approach.
Rather than providing a full-fledged inference pipeline,
Formatron focuses on being modular and easily embeddable into existing
and future pipelines.
While this may require users to write a bit more code initially,
it makes maintaining and updating the pipeline in the long run.
## What Formatron Can't Do Now
### Support OpenAI or in general API-based LLM solutions
They don't support efficient logits masking per token, nullifying most benefits
of constrained decoding.
### Context-Sensitive Validation
Unfortunately, many formats require context-sensitive validation.
For example, two keys in a JSON object must not be equal to each other.
Unlike CFGs, there is no efficient, generic algorithm to validate
such constraints. However, for a specific format, it is possible to validate
them efficiently with a specialized algorithm. In a future release,
Formatron will support context-sensitive validation for popular formats like JSON.

### Abstract Syntax Tree (AST) Construction<a id='ast'></a>

Formatron uses an Earley recognizer rather than a parser under the hood.
This approach allows for more efficient generation and validation
but also means that the AST of a given format is not available.
In most cases, this is not a problem,
as it is usually possible to extract the format from the generated string
using simple algorithms and then parse it with a parser.
However, in some cases, obtaining the AST might be necessary.
In a future release, Formatron will support AST construction.

### Process batch logits in parallel

While it is *technically possible* to process batch logits in parallel CPU threads
since Formatron uses Rust internally, most frameworks' generation loop call
Formatron's plugin for each logits in a batch in sequential order. Modifying
this behaviour requires a breaking change to the frameworks' API or let
Formatron take over the control flow from frameworks, either of which implies
substantial work.