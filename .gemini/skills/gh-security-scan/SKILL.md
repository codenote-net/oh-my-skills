---
name: gh-security-scan
description: "Investigates security vulnerabilities across GitHub Enterprise/Organization/Repository hierarchies, creates tracking issues, and reports findings via the gh CLI."
---

# gh-security-scan

## Overview

A Gemini CLI skill that automates security vulnerability investigation across GitHub Enterprise, Organization, or Repository scopes. It enumerates targets, creates a hierarchical issue structure for tracking, performs the investigation, and reports findings — all via the `gh` CLI.

## Core Capabilities

- **Enterprise-wide scanning**: Enumerate all orgs under an enterprise, then all repos under each org.
- **Org-level scanning**: Enumerate all repos under a specified org.
- **Repo-level scanning**: Investigate a single repository.
- **Automated issue tracking**: Creates a main issue with sub-issues per org/repo for structured tracking.
- **Multilingual support**: Writes issues and comments in the same language as the user's request (English or Japanese).
- **Comprehensive investigation**: Searches lockfiles, dependency manifests, config files, and source code using the GitHub Code Search API.

## Workflow

1. **Parse scope** (enterprise / org / repo) and topic from the user request.
2. **Enumerate target repositories** via the `gh` CLI (`gh repo list` or `gh api`).
3. **Create main tracking issue** in a centralized security repository or the target repository.
4. **Iterate through targets**:
   a. Create sub-issue for each organization (if applicable).
   b. Investigate each repository using search targets defined in [investigation_patterns.md](references/investigation_patterns.md).
   c. Comment results on the corresponding sub-issue or main issue.
   d. Update the main issue checklist.
5. **Post final summary** on the main issue and close non-affected sub-issues.

## Usage

Invoke by asking Gemini CLI to perform a scan:

```
Investigate compromised npm package foo@1.2.3 across the --enterprise acme
Check for vulnerable library versions related to CVE-2025-12345 in the --org my-org
Search for hardcoded API keys in the --repo my-org/my-app
```

## Investigation Patterns

For detailed search targets and remediation steps, see [investigation_patterns.md](references/investigation_patterns.md).

### Summary of Patterns:
- **npm / yarn / pnpm compromise**: Search lockfiles (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`) for specific versions or malicious packages.
- **CVE-based vulnerability**: Search dependency manifests, Dockerfiles, and CI/CD configs for vulnerable versions.
- **Credential exposure**: Search `.env` files, config files, and source code for AWS keys, private keys, or generic secrets.
