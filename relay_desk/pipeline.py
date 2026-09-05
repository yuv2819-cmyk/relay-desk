from __future__ import annotations

from dataclasses import dataclass, asdict

from . import llm, offline


RESEARCH_SYS = (
    "You are a skeptical researcher. Extract the real question, list unknowns, "
    "propose 3 angles, and refuse to invent citations. Short bullets."
)
DRAFT_SYS = (
    "You write sharp product/research briefs. Short sentences. One example. "
    "No buzzwords. End with what would change your mind."
)
ROAST_SYS = (
    "You are an editor who is mildly annoyed. Point out holes, vague claims, "
    "missing numbers, and sentences that should die. Be specific."
)


@dataclass
class RunResult:
    question: str
    mode: str
    research: str
    draft: str
    roast: str
    provider: str | None = None
    model: str | None = None

    def as_markdown(self) -> str:
        return "\n\n---\n\n".join(
            [
                f"# Relay Desk\n\n**Question:** {self.question}\n**Mode:** {self.mode}",
                self.research,
                self.draft,
                self.roast,
            ]
        )

    def as_dict(self) -> dict:
        return asdict(self)


def run(question: str, offline_mode: bool = False) -> RunResult:
    question = question.strip()
    if not question:
        raise ValueError("Question is empty.")

    if offline_mode or not llm.available():
        notes = offline.research(question)
        draft_text = offline.draft(question, notes)
        roast_text = offline.roast(draft_text)
        return RunResult(
            question=question,
            mode="offline",
            research=notes,
            draft=draft_text,
            roast=roast_text,
            provider=None,
            model=None,
        )

    r = llm.complete(RESEARCH_SYS, question)
    d = llm.complete(DRAFT_SYS, f"QUESTION:\n{question}\n\nRESEARCH:\n{r.text}")
    c = llm.complete(ROAST_SYS, f"QUESTION:\n{question}\n\nDRAFT:\n{d.text}")
    return RunResult(
        question=question,
        mode="llm",
        research=r.text,
        draft=d.text,
        roast=c.text,
        provider=r.provider,
        model=r.model,
    )
