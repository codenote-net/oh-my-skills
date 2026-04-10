---
name: gh-security-scan
description: Investigate security vulnerabilities across GitHub Enterprise, organization, or repository scopes, create tracking issues, and report findings. Use when Codex is asked to scan GitHub repos for compromised packages, CVEs, or credential exposure.
---

# GH Security Scan

## Overview

Investigate a security concern across GitHub Enterprise, organization, or repository scope.
Build the target list, create tracking issues, inspect repositories, and summarize findings.

Prefer the GitHub app tools available in Codex. Use `gh api` when thread-level issue operations or bulk API access are faster or more complete.

## Input

The user should provide:

1. Scope: one of `--enterprise <name>`, `--org <owner>`, or `--repo <owner/repo>`
2. Topic: a description of the security concern to investigate

Examples:

- `Use $codenote:gh-security-scan with --enterprise acme "axios compromise: check for axios@1.14.1 or axios@0.30.4 in lockfiles"`
- `Use $codenote:gh-security-scan with --org my-org "CVE-2025-12345: check for vulnerable versions"`
- `Use $codenote:gh-security-scan with --repo my-org/my-app "Search for hardcoded API keys"`

## Language

Detect the language of the user's request.
If the request is in Japanese, write issue titles, issue bodies, comments, and the final user-facing summary in Japanese.
If the request is in English, keep the workflow in English.

## Workflow

Execute the phases in order.

### 1. Validate Scope and Build Targets

If `--enterprise` is specified:

- Enumerate organizations under the enterprise.
- Enumerate repositories under each organization.

If `--org` is specified:

- Enumerate repositories under the organization.

If `--repo` is specified:

- The target list is that single repository.

Before scanning, report the total counts of organizations and repositories to the user.

### 2. Create the Tracking Structure

Create a main tracking issue in the first reachable `.github` repository, or another repository explicitly requested by the user.

The main issue should contain:

- Overview of the topic
- Scope summary
- Organization count
- Repository count
- Investigation checklist

Store the issue URL and number.

### 3. Investigate Each Organization or Repository

For each organization in scope:

- Create one sub-issue per organization if issue creation is possible.
- If sub-issues are unavailable, create a normal linked issue and reference the parent manually.

For each repository:

- Search relevant manifests, lockfiles, config files, and source code.
- Prefer API/code search for broad sweeps.
- Clone locally only when deeper inspection is required.

Common patterns:

- npm compromise: inspect `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, and suspicious transitive dependencies
- CVE checks: inspect language-specific manifests, lockfiles, Dockerfiles, and CI version pins
- Credential exposure: inspect `.env`, config files, and source for secret-like patterns

For each organization or repository grouping, comment results with:

- Repositories scanned
- Affected repositories
- Evidence
- Recommended remediation

Update the main issue checklist as progress is made.

### 4. Finalize

After all targets are scanned:

- Post a final summary comment on the main issue
- Close sub-issues that are confirmed not affected when appropriate
- Report the overall result to the user with the main issue URL

## Important Notes

- Paginate all GitHub API requests.
- Do not skip archived repositories unless the user explicitly narrows scope.
- Default to the default branch for efficiency, but widen scope if the incident requires it.
- If rate limiting becomes a risk, pause and report that constraint to the user.
- If a `.github` repository does not exist, fall back to another writable repository in the same organization.

## Resources

- `references/investigation-patterns-guide.md`: concrete search patterns and remediation guidance
