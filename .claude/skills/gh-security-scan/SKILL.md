---
name: gh-security-scan
description: "Investigates security vulnerabilities across GitHub Enterprise/Organization/Repository hierarchies, creates tracking issues, and reports findings"
---

# gh-security-scan

## Overview

A Claude Code skill that automates security vulnerability investigation across GitHub Enterprise, Organization, or Repository scopes. It enumerates targets, creates a hierarchical issue structure for tracking, performs the investigation, and reports findings — all via the `gh` CLI.

## Core Capabilities

- **Enterprise-wide scanning**: Enumerate all orgs under an enterprise, then all repos under each org
- **Org-level scanning**: Enumerate all repos under a specified org
- **Repo-level scanning**: Investigate a single repository
- **Automated issue tracking**: Creates a main issue with sub-issues per org/repo
- **Multilingual support**: Writes issues and comments in the same language as the user's request (English or Japanese)
- **Comprehensive investigation**: Searches lockfiles, dependency manifests, config files, and source code

## Workflow

```
1. Parse scope (enterprise / org / repo) and topic
2. Enumerate target repositories via GitHub API
3. Create main tracking issue
4. For each org:
   a. Create sub-issue
   b. Investigate each repo (search code, lockfiles, configs)
   c. Comment results on sub-issue
   d. Update main issue checklist
5. Post final summary on main issue
6. Close non-affected sub-issues
```

## Usage

Invoke via Claude Code:

```
/gh-security-scan --enterprise acme "Investigate compromised npm package foo@1.2.3"
/gh-security-scan --org my-org "CVE-2025-12345: Check for vulnerable library versions"
/gh-security-scan --repo my-org/my-app "Search for hardcoded API keys"
```

## Resources

- **Command file**: `/.claude/commands/gh-security-scan.md`
- **References**: `references/` — guides for common investigation patterns

## Investigation Patterns

### npm / yarn / pnpm compromise

Search targets:
- `package-lock.json` for `"resolved"` URLs or version strings
- `yarn.lock` for package entries
- `pnpm-lock.yaml` for dependency entries
- `node_modules/` for malicious packages (rare in repos, but possible)

### CVE-based vulnerability

Search targets:
- Language-specific lockfiles and manifests
- Docker images (`Dockerfile`, `docker-compose.yml`)
- CI/CD configs for pinned tool versions

### Credential exposure

Search targets:
- `.env` files (should be gitignored but sometimes committed)
- Config files with hardcoded tokens
- Source code with API keys or connection strings
