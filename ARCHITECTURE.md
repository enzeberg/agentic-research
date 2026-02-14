# Architecture Documentation

## Design Philosophy

- **Agent where it matters**: Only the research step uses a real agent (ReAct with tool calling). It needs to autonomously decide what to search, when to fetch full content, and when it has enough information.
- **Chains for fixed patterns**: Planning and report generation are single-pass LLM calls — no need for agent abstractions.
- **Tools as capabilities**: Web search and content fetching are tools the agent can invoke.
- **Simple workflow**: Three-step pipeline with no unnecessary abstraction.

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     LangGraph Workflow                        │
│                                                              │
│  ┌──────────┐     ┌──────────────────┐     ┌─────────────┐  │
│  │ Planner  │────▶│  Research Agent   │────▶│   Report    │  │
│  │ (Chain)  │     │  (ReAct Agent)    │     │  Generator  │  │
│  └──────────┘     └────────┬─────────┘     │  (Chain)    │  │
│       │                    │               └─────────────┘  │
│       │           ┌────────┼────────┐           │           │
│       │           ▼        ▼        ▼           │           │
│       │      web_search  get_urls fetch_webpage  │           │
│       ▼                                         ▼           │
│   Memory ◄──────────────────────────────── Memory           │
│  (read context)                         (save session)      │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Planner (`src/core/planner.py`)

- **Type**: LLM Chain (prompt → LLM → JSON parser)
- **Input**: Research query + optional memory context
- **Output**: Structured plan (objective, sub-topics, search queries, priority areas, depth)

### 2. Research Agent (`src/core/researcher.py`)

- **Type**: ReAct Agent (via `langgraph.prebuilt.create_react_agent`)
- **Input**: Research plan as a structured prompt
- **Output**: Structured findings summary with sources
- **Tools**: `web_search`, `get_search_urls`, `fetch_webpage`

### 3. Report Generator (`src/core/report_generator.py`)

- **Type**: LLM Chain (prompt → LLM)
- **Input**: Query, plan, and findings
- **Output**: Markdown research report

### 4. Tools (`src/tools/`)

| Tool | Description |
|------|-------------|
| `web_search` | Tavily advanced web search |
| `get_search_urls` | Get URLs for deeper fetching |
| `fetch_webpage` | Extract text content from a URL |

### 5. Memory System (`src/memory/`)

- **WorkingMemory**: Current session context (plan, findings)
- **ShortTermMemory**: Recent research sessions for cross-session context
- **MemoryManager**: Coordinates both

### 6. LLM Router (`src/llm/router.py`)

- Supports OpenAI (GPT-4) and Anthropic (Claude)
- Model caching for efficiency

## Workflow State

```python
class ResearchState(TypedDict):
    query: str           # Input research question
    plan: dict           # Generated research plan
    memory_context: str  # Context from previous sessions
    findings: str        # Agent's research findings
    report: str          # Final generated report
    completed: bool
    error: str | None
```

## Flow

```
Start → Plan → Research (Agent with tools) → Report → End
```

## Extensibility

### Adding New Tools
1. Create a function with `@tool` decorator in `src/tools/`
2. Add it to `get_default_tools()` in `src/core/researcher.py`
3. Update the agent's system prompt to describe the new tool

### Adding New LLM Providers
1. Add provider in `src/llm/router.py`
2. Update `Settings` and `ResearchConfig`
3. Add API key to `.env`
