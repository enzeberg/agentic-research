"""Compare research results from different LLM providers."""

import asyncio
from src.main import DeepResearchSystem
from src.config import ResearchConfig


async def main():
    query = "What are the key differences between transformer and RNN architectures?"
    print(f"Query: {query}\n")

    for provider in ["openai", "anthropic"]:
        print("=" * 80)
        print(f"PROVIDER: {provider.upper()}")
        print("=" * 80)

        config = ResearchConfig(llm_provider=provider)
        system = DeepResearchSystem(config=config)
        result = await system.research(query)

        if result.get("report"):
            # Print first 500 chars as preview
            print(result["report"][:500] + "...\n")
        else:
            print(f"Error: {result.get('error')}\n")


if __name__ == "__main__":
    asyncio.run(main())
