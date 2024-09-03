from .strategies import SimpleParsingStrategy, USEEmbeddingStrategy, SimpleRetrievalStrategy, SimplePromptGenerationStrategy
from .pipeline import Pipeline, ParsingStage, RetrievalStage, PromptGeneratorStage
from ..singletons.singleton_classifier import ClassifierSingleton

def create_code_suggestion_pipeline():
    # Instantiate the strategies and stages
    parsing_stage = ParsingStage(SimpleParsingStrategy())
    embedding_strategy = USEEmbeddingStrategy()
    classifier = ClassifierSingleton()
    retrieval_stage = RetrievalStage(SimpleRetrievalStrategy(embedding_strategy, classifier))
    prompt_generation_stage = PromptGeneratorStage(SimplePromptGenerationStrategy())

    # Create and configure the pipeline
    pipeline = Pipeline()
    pipeline.add_stage(parsing_stage)
    pipeline.add_stage(retrieval_stage)
    pipeline.add_stage(prompt_generation_stage)

    return pipeline
