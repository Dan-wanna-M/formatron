"""
Configuration classes for Formatron.
"""
from dataclasses import dataclass


@dataclass
class EngineGenerationConfig:
    """
    Configuration for how an KBNF engine should be used in text generation.

    Attributes:
        read_prompt: Whether to accept the prompt tokens when a generation begins.
        reset_at_beginning: Whether to reset the engine when a new generation begins.
    """
    read_prompt: bool = False
    reset_at_beginning: bool = True
