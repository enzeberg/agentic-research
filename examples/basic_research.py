"""Basic research example — search the web and generate a report."""

import asyncio
from src.main import AgenticResearchSystem


async def main():
    system = AgenticResearchSystem()

    result = await system.research(
        "What are the latest developments in AI in 2025?"
    )

    if result.get("report"):
        print("=" * 80)
        print("RESEARCH REPORT")
        print("=" * 80)
        print(result["report"])
    else:
        print(f"Error: {result.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())
