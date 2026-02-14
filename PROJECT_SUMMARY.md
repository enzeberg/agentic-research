# Deep Research - Project Summary

## Overview

An AI-powered deep research system built with LangChain and LangGraph. Given a question, it autonomously searches the web, gathers information, and generates a comprehensive Markdown report.

## Architecture

```
Query → Planner (Chain) → Research Agent (ReAct) → Report Generator (Chain) → Report
                                  │
                          ┌───────┼───────┐
                          ▼       ▼       ▼
                     web_search get_urls fetch_webpage
```

### Design Principles

- **Agent where it matters**: Only research uses a real ReAct agent
- **Chains for fixed patterns**: Planning and report generation are single-pass LLM calls
- **No unnecessary abstraction**: Three-step pipeline, no forced "multi-agent" design

## Project Structure

```
src/
├── core/                  # Planner (chain) + Research Agent (ReAct) + Report Generator (chain)
├── workflows/             # LangGraph workflow: plan → research → report
├── tools/                 # web_search, fetch_webpage, document chunking
├── memory/                # Working memory + short-term memory
├── llm/                   # Model router (OpenAI / Anthropic)
├── config.py, main.py, cli.py
```

## Usage

```bash
uv run python -m src.cli "What are the latest developments in AI?"
```

```python
system = DeepResearchSystem()
result = await system.research("Your question")
print(result["report"])
```

## Dependencies

- **LangChain / LangGraph** — LLM framework and workflow
- **Tavily** — Web search API
- **Pydantic** — Configuration
- **Rich** — CLI formatting

---

**Version**: 0.2.0 | **Python**: 3.11+ | **License**: MIT
