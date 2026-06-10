# llm_client.py
# Handles all communication with the LLM.
# Separated from app.py so the API logic can be read and explained independently.

import os
from openai import OpenAI


def get_client() -> OpenAI:
    """Create and return an OpenAI-compatible client using environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. Please add it to your .env file."
        )

    return OpenAI(api_key=api_key, base_url=base_url)


def stream_llm_response(system_prompt: str, user_prompt: str, model: str):
    """
    Call the LLM with a system prompt and user prompt, streaming the response.

    Yields cumulative markdown text so Gradio can update the output progressively
    as each new chunk arrives — rather than waiting for the full response.

    Args:
        system_prompt: The assistant's instructions and persona.
        user_prompt:   The user's input text.
        model:         The model name to use (e.g. "gpt-4o-mini").

    Yields:
        str: The response text accumulated so far.
    """
    client = get_client()

    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        stream=True,
    )

    accumulated = ""
    for chunk in stream:
        # Each chunk may or may not contain a delta — guard against None
        delta = chunk.choices[0].delta.content
        if delta:
            accumulated += delta
            yield accumulated
