import argparse
import json
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agentic_codegen.pipeline import run_task_pipeline

def main():
    parser = argparse.ArgumentParser(description="Process dataset JSON using the full agentic pipeline.")
    parser.add_argument("--input", required=True, help="Input JSON file path")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--max-iterations", type=int, default=5, help="Max self-healing iterations per task")
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"🚀 Processing {len(data)} items through the agentic pipeline...")

    for count, item in enumerate(data, 1):
        print(f"\n{'='*50}")
        print(f"📦 ITEM {count}/{len(data)}")
        print(f"{'='*50}")

        prompt = item.get("generation_prompt", "")
        if not prompt:
            print("⚠️ Skipping: no 'generation_prompt' found in item.")
            item["agentic_approach_results"] = "error: missing prompt"
            continue

        try:
            result = run_task_pipeline(
                user_request=prompt,
                max_iterations=args.max_iterations
            )

            if result and result.get("validation") == "PASS":
                answer = result["generated_code"]
                iterations = result.get("iterations", "?")
                print(f"✅ PASS after {iterations} iteration(s)")
                print(f"📝 Preview:\n{answer[:200]}...")
                item["agentic_approach_results"] = answer
                item["agentic_metadata"] = {
                    "status": "PASS",
                    "iterations": iterations,
                    "compilation": result.get("compilation_result", {})
                }
            else:
                # Pipeline exhausted retries without passing
                fallback_code = result.get("generated_code", "") if result else ""
                print(f"❌ FAIL after max iterations")
                item["agentic_approach_results"] = fallback_code or "error: validation failed"
                item["agentic_metadata"] = {
                    "status": "FAIL",
                    "iterations": result.get("iterations", "?") if result else 0,
                    "compilation": result.get("compilation_result", {}) if result else {}
                }

        except Exception as e:
            print(f"💥 Unexpected error: {e}")
            item["agentic_approach_results"] = f"error: {str(e)}"
            item["agentic_metadata"] = {"status": "ERROR"}

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done! Results saved to: {args.output}")


if __name__ == "__main__":
    main()