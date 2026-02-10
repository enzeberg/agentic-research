# Architecture Documentation

## System Overview

The Agentic Research System is a multi-agent platform designed to conduct deep research and generate comprehensive reports. It leverages LangChain and LangGraph to orchestrate multiple specialized agents working together.

## Core Components

### 1. Multi-Agent System

#### Orchestrator (ResearchWorkflow)
- **Implementation**: `src/workflows/research_flow.py`
- **Technology**: LangGraph StateGraph
- **Responsibilities**:
  - Coordinates all agents through a state machine
  - Manages workflow transitions between nodes
  - Handles error recovery and iteration control
  - Determines conditional routing (continue research, move to RAG, or generate report)
- **Note**: The orchestrator is not a separate agent file but a workflow class that uses LangGraph to coordinate specialized agents

#### Planning Agent
- Analyzes user queries
- Creates structured research plans
- Identifies key topics and search strategies
- Leverages memory for context-aware planning

#### Task Manager Agent
- Converts plans into actionable tasks
- Maintains dynamic to-do lists
- Prioritizes tasks based on importance
- Updates tasks based on research findings

#### Research Agent
- Executes web searches via Tavily API
- Fetches and processes web content
- Analyzes research results
- Prepares documents for RAG storage

#### RAG Agent
- Manages document storage in Chroma vector store
- Retrieves relevant context for queries
- Provides semantic search capabilities
- Answers questions using retrieved context

#### Report Generator Agent
- Synthesizes research findings
- Creates structured markdown reports
- Includes citations and sources
- Generates executive summaries

### 2. Memory System

#### Working Memory
- Stores current session context
- Limited size (configurable, default: 5 items)
- Cleared at session end
- Used for immediate context

#### Short-term Memory
- Stores recent research sessions
- Limited size (configurable, default: 10 sessions)
- Enables learning from past research
- Supports similarity search for relevant history

### 3. RAG System

#### Vector Store (Chroma)
- Persistent document storage
- Semantic similarity search
- Metadata filtering
- Efficient retrieval

#### Embeddings
- OpenAI embeddings (primary)
- HuggingFace embeddings (alternative)
- Configurable embedding models

### 4. LLM Management

#### Model Router
- Supports OpenAI (GPT-4)
- Supports Anthropic (Claude)
- Seamless provider switching
- Model caching for efficiency

### 5. Tool System

#### Web Search (Tavily)
- Advanced web search
- Domain filtering
- Result ranking
- Quick answers

#### Content Fetcher
- Web page content extraction
- HTML parsing
- Content cleaning
- Batch fetching

#### Document Processor
- Text chunking
- Metadata management
- Key point extraction
- Content summarization

## Workflow Architecture

### LangGraph State Machine

```
┌─────────┐
│  Start  │
└────┬────┘
     │
     ▼
┌─────────────┐
│   Planning  │ ◄─── Memory Context
└──────┬──────┘
       │
       ▼
┌──────────────┐
│ Create Tasks │
└──────┬───────┘
       │
       ▼
┌────────────────┐
│    Research    │ ◄─┐
│   Execution    │   │
└────────┬───────┘   │
         │           │
         ├───────────┘ (Continue)
         │
         ▼
┌────────────────┐
│   Update RAG   │ (Optional)
└────────┬───────┘
         │
         ▼
┌────────────────┐
│ Generate Report│
└────────┬───────┘
         │
         ▼
     ┌───────┐
     │  End  │
     └───────┘
```

### State Flow

1. **Planning Phase**
   - Analyze query
   - Load memory context
   - Create research plan

2. **Task Creation Phase**
   - Convert plan to tasks
   - Assign priorities
   - Set dependencies

3. **Research Phase** (Iterative)
   - Execute next task
   - Collect results
   - Update task list
   - Continue until complete or max iterations

4. **RAG Phase** (Optional)
   - Store documents in vector store
   - Retrieve relevant context
   - Enhance report with RAG context

5. **Report Generation Phase**
   - Synthesize all findings
   - Create structured report
   - Save to memory

## Data Flow

```
User Query
    │
    ▼
Planning Agent ──► Research Plan
    │
    ▼
Task Manager ──► Task List
    │
    ▼
Research Agent ──► Search Results ──► Documents
    │                                      │
    │                                      ▼
    │                                  RAG System
    │                                      │
    ▼                                      │
Report Generator ◄─────────────────────────┘
    │
    ▼
Final Report
```

## Configuration

### Environment Variables
- API keys for LLM providers
- Tavily API key
- Model selections
- Memory limits
- Iteration limits

### Runtime Configuration
- LLM provider selection
- RAG enable/disable
- Memory enable/disable
- Verbosity level
- Max iterations

## Extensibility

### Adding New Agents
1. Create agent class in `src/agents/`
2. Implement required methods
3. Initialize agent in `ResearchWorkflow.__init__()` in `src/workflows/research_flow.py`
4. Add corresponding node method (e.g., `_new_agent_node()`)
5. Update workflow graph in `_build_graph()` to include the new node
6. Update state definition in `src/workflows/states.py` if needed

### Adding New Tools
1. Create tool class in `src/tools/`
2. Implement tool interface
3. Integrate with Research Agent
4. Update documentation

### Adding New LLM Providers
1. Add provider in `src/llm/router.py`
2. Update configuration
3. Add API key to `.env`
4. Test integration

## Performance Considerations

### Memory Management
- Working memory: O(1) access, limited size
- Short-term memory: O(n) search, limited size
- Vector store: O(log n) similarity search

### Optimization Strategies
- Model caching to reduce initialization
- Batch document processing
- Parallel task execution (future enhancement)
- Incremental RAG updates

## Security

### API Key Management
- Environment variables only
- Never commit `.env` file
- Use `.env.example` as template

### Content Safety
- Input validation
- Output sanitization
- Rate limiting (via API providers)

## Testing Strategy

### Unit Tests
- Individual agent functionality
- Memory operations
- Tool implementations

### Integration Tests
- Workflow execution
- Agent coordination
- End-to-end scenarios

### Performance Tests
- Response time benchmarks
- Memory usage monitoring
- Scalability testing
