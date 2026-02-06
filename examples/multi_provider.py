"""Example comparing results from different LLM providers."""

import asyncio
from src.main import AgenticResearchSystem


async def main():
    """Compare research results from OpenAI and Anthropic."""
    query = "What are the key differences between transformer and RNN architectures?"
    
    print(f"Researching: {query}\n")
    
    # Research with OpenAI
    print("="*80)
    print("USING OPENAI (GPT-4)")
    print("="*80)
    
    system_openai = AgenticResearchSystem()
    result_openai = await system_openai.research(query, llm_provider="openai")
    
    if result_openai.get("report"):
        print(result_openai["report"][:500] + "...\n")
    
    # Research with Anthropic
    print("="*80)
    print("USING ANTHROPIC (CLAUDE)")
    print("="*80)
    
    system_anthropic = AgenticResearchSystem()
    result_anthropic = await system_anthropic.research(query, llm_provider="anthropic")
    
    if result_anthropic.get("report"):
        print(result_anthropic["report"][:500] + "...")


if __name__ == "__main__":
    asyncio.run(main())
