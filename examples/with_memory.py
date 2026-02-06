"""Example demonstrating memory system."""

import asyncio
from src.main import AgenticResearchSystem


async def main():
    """Demonstrate memory system with multiple queries."""
    system = AgenticResearchSystem()
    
    # First query
    query1 = "What is machine learning?"
    print(f"Query 1: {query1}\n")
    result1 = await system.research(query1)
    print(f"Report length: {len(result1.get('report', ''))} characters\n")
    
    # Second related query (should benefit from memory)
    query2 = "What are the main types of machine learning algorithms?"
    print(f"Query 2: {query2}\n")
    result2 = await system.research(query2)
    print(f"Report length: {len(result2.get('report', ''))} characters\n")
    
    # Check memory
    print("="*80)
    print("MEMORY SUMMARY")
    print("="*80)
    memory_summary = system.get_memory_summary()
    print(f"Short-term memory sessions: {len(memory_summary.get('short_term_memory', []))}")
    
    # Find similar research
    print("\n" + "="*80)
    print("SIMILAR PAST RESEARCH")
    print("="*80)
    similar = system.find_similar_research("machine learning basics")
    for i, session in enumerate(similar, 1):
        print(f"{i}. {session['query']}")


if __name__ == "__main__":
    asyncio.run(main())
