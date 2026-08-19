import requests
from bs4 import BeautifulSoup
try:
    from duckduckgo_search import DDGS
except ImportError:
    from ddgs import DDGS

def get_library_usage(library_name: str, max_results: int, max_snippets: int):
    query = f"{library_name} Python documentation and usage examples"
    imports, examples = [], []
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results, safe_search='off')
        for r in results:
            url = r.get("href", "")
            try:
                resp = requests.get(url, timeout=10)
                soup = BeautifulSoup(resp.text, "html.parser")
                code_blocks = [c.get_text(" ", strip=True) for c in soup.find_all(["code", "pre"])]
                for block in code_blocks:
                    if "import" in block and library_name in block and block not in imports:
                        imports.append(block)
                    elif library_name in block and block not in examples:
                        examples.append(block)
            except Exception: continue
    return {"imports": imports[:max_snippets], "examples": examples[:max_snippets]}

def get_docs_for_libraries(libraries, max_results=10, max_snippets=10):
    final_text = ""
    for lib in libraries:
        docs = get_library_usage(lib, max_results, max_snippets)
        final_text += f"\n************* {lib} *************\n"
        if docs["imports"]:
            final_text += "📌 Import Syntax:\n" + "\n".join([f"- {imp}" for imp in docs["imports"]]) + "\n"
        if docs["examples"]:
            final_text += "\n📌 Usage Examples:\n" + "\n".join([f"- {ex}" for ex in docs["examples"]]) + "\n"
        final_text += "***********************************\n"
    return final_text
