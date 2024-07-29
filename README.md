# formatron
 
Formatron allows users to control the output format of language models
with minimal overhead. It is lightweight, user-friendly,
and seamlessly integrates into existing codebases and frameworks.

## Features

- **🔗 Popular Library Integrations**: Supports transformers and RWKV.
- **🔌 Plugins, not wrappers**:
Instead of wrapping third-party libraries in large, cumbersome classes,
Formatron offers convenient, clean plugins for different libraries.
- **💡 Utilities, not frameworks**:
Instead of unifying everything into a bulky framework,
Formatron provides flexible utilities that can be used anywhere.
- **✍️ Fluent Formatting**: Describe your format as easily as writing natural language.
- **📜 Regex and CFG Support**:
Effortlessly interleave regular expressions and context-free grammars (CFG) in formats.
- **⚙️ Efficient JSON Generation**: Feature-complete JSON generation based on Pydantic models.
- **🚀 Minimal Runtime Overhead**: 
With Leo optimization, a specialized compacting algorithm,
and CFG caches across generations, Earley algorithm implemented in Rust is
the aymptotically and practically fastest algorithms.
Here's a refined version of the bullet point:
- **🔧 Customizable**: Everything is configurable, including schema generation,
grammar generation, and post-generation processing (such as function calls).

## Feature matrix
TODO: create a feature matrix comparing Formatron to other libraries
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
## Benchmarks
TODO: show Formatron's speed against other libraries
## What Formatron won't do
TODO: write philosophy of Formatron and what it won't do
## What Formatron can't do now
TODO: write limitations of Formatron and constrained decoding
## Integrations
Check out integration examples in the `tests` directory.
