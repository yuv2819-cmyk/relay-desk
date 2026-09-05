from __future__ import annotations

import re


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def research(question: str) -> str:
    sents = _sentences(question)
    unknowns = [
        "Who is the buyer and what do they already believe?",
        "What would falsify the main claim?",
        "What number or example would make this concrete?",
        "What is the Indian / SMB version of this problem, if any?",
    ]
    lines = ["# Research notes (offline)", "", "## Prompt distilled"]
    lines.extend(f"- {s}" for s in sents[:8] or [question.strip()])
    lines += ["", "## Gaps to close"]
    lines.extend(f"- {q}" for q in unknowns)
    lines += [
        "",
        "## Working angle",
        "Treat the question as a system: inputs, incentives, failure modes, output.",
        "Do not invent sources. Flag every claim that needs a citation.",
    ]
    return "\n".join(lines)


def draft(question: str, notes: str) -> str:
    return "\n".join(
        [
            f"# Brief: {question.strip()[:80]}",
            "",
            "## One-line take",
            "The useful answer is the one that names the constraint, not the slogan.",
            "",
            "## Shape",
            "1. Restate the real problem in one sentence.",
            "2. Name the constraint most people skip.",
            "3. Give a worked example.",
            "4. Say what would change your mind.",
            "",
            "## From the researcher",
            notes.strip()[:1200],
            "",
            "## Draft answer",
            f"{question.strip()} is usually framed as a knowledge gap. It is more often an incentive or workflow gap.",
            "Ship a small loop you can measure this week. Then widen.",
        ]
    )


def roast(draft_text: str) -> str:
    weak = []
    low = draft_text.lower()
    if "synergy" in low or "leverage" in low or "delve" in low:
        weak.append("Buzzwords survived the draft. Cut them.")
    if len(draft_text) < 400:
        weak.append("Too thin. Add one concrete example with a number.")
    if "citation" not in low and "source" not in low:
        weak.append("No source discipline. Mark claims that are guesses.")
    if "india" not in low and "inr" not in low:
        weak.append("No local context. Add who pays and in what currency.")
    if not weak:
        weak.append("Readable. Still needs one sharper example and one killed sentence.")
    lines = ["# Roast", ""]
    lines.extend(f"- {w}" for w in weak)
    lines += [
        "",
        "## Keep",
        "- The constraint-first framing.",
        "- Anything that a buyer could run on Monday.",
        "",
        "## Kill",
        "- Generic advice.",
        "- Unsourced totals.",
    ]
    return "\n".join(lines)
