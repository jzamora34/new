# Making multiple tools follow OSCAL

For a team not using OSCAL today, it adds little on its own: it pays off only when another system reads it. You do not make each tool speak OSCAL natively (almost none do). You keep OSCAL as a hub in one git repository; each tool keeps its own format, and small adapter scripts translate between that format and OSCAL. Exchange, automated checks, reuse and mandate-readiness come from the hub. The skeleton lives in `../oscal-hub/`.

## The pattern

```
 Tools (native data)        Adapters            OSCAL repo (git)           Readers
 -------------------        --------            ----------------           -------
 Entra ID  ----+                                catalog   (800-53)         CI checks
 SIEM      ----+--> scripts pull from APIs -->  profile   (your baseline)  GRC tool import
 EDR       ----+    and write OSCAL             components (one per tool)  HTML/PDF for auditors
 Jira/SNOW ----+                                SSP       (the system)     FedRAMP-style submission
 Cloud cfg ----+                                assessment results         Jira tickets for open items
                                                POA&M     (open findings)
```

## Documents to keep, in order

1. **Catalog:** take SP 800-53 from [oscal-content](https://github.com/usnistgov/oscal-content); [capordino](https://github.com/usnistgov/capordino) supplies CSF 2.0, SSDF and AI RMF.
2. **Profile:** your baseline, for example 800-53 Moderate plus your tailoring.
3. **Component definitions, one per tool** (where reuse happens). Proposed mappings, to be confirmed by control owners: Entra ID IA-2, AC-2; SIEM AU-6, AU-12; EDR SI-4, SI-3; SOAR IR-4, IR-5; Jira/ServiceNow CM-3. Check whether the vendor publishes one.
4. **System security plan (SSP):** imports the profile and references components, so it is mostly assembled.
5. **Assessment results:** produced by adapters; each check is a timestamped observation linking to evidence.
6. **POA&M:** failed checks become open items; an adapter opens a Jira or ServiceNow ticket for each.

## Tools

| Tool | Role |
| --- | --- |
| [compliance-trestle](https://github.com/oscal-compass/compliance-trestle) (OSCAL Compass) | Manage OSCAL in git; write controls in markdown instead of raw JSON |
| [oscal-cli](https://github.com/usnistgov/oscal-cli) (NIST) | Validate, convert, resolve profiles; run in CI |
| [compliance-to-policy](https://github.com/oscal-compass/compliance-to-policy), [Lula](https://github.com/defenseunicorns/lula) | Connect OSCAL controls to policy-as-code (OPA, Kyverno) and Kubernetes checks |
| [oscal-xslt](https://github.com/usnistgov/oscal-xslt) (NIST) | Render OSCAL as HTML for auditors |
| GSA FedRAMP automation templates | Only if FedRAMP applies; the GitHub location could not be confirmed on Nov 25, 2026, so search fedramp.gov |

These projects change quickly; check each one's OSCAL version support before relying on it.

## Rollout

1. One system, one baseline, three components (Entra ID, SIEM, EDR). Repo layout: `catalogs/ profiles/ components/ ssp/ results/ poam/`.
2. CI validation: every pull request runs oscal-cli; broken files never merge.
3. One evidence adapter end to end, for example a nightly job writing the MFA coverage percentage as an IA-2 observation.
4. POA&M to ticketing: failed checks open tickets; closed tickets update the POA&M. This is where the SOC sees value.
5. Expand one tool at a time; each component is reused by every system that uses the tool.
6. Publish readable HTML or PDF; import into the GRC platform if it supports OSCAL.

## Pitfalls

- Keep UUIDs stable; regenerating them breaks every cross-reference.
- Link to evidence with a hash instead of embedding logs or screenshots, which may hold sensitive data; keep the repo access-controlled.
- Treat tool output as untrusted input: parse and validate, never execute.
- Every component needs an owner, or it goes stale like a Word document.
- Do not hand-edit large JSON; author in markdown with trestle or generate the files.

Adopt properly when the GRC platform imports OSCAL, a customer or regulator asks for it (FedRAMP is moving to OSCAL submissions), or compliance wants automated evidence. Until then, two cheap uses: take exact control IDs and wording from oscal-content, and tag detections and automations with control IDs so "which controls does this alert support?" is a lookup.
