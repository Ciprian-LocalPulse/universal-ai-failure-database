#!/usr/bin/env python3
"""
Universal AI Failure Database — Query Tool
==========================================
Search, filter, and export entries from the UAIFD.

Usage:
    python tools/query.py --category hallucination
    python tools/query.py --model gpt-4
    python tools/query.py --severity critical
    python tools/query.py --search "fabricated citation"
    python tools/query.py --format csv --output results.csv
"""

import json
import sys
import os
import csv
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()

DATA_DIR = Path(__file__).parent.parent / "data"

CATEGORIES = {
    "hallucination": DATA_DIR / "hallucinations",
    "hallucinations": DATA_DIR / "hallucinations",
    "math-error": DATA_DIR / "math-errors",
    "math-errors": DATA_DIR / "math-errors",
    "logic-error": DATA_DIR / "logic-errors",
    "logic-errors": DATA_DIR / "logic-errors",
    "legal-error": DATA_DIR / "legal-errors",
    "legal-errors": DATA_DIR / "legal-errors",
    "vulnerability": DATA_DIR / "vulnerabilities",
    "vulnerabilities": DATA_DIR / "vulnerabilities",
}


def load_all_entries() -> list[dict]:
    """Load all JSON entries from all data subdirectories."""
    entries = []
    for subdir in DATA_DIR.iterdir():
        if subdir.is_dir():
            for json_file in subdir.glob("*.json"):
                try:
                    with open(json_file, encoding="utf-8") as f:
                        entry = json.load(f)
                        entry["_file"] = str(json_file.relative_to(DATA_DIR.parent))
                        entries.append(entry)
                except (json.JSONDecodeError, OSError) as e:
                    console.print(f"[yellow]Warning: Could not load {json_file}: {e}[/yellow]")
    return entries


def filter_entries(
    entries: list[dict],
    category: Optional[str] = None,
    model: Optional[str] = None,
    severity: Optional[str] = None,
    provider: Optional[str] = None,
    verified: Optional[bool] = None,
    search: Optional[str] = None,
    tags: Optional[list[str]] = None,
) -> list[dict]:
    """Apply filters to the entry list."""
    results = entries

    if category:
        cat_norm = category.lower().rstrip("s")
        results = [
            e for e in results
            if e.get("category", "").lower().rstrip("s") == cat_norm
        ]

    if model:
        model_lower = model.lower()
        results = [
            e for e in results
            if model_lower in e.get("model", {}).get("name", "").lower()
        ]

    if provider:
        provider_lower = provider.lower()
        results = [
            e for e in results
            if provider_lower in e.get("model", {}).get("provider", "").lower()
        ]

    if severity:
        results = [
            e for e in results
            if e.get("severity", "").lower() == severity.lower()
        ]

    if verified is not None:
        results = [e for e in results if e.get("verified") == verified]

    if search:
        search_lower = search.lower()
        results = [
            e for e in results
            if (
                search_lower in json.dumps(e).lower()
            )
        ]

    if tags:
        for tag in tags:
            results = [
                e for e in results
                if tag.lower() in [t.lower() for t in e.get("tags", [])]
            ]

    return results


def display_table(entries: list[dict]) -> None:
    """Display entries as a rich table."""
    table = Table(title=f"UAIFD — {len(entries)} result(s)", show_lines=True)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Category", style="magenta")
    table.add_column("Severity", style="bold")
    table.add_column("Model", style="green")
    table.add_column("Subcategory")
    table.add_column("Verified", justify="center")

    severity_colors = {
        "critical": "[red]critical[/red]",
        "high": "[orange3]high[/orange3]",
        "medium": "[yellow]medium[/yellow]",
        "low": "[dim]low[/dim]",
    }

    for e in entries:
        sev = e.get("severity", "unknown").lower()
        sev_display = severity_colors.get(sev, sev)
        verified_display = "✓" if e.get("verified") else "○"
        table.add_row(
            e.get("id", "PENDING"),
            e.get("category", ""),
            sev_display,
            e.get("model", {}).get("name", "unknown"),
            e.get("subcategory", ""),
            verified_display,
        )

    console.print(table)


def export_csv(entries: list[dict], output_path: str) -> None:
    """Export entries to CSV."""
    if not entries:
        console.print("[yellow]No entries to export.[/yellow]")
        return

    fieldnames = [
        "id", "category", "subcategory", "severity",
        "model_name", "model_provider", "model_api_date",
        "prompt", "failure_type", "failure_description",
        "impact", "verified", "submission_date", "tags"
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for e in entries:
            writer.writerow({
                "id": e.get("id", ""),
                "category": e.get("category", ""),
                "subcategory": e.get("subcategory", ""),
                "severity": e.get("severity", ""),
                "model_name": e.get("model", {}).get("name", ""),
                "model_provider": e.get("model", {}).get("provider", ""),
                "model_api_date": e.get("model", {}).get("api_date", ""),
                "prompt": e.get("prompt", ""),
                "failure_type": e.get("failure_analysis", {}).get("type", ""),
                "failure_description": e.get("failure_analysis", {}).get("description", ""),
                "impact": e.get("impact", ""),
                "verified": e.get("verified", False),
                "submission_date": e.get("submission_date", ""),
                "tags": ", ".join(e.get("tags", [])),
            })

    console.print(f"[green]Exported {len(entries)} entries to {output_path}[/green]")


def export_jsonl(entries: list[dict], output_path: str) -> None:
    """Export entries to JSONL (one JSON object per line)."""
    with open(output_path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    console.print(f"[green]Exported {len(entries)} entries to {output_path}[/green]")


@click.command()
@click.option("--category", "-c", help="Filter by category (hallucination, math-error, logic-error, legal-error, vulnerability)")
@click.option("--model", "-m", help="Filter by model name (partial match, case-insensitive)")
@click.option("--provider", "-p", help="Filter by provider (partial match, case-insensitive)")
@click.option("--severity", "-s", help="Filter by severity (critical, high, medium, low)")
@click.option("--verified/--unverified", default=None, help="Filter by verification status")
@click.option("--search", help="Full-text search across all fields")
@click.option("--tag", "tags", multiple=True, help="Filter by tag (can be used multiple times)")
@click.option("--format", "output_format", default="table", type=click.Choice(["table", "json", "csv", "jsonl"]), help="Output format")
@click.option("--output", "-o", help="Output file path (for csv/jsonl formats)")
@click.option("--limit", "-n", default=50, help="Maximum number of results to display (default: 50)")
@click.option("--show-prompt", is_flag=True, help="Show full prompt and response in output")
def main(
    category, model, provider, severity, verified, search, tags,
    output_format, output, limit, show_prompt
):
    """Query the Universal AI Failure Database."""

    console.print("[bold blue]Universal AI Failure Database — Query Tool[/bold blue]")
    console.print(f"Loading entries from [dim]{DATA_DIR}[/dim]...\n")

    all_entries = load_all_entries()

    if not all_entries:
        console.print("[yellow]No entries found. Ensure the data/ directory contains JSON files.[/yellow]")
        sys.exit(0)

    filtered = filter_entries(
        all_entries,
        category=category,
        model=model,
        severity=severity,
        provider=provider,
        verified=verified,
        search=search,
        tags=list(tags) if tags else None,
    )

    console.print(f"Found [bold]{len(filtered)}[/bold] matching entries out of {len(all_entries)} total.\n")

    if output_format == "table":
        display_table(filtered[:limit])
        if len(filtered) > limit:
            console.print(f"\n[dim]Showing first {limit} results. Use --limit to adjust.[/dim]")

        if show_prompt and filtered:
            for entry in filtered[:5]:
                console.rule(f"[bold]{entry.get('id', 'PENDING')}[/bold]")
                console.print(f"[bold]Prompt:[/bold] {entry.get('prompt', 'N/A')}")
                console.print(f"[bold]Response:[/bold] {entry.get('response', 'N/A')}")
                console.print(f"[bold]Analysis:[/bold] {entry.get('failure_analysis', {}).get('description', 'N/A')}")
                console.print()

    elif output_format == "json":
        print(json.dumps(filtered[:limit], indent=2, ensure_ascii=False))

    elif output_format == "csv":
        out = output or "uaifd-export.csv"
        export_csv(filtered, out)

    elif output_format == "jsonl":
        out = output or "uaifd-export.jsonl"
        export_jsonl(filtered, out)


if __name__ == "__main__":
    main()
