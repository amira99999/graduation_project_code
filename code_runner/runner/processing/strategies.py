from abc import ABC, abstractmethod
from typing import List, Tuple
from ..utils import extract_definitions, extract_docstring
from ..singletons.singleton_encoder import USESingleton
import re
import numpy as np

class ParsingStrategy(ABC):
    @abstractmethod
    def parse(self, code: str) -> Tuple[str, str, List]:
        pass

class EmbeddingStrategy(ABC):
    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        pass

class RetrievalStrategy(ABC):
    @abstractmethod
    def retrieve_related_candidates(self, code: str, candidates: List) -> str:
        pass

class PromptGenerationStrategy(ABC):
    @abstractmethod
    def generate_prompt(self, candidates: str, related_candidates: str, code: str) -> str:
        pass

class SimpleParsingStrategy(ParsingStrategy):
    def parse(self, input_script: str) -> Tuple[str, str, List]:
        parts = re.split(r'\n\s*\n', input_script)
        if len(parts) < 2:
            # If there are less than two parts, treat the entire input as code and no candidates
            return parts[-1], "", []
        
        # Last part is the description, and the rest are candidates
        description_block = parts[-1].strip()
        candidate_blocks = parts[:-1]
        candidates_code = '\n\n'.join(candidate_blocks)
        parsed_candidates = extract_definitions(candidates_code)
        
        return description_block, candidates_code, parsed_candidates

class USEEmbeddingStrategy(EmbeddingStrategy):
    def __init__(self):
        self.use_model = USESingleton()  # Get the singleton instance of USE

    def get_embedding(self, text: str) -> List[float]:
        return self.use_model([text]).numpy()[0]

class SimpleRetrievalStrategy(RetrievalStrategy):
    def __init__(self, embedding_strategy: EmbeddingStrategy, classifier):
        self.embed_strategy = embedding_strategy
        self.classifier = classifier

    def retrieve_related_candidates(self, description: str, candidates: List) -> str:
        if not candidates:
            return ""

        docstring = extract_docstring(description)
        docstring_embedding = self.embed_strategy.get_embedding(docstring)

        related_candidates = []
        related_candidates_names = []
        formatted_names = ""

        # Process each parsed definition
        for candidate in candidates:
            candidate_name, candidate_implementation = candidate
            candidate_embedding = self.embed_strategy.get_embedding(candidate_implementation)
            combined_embedding = np.concatenate([docstring_embedding, candidate_embedding])

            # Ensure the input shape is (1, 1024)
            combined_embedding = combined_embedding.reshape(1, -1)  # Reshape to (1, 1024)

            # Get probability prediction from classifier
            y_pred_prob = self.classifier.predict([combined_embedding])
            # Apply threshold to classify
            y_pred = (y_pred_prob > 0.5).astype(int)

            if y_pred[0] == 1:  # Check if the classification is 1 (relevant)
                related_candidates.append(candidate_implementation)
                related_candidates_names.append(candidate_name)
        
        if related_candidates_names:
            if len(related_candidates_names) > 1:
                elem = ', '.join(related_candidates_names[:-1])
                last_elem = related_candidates_names[-1]
                formatted_names = f"{elem} and {last_elem}"
            else:
                formatted_names = f"{related_candidates_names[0]}"

        # print(formatted_names)

        return formatted_names

# class SimplePromptGenerationStrategy(PromptGenerationStrategy):
#     def generate_prompt(self, candidates: str, related_candidates: str, description: str) -> str:
#         prompt = ""
#         if not candidates.strip() or not related_candidates.strip():
#             # Handle the case where both candidates or related_candidates are empty            
#             prompt = (
#                 f"please generate a function as it is a standalone function with no contexts above it based on this description:\n{description}\n"
#             )
#         else:
#             # Handle the case where either candidates or related_candidates is not empty
#             prompt = (
#                 f"the context above: ```Python\n{candidates}```\n\n"
#                 f"Use the following related functions and classes to enhance the solution: {related_candidates}\n"
#                 f"please generate a function based on the context above and this description:\n{description}\n\n"
#             )
        
#         return prompt

class SimplePromptGenerationStrategy(PromptGenerationStrategy):
    def generate_prompt(self, candidates: str, related_candidates: str, description: str) -> str:
        prompt = ""
        if not candidates.strip() or not related_candidates.strip():
            # Handle the case where both candidates or related_candidates are empty            
            prompt = (
                f"please generate a function as it is a standalone function with no contexts above it based on this description:\n{description}\n"
            )
        else:
            # Handle the case where either candidates or related_candidates is not empty
            prompt = (
                f"the context above: ```Python\n{candidates}```\n\n"
                f"Use the following related functions and classes to enhance the solution: {related_candidates}\n"
                f"please generate a function based on the context above and this description:\n{description}\n\n"
            )
        
        return prompt
        