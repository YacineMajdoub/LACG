import sys, subprocess, importlib, requests, re

def check_and_prepare_code(code: str, verbose=False):
    try:
        compile(code, "<string>", "exec")
    except SyntaxError as e:
        return {"status": "error", "message": f"Syntax error: {e}"}

    imports = re.findall(r'^\s*(?:from|import)\s+([a-zA-Z0-9_\.]+)', code, re.MULTILINE)
    imports = {m.split(".")[0] for m in imports}
    
    previously_installed, installed, failed = [], [], []
    for module in imports:
        try:
            importlib.import_module(module)
            previously_installed.append(module)
        except ImportError:
            pkg = next((c for c in [module, module.replace("_", "-"), module.replace("-", "_"), module + "s"] 
                        if requests.get(f"https://pypi.org/pypi/{c}/json", timeout=3).status_code == 200), None)
            if not pkg:
                failed.append(module); continue
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                importlib.import_module(module)
                installed.append(module)
            except Exception: failed.append(module)
            
    return {
        "status": "ok" if not failed else "partial",
        "message": "✅ Code validated" if not failed else f"⚠️ Failed imports: {failed}",
        "previously_installed": previously_installed, "installed": installed, "failed": failed
    }
