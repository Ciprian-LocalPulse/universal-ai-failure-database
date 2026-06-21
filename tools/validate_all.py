#!/usr/bin/env python3
"""
Validate all entries in the UAIFD database.

Usage:
    python tools/validate_all.py
    python tools/validate_all.py --category hallucinations
    python tools/validate_all.py --fail-fast
"""

import sys
from pathlib import Path
import click
from rich.console import Console
from rich.progress import track

sys.path.insert(0, str(Path(__file__).parent))
from validate import validate_file

console = Console()
DATA_DIR = Path(__file__).parent.parent / "data"


@click.command()
@click.option("--category", help="Validate only a specific category subdirectory")
@click.option("--fail-fast", is_flag=True, help="Stop on first error")
@click.option("--show-valid", is_flag=True, help="Print valid entries too")
def main(category, fail_fast, show_valid):
    """Validate all entries in the UAIFD database."""

    if category:
        dirs = [DATA_DIR / category]
    else:
        dirs = [d for d in DATA_DIR.iterdir() if d.is_dir()]

    all_files = []
    for d in dirs:
        all_files.extend(list(d.glob("*.json")))

    if not all_files:
        console.print("[yellow]No JSON files found.[/yellow]")
        sys.exit(0)

    console.print(f"[bold]Validating {len(all_files)} entries...[/bold]\n")

    valid_count = 0
    error_count = 0
    all_errors = []

    for filepath in track(all_files, description="Validating..."):
        is_valid, errors = validate_file(filepath)
        if is_valid:
            valid_count += 1
            if show_valid:
                console.print(f"  [green]✓[/green] {filepath.name}")
        else:
            error_count += 1
            all_errors.append((filepath, errors))
            if fail_fast:
                console.print(f"\n[red]✗ FAIL: {filepath}[/red]")
                for err in errors:
                    console.print(f"    {err}")
                sys.exit(1)

    console.print(f"\n[bold]Results:[/bold]")
    console.print(f"  [green]✓ Valid:   {valid_count}[/green]")
    console.print(f"  [red]✗ Invalid: {error_count}[/red]")

    if all_errors:
        console.print("\n[bold red]Errors:[/bold red]")
        for filepath, errors in all_errors:
            console.print(f"\n  [bold]{filepath.name}[/bold]")
            for err in errors:
                console.print(f"    [red]•[/red] {err}")
        sys.exit(1)
    else:
        console.print("\n[bold green]All entries are valid.[/bold green]")
        sys.exit(0)


if __name__ == "__main__":
    main()
