# Process Improvement Assistant

A local AI assistant for business analysts, process improvement consultants, and operational
excellence practitioners. Built as a portfolio project to demonstrate AI workflow design,
prompt engineering, and practical LLM application development.

---

## What it does

You paste messy business text — rough process descriptions, stakeholder interview notes,
or a problem you want to fix — and the assistant returns structured, professional output
ready to use in your analysis work.

There are three modes, each with a different system prompt and output structure:

| Mode | Input | Output |
|---|---|---|
| **Process Intake Assistant** | Rough process description | Structured intake document with trigger, steps, roles, gaps, and clarification questions |
| **Pain Point Analyst** | Stakeholder notes or workshop output | Pain point table, root cause table, risks, and suggested next analysis steps |
| **Improvement Brief Generator** | Problem description and desired outcome | Concise improvement brief with problem statement, current state, benefits, risks, and first steps |

---

## Why this is a useful portfolio project

This project demonstrates several concepts relevant to an AI business analyst or AI consultant role:

- **Prompt engineering** — each mode has a carefully structured system prompt that controls tone, output format, and analytical behaviour
- **LLM API usage** — uses the OpenAI Chat Completions API with streaming
- **Provider portability** — the base URL is configurable, so the same code can work with other OpenAI-compatible providers
- **Gradio UI** — a clean, functional interface built without a frontend framework
- **Separation of concerns** — prompts, LLM logic, and UI are kept in separate files
- **Business analysis thinking** — the output structures reflect real BA artefacts (process intake forms, root cause analysis, improvement briefs)

---

## Installation

**1. Clone or download this project**

```bash
cd process-improvement-assistant
```

**2. Create a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Configuration

**4. Create your `.env` file**

Copy the example file and add your API key:

```bash
cp .env.example .env
```

Then open `.env` and set your values:

```
OPENAI_API_KEY=sk-...your key here...
OPENAI_BASE_URL=https://api.openai.com/v1
DEFAULT_MODEL=gpt-4o-mini
```

- `OPENAI_API_KEY` — required. Get yours at [platform.openai.com](https://platform.openai.com).
- `OPENAI_BASE_URL` — optional. Change this to use a different OpenAI-compatible provider.
- `DEFAULT_MODEL` — optional. Sets which model is selected when the app loads.

---

## Running the app

```bash
python app.py
```

Gradio will print a local URL (usually `http://127.0.0.1:7860`). Open it in your browser.

---

## Assistant modes in detail

### Mode 1 — Process Intake Assistant

Takes an informal or incomplete process description and returns a structured intake document.
Useful at the start of a process improvement or process documentation engagement.

The assistant will flag missing information and suggest clarification questions rather than
inventing details.

### Mode 2 — Pain Point Analyst

Takes raw notes from interviews, workshops, or retrospectives and organises them into:
- A pain point table with evidence and confidence levels
- A root cause table with evidence strength
- Risks of leaving the problem unaddressed
- Suggested analysis steps before moving to solutions

The assistant distinguishes between what was stated and what is being inferred.

### Mode 3 — Improvement Brief Generator

Takes a problem description and desired outcome and produces a concise improvement brief —
the kind of document used to kick off a Lean, Six Sigma, or general process improvement project.

The assistant makes assumptions explicit, avoids overclaiming benefits, and focuses on
practical first steps.

---

## Concepts demonstrated

| Concept | Where |
|---|---|
| System prompts | `prompts.py` |
| LLM API calls | `llm_client.py` |
| Streaming responses | `llm_client.py` → `app.py` |
| Gradio UI | `app.py` |
| Markdown output | Gradio `gr.Markdown` component |
| Environment variables | `.env` + `python-dotenv` |
| Model selection | Dropdown in UI, `DEFAULT_MODEL` env var |
| Input validation | `run_assistant()` in `app.py` |
| Provider portability | `OPENAI_BASE_URL` in `.env` |

---

## Limitations

- **No conversation history** — each submission is independent. The assistant has no memory of previous turns.
- **No file upload** — input must be pasted as text.
- **No output saving** — results are not saved anywhere. Copy what you need before refreshing.
- **Model availability** — the models in the dropdown require an OpenAI API key with access to those models.

---

> **Portfolio note**
>
> This is a portfolio prototype. It is designed to demonstrate AI workflow design, prompt structuring,
> Gradio UI creation and business analysis use cases. It is not a production system and should not be
> used with confidential company data unless security, hosting, logging and data handling have been
> properly reviewed.
