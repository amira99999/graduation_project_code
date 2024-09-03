from django.apps import AppConfig
from .singletons.singleton_llm_client import ModelClient
from .singletons.singleton_pipeline import SingletonPipeline
from .singletons.singleton_encoder import USESingleton
from .singletons.singleton_classifier import ClassifierSingleton


class RunnerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'runner'

    def ready(self):
        # Initialize Models when the app is ready
        ModelClient()
        SingletonPipeline()
        USESingleton()
        ClassifierSingleton()
