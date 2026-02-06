"""Report generator agent for creating research reports."""

from typing import Any
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate


class ReportGeneratorAgent:
    """Agent responsible for generating research reports."""

    def __init__(self, llm: BaseChatModel):
        """Initialize report generator agent.
        
        Args:
            llm: Language model to use
        """
        self.llm = llm

    async def generate_report(
        self,
        query: str,
        plan: dict[str, Any],
        research_results: list[dict[str, Any]],
        rag_context: str | None = None,
    ) -> str:
        """Generate a comprehensive research report.
        
        Args:
            query: Original research query
            plan: Research plan
            research_results: All research results
            rag_context: Additional context from RAG
            
        Returns:
            Formatted research report in markdown
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("user", self._get_user_prompt()),
        ])

        chain = prompt | self.llm

        response = await chain.ainvoke({
            "query": query,
            "plan": self._format_plan(plan),
            "results": self._format_results(research_results),
            "rag_context": rag_context or "No additional context available.",
        })

        return response.content

    async def generate_summary(
        self,
        report: str,
        max_length: int = 500,
    ) -> str:
        """Generate a summary of the report.
        
        Args:
            report: Full report text
            max_length: Maximum summary length
            
        Returns:
            Summary text
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a summarization expert. Create concise summaries."),
            ("user", "Summarize the following research report in {max_length} words or less:\n\n{report}"),
        ])

        chain = prompt | self.llm
        response = await chain.ainvoke({"report": report, "max_length": max_length})

        return response.content

    def _get_system_prompt(self) -> str:
        """Get system prompt for report generation."""
        return """You are an expert research report writer. Create comprehensive, well-structured research reports.

Your reports should:
1. Start with an executive summary
2. Clearly present key findings
3. Organize information logically
4. Include relevant citations and sources
5. Provide actionable insights
6. Use proper markdown formatting

Structure:
# [Report Title]

## Executive Summary
Brief overview of findings

## Introduction
Context and research objectives

## Key Findings
Main discoveries organized by topic

## Detailed Analysis
In-depth analysis of each finding

## Sources and References
List of all sources used

## Conclusion
Summary and recommendations"""

    def _get_user_prompt(self) -> str:
        """Get user prompt template."""
        return """Research Query: {query}

Research Plan:
{plan}

Research Results:
{results}

Additional Context:
{rag_context}

Generate a comprehensive research report based on the above information. Use markdown formatting and include proper citations."""

    def _format_plan(self, plan: dict[str, Any]) -> str:
        """Format research plan for the prompt.
        
        Args:
            plan: Research plan
            
        Returns:
            Formatted plan string
        """
        parts = []
        
        if "objective" in plan:
            parts.append(f"Objective: {plan['objective']}")
        
        if "sub_topics" in plan:
            parts.append(f"Sub-topics: {', '.join(plan['sub_topics'])}")
        
        if "priority_areas" in plan:
            parts.append(f"Priority Areas: {', '.join(plan['priority_areas'])}")

        return "\n".join(parts) if parts else str(plan)

    def _format_results(self, results: list[dict[str, Any]]) -> str:
        """Format research results for the prompt.
        
        Args:
            results: Research results
            
        Returns:
            Formatted results string
        """
        formatted = []
        
        for i, result in enumerate(results, 1):
            formatted.append(f"\n--- Result {i} ---")
            
            if "query" in result:
                formatted.append(f"Query: {result['query']}")
            
            if "answer" in result:
                formatted.append(f"Answer: {result['answer']}")
            
            if "results" in result:
                for j, item in enumerate(result["results"][:3], 1):  # Limit to top 3
                    formatted.append(f"\nSource {j}:")
                    formatted.append(f"  Title: {item.get('title', 'N/A')}")
                    formatted.append(f"  URL: {item.get('url', 'N/A')}")
                    formatted.append(f"  Content: {item.get('content', 'N/A')[:200]}...")

        return "\n".join(formatted) if formatted else "No results available."
