
## 🗂️ Repository structure

```text
agentic-codegen/
├── README.md
├── requirements.txt
├── .env.example                  # ← your keys go here (never committed)
├── .gitignore
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
└── scripts/
    ├── run_task.py               # CLI: single task
    └── process_dataset.py        # CLI: batch JSON benchmarking
```

## 🚀 Quick start

```bash
# 1. Clone & enter
git clone https://github.com/<you>/agentic-codegen.git
cd agentic-codegen

# 2. Environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Keys
cp .env.example .env               # then paste your (rotated!) API keys
```

### Run a single task

```bash
python scripts/run_task.py --task "Create a structured output example using LangChain and Pydantic with a BaseModel named AnswerWithJustification..."
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
python scripts/process_dataset.py --input tasks.json --output results.json
```

