# Quick Start Guide

Get started in 5 minutes.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- API keys: OpenAI (or Anthropic) + Tavily

## Installation

```bash
# Install uv (if needed)
# macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

git clone <repository-url>
cd agentic-research
uv sync
cp .env.example .env
```

## Configure API Keys

Edit `.env`:

```bash
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

### Getting API Keys

| Provider | URL |
|----------|-----|
| OpenAI | https://platform.openai.com/api-keys |
| Tavily | https://tavily.com/ (free tier available) |
| Anthropic | https://console.anthropic.com/settings/keys (optional) |

## First Research

```bash
uv run python -m src.cli "What are the latest developments in AI?"
```

Or with Python:

```python
import asyncio
from src.main import AgenticResearchSystem

async def main():
    system = AgenticResearchSystem()
    result = await system.research("What are the benefits of renewable energy?")
    print(result["report"])

asyncio.run(main())
```

## CLI Options

```bash
uv run python -m src.cli "query"                        # Default (OpenAI)
uv run python -m src.cli "query" --provider anthropic    # Use Claude
uv run python -m src.cli "query" --verbose               # Show stats
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| `OpenAI API key not configured` | Check `OPENAI_API_KEY` in `.env` |
| `Tavily API key not configured` | Check `TAVILY_API_KEY` in `.env` |
| `ModuleNotFoundError` | Run `uv sync` |

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Try `examples/` scripts
- Run `uv run pytest` for tests
