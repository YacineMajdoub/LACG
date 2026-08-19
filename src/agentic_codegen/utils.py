import re
import regex
import json
import ast
from typing import List, Any

def cleanCODE(text: str) -> str:
    lines = text.strip().split('\n')
    if lines and lines[0].startswith('```'):
        lines = lines[1:]
    closing_index = None
    for i, line in enumerate(lines):
        if '```' in line:
            closing_index = i
            break
    if closing_index is not None:
        lines = lines[:closing_index]
    return '\n'.join(lines)

def cleanJSON(text: str) -> str:
    matchy = regex.search(r'\{(?:[^{}]|(?R))*\}', text)
    return matchy.group() if matchy else "{}"

def safe_json_parse(response: str, fallback: Any = None) -> Any:
    try:
        clean_response = cleanJSON(response)
        return json.loads(clean_response)
    except json.JSONDecodeError:
        clean_response = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', clean_response)
        try:
            return json.loads(clean_response)
        except json.JSONDecodeError:
            return fallback if fallback is not None else 'error'

def extract_imports_from_code(code: str) -> List[str]:
    code = code.strip()
    if code.startswith("```"):
        code = "\n".join(code.splitlines()[1:-1])
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return sorted(imports)

def extract_libraries_from_analysis(raw_output: str):
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", raw_output, re.DOTALL)
    if match: raw_output = match.group(1)
    try:
        data = json.loads(raw_output)
        return list(dict.fromkeys([d.get("library", "").strip() for d in data.get("dependencies", []) if d.get("library")]))
    except Exception: return []
