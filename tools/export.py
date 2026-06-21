#!/usr/bin/env python3
"""
Export the UAIFD database to various formats.

Usage:
    python tools/export.py --format csv --output dataset.csv
    python tools/export.py --format jsonl --output dataset.jsonl
    python tools/export.py --format parquet --output dataset.parquet
    python tools/export.py --format huggingface --output hf-dataset/
"""

import json
import sys
import csv
from pathlib import Path
import click
from rich.console import Console

console = Console()
DATA_DIR = Path(__file__).parent.parent / "data"


def load_all():
    entries = []
    for d in DATA_DIR.iterdir():
        if d.is_dir():
            for f in d.glob("*.json"):
                try:
                    entries.append(json.loads(f.read_text(encoding="utf-8")))
                except Exception as e:
                    console.print(f"[yellow]Warning: {f.name}: {e}[/yellow]")
    return entries


def flatten_entry(e: dict) -> dict:
    """Flatten nested entry for tabular formats."""
    return {
        "id": e.get("id", ""),
        "category": e.get("category", ""),
        "subcategory": e.get("subcategory", ""),
        "severity": e.get("severity", ""),
        "model_name": e.get("model", {}).get("name", ""),
        "model_version": e.get("model", {}).get("version", ""),
        "model_provider": e.get("model", {}).get("provider", ""),
        "model_api_date": e.get("model", {}).get("api_date", ""),
        "prompt": e.get("prompt", ""),
        "response": e.get("response", ""),
        "failure_type": e.get("failure_analysis", {}).get("type", ""),
        "failure_description": e.get("failure_analysis", {}).get("description", ""),
        "verified_by": e.get("failure_analysis", {}).get("verified_by", ""),
        "impact": e.get("impact", ""),
        "mitigation": e.get("mitigation", ""),
        "tags": "|".join(e.get("tags", [])),
        "submitted_by": e.get("submitted_by", ""),
        "submission_date": e.get("submission_date", ""),
        "verified": e.get("verified", False),
        "verified_date": e.get("verified_date", ""),
        "license": e.get("license", "CC0-1.0"),
    }


@click.command()
@click.option(
    "--format", "fmt",
    type=click.Choice(["csv", "jsonl", "parquet", "huggingface"]),
    default="csv",
    help="Export format"
)
@click.option("--output", "-o", required=True, help="Output path")
@click.option("--verified-only", is_flag=True, help="Export only verified entries")
def main(fmt, output, verified_only):
    """Export the UAIFD database."""

    console.print("[bold]Loading entries...[/bold]")
    entries = load_all()

    if verified_only:
        entries = [e for e in entries if e.get("verified")]
        console.print(f"Filtered to {len(entries)} verified entries.")

    console.print(f"Exporting {len(entries)} entries as [bold]{fmt}[/bold] to [bold]{output}[/bold]...")

    if fmt == "csv":
        flat = [flatten_entry(e) for e in entries]
        with open(output, "w", newline="", encoding="utf-8") as f:
            if flat:
                writer = csv.DictWriter(f, fieldnames=flat[0].keys())
                writer.writeheader()
                writer.writerows(flat)

    elif fmt == "jsonl":
        with open(output, "w", encoding="utf-8") as f:
            for e in entries:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")

    elif fmt == "parquet":
        try:
            import pandas as pd
            flat = [flatten_entry(e) for e in entries]
            df = pd.DataFrame(flat)
            df.to_parquet(output, index=False)
        except ImportError:
            console.print("[red]pandas and pyarrow are required for Parquet export. Run: pip install pandas pyarrow[/red]")
            sys.exit(1)

    elif fmt == "huggingface":
        try:
            import pandas as pd
            out_dir = Path(output)
            out_dir.mkdir(parents=True, exist_ok=True)
            flat = [flatten_entry(e) for e in entries]
            df = pd.DataFrame(flat)
            df.to_parquet(out_dir / "data.parquet", index=False)

            # Write dataset card
            card = """---
license: cc0-1.0
task_categories:
  - text-classification
  - text-generation
language:
  - en
tags:
  - ai-safety
  - hallucination
  - ai-failures
  - llm-evaluation
pretty_name: Universal AI Failure Database (UAIFD)
---

# Universal AI Failure Database

Structured dataset of documented AI model failures.
See https://github.com/yourusername/universal-ai-failure-database for full details.
"""
            (out_dir / "README.md").write_text(card)
        except ImportError:
            console.print("[red]pandas and pyarrow are required for HuggingFace export.[/red]")
            sys.exit(1)

    console.print(f"[green]✓ Export complete.[/green]")


if __name__ == "__main__":
    main()
