"""Basic research example."""

import asyncio
from src.main import AgenticResearchSystem


async def main():
    """Run a basic research query."""
    # Initialize system
    system = AgenticResearchSystem()
    
    # Research query
    query = "What are the latest developments in quantum computing in 2024?"
    
    print(f"Researching: {query}\n")
    
    # Run research
    result = await system.research(query, llm_provider="openai")
    
    # Display report
    if result.get("report"):
        print("="*80)
        print("RESEARCH REPORT")
        print("="*80)
        print(result["report"])
    else:
        print(f"Error: {result.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())
