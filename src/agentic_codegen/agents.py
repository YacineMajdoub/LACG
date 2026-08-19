from typing import Dict, Any
from .clients import call_llm_op
from .prompts import (task_analyzer_prompt, docs_analyzer_prompt, code_generator_prompt, 
                      code_regenerator_prompt, validator_prompt)
from .utils import safe_json_parse

def task_Analyzer(user_request: str): return call_llm_op(task_analyzer_prompt(user_request))
def docs_Analyzer(docs: str): return call_llm_op(docs_analyzer_prompt(docs))
def code_Generator(detailed_task: str, docs: str): return call_llm_op(code_generator_prompt(detailed_task, docs))
def code_Regenerator(code: str, feedback: str, instructions: str, docs: str): 
    return call_llm_op(code_regenerator_prompt(code, feedback, instructions, docs))

def validator(code: str, task: str, docs: str, compile_result: Any) -> Dict[str, Any]:
    result = call_llm_op(validator_prompt(code, task, docs, compile_result))
    return safe_json_parse(result, fallback={"status": "FAIL", "feedback": "...", "instructions": "...", "libraries": []})
