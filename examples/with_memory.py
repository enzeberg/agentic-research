"""Demonstrate the memory system across multiple related queries."""

import asyncio
from src.main import DeepResearchSystem


async def main():
    system = DeepResearchSystem()

    # First query
    print("Query 1: What is machine learning?\n")
    result1 = await system.research("What is machine learning?")
    print(f"Report 1: {len(result1.get('report', ''))} chars\n")

    # Second related query — benefits from memory context
    print("Query 2: What are the main types of ML algorithms?\n")
    result2 = await system.research(
        "What are the main types of machine learning algorithms?"
    )
    print(f"Report 2: {len(result2.get('report', ''))} chars\n")

    # Show memory state
    print("=" * 60)
    print("MEMORY SUMMARY")
    print("=" * 60)
    summary = system.get_memory_summary()
    sessions = summary.get("short_term_memory", [])
    print(f"Sessions in memory: {len(sessions)}")
    for i, s in enumerate(sessions, 1):
        print(f"  {i}. {s['query']}")

    # Find similar past research
    print("\nSimilar to 'machine learning basics':")
    for s in system.find_similar_research("machine learning basics"):
        print(f"  - {s['query']}")


if __name__ == "__main__":
    asyncio.run(main())
