import re
from typing import Optional, List, Tuple
import ast

def extract_code_from_block(text: str) -> Optional[str]:
    """
    Extracts the code block from a string that starts with ```python ``` and ends with the next occurrence of '''.

    Args:
        text: A string that contains the code block.

    Returns:
        The extracted code block as a string, or None if no valid code block is found.
    """
    pattern = r"```[Pp]ython\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def replace_code_block(text: str, new_code: str) -> str:
    """
    Replaces the description block in the input text with a new code block.

    Args:
        text: The original input text.
        new_code: The new code to replace the existing code block.

    Returns:
        The text with the code block replaced.
    """
    parts = text.split('\n\n')
    if len(parts) < 2:
        return f"{text}\n{new_code}"  # No replacement if not enough parts

    # Replace the last part (code) with the new code
    parts[-1] = new_code
    return '\n\n'.join(parts)

def extract_definitions(code: str) -> List[Tuple[str, str]]:
    """
    Extract function and class definitions from the given code and return a list of unique code blocks.
    """
    tree = ast.parse(code)
    results = []
    seen_blocks = set()

    class CodeBlockVisitor(ast.NodeVisitor):
        def __init__(self, source_code: str):
            self.source_code = source_code
            self.current_class = None
            super().__init__()

        def get_code(self, node: ast.AST) -> str:
            """
            Extracts the source code for the given node.
            """
            start = node.lineno - 1
            end = node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
            lines = self.source_code.splitlines()
            return '\n'.join(lines[start:end])

        def visit_FunctionDef(self, node: ast.FunctionDef):
            function_name = node.name
            if self.current_class:
                function_name = f"{self.current_class}.{function_name}"

            code = self.get_code(node)
            code_block = (function_name, code)
            if code_block not in seen_blocks:
                results.append(code_block)
                seen_blocks.add(code_block)
            self.generic_visit(node)

        def visit_ClassDef(self, node: ast.ClassDef):
            previous_class = self.current_class
            self.current_class = node.name

            code = self.get_code(node)
            code_block = (self.current_class, code)
            if code_block not in seen_blocks:
                results.append(code_block)
                seen_blocks.add(code_block)

            self.generic_visit(node)
            self.current_class = previous_class

    visitor = CodeBlockVisitor(code)
    visitor.visit(tree)

    return list(set(results))

def extract_docstring(input_code):
    # Regex patterns for triple-quoted docstrings and single-line comments
    docstring_pattern = r'\"\"\"(.*?)\"\"\"'
    comment_pattern = r'#(.*)'  # Matches single-line comments and captures the content after #

    # Extract triple-quoted docstring
    docstring_match = re.search(docstring_pattern, input_code, re.DOTALL)
    if docstring_match:
        return docstring_match.group(1).strip()
    
    # Extract single-line comments
    comment_matches = re.findall(comment_pattern, input_code)
    if comment_matches:
        # Remove leading/trailing whitespace from each comment and join with a newline
        return '\n'.join(comment.strip() for comment in comment_matches).strip()
    
    return ""
