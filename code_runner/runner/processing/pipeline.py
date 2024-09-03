from abc import ABC, abstractmethod
from typing import Any, List

class PipelineStage(ABC):
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        pass

class Pipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, stage: PipelineStage):
        self.stages.append(stage)

    def execute(self, input_data: Any) -> Any:
        data = input_data
        for stage in self.stages:
            data = stage.process(data)
        return data

class ParsingStage(PipelineStage):
    def __init__(self, parser):
        self.parser = parser

    def process(self, input_data: str) -> Any:
        code, original_candidates, candidates = self.parser.parse(input_data)
        return {'candidates': candidates, 'original_candidates': original_candidates, 'code': code}

class RetrievalStage(PipelineStage):
    def __init__(self, retriever):
        self.retriever = retriever

    def process(self, input_data: Any) -> Any:
        candidates, original_candidates, code = input_data['candidates'], input_data['original_candidates'], input_data['code']
        related_candidates = self.retriever.retrieve_related_candidates(code, candidates)
        return {'candidates': original_candidates, 'related_candidates': related_candidates, 'code': code}

class PromptGeneratorStage(PipelineStage):
    def __init__(self, prompt_generation_strategy):
        self.prompt_generation_strategy = prompt_generation_strategy

    def process(self, input_data: Any) -> Any:
        candidates, related_candidates, code = input_data['candidates'], input_data['related_candidates'], input_data['code']
        prompt = self.prompt_generation_strategy.generate_prompt(candidates, related_candidates, code)
        return prompt
