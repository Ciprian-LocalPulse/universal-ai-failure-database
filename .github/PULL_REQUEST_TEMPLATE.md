# Pull Request — UAIFD Entry Submission

## Type of Change
- [ ] New entry (or multiple entries)
- [ ] Entry correction
- [ ] Tooling improvement
- [ ] Documentation update
- [ ] Other

## Entries Affected
<!-- List the entry IDs (or PENDING for new entries) -->

## Checklist

### For new entries:
- [ ] Entry follows the JSON schema for its category
- [ ] `id` is set to `"PENDING"` (maintainers assign IDs on merge)
- [ ] Prompt and response are accurately and completely reproduced
- [ ] Failure analysis is substantive (not just "this is wrong" — explains why and how verified)
- [ ] Severity rating follows the [severity guide](docs/severity-guide.md)
- [ ] No PII in any field
- [ ] `validated.py` passes locally: `python tools/validate.py path/to/my/entry.json`
- [ ] `license` field is `"CC0-1.0"`
- [ ] For vulnerabilities: responsible disclosure confirmed (not an active unpatched exploit)

### For all PRs:
- [ ] I have read [CONTRIBUTING.md](CONTRIBUTING.md)
- [ ] CI checks pass (or I understand why they fail and have explained below)

## Description
<!-- Brief description of what this PR adds or changes -->

## Verification Method
<!-- For new entries: how did you verify the failure? For corrections: what is your source? -->
