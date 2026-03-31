# Investigation Patterns Guide

## npm Supply Chain Attack

When a npm package is compromised, check these first:

1. Lockfiles
   - `package-lock.json`: exact `version` and `resolved`
   - `yarn.lock`: package-version entries
   - `pnpm-lock.yaml`: dependency path entries
2. Malicious transitive dependencies
   - Search for dependency names injected by the compromised package
3. CI and install artifacts
   - Build logs, install scripts, and evidence of `postinstall` execution

Example searches:

```bash
gh api '/search/code?q="axios%401.14.1"+org:my-org&per_page=100' --paginate
gh api '/search/code?q="plain-crypto-js"+org:my-org&per_page=100' --paginate
```

Remediation checklist:

1. Pin to a known-safe version
2. Remove malicious transitive dependencies
3. Reinstall with `--ignore-scripts` when relevant
4. Investigate execution artifacts and outbound traffic
5. Rotate reachable credentials

## CVE-Based Vulnerability Investigation

Inspect:

- JavaScript: `package.json`, lockfiles
- Python: `requirements.txt`, `Pipfile.lock`, `poetry.lock`, `pyproject.toml`
- Ruby: `Gemfile.lock`
- Java: `pom.xml`, `build.gradle`, `gradle.lockfile`
- Go: `go.sum`
- Rust: `Cargo.lock`
- PHP: `composer.lock`
- Containers: `Dockerfile`, `docker-compose.yml`
- IaC: Terraform and Helm files

Version checks should account for:

- Exact versions versus ranges
- Lockfile pins overriding a loose manifest range
- Pre-release suffixes and build metadata

## Credential Exposure Investigation

Example searches:

```bash
gh api '/search/code?q=AKIA+org:my-org&per_page=100' --paginate
gh api '/search/code?q=api_key+org:my-org+extension:env&per_page=100' --paginate
gh api '/search/code?q="BEGIN+RSA+PRIVATE+KEY"+org:my-org&per_page=100' --paginate
```

Common patterns:

| Type | Pattern |
|------|---------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` |
| GitHub Token | `ghp_[A-Za-z0-9]{36}` |
| Slack Token | `xox[bpras]-[A-Za-z0-9-]+` |
| Generic Secret | `password`, `secret`, `token`, `api_key` in config files |

Remediation checklist:

1. Rotate the exposed credential
2. Review access logs
3. Remove or gitignore the committed secret source
4. Move secrets to a managed secret store
5. Enable secret scanning where possible
