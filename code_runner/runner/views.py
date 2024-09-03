import io
import sys
from django.shortcuts import render
from django.http import JsonResponse
from .singletons.singleton_llm_client import ModelClient, chat_with_model
from .singletons.singleton_pipeline import SingletonPipeline
from .utils import extract_code_from_block, replace_code_block


def get_code_suggestion(request):
    if request.method == 'POST':
        code_input = request.POST.get('code_input', '')

        try:
            pipeline = SingletonPipeline() # Get the singleton pipeline instance
            processed_input = pipeline.execute(code_input)
            client = ModelClient().get_client()  # Get the singleton model client
            model = 'codegemma'  # Specify the model name
            suggested_code = chat_with_model(client, model, processed_input)
            suggested_code = suggested_code[0]  # Get the single completion

            # Extract code from the suggestion if available
            extracted_code = extract_code_from_block(suggested_code)

            # Replace the original code block with the extracted code
            updated_code = replace_code_block(code_input, extracted_code)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'suggested_code': updated_code})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def execute_code(code):
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer
    
    try:
        exec(code, globals())
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        sys.stdout = old_stdout
        output = buffer.getvalue()
    
    return output if output else "Code executed successfully with no output."

# View to run code
def run_code(request):
    if request.method == 'POST':
        code_input = request.POST.get('code_input', '')
        result = execute_code(code_input)
        return JsonResponse({'result': result})
    return JsonResponse({'result': 'No code to run.'})

def index(request):
    return render(request, 'runner/index.html')
