## AUTH_TOKENS_POLICY.md

Purpose
-------
Short, actionable policy for generating, storing, and rotating GitHub authentication tokens used by AIOS agents and tooling (MCP, CLI, integration tests, local dev). Designed for safe, least-privilege operational use.

Token Types
-----------
- Fine‑grained Personal Access Tokens (recommended): Scope-limited to specific repositories/orgs, choose only required permissions.
- Classic Personal Access Tokens (legacy): Broad account-level scopes; avoid for agentic automation when possible.
- GitHub App tokens: Best for organization-level automation; support fine-grained permissions and SAML SSO authorization.
- GITHUB_TOKEN (Actions): Use inside GitHub Actions workflows; grant permissions via `permissions:` in workflow YAML.

Generation (developer steps)
---------------------------
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Fine‑grained tokens.
2. Choose the repository scope and grant only required permissions (e.g., Issues: read/write, Pull requests: read/write, Contents: read if needed).
3. Copy the token to clipboard immediately; you won't be able to view it again.

Storage and Usage
-----------------
- Local development: store tokens in OS credential managers (Windows Credential Manager, macOS Keychain, Linux Secret Service) or a local password manager. Avoid plaintext in files.
- CI/CD & automation: store tokens in pipeline secrets (GitHub Secrets, Azure Key Vault, HashiCorp Vault). Use the secret name in workflows.
- VS Code / MCP local config: use workspace input prompts that mark the value as password and prefer `env` or OS keyring when possible.
- Do NOT commit tokens to git or store them in plaintext in repo files.

SAML SSO and Organization Access
--------------------------------
- Fine‑grained PATs are authorized during creation for SAML‑enforced orgs. Classic PATs may require explicit SSO authorization after creation; if you receive `403` with an `X-GitHub-SSO` header, follow the provided URL to authorize.

Rotation & Revocation
---------------------
- Rotate tokens on a schedule (recommended: every 90 days) or immediately on suspected exposure.
- Use distinct tokens per integration/service to allow per-service revocation.

Least Privilege & Auditing
--------------------------
- Grant the minimum permissions needed; prefer repository-scoped fine‑grained tokens.
- Track token usage and owners in a simple registry file or internal wiki (owner, purpose, created, last rotated, expiry).

Examples (curl / gh)
---------------------
Curl example:

```
curl --request GET \
  --url "https://api.github.com/repos/<owner>/<repo>" \
  --header "Authorization: Bearer YOUR_TOKEN" \
  --header "X-GitHub-Api-Version: 2022-11-28"
```

gh CLI example (uses env var `GH_TOKEN`):

```
export GH_TOKEN=YOUR_TOKEN
gh api repos/<owner>/<repo>
```

MCP / VS Code notes
--------------------
For MCP server configuration, prefer using an environment variable for automated agent workflows and CI.

Example `.vscode/mcp.json` (prefer env var):

```
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${env:github_api}",
        "X-GitHub-Api-Version": "2022-11-28"
      }
    }
  }
}
```

If you prefer an interactive prompt in VS Code, keep the input scaffold and paste the token when requested (`${input:github_mcp_pat}`).

Docker MCP server (local test)
-----------------------------
Run a local MCP server container for testing (example):

```
docker run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=<your-fine-grained-token> \
  -e GITHUB_TOOLSETS="repos,issues,pull_requests,actions" \
  ghcr.io/github/github-mcp-server
```

Responsibility
--------------
- Keep tokens secret. If a token is exposed, revoke it immediately and rotate downstream credentials.

Appendix: quick checklist
-------------------------
- [ ] Use fine‑grained PAT where possible
- [ ] Store token in OS keyring or secrets manager
- [ ] Limit scope to required permissions
- [ ] Authorize classic PAT for SAML SSO if needed
- [ ] Rotate tokens periodically (90 days recommended)
