"""Planning agent for research strategy."""

from typing import Any
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


class PlanningAgent:
    """Agent responsible for understanding requirements and creating research plans."""

    def __init__(self, llm: BaseChatModel):
        """Initialize planning agent.
        
        Args:
            llm: Language model to use
        """
        self.llm = llm
        self.parser = JsonOutputParser()

    async def create_plan(
        self,
        query: str,
        memory_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a research plan based on the query.
        
        Args:
            query: Research query
            memory_context: Context from memory system
            
        Returns:
            Research plan with objectives, tasks, and strategy
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("user", self._get_user_prompt()),
        ])

        chain = prompt | self.llm | self.parser

        result = await chain.ainvoke({
            "query": query,
            "memory_context": self._format_memory_context(memory_context),
        })

        return result

    def _get_system_prompt(self) -> str:
        """Get system prompt for planning."""
        return """You are an expert research planning agent. Your role is to analyze research queries and create comprehensive research plans.

Your responsibilities:
1. Understand the user's research requirements deeply
2. Break down complex queries into manageable sub-topics
3. Identify key areas to investigate
4. Determine appropriate research strategies
5. Prioritize tasks based on importance

Output a JSON plan with the following structure:
{
    "objective": "Clear statement of research goal",
    "sub_topics": ["List of sub-topics to research"],
    "search_queries": ["List of specific search queries to execute"],
    "expected_sources": ["Types of sources to look for"],
    "priority_areas": ["Most important areas to focus on"],
    "estimated_depth": "shallow/medium/deep"
}"""

    def _get_user_prompt(self) -> str:
        """Get user prompt template."""
        return """Research Query: {query}

Previous Research Context:
{memory_context}

Create a comprehensive research plan for this query. Consider:
- What are the key questions to answer?
- What sub-topics need investigation?
- What search queries would be most effective?
- What types of sources would be most valuable?

Provide your plan in JSON format."""

    def _format_memory_context(self, memory_context: dict[str, Any] | None) -> str:
        """Format memory context for the prompt.
        
        Args:
            memory_context: Memory context dictionary
            
        Returns:
            Formatted context string
        """
        if not memory_context:
            return "No previous research context available."

        parts = []
        
        if memory_context.get("short_term_summary"):
            parts.append(f"Recent Research:\n{memory_context['short_term_summary']}")
        
        if memory_context.get("working_summary"):
            parts.append(f"Current Session:\n{memory_context['working_summary']}")

        return "\n\n".join(parts) if parts else "No previous research context available."
