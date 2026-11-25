# OSCAL hub (skeleton)

Layout for the plan in `../docs/oscal-hub-plan.md`. Empty until the first system is onboarded.

| Folder | Holds | Source |
| --- | --- | --- |
| `catalogs/` | SP 800-53 rev 5, CSF 2.0, AI RMF catalogs | oscal-content (pin the commit), capordino output |
| `profiles/` | Your tailored baseline | Hand-authored with compliance-trestle |
| `components/` | One component definition per tool (Entra ID, Sentinel, CrowdStrike, Jira) | Hand-authored, owner named in metadata |
| `ssp/` | System security plans | Assembled from profile + components |
| `results/` | Assessment results from adapters | Generated nightly; never hand-edited |
| `poam/` | Open findings | Generated; synced to Jira |

Rules: validate every file with oscal-cli in CI; keep UUIDs stable; store evidence links and SHA-256 hashes, not evidence content.
