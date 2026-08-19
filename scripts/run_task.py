import argparse, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agentic_codegen.pipeline import run_task_pipeline

def main():
    parser = argparse.ArgumentParser(description="Run a single agentic code generation task.")
    parser.add_argument("--task", required=True, help="The task description string")
    args = parser.parse_args()

    result = run_task_pipeline(args.task)
    if result and result.get("validation") == "PASS":
        print("\n🎯 Final Generated Code:\n")
        print(result["generated_code"])
    else:
        print("\n❌ Could not generate valid code.")
        print(result)

if __name__ == "__main__":
    main()
