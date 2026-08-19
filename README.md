## LACG: Library Aware Code Generation

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)

This repository contains the implementation and experimental materials for our study of library-related errors in LLM-generated code. The system evaluates and reduces common library usage issues, including incorrect import paths, deprecated library usage, hallucinated libraries, unused imports, and missing imports. It combines LLM-based code generation with documentation retrieval and validation to identify and correct library-related errors, enabling a systematic evaluation of how different LLMs handle evolving software libraries.

## 🗂️ Repository structure

```text
LAGC/
├── datasets            
│   ├── evaluation_dataset.json
│   └── exploratory_dataset.json
├── scripts/
│   ├── run_task.py               # CLI: single task
│   └── process_dataset.py        # CLI: batch JSON benchmarking
├── src/
│   └── agentic_codegen/
│       ├── __init__.py
│       ├── clients.py            # LLM SDK wrappers
│       ├── prompts.py            # all agent prompt templates
│       ├── utils.py              # JSON / code cleaning helpers
│       ├── retrieval.py          # live docs scraping (DDGS + BS4)
│       ├── compiler.py           # syntax check + auto pip-install
│       ├── agents.py             # analyzer / generator / validator roles
│       └── pipeline.py           # orchestration + self-healing loop
├── .env.example                  # ← your keys go here (never committed)
├── .gitignore
├── README.md
└── requirements.txt
```

## 🚀 Quick start

```bash
# 1. Clone & enter
git clone https://github.com/YacineMajdoub/LACG.git
cd LACG

# 2. Environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Keys
cp .env.example .env               # then paste your (rotated!) API keys
```

### Run a single task

```bash
python scripts/run_task.py --task <natural language task>
```

```text
🔹 Task Analysis
🔹 Fetch & Filter Documentations
🔹 Code Generation (Iteration 1)
🔹 Compile & Validate Code
🎉 Code validated successfully!

🎯 Final Generated Code:
...
```

### Run a batch dataset

```bash
python scripts/process_dataset.py --input <dataset_name>.json --output results.json
```

