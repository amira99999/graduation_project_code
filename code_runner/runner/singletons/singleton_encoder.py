import tensorflow_hub as hub

class USESingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            model_path = r"C:\Users\123\Desktop\django_python_ide\code_runner\runner\load_from\universal-sentence-encoder"
            cls._instance = hub.load(model_path)
        return cls._instance