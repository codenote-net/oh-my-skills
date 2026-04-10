# Investigation Patterns Guide

## npm Supply Chain Attack

When a npm package is compromised (account hijack, malicious publish), investigate as follows:

### What to search

1. **Lockfiles** — These pin exact versions and are the most reliable indicator:
   - `package-lock.json`: Look for `"version": "<compromised_version>"` and `"resolved"` URLs
   - `yarn.lock`: Look for `<package>@<version>:` entries
   - `pnpm-lock.yaml`: Look for `/<package>/<version>:` entries

2. **Malicious transitive dependencies** — Compromised packages often inject fake dependencies:
   - Search for the malicious dependency name in all lockfiles
   - Check `node_modules/` if committed (rare but possible)

3. **CI/CD artifacts** — If the compromised version was installed in CI:
   - Check CI logs for `npm install` / `yarn install` output
   - Check if `postinstall` scripts ran

### GitHub Code Search API

```bash
# Search for a specific package version across an org
gh api '/search/code?q="axios%401.14.1"+org:my-org&per_page=100' --paginate

# Search for a malicious dependency
gh api '/search/code?q="plain-crypto-js"+org:my-org&per_page=100' --paginate
```

### Remediation steps (if affected)

1. Pin to the last known safe version
2. Remove the malicious transitive dependency
3. Reinstall with `--ignore-scripts` to prevent postinstall execution
4. Investigate if the malicious payload executed (check for RAT artifacts, outbound connections)
5. Rotate all credentials accessible from the affected environment
6. Block the C2 domain at the network level

---

## CVE-based Vulnerability Investigation

### What to search

1. **Dependency manifests** by language:
   - JavaScript: `package.json`, lockfiles
   - Python: `requirements.txt`, `Pipfile.lock`, `poetry.lock`, `pyproject.toml`
   - Ruby: `Gemfile.lock`
   - Java: `pom.xml`, `build.gradle`, `gradle.lockfile`
   - Go: `go.sum`
   - Rust: `Cargo.lock`
   - PHP: `composer.lock`

2. **Container images**:
   - `Dockerfile` for `FROM` base images with known vulnerabilities
   - `docker-compose.yml` for image references

3. **Infrastructure-as-Code**:
   - Terraform files for provider/module versions
   - Helm charts for image tags

### Version matching

When checking versions, consider:
- Exact version match vs. version range
- Whether the lockfile pins a vulnerable version even if `package.json` uses a range
- Pre-release and build metadata suffixes

---

## Credential Exposure Investigation

### Search patterns

```bash
# AWS keys
gh api '/search/code?q=AKIA+org:my-org&per_page=100' --paginate

# Generic API keys/tokens
gh api '/search/code?q=api_key+org:my-org+extension:env&per_page=100' --paginate

# Private keys
gh api '/search/code?q="BEGIN+RSA+PRIVATE+KEY"+org:my-org&per_page=100' --paginate
```

### Common patterns to look for

| Type | Pattern |
|------|---------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` |
| AWS Secret Key | 40-character base64 string |
| GitHub Token | `ghp_[A-Za-z0-9]{36}` |
| Slack Token | `xox[bpras]-[A-Za-z0-9-]+` |
| Generic Secret | `password`, `secret`, `token`, `api_key` in config files |

### Remediation

1. Immediately rotate the exposed credential
2. Check access logs for unauthorized usage
3. Add the file pattern to `.gitignore`
4. Consider using a secrets manager
5. Set up secret scanning (GitHub Advanced Security, git-secrets, etc.)
