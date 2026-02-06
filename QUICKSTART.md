# Quick Start Guide

Get started with the Agentic Research System in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- API keys for:
  - OpenAI (for GPT-4) OR Anthropic (for Claude)
  - Tavily (for web search)

## Installation

### 1. Install uv

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd agentic-research

# Install dependencies
uv sync

# Setup environment
cp .env.example .env
```

### 3. Configure API Keys

Edit `.env` file:

```bash
# Required: At least one LLM provider
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...

# Required: Web search
TAVILY_API_KEY=tvly-...

# Optional: Choose default provider
DEFAULT_LLM_PROVIDER=openai  # or anthropic
```

## Getting API Keys

### OpenAI
1. Visit https://platform.openai.com/api-keys
2. Create new API key
3. Copy to `.env` file

### Anthropic
1. Visit https://console.anthropic.com/settings/keys
2. Create new API key
3. Copy to `.env` file

### Tavily
1. Visit https://tavily.com/
2. Sign up for free account
3. Get API key from dashboard
4. Copy to `.env` file

## First Research

### Using CLI

```bash
# Basic research
uv run python -m src.cli "What are the latest developments in AI?"

# With specific provider
uv run python -m src.cli "Explain quantum computing" --provider anthropic

# Verbose output
uv run python -m src.cli "Machine learning trends" --verbose
```

### Using Python

Create `my_research.py`:

```python
import asyncio
from src.main import AgenticResearchSystem

async def main():
    # Initialize system
    system = AgenticResearchSystem()
    
    # Run research
    result = await system.research(
        query="What are the benefits of renewable energy?",
        llm_provider="openai"
    )
    
    # Print report
    print(result["report"])

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
uv run python my_research.py
```

## Examples

### Basic Research
```bash
uv run python examples/basic_research.py
```

### Compare Providers
```bash
uv run python examples/multi_provider.py
```

### Memory System Demo
```bash
uv run python examples/with_memory.py
```

## Common Use Cases

### 1. Academic Research
```python
result = await system.research(
    "What are the latest findings in CRISPR gene editing?"
)
```

### 2. Market Research
```python
result = await system.research(
    "What are the current trends in electric vehicle market?"
)
```

### 3. Technical Research
```python
result = await system.research(
    "Compare microservices vs monolithic architecture"
)
```

### 4. Competitive Analysis
```python
result = await system.research(
    "What are the key features of leading CRM platforms?"
)
```

## Configuration Options

### Research Configuration

```python
from src.config import ResearchConfig

config = ResearchConfig(
    llm_provider="openai",      # or "anthropic"
    max_iterations=5,            # research depth
    enable_rag=True,             # use vector store
    memory_enabled=True,         # use memory system
    verbose=False                # detailed logging
)

system = AgenticResearchSystem(config=config)
```

### CLI Options

```bash
uv run python -m src.cli "query" \
    --provider openai \
    --max-iterations 10 \
    --no-rag \
    --verbose
```

## Troubleshooting

### API Key Errors
```
Error: OpenAI API key not configured
```
**Solution:** Check `.env` file has correct API key

### Import Errors
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution:** Run `uv sync` to install dependencies

### Tavily Search Errors
```
Error: Tavily API key not configured
```
**Solution:** Get Tavily API key and add to `.env`

### Memory/Disk Space
```
Error: Cannot create Chroma database
```
**Solution:** Ensure `./data/chroma` directory is writable

## Next Steps

1. **Read the full README**: `README.md`
2. **Explore architecture**: `ARCHITECTURE.md`
3. **Run tests**: `uv run pytest`
4. **Customize agents**: See `src/agents/`
5. **Add new tools**: See `src/tools/`

## Tips

- Start with shorter queries to test setup
- Use `--verbose` flag to see detailed progress
- Check `data/chroma` for stored documents
- Memory persists between sessions
- Use `system.clear_memory()` to reset

## Getting Help

- Check documentation in `docs/`
- Review examples in `examples/`
- Open an issue on GitHub
- Read `CONTRIBUTING.md` for development

Happy researching! 🚀
