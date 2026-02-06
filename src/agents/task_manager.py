"""Task manager agent for dynamic to-do list management."""

from typing import Any
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


class TaskManagerAgent:
    """Agent responsible for managing research tasks and to-do lists."""

    def __init__(self, llm: BaseChatModel):
        """Initialize task manager agent.
        
        Args:
            llm: Language model to use
        """
        self.llm = llm
        self.parser = JsonOutputParser()

    async def create_tasks(
        self,
        plan: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Create initial task list from research plan.
        
        Args:
            plan: Research plan
            
        Returns:
            List of tasks with priorities and dependencies
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("user", "Research Plan:\n{plan}\n\nCreate a prioritized task list."),
        ])

        chain = prompt | self.llm | self.parser

        result = await chain.ainvoke({"plan": str(plan)})
        return result.get("tasks", [])

    async def update_tasks(
        self,
        current_tasks: list[dict[str, Any]],
        completed_task: dict[str, Any],
        results: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Update task list based on completed task and results.
        
        Args:
            current_tasks: Current task list
            completed_task: Task that was just completed
            results: Results from the completed task
            
        Returns:
            Updated task list
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_update_prompt()),
            ("user", self._get_update_user_prompt()),
        ])

        chain = prompt | self.llm | self.parser

        result = await chain.ainvoke({
            "current_tasks": str(current_tasks),
            "completed_task": str(completed_task),
            "results": str(results),
        })

        return result.get("tasks", current_tasks)

    def get_next_task(self, tasks: list[dict[str, Any]]) -> dict[str, Any] | None:
        """Get the next task to execute.
        
        Args:
            tasks: List of tasks
            
        Returns:
            Next task to execute or None if no tasks available
        """
        # Filter pending tasks
        pending_tasks = [t for t in tasks if t.get("status") == "pending"]
        
        if not pending_tasks:
            return None
        
        # Sort by priority (higher first)
        pending_tasks.sort(key=lambda t: t.get("priority", 0), reverse=True)
        return pending_tasks[0]

    def mark_completed(
        self,
        tasks: list[dict[str, Any]],
        task_id: str,
    ) -> list[dict[str, Any]]:
        """Mark a task as completed.
        
        Args:
            tasks: Task list
            task_id: ID of task to mark as completed
            
        Returns:
            Updated task list
        """
        for task in tasks:
            if task.get("id") == task_id:
                task["status"] = "completed"
        return tasks

    def _get_system_prompt(self) -> str:
        """Get system prompt for task creation."""
        return """You are a task management agent. Create actionable research tasks from a research plan.

Each task should have:
- id: Unique identifier
- description: Clear task description
- type: Type of task (search, fetch, analyze, synthesize)
- priority: Priority level (1-5, 5 being highest)
- status: Task status (pending, in_progress, completed)
- dependencies: List of task IDs this depends on

Output JSON format:
{
    "tasks": [
        {
            "id": "task_1",
            "description": "Search for X",
            "type": "search",
            "priority": 5,
            "status": "pending",
            "dependencies": []
        }
    ]
}"""

    def _get_update_prompt(self) -> str:
        """Get system prompt for task updates."""
        return """You are a task management agent. Update the task list based on completed work and new findings.

Consider:
1. Mark completed tasks
2. Add new tasks if needed based on findings
3. Adjust priorities based on results
4. Remove redundant tasks

Output the updated task list in the same JSON format."""

    def _get_update_user_prompt(self) -> str:
        """Get user prompt for task updates."""
        return """Current Tasks:
{current_tasks}

Completed Task:
{completed_task}

Results:
{results}

Update the task list accordingly."""
