# Security Policy

## Scope

This security policy governs submissions to the **vulnerability** category of the Universal AI Failure Database and applies to any active security weaknesses in AI systems that have not yet been publicly disclosed or patched.

---

## Responsible Disclosure

We are committed to responsible disclosure. If your submission documents an **active, unpatched vulnerability** in a production AI system:

1. **Do not open a public Pull Request or Issue.**
2. Contact the affected vendor's security team directly first.
3. Allow a reasonable remediation period (90 days is standard).
4. After the vendor has patched or publicly acknowledged the issue, submit your entry here.

---

## Submitting Vulnerability Entries

Vulnerability entries that document **already-disclosed** or **patched** issues, or issues where the affected model/system has been notified, are welcome through the standard PR process.

For entries where you are uncertain about disclosure status, open a **private Discussion** (if available) or contact maintainers via the contact method listed in the repository.

---

## Categories of Accepted Vulnerability Entries

- Successful prompt injection attacks (against patched or publicly known vectors)
- Jailbreak techniques that have been publicly demonstrated
- Data extraction methods (without including any extracted private data)
- Safety filter bypass demonstrations
- Model inversion or membership inference (conceptual/reproduced, no live data)

---

## What Not to Include

- Actual extracted private data or PII from any model
- Live working exploits for unpatched production systems
- Content that could enable harm by others (e.g., working CSAM-generating prompts)

---

## Contact

For private security communications: open a GitHub Discussion marked `[PRIVATE-SECURITY]` or contact the maintainers directly through GitHub.
