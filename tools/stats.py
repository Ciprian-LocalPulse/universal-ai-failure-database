#!/usr/bin/env python3
"""
Generate statistics about the UAIFD database.

Usage:
    python tools/stats.py
    python tools/stats.py --json
"""

import json
import sys
from pathlib import Path
from collections import Counter
import click
from rich.console import Console
from rich.table import Table

console = Console()
DATA_DIR = Path(__file__).parent.parent / "data"


def load_all():
    entries = []
    for d in DATA_DIR.iterdir():
        if d.is_dir():
            for f in d.glob("*.json"):
                try:
                    entries.append(json.loads(f.read_text(encoding="utf-8")))
                except Exception:
                    pass
    return entries


@click.command()
@click.option("--json", "as_json", is_flag=True, help="Output stats as JSON")
def main(as_json):
    """Print database statistics."""
    entries = load_all()

    if not entries:
        console.print("[yellow]No entries found.[/yellow]")
        sys.exit(0)

    stats = {
        "total": len(entries),
        "verified": sum(1 for e in entries if e.get("verified")),
        "unverified": sum(1 for e in entries if not e.get("verified")),
        "by_category": dict(Counter(e.get("category", "unknown") for e in entries)),
        "by_severity": dict(Counter(e.get("severity", "unknown") for e in entries)),
        "by_provider": dict(Counter(e.get("model", {}).get("provider", "unknown") for e in entries)),
        "by_model": dict(Counter(e.get("model", {}).get("name", "unknown") for e in entries)),
        "unique_models": len(set(e.get("model", {}).get("name", "") for e in entries)),
        "unique_providers": len(set(e.get("model", {}).get("provider", "") for e in entries)),
    }

    all_tags = []
    for e in entries:
        all_tags.extend(e.get("tags", []))
    stats["top_tags"] = dict(Counter(all_tags).most_common(10))

    if as_json:
        print(json.dumps(stats, indent=2))
        return

    console.print("[bold blue]Universal AI Failure Database — Statistics[/bold blue]\n")

    # Overview
    t = Table(show_header=False, box=None)
    t.add_column(style="bold", width=25)
    t.add_column()
    t.add_row("Total entries", str(stats["total"]))
    t.add_row("Verified", f"[green]{stats['verified']}[/green]")
    t.add_row("Unverified", f"[yellow]{stats['unverified']}[/yellow]")
    t.add_row("Unique models", str(stats["unique_models"]))
    t.add_row("Unique providers", str(stats["unique_providers"]))
    console.print(t)
    console.print()

    # By category
    cat_table = Table(title="By Category", show_lines=True)
    cat_table.add_column("Category", style="magenta")
    cat_table.add_column("Count", justify="right")
    for cat, count in sorted(stats["by_category"].items(), key=lambda x: -x[1]):
        cat_table.add_row(cat, str(count))
    console.print(cat_table)
    console.print()

    # By severity
    sev_table = Table(title="By Severity", show_lines=True)
    sev_table.add_column("Severity", style="bold")
    sev_table.add_column("Count", justify="right")
    sev_order = ["critical", "high", "medium", "low"]
    for sev in sev_order:
        count = stats["by_severity"].get(sev, 0)
        color = {"critical": "red", "high": "orange3", "medium": "yellow", "low": "dim"}.get(sev, "white")
        sev_table.add_row(f"[{color}]{sev}[/{color}]", str(count))
    console.print(sev_table)
    console.print()

    # By provider
    prov_table = Table(title="By Provider (top 10)", show_lines=True)
    prov_table.add_column("Provider", style="cyan")
    prov_table.add_column("Count", justify="right")
    for prov, count in sorted(stats["by_provider"].items(), key=lambda x: -x[1])[:10]:
        prov_table.add_row(prov, str(count))
    console.print(prov_table)
    console.print()

    # Top tags
    tag_table = Table(title="Top Tags", show_lines=True)
    tag_table.add_column("Tag", style="green")
    tag_table.add_column("Count", justify="right")
    for tag, count in stats["top_tags"].items():
        tag_table.add_row(tag, str(count))
    console.print(tag_table)


if __name__ == "__main__":
    main()
