from ..processing.pipelines import create_code_suggestion_pipeline

class SingletonPipeline:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = create_code_suggestion_pipeline()
        return cls._instance