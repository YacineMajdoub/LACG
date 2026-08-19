<div align="center">

```text
    _    ____ _____ _   _ _____ ___ ____  
   / \  / ___| ____| \ | |_   _|_ _/ ___| 
  / _ \| |  _|  _| |  \| | | |  | | |     
 / ___ \ |_| | |___| |\  | | |  | | |___  
/_/   \_\____|_____|_| \_| |_| |___\____| 
  ____  ___  ____  _____  ____ _____ _   _ 
 / ___|/ _ \|  _ \| ____|/ ___| ____| \ | |
| |   | | | | | | |  _| | |  _|  _| |  \| |
| |___| |_| | |_| | |___| |_| | |___| |\  |
 \____|\___/|____/|_____\____|_____|_| \_|
```

**An autonomous pipeline that researches live documentation, writes code, compiles it, validates it — and self-heals until it's right.**

![Python](https://img.shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Multi-LLM](https://img.shields.io/badge/multi--LLM-OpenRouter%20%C2%B7%20Groq%20%C2%B7%20Together%20%C2%B7%20OpenAI-7C3AED)
![Pipeline](https://img.shields.io/badge/pipeline-self--healing-orange)
![Docs](https://img.shields.io/badge/docs-live%20web%20retrieval-teal)

</div>

---

## 🤔 What is this?

Give it a task like *"build a LangChain structured-output example"* and the pipeline will:

1. **Figure out** which libraries the task needs,
2. **Scrape live documentation** and usage examples from the web,
3. **Distill** that docs into a clean API bundle,
4. **Generate** code strictly grounded in the retrieved docs,
5. **Compile** it and auto-install any missing dependencies,
6. **Validate** it with an LLM judge — and if it fails, **regenerate** with feedback until it passes.

No hallucinated APIs. No stale training-data syntax. Just code that matches *today's* documentation.

## 🔄 How it works

```text
                 ┌─────────────────┐
                 │  📝 USER TASK   │
                 └────────┬────────┘
                          ▼
        ┌─────────────────────────────────┐
        │   🔍 TASK ANALYZER              │  → detects required libraries
        └────────────────┬────────────────┘
                          ▼
        ┌─────────────────────────────────┐
        │   🌐 DOCS RETRIEVER             │  → scrapes live docs (DDGS + BS4)
        └────────────────┬────────────────┘
                          ▼
        ┌─────────────────────────────────┐
        │   🧹 DOCS ANALYZER              │  → distills noise into API bundle
        └────────────────┬────────────────┘
                          ▼
        ┌─────────────────────────────────┐
        │   ⚡ CODE GENERATOR             │  → writes docs-grounded code
        └────────────────┬────────────────┘
                          ▼
        ┌─────────────────────────────────┐
        │   🛠️  COMPILER CHECK            │  → syntax + auto pip-install
        └────────────────┬────────────────┘
                          ▼
        ┌─────────────────────────────────┐   FAIL   ┌──────────────────────┐
        │   🧪 VALIDATOR                  │─────────►│  🔄 CODE REGENERATOR │──┐
        └────────────────┬────────────────┘          └──────────────────────┘  │
                          │ PASS                                               │
                          ▼                                    (loops back) ◄──┘
                 ┌─────────────────┐
                 │  ✅ FINAL CODE  │
                 └─────────────────┘
```

## ✨ Features

- 🤖 **Multi-LLM orchestration** — swap between OpenRouter, Groq, Together & OpenAI
- 🌐 **Live docs retrieval** — DuckDuckGo search + BeautifulSoup scraping of real docs
- 🧠 **Docs distillation** — an LLM filters noise into a structured, token-efficient API bundle
- 🛠️ **Auto dependency resolution** — parses imports and `pip install`s whatever is missing
- 🔁 **Self-healing loop** — validator feedback drives regeneration (up to *N* iterations)
- 📦 **Batch mode** — process whole JSON datasets from the CLI (goodbye, Colab uploads)
- 🔐 **Secure by design** — keys live in `.env`, never in code

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

## 🧠 Model registry

| Client      | Default model                              | Role                          |
|-------------|--------------------------------------------|-------------------------------|
| OpenRouter  | `nvidia/nemotron-3-super-120b-a12b:free`   | Main reasoning engine (agents) |
| Together AI | `meta-llama/Llama-3.3-70B-Instruct-Turbo`  | Alternative generator          |
| Groq        | `groq/compound-mini`                       | Fast inference                 |
| OpenAI      | `gpt-4` / `gpt-5`                          | Baselines & testing            |

## 🔑 Environment variables

| Variable             | Provider    | Get one at                |
|----------------------|-------------|---------------------------|
| `OPENROUTER_API_KEY` | OpenRouter  | openrouter.ai             |
| `GROQ_API_KEY`       | Groq        | console.groq.com          |
| `TOGETHER_API_KEY`   | Together AI | api.together.ai           |
| `OPENAI_API_KEY`     | OpenAI      | platform.openai.com       |

> ⚠️ **Security note:** `.env` is git-ignored. If you ever shared keys in plaintext (chat prompts, notebooks, gists…) — **rotate them immediately**.

## 🗺️ Roadmap

- [ ] Async, parallel docs retrieval
- [ ] Sandboxed *execution* tests (Docker) instead of compile-only checks
- [ ] Pytest-generation validation stage
- [ ] YAML-driven model & prompt configuration
- [ ] Tracing / observability hooks (LangSmith, OpenTelemetry)
- [ ] PyPI packaging (`pip install agentic-codegen`)

## 📄 License

MIT — do whatever you want with it, just don't blame me when the agent out-codes you. 

---

<div align="center">
  <sub>Built by refactoring a very chaotic Colab notebook into something its author can pretend was planned all along.</sub>
</div>
