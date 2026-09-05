# Relay Desk

A question goes through three seats: researcher, drafter, critic.

Works offline with a structured heuristic. Plug in `OPENAI_API_KEY` or `GEMINI_API_KEY` when you want a real model.

## Why

Most multi-agent demos are one prompt with extra labels. This one keeps the stages separate so you can read the notes, the brief, and the roast on their own.

## Install

```bash
pip install -e .
relay-desk --offline "Should an SMB buy an AI support bot this quarter?"
```

Or:

```bash
python -m relay_desk.cli --offline "Same question"
```

## LLM mode

```bash
export OPENAI_API_KEY=sk-...
# optional: OPENAI_MODEL=gpt-4o-mini
relay-desk "Design a kill-switch for customer-facing agents."
```

Gemini instead:

```bash
export GEMINI_API_KEY=...
relay-desk "Design a kill-switch for customer-facing agents."
```

`--json` prints the three stages as JSON.

## Layout

```text
relay_desk/pipeline.py   orchestration
relay_desk/offline.py    no-key path
relay_desk/llm.py        OpenAI-compatible + Gemini
relay_desk/cli.py        CLI
```

This is a small desk, not an agent OS. No tools, no memory, no pretence of autonomy.
