# Option 2 — A poisoned VS Code extension breached GitHub itself

Eighteen minutes was enough. A compromised Nx Console build (v18.95.0, 2.2M installs) sat live in the VS Code Marketplace long enough for TeamPCP to seed a credential stealer that exfiltrated ~3,800 internal GitHub repos.

The payload harvested tokens from GitHub, npm, AWS, HashiCorp Vault, 1Password, and Anthropic Claude Code configs.

The next 6 months reset how every CTO treats IDE extensions: same blast radius as a CI runner. If developer tooling isn't in your SBOM, your supply chain isn't secured — it is performed.

Who owns extension governance on your engineering org chart?

#CyberSecurity #SupplyChain #DevSecOps #AI #Leadership

---

**Type:** patch_update
**Source:** The Hacker News · 2026-05-20
**Source URL:** https://thehackernews.com/2026/05/github-internal-repositories-breached.html
**Watch / follow:** https://github.com/nrwl/nx-console/security/advisories/GHSA-c9j4-9m59-847w
