# Deep Research

An AI-powered deep research system built with LangChain and LangGraph. It autonomously plans research, searches the web, gathers information, and generates comprehensive reports.

## Architecture

```
┌────────────────────────────────────────────────────┐
│                 LangGraph Workflow                   │
│                                                     │
│  ┌──────────┐    ┌────────────────┐   ┌──────────┐ │
│  │ Planner  │───▶│ Research Agent │──▶│  Report  │ │
│  │ (Chain)  │    │    (ReAct)     │   │Generator │ │
│  └──────────┘    └───────┬────────┘   │ (Chain)  │ │
│                          │            └──────────┘ │
│                 ┌────────┼────────┐                 │
│                 ▼        ▼        ▼                 │
│            web_search  get_urls  fetch_webpage      │
└────────────────────────────────────────────────────┘
```

| Component | Type | Role |
|-----------|------|------|
| **Planner** | LLM Chain | Analyzes query, creates research plan |
| **Research Agent** | ReAct Agent | Autonomously searches and gathers information |
| **Report Generator** | LLM Chain | Synthesizes findings into a Markdown report |

### Tools (used by the Research Agent)

| Tool | Description |
|------|-------------|
| `web_search` | Search the web via Tavily API |
| `get_search_urls` | Get URLs from search results |
| `fetch_webpage` | Fetch full text content from a web page |

## Installation

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

```bash
git clone <repository-url>
cd deep-research
uv sync
cp .env.example .env
# Edit .env with your API keys
```

Required API keys:
- **OpenAI API key** — for GPT-4
- **Tavily API key** — for web search
- _Optional_: Anthropic API key (for Claude as alternative)

## Usage

### Command Line

```bash
# Basic research
uv run python -m src.cli "What are the latest developments in quantum computing?"

# Use Anthropic
uv run python -m src.cli "Your query" --provider anthropic

# Verbose output
uv run python -m src.cli "Your query" --verbose
```

### Python API

```python
import asyncio
from src.main import DeepResearchSystem

async def main():
    system = DeepResearchSystem()
    result = await system.research("What are the latest developments in AI?")
    print(result["report"])

asyncio.run(main())
```

## Project Structure

```
deep-research/
├── src/
│   ├── core/                  # Core components
│   │   ├── planner.py         # Research planner (LLM chain)
│   │   ├── researcher.py      # Research agent (ReAct with tools)
│   │   └── report_generator.py
│   ├── workflows/             # LangGraph workflow
│   │   ├── research_flow.py   # Plan → Research → Report pipeline
│   │   └── states.py
│   ├── tools/                 # Agent tools
│   │   ├── web_search.py      # Tavily web search
│   │   ├── content_fetch.py   # Web page content fetching
│   │   └── document.py        # Document chunking
│   ├── memory/                # Memory system
│   │   ├── working.py         # Current session memory
│   │   ├── short_term.py      # Recent sessions memory
│   │   └── manager.py
│   ├── llm/                   # LLM management
│   │   └── router.py          # Model router (OpenAI / Anthropic)
│   ├── config.py
│   ├── main.py
│   └── cli.py
├── tests/
├── examples/
├── pyproject.toml
└── .env.example
```

## Development

```bash
uv run pytest           # Run tests
uv run black src/       # Format code
uv run ruff check src/  # Lint
```

## License

MIT License
