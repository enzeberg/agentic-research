"""Main research workflow using LangGraph."""

from typing import Any
from langgraph.graph import StateGraph, END

from src.workflows.states import ResearchState
from src.agents import (
    PlanningAgent,
    TaskManagerAgent,
    ResearchAgent,
    RAGAgent,
    ReportGeneratorAgent,
)
from src.memory import MemoryManager
from src.llm import ModelRouter
from src.config import ResearchConfig


class ResearchWorkflow:
    """LangGraph workflow for research process."""

    def __init__(
        self,
        config: ResearchConfig,
        memory_manager: MemoryManager,
    ):
        """Initialize research workflow.
        
        Args:
            config: Research configuration
            memory_manager: Memory manager instance
        """
        self.config = config
        self.memory_manager = memory_manager
        
        # Initialize model router
        self.model_router = ModelRouter(provider=config.llm_provider)
        self.llm = self.model_router.get_model()
        
        # Initialize agents
        self.planning_agent = PlanningAgent(self.llm)
        self.task_manager = TaskManagerAgent(self.llm)
        self.research_agent = ResearchAgent(self.llm)
        self.rag_agent = RAGAgent(self.llm) if config.enable_rag else None
        self.report_agent = ReportGeneratorAgent(self.llm)
        
        # Build workflow graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow.
        
        Returns:
            Compiled workflow graph
        """
        workflow = StateGraph(ResearchState)
        
        # Add nodes
        workflow.add_node("plan", self._plan_node)
        workflow.add_node("create_tasks", self._create_tasks_node)
        workflow.add_node("execute_research", self._execute_research_node)
        workflow.add_node("update_rag", self._update_rag_node)
        workflow.add_node("generate_report", self._generate_report_node)
        
        # Define edges
        workflow.set_entry_point("plan")
        workflow.add_edge("plan", "create_tasks")
        workflow.add_edge("create_tasks", "execute_research")
        
        # Conditional edge: continue research or move to RAG
        workflow.add_conditional_edges(
            "execute_research",
            self._should_continue_research,
            {
                "continue": "execute_research",
                "rag": "update_rag",
                "report": "generate_report",
            }
        )
        
        workflow.add_edge("update_rag", "generate_report")
        workflow.add_edge("generate_report", END)
        
        return workflow.compile()

    async def _plan_node(self, state: ResearchState) -> dict[str, Any]:
        """Planning node: Create research plan.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state
        """
        # Get memory context
        memory_context = self.memory_manager.get_context() if self.config.memory_enabled else None
        
        # Create plan
        plan = await self.planning_agent.create_plan(state["query"], memory_context)
        
        # Store in working memory
        if self.config.memory_enabled:
            self.memory_manager.add_to_working("plan", plan)
        
        return {
            "plan": plan,
            "memory_context": memory_context or {},
            "iteration": 0,
            "max_iterations": self.config.max_iterations,
            "completed": False,
        }

    async def _create_tasks_node(self, state: ResearchState) -> dict[str, Any]:
        """Task creation node: Generate task list.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state
        """
        tasks = await self.task_manager.create_tasks(state["plan"])
        
        if self.config.memory_enabled:
            self.memory_manager.add_to_working("tasks", tasks)
        
        return {"tasks": tasks}

    async def _execute_research_node(self, state: ResearchState) -> dict[str, Any]:
        """Research execution node: Execute next task.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state
        """
        # Get next task
        next_task = self.task_manager.get_next_task(state.get("tasks", []))
        
        if not next_task:
            return {"completed": True}
        
        # Execute task
        result = await self.research_agent.execute_task(next_task)
        
        # Mark task as completed
        updated_tasks = self.task_manager.mark_completed(
            state.get("tasks", []),
            next_task["id"]
        )
        
        # Store results
        if self.config.memory_enabled:
            self.memory_manager.add_to_working("research_result", result)
        
        # Process for RAG if enabled
        documents = []
        if self.config.enable_rag and "results" in result:
            for item in result["results"]:
                if "content" in item:
                    docs = self.research_agent.process_for_rag(
                        item["content"],
                        {"url": item.get("url"), "title": item.get("title")}
                    )
                    documents.extend(docs)
        
        return {
            "tasks": updated_tasks,
            "search_results": [result],
            "documents": documents,
            "iteration": state.get("iteration", 0) + 1,
        }

    async def _update_rag_node(self, state: ResearchState) -> dict[str, Any]:
        """RAG update node: Add documents to knowledge base.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state
        """
        if not self.config.enable_rag or not self.rag_agent:
            return {"rag_context": ""}
        
        # Add documents to RAG
        documents = state.get("documents", [])
        if documents:
            await self.rag_agent.add_documents(documents)
        
        # Retrieve relevant context
        rag_context = await self.rag_agent.retrieve_context(state["query"])
        
        return {"rag_context": rag_context}

    async def _generate_report_node(self, state: ResearchState) -> dict[str, Any]:
        """Report generation node: Create final report.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state
        """
        report = await self.report_agent.generate_report(
            query=state["query"],
            plan=state["plan"],
            research_results=state.get("search_results", []),
            rag_context=state.get("rag_context"),
        )
        
        # Save session to short-term memory
        if self.config.memory_enabled:
            self.memory_manager.save_session(
                query=state["query"],
                plan=state["plan"],
                results=state.get("search_results", []),
                report=report,
            )
        
        return {"report": report, "completed": True}

    def _should_continue_research(self, state: ResearchState) -> str:
        """Determine if research should continue.
        
        Args:
            state: Current workflow state
            
        Returns:
            Next node to execute
        """
        # Check if max iterations reached
        if state.get("iteration", 0) >= state.get("max_iterations", 5):
            if self.config.enable_rag:
                return "rag"
            return "report"
        
        # Check if all tasks completed
        tasks = state.get("tasks", [])
        pending_tasks = [t for t in tasks if t.get("status") == "pending"]
        
        if not pending_tasks:
            if self.config.enable_rag:
                return "rag"
            return "report"
        
        return "continue"

    async def run(self, query: str) -> dict[str, Any]:
        """Run the research workflow.
        
        Args:
            query: Research query
            
        Returns:
            Final workflow state
        """
        initial_state: ResearchState = {
            "query": query,
            "llm_provider": self.config.llm_provider,
            "plan": {},
            "tasks": [],
            "search_results": [],
            "documents": [],
            "rag_context": "",
            "memory_context": {},
            "report": "",
            "iteration": 0,
            "max_iterations": self.config.max_iterations,
            "completed": False,
            "error": None,
        }
        
        try:
            final_state = await self.graph.ainvoke(initial_state)
            return final_state
        except Exception as e:
            return {
                **initial_state,
                "error": str(e),
                "completed": True,
            }
