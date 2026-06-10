# app.py
# Main entry point for the Process Improvement Assistant.
# Builds the Gradio UI, handles user input, and streams LLM responses.

import os
from dotenv import load_dotenv
import gradio as gr

from prompts import PROMPTS
from llm_client import stream_llm_response

# Load environment variables from .env before anything else
load_dotenv()

# ── Model selector ────────────────────────────────────────────────────────────

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")

# Start with the standard model list
MODEL_OPTIONS = ["gpt-4o-mini", "gpt-4o"]

# If the env default is something custom (e.g. a local or alternative provider),
# add it to the list so it can still be selected
if DEFAULT_MODEL not in MODEL_OPTIONS:
    MODEL_OPTIONS.insert(0, DEFAULT_MODEL)

# ── Callback ──────────────────────────────────────────────────────────────────

def run_assistant(mode: str, user_input: str, model: str):
    """
    Called when the user clicks Submit.
    Validates inputs, selects the right system prompt, and streams the response.
    """
    # Input validation
    if not user_input or not user_input.strip():
        yield (
            "Please enter a process description, stakeholder notes, or improvement idea "
            "before running the assistant."
        )
        return

    if mode not in PROMPTS:
        yield (
            "The selected mode was not recognised. Please choose one of the available "
            "assistant modes."
        )
        return

    if not os.getenv("OPENAI_API_KEY"):
        yield (
            "**API key missing.** Please set `OPENAI_API_KEY` in your `.env` file and "
            "restart the app."
        )
        return

    system_prompt = PROMPTS[mode]

    # Stream the response — each yield updates the Gradio output in place
    yield from stream_llm_response(
        system_prompt=system_prompt,
        user_prompt=user_input,
        model=model,
    )

# ── UI ────────────────────────────────────────────────────────────────────────

with gr.Blocks(title="Process Improvement Assistant") as demo:

    gr.Markdown(
        """
# Process Improvement Assistant

An AI assistant for business analysts, process improvement consultants, and operational
excellence practitioners.

---
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            mode = gr.Dropdown(
                label="Assistant mode",
                choices=list(PROMPTS.keys()),
                value="Process Intake Assistant",
            )
            model = gr.Dropdown(
                label="Model",
                choices=MODEL_OPTIONS,
                value=DEFAULT_MODEL,
            )

        with gr.Column(scale=2):
            user_input = gr.Textbox(
                label="Your input",
                placeholder=(
                    "Paste a process description, stakeholder interview notes, "
                    "or improvement problem here..."
                ),
                lines=10,
            )

    submit_btn = gr.Button("Run assistant", variant="primary")

    output = gr.Markdown(label="Assistant output")

    submit_btn.click(
        fn=run_assistant,
        inputs=[mode, user_input, model],
        outputs=output,
    )

# ── Launch ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    demo.launch()
