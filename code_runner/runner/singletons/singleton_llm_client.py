from ollama import Client

class ModelClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelClient, cls).__new__(cls)
            cls._instance.client = Client(host='http://172.25.1.139:11434')
        return cls._instance

    def get_client(self):
        return self.client

def chat_with_model(client, model, prompt):
    if not prompt.strip():
        return ["Error: Prompt is empty. Please provide some code or text."]

    response = client.chat(model=model, messages=[
        {'role': 'user', 'content': prompt},
    ])
    return [response['message']['content']]
