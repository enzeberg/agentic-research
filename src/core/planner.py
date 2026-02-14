"""Research planner — a single LLM chain that creates a research plan."""

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


SYSTEM_PROMPT = """\
You are an expert research planner. Given a research query and optional context
from previous research sessions, produce a structured research plan in JSON.

Output exactly this JSON structure:
{{
    "objective": "One-sentence research goal",
    "sub_topics": ["sub-topic 1", "sub-topic 2", ...],
    "search_queries": ["specific search query 1", "query 2", ...],
    "priority_areas": ["most important area 1", ...],
    "depth": "shallow | medium | deep"
}}

Guidelines:
- Generate 3-6 specific, diverse search queries that cover different angles.
- Identify 2-4 sub-topics that break the research into logical parts.
- Set depth based on query complexity: factual questions → shallow, multi-faceted
  analysis → deep.
"""

USER_PROMPT = """\
Research Query: {query}

Previous Research Context:
{memory_context}

Create a research plan in JSON format."""


class Planner:
    """Creates a structured research plan from a query.

    This is a simple LLM chain (prompt → LLM → JSON parser), not an agent.
    """

    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.parser = JsonOutputParser()
        self.chain = (
            ChatPromptTemplate.from_messages([
                ("system", SYSTEM_PROMPT),
                ("user", USER_PROMPT),
            ])
            | self.llm
            | self.parser
        )

    async def create_plan(
        self,
        query: str,
        memory_context: str = "",
    ) -> dict[str, Any]:
        """Create a research plan.

        Args:
            query: The research question.
            memory_context: Optional context from previous sessions.

        Returns:
            A structured plan dict with objective, sub_topics, search_queries, etc.
        """
        result = await self.chain.ainvoke({
            "query": query,
            "memory_context": memory_context or "No previous research context.",
        })
        return result
