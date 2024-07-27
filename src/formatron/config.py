class EngineGenerationConfig:
    __slots__ = ("read_prompt", "reset_on_completion")

    def __init__(self, read_prompt=False, reset_on_completion=True):
        self.read_prompt = read_prompt
        self.reset_on_completion = reset_on_completion
