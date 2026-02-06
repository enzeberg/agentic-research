# Agentic Research System

An intelligent multi-agent research system powered by LangChain and LangGraph that understands user requirements, conducts deep research, and generates high-value research reports.

## Features

- **Multi-Agent Architecture**: Coordinated agents for planning, research, RAG, and report generation
- **Intelligent Planning**: Automatic research plan generation based on user requirements
- **Dynamic Task Management**: Adaptive to-do list that evolves during research
- **Advanced RAG**: Vector-based document retrieval with Chroma
- **Memory System**: Working memory and short-term memory for context awareness
- **Dual LLM Support**: Seamless switching between OpenAI and Anthropic models
- **Web Research**: Integrated Tavily API for comprehensive web search
- **Structured Reports**: Professional research reports with citations

## Architecture

### Agent System

1. **Orchestrator Agent**: Main controller coordinating all agents
2. **Planning Agent**: Analyzes requirements and creates research plans
3. **Task Manager Agent**: Manages dynamic to-do lists and task tracking
4. **Research Agent**: Executes web searches and content analysis
5. **RAG Agent**: Handles document retrieval and knowledge base queries
6. **Memory Manager**: Manages working and short-term memory
7. **Report Generator Agent**: Produces structured research reports

### Core Modules

- **Planning Module**: Requirement analysis + research plan generation
- **Task Management**: Dynamic to-do list with priority management
- **Tool Calling**: Web search, content fetching, document processing
- **RAG System**: Vector store (Chroma) + semantic retrieval
- **Memory System**: 
  - Working Memory: Current session context
  - Short-term Memory: Recent research history
- **Report Generation**: Structured markdown reports with citations

## Installation

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd agentic-research
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Required API Keys:
   - OpenAI API key (for GPT-4)
   - Anthropic API key (for Claude)
   - Tavily API key (for web search)

## Usage

### Basic Usage

```python
from src.main import AgenticResearchSystem

# Initialize the system
system = AgenticResearchSystem()

# Run research
result = await system.research(
    query="What are the latest developments in quantum computing?",
    llm_provider="openai"  # or "anthropic"
)

# Access the report
print(result.report)
```

### Command Line Interface

```bash
# Run research with default settings
uv run python -m src.cli "Your research query here"

# Specify LLM provider
uv run python -m src.cli "Your query" --provider anthropic

# Enable verbose output
uv run python -m src.cli "Your query" --verbose
```

### Advanced Usage

```python
from src.main import AgenticResearchSystem
from src.config import ResearchConfig

# Custom configuration
config = ResearchConfig(
    llm_provider="anthropic",
    max_iterations=10,
    enable_rag=True,
    memory_enabled=True
)

system = AgenticResearchSystem(config=config)
result = await system.research("Your research query")
```

## Project Structure

```
agentic-research/
├── src/
│   ├── agents/              # Agent implementations
│   │   ├── orchestrator.py  # Main orchestrator agent
│   │   ├── planning.py      # Planning agent
│   │   ├── task_manager.py  # Task management agent
│   │   ├── research.py      # Research agent
│   │   ├── rag.py           # RAG agent
│   │   ├── memory.py        # Memory manager
│   │   └── report.py        # Report generator
│   ├── workflows/           # LangGraph workflows
│   │   ├── research_flow.py # Main research workflow
│   │   └── states.py        # Workflow state definitions
│   ├── memory/              # Memory system
│   │   ├── working.py       # Working memory
│   │   └── short_term.py    # Short-term memory
│   ├── rag/                 # RAG module
│   │   ├── vectorstore.py   # Chroma integration
│   │   ├── retriever.py     # Document retrieval
│   │   └── embeddings.py    # Embedding management
│   ├── tools/               # Tool implementations
│   │   ├── web_search.py    # Tavily integration
│   │   ├── content_fetch.py # Web content fetching
│   │   └── document.py      # Document processing
│   ├── llm/                 # LLM management
│   │   ├── router.py        # Model router
│   │   ├── openai.py        # OpenAI integration
│   │   └── anthropic.py     # Anthropic integration
│   ├── config.py            # Configuration management
│   ├── main.py              # Main system entry
│   └── cli.py               # Command line interface
├── tests/                   # Test suite
├── examples/                # Example scripts
├── data/                    # Data directory (gitignored)
├── pyproject.toml           # Project configuration
├── .env.example             # Environment template
└── README.md                # This file
```

## Configuration

Edit `.env` file to configure:

- **LLM Providers**: API keys and default provider
- **Models**: Specific model versions
- **Memory**: Memory size limits
- **Research**: Max iterations and other parameters

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run black src/
uv run ruff check src/
```

### Type Checking

```bash
uv run mypy src/
```

## Examples

See the `examples/` directory for:
- Basic research queries
- Custom agent configurations
- RAG integration examples
- Memory system usage

## License

MIT License

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.
