# Changelog

All notable changes to the Universal AI Failure Database are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- Initial public release of database structure and tooling

---

## [1.0.0] — 2025-06-01

### Added
- Core database schema for all five failure categories
- 500+ curated failure entries across hallucination, math, logic, legal, and vulnerability categories
- Command-line query tool (`tools/query.py`)
- JSON schema validator (`tools/validate.py`)
- Export tool supporting CSV, JSONL, and Parquet formats
- Statistics generator (`tools/stats.py`)
- Full documentation suite (README, CONTRIBUTING, SECURITY, DONATE)
- GitHub Actions CI pipeline for PR validation
- Issue templates for new entries, verification requests, and bug reports
- CC0 data license for maximum reusability
- MIT license for tooling
- Example Jupyter notebook for data analysis (`examples/analysis-notebook.ipynb`)

### Data Coverage
- 120+ hallucination entries
- 90+ math error entries
- 85+ logic error entries
- 70+ legal error entries
- 140+ vulnerability entries
- 18 distinct AI models covered
- Date range: 2020–2025
