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
    verbose: bool = False,
) -> None:
    """Run research and display results."""
    config = ResearchConfig(
        llm_provider=provider,
        verbose=verbose,
    )

    system = AgenticResearchSystem(config=config)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"[cyan]Researching: {query[:60]}...", total=None
        )
        result = await system.research(query)
        progress.update(task, completed=True)

    if result.get("error"):
        console.print(f"\n[red]Error:[/red] {result['error']}")
        sys.exit(1)

    if result.get("report"):
        console.print("\n" + "=" * 80)
        console.print("[bold cyan]RESEARCH REPORT[/bold cyan]")
        console.print("=" * 80 + "\n")
        md = Markdown(result["report"])
        console.print(md)

    if verbose:
        console.print("\n" + "=" * 80)
        console.print("[bold]Research Statistics[/bold]")
        console.print("=" * 80)
        console.print(f"Findings length: {len(result.get('findings', ''))} chars")
        console.print(f"Report length: {len(result.get('report', ''))} chars")


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Agentic Research System - AI-powered deep research assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("query", type=str, help="Research query")

    parser.add_argument(
        "--provider",
        type=str,
        choices=["openai", "anthropic"],
        default="openai",
        help="LLM provider (default: openai)",
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    console.print("\n[bold cyan]Agentic Research System[/bold cyan]")
    console.print(f"Provider: {args.provider}")
    console.print(f"Query: {args.query}\n")

    try:
        asyncio.run(
            run_research(
                query=args.query,
                provider=args.provider,
                verbose=args.verbose,
            )
        )
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
