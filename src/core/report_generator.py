"""Report generator — a single LLM chain that synthesizes research into a report."""

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate


SYSTEM_PROMPT = """\
You are an expert research report writer. Given a research query, a research plan,
and the research findings, produce a comprehensive, well-structured Markdown report.

## Report Structure

# [Report Title]

## Executive Summary
A concise overview of the key findings (2-3 paragraphs).

## Introduction
Context, background, and research objectives.

## Key Findings
Main discoveries organized by topic/sub-topic. Use subsections as needed.

## Detailed Analysis
In-depth discussion of findings, comparisons, trends, and implications.

## Sources and References
Numbered list of all sources used, with URLs.

## Conclusion
Summary of key takeaways, limitations, and suggestions for further research.

## Guidelines
- Be factual and cite sources inline (e.g., [1], [2]).
- Use proper Markdown formatting: headers, bullet points, bold, etc.
- Do NOT fabricate information — only include what the research findings support.
- If information gaps exist, acknowledge them honestly.
- Write in a professional, objective tone.
"""

USER_PROMPT = """\
Research Query: {query}

Research Plan:
{plan}

Research Findings:
{findings}

Generate a comprehensive research report based on the above information."""


class ReportGenerator:
    """Generates a structured Markdown research report.

    This is a simple LLM chain (prompt -> LLM), not an agent.
    """

    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.chain = (
            ChatPromptTemplate.from_messages([
                ("system", SYSTEM_PROMPT),
                ("user", USER_PROMPT),
            ])
            | self.llm
        )

    async def generate(
        self,
        query: str,
        plan: dict[str, Any],
        findings: str,
    ) -> str:
        """Generate a research report.

        Args:
            query: The original research query.
            plan: The research plan that was executed.
            findings: The structured findings from the research agent.

        Returns:
            A Markdown-formatted research report.
        """
        response = await self.chain.ainvoke({
            "query": query,
            "plan": self._format_plan(plan),
            "findings": findings,
        })
        return response.content

    @staticmethod
    def _format_plan(plan: dict[str, Any]) -> str:
        """Format the plan dict into a readable string."""
        parts = []
        if "objective" in plan:
            parts.append(f"Objective: {plan['objective']}")
        if "sub_topics" in plan:
            parts.append(f"Sub-topics: {', '.join(plan['sub_topics'])}")
        if "search_queries" in plan:
            parts.append(f"Search queries: {', '.join(plan['search_queries'])}")
        if "priority_areas" in plan:
            parts.append(f"Priority areas: {', '.join(plan['priority_areas'])}")
        if "depth" in plan:
            parts.append(f"Depth: {plan['depth']}")
        return "\n".join(parts) if parts else str(plan)
