# gh-security-scan

Investigate a security vulnerability across GitHub Enterprise / Organization / Repository.

## Input

$ARGUMENTS

The user provides:
1. **Scope** — one of: `--enterprise <name>`, `--org <owner>`, or `--repo <owner/repo>`
2. **Topic** — a description of the security concern to investigate (e.g. compromised package name, CVE ID, vulnerability details)

Examples:
- `/gh-security-scan --enterprise acme "axios npm compromise: check for axios@1.14.1 or axios@0.30.4 in lockfiles"`
- `/gh-security-scan --org my-org "CVE-2025-12345: log4j vulnerable versions 2.0-2.14.1"`
- `/gh-security-scan --repo my-org/my-app "Check for exposed AWS credentials in config files"`

## Language

Detect the language of the user's request. If the user wrote in Japanese, write ALL issue titles, issue bodies, and comments in Japanese. If the user wrote in English, write everything in English. Maintain the same language throughout the entire workflow.

## Workflow

### Phase 1: Understand the scope and build the target list

1. **If `--enterprise` is specified:**
   - Run `gh api /enterprises/{enterprise}/organizations --paginate` (or equivalent) to list all orgs.
   - For each org, run `gh api /orgs/{org}/repos --paginate -q '.[].full_name'` to list all repos.

2. **If `--org` is specified:**
   - Run `gh api /orgs/{org}/repos --paginate -q '.[].full_name'` to list all repos.

3. **If `--repo` is specified:**
   - The target list is just that single repo.

Report the total count of orgs and repos to the user before proceeding.

### Phase 2: Create the tracking issue

Create a **main tracking issue** in the first org's `.github` repo (or a repo the user specifies):

```
gh issue create --repo {owner}/.github \
  --title "[Security] {short topic summary}" \
  --body "$(cat <<'EOF'
## Overview

{topic description}

## Scope

- Enterprise/Org: {name}
- Total organizations: {count}
- Total repositories: {count}

## Investigation checklist

(This will be updated as sub-issues are created)

EOF
)"
```

Store the created issue number and URL.

### Phase 3: Investigate each org/repo

For each organization in scope:

1. **Create a sub-issue** per org in that org's `.github` repo (or the same repo as the main issue if org-level repos are not accessible):

```
gh issue create --repo {org}/.github \
  --title "[Security] {short topic} - {org}" \
  --body "Parent: {main_issue_url}

## Scope
Repositories in {org}: {count}

## Results
(Investigation in progress...)
"
```

2. **Investigate each repo** in the org:
   - Clone or use `gh api` to search for relevant files (lockfiles, config files, source code) depending on the topic.
   - Common investigation patterns:
     - **npm compromise**: Search `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` for the compromised package/version. Also check for the malicious dependency.
     - **CVE check**: Search dependency files for vulnerable library versions.
     - **Credential exposure**: Search config files and source for patterns matching secrets.
   - Use `gh api /search/code` when possible for efficiency:
     ```
     gh api '/search/code?q={query}+org:{org}' --paginate
     ```
   - For deeper investigation, clone the repo and search locally.

3. **Comment the results** on the org's sub-issue:

```
gh issue comment {sub_issue_number} --repo {org}/.github \
  --body "$(cat <<'EOF'
## Investigation Results for {org}

### Summary
- Repositories scanned: {count}
- Affected repositories: {count}

### Details

| Repository | Status | Details |
|------------|--------|---------|
| repo-a | OK | No affected files found |
| repo-b | AFFECTED | Found in yarn.lock line 1234 |

### Recommended Actions
(if affected, list specific remediation steps)

EOF
)"
```

4. **Update the main issue** with a summary comment and update the checklist in the body.

### Phase 4: Final summary

After all orgs/repos are scanned:

1. **Comment on the main issue** with the full summary:
   - Total repos scanned
   - Total repos affected
   - List of affected repos with links to sub-issues
   - Recommended next steps

2. **Close sub-issues** for orgs that are confirmed not affected (with a comment explaining the result).

3. **Report to the user** with a final summary and the main issue URL.

## Important notes

- Use `gh` CLI for all GitHub API interactions.
- Paginate all API calls to ensure completeness.
- If the GitHub API rate limit is approached, pause and inform the user.
- If a `.github` repo does not exist in an org, create the sub-issue in the first available repo in that org, or fall back to the main issue's repo.
- For large enterprises (100+ repos), batch the work and provide progress updates.
- Do NOT skip archived repos — they may still contain evidence of past exposure.
- When investigating, be thorough: check all branches if the topic warrants it, but default to the default branch for efficiency.
- Use sub-issues feature (`gh issue create --parent`) if available, otherwise link issues manually via body text.
