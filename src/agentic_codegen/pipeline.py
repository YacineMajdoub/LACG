import json, re
from .agents import task_Analyzer, docs_Analyzer, code_Generator, code_Regenerator, validator
from .retrieval import get_docs_for_libraries
from .compiler import check_and_prepare_code
from .utils import cleanCODE, extract_libraries_from_analysis

def run_task_pipeline(user_request: str, max_iterations: int = 5):
    print("🔹 Task Analysis")
    modules = task_Analyzer(user_request)
    f_modules = extract_libraries_from_analysis(modules)
    
    print("\n🔹 Fetch & Filter Documentations")
    docs = get_docs_for_libraries(f_modules)
    f_docs = docs_Analyzer(docs)

    iteration, code, feedback, instructions = 0, None, "", ""
    while iteration < max_iterations:
        iteration += 1
        print(f"\n🔹 Code Generation (Iteration {iteration})")
        
        code = code_Generator(user_request, f_docs) if iteration == 1 else code_Regenerator(code, feedback, instructions, f_docs)
        code = cleanCODE(code)
        
        print("\n🔹 Compile & Validate Code")
        compile_result = check_and_prepare_code(code)
        validation_feedback = validator(code, user_request, f_docs, compile_result)
        
        if validation_feedback['status'] == "PASS":
            print("\n🎉 Code validated successfully!")
            return {"generated_code": code, "validation": "PASS", "iterations": iteration, "compilation_result": compile_result}
            
        feedback, instructions = validation_feedback['feedback'], validation_feedback['instructions']
        new_libraries = validation_feedback['libraries']
        if new_libraries:
            docs = get_docs_for_libraries(new_libraries)
            f_docs = docs_Analyzer(docs)

    print("\n❌ Max iterations reached.")
    return {"generated_code": code, "validation": "FAIL", "iterations": iteration, "compilation_result": compile_result}
