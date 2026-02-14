"""State definitions for the research workflow."""

from typing import Any, TypedDict


class ResearchState(TypedDict):
    """State flowing through the research workflow."""

    # Input
    query: str

    # Plan step output
    plan: dict[str, Any]
    memory_context: str

    # Research step output
    findings: str

    # Report step output
    report: str

    # Control
    completed: bool
    error: str | None
