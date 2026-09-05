from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass


@dataclass
class LLMResult:
    text: str
    provider: str
    model: str


def available() -> bool:
    return bool(os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY"))


def complete(system: str, user: str) -> LLMResult:
    if os.getenv("OPENAI_API_KEY"):
        return _openai(system, user)
    if os.getenv("GEMINI_API_KEY"):
        return _gemini(system, user)
    raise RuntimeError("No LLM key set. Use --offline or export OPENAI_API_KEY / GEMINI_API_KEY.")


def _openai(system: str, user: str) -> LLMResult:
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    body = {
        "model": model,
        "temperature": 0.4,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    req = urllib.request.Request(
        os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions"),
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = json.loads(resp.read().decode())
    text = payload["choices"][0]["message"]["content"].strip()
    return LLMResult(text=text, provider="openai", model=model)


def _gemini(system: str, user: str) -> LLMResult:
    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    key = os.environ["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"parts": [{"text": user}]}],
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Gemini error: {exc.read().decode()}") from exc
    text = payload["candidates"][0]["content"]["parts"][0]["text"].strip()
    return LLMResult(text=text, provider="gemini", model=model)
