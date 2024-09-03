from django import forms

class CodeForm(forms.Form):
    code_file = forms.FileField(required=False, label="Upload a Python file")
    code_input = forms.CharField(widget=forms.Textarea, required=False, label="Enter your Python code below:")
    file_name = forms.CharField(max_length=100, initial="code", label="Enter file name (without extension)")
