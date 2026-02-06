"""Command-line interface for the Agentic Research System."""

import asyncio
import argparse
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.main import AgenticResearchSystem
from src.config import ResearchConfig


console = Console()


async def run_research(
    query: str,
    provider: str = "openai",
    max_iterations: int = 5,
    enable_rag: bool = True,
    verbose: bool = False,
) -> None:
    """Run research and display results.
    
    Args:
        query: Research query
        provider: LLM provider
        max_iterations: Maximum research iterations
        enable_rag: Enable RAG
        verbose: Enable verbose output
    """
    # Create configuration
    config = ResearchConfig(
        llm_provider=provider,
        max_iterations=max_iterations,
        enable_rag=enable_rag,
        verbose=verbose,
    )
    
    # Initialize system
    system = AgenticResearchSystem(config=config)
    
    # Show progress
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"[cyan]Researching: {query[:60]}...", total=None)
        
        # Run research
        result = await system.research(query)
        
        progress.update(task, completed=True)
    
    # Display results
    if result.get("error"):
        console.print(f"\n[red]Error:[/red] {result['error']}")
        sys.exit(1)
    
    # Display report
    if result.get("report"):
        console.print("\n" + "="*80)
        console.print("[bold cyan]RESEARCH REPORT[/bold cyan]")
        console.print("="*80 + "\n")
        
        # Render markdown
        md = Markdown(result["report"])
        console.print(md)
    
    # Display statistics if verbose
    if verbose:
        console.print("\n" + "="*80)
        console.print("[bold]Research Statistics[/bold]")
        console.print("="*80)
        console.print(f"Iterations: {result.get('iteration', 0)}")
        console.print(f"Search Results: {len(result.get('search_results', []))}")
        console.print(f"Documents Processed: {len(result.get('documents', []))}")


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Agentic Research System - AI-powered research assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "query",
        type=str,
        help="Research query",
    )
    
    parser.add_argument(
        "--provider",
        type=str,
        choices=["openai", "anthropic"],
        default="openai",
        help="LLM provider to use (default: openai)",
    )
    
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=5,
        help="Maximum research iterations (default: 5)",
    )
    
    parser.add_argument(
        "--no-rag",
        action="store_true",
        help="Disable RAG system",
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )
    
    args = parser.parse_args()
    
    # Display header
    console.print("\n[bold cyan]Agentic Research System[/bold cyan]")
    console.print(f"Provider: {args.provider}")
    console.print(f"Query: {args.query}\n")
    
    # Run research
    try:
        asyncio.run(run_research(
            query=args.query,
            provider=args.provider,
            max_iterations=args.max_iterations,
            enable_rag=not args.no_rag,
            verbose=args.verbose,
        ))
    except KeyboardInterrupt:
        console.print("\n[yellow]Research interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Unexpected error:[/red] {e}")
        if args.verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
