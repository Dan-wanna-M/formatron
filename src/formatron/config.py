class EngineGenerationConfig:
    """
    Configuration for how an KBNF engine should be used in text generation.
    """
    __slots__ = ("read_prompt", "reset_on_completion")

    def __init__(self, read_prompt=False, reset_on_completion=True):
        """
        Initialize the engine generation configuration.
        """
        self.read_prompt = read_prompt
        self.reset_on_completion = reset_on_completion
