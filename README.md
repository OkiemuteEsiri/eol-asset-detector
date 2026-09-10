# End-of-Life Asset Detector

A defensive vulnerability-management and exposure-engineering project that identifies unsupported technology from normalized inventory, contextualizes risk, and produces explainable remediation queues.

## Why this project exists

End-of-life (EOL) technology creates a persistent security and governance problem: once vendor support ends, security fixes may no longer be available, yet raw lifecycle data alone does not tell teams what to remediate first. This project demonstrates how to turn support dates into an actionable, auditable prioritization workflow without scanning or targeting live infrastructure.

## What it demonstrates

- Vulnerability and exposure-management engineering
- Asset lifecycle governance
- Contextual risk scoring
- Data-quality controls
- Exception-aware remediation tracking
- Executive and technical reporting
- Remediation validation design
- Secure CI/CD practices
- MITRE ATT&CK threat-model mapping

## Architecture

```text
Synthetic / exported CSV inventory
          |
          v
Parsing + validation
          |
          v
Immutable asset model
          |
          v
Lifecycle classification
          |
          v
Contextual risk engine
  +---------------------------+
  | time past EOL             |
  | business criticality      |
  | internet exposure         |
  | missing ownership         |
  +---------------------------+
          |
          v
Prioritized findings (P0-P3)
          |
          +--> evidence
          +--> remediation
          +--> validation criteria
          +--> accepted-risk visibility
          |
          v
Markdown assessment report
```

See [`docs/architecture.md`](docs/architecture.md) for the design details.

## Repository structure

```text
.github/workflows/security-quality.yml  # compile, tests, CLI/report validation
src/eol_detector/models.py              # immutable domain models
src/eol_detector/engine.py              # deterministic assessment engine
src/eol_detector/io.py                  # CSV ingestion + Markdown reporting
src/eol_detector/cli.py                 # offline command-line interface
data/synthetic_inventory.csv            # realistic synthetic test inventory
tests/test_engine.py                    # unit-test suite
docs/architecture.md                    # component/data-flow design
docs/methodology.md                     # assessment + revalidation methodology
reports/example-assessment.md            # stakeholder-facing sample output
```

## Risk model

The engine uses an intentionally explainable 0-100 model. It combines:

| Driver | Rationale |
|---|---|
| Time past end-of-support | Longer unsupported periods increase lifecycle exposure |
| Business criticality | Failure or compromise of critical systems has greater impact |
| Internet exposure | Externally reachable unsupported services warrant faster action |
| Missing ownership | Unowned risk is less likely to be remediated effectively |

Scores are converted to P0-P3 remediation queues. The model is deterministic and transparent so every priority can be explained to engineering and risk stakeholders.

The scoring weights are illustrative. A production program should calibrate them against enterprise risk appetite, application/asset taxonomy, threat intelligence, compensating controls, and policy-defined SLAs.

## Exception handling

A key governance decision in this project is that an active risk exception **does not suppress the finding**. The technical exposure remains visible with status `accepted-risk` until the asset is upgraded, migrated, retired, or otherwise becomes supported.

This prevents an administrative decision from being misrepresented as technical remediation.

## Usage

Python 3.12+ is sufficient; the implementation intentionally uses the standard library only.

Run the assessment against the included synthetic inventory:

```bash
PYTHONPATH=. python -m src.eol_detector.cli data/synthetic_inventory.csv --as-of 2026-09-10
```

Write a Markdown report:

```bash
PYTHONPATH=. python -m src.eol_detector.cli data/synthetic_inventory.csv \
  --as-of 2026-09-10 \
  --output eol-assessment.md
```

Run the tests:

```bash
python -m unittest discover -s tests -v
```

## Implemented controls

The current implementation provides:

- stable asset identity validation
- duplicate asset-ID rejection (fail closed)
- explicit support-end-date evaluation
- contextual risk scoring bounded to 0-100
- deterministic finding IDs
- P0-P3 remediation prioritization
- missing-owner risk uplift
- internet-exposure risk uplift
- business-criticality weighting
- time-bound exception visibility
- remediation guidance
- explicit revalidation criteria
- Markdown executive/technical reporting
- synthetic-only sample data
- CI compilation, unit tests, CLI smoke testing, and report validation

## Tests

The unit suite covers:

1. supported assets do not produce findings
2. unsupported assets produce lifecycle findings
3. internet exposure increases risk
4. missing ownership increases risk
5. accepted risk remains visible
6. duplicate asset IDs fail closed
7. findings are ordered by risk
8. posture scores stay within 0-100

## Remediation workflow

1. Confirm the product/version and authoritative vendor lifecycle date.
2. Assign an accountable service or asset owner.
3. Prioritize internet-exposed and business-critical unsupported systems.
4. Upgrade to a supported version, migrate the workload, or retire the component.
5. If immediate remediation is impossible, reduce exposure and document a time-bound exception with an exit plan.
6. Re-inventory the system after remediation.
7. Close only after the installed release is confirmed supported on the validation date.

## MITRE ATT&CK context

This project uses ATT&CK only as defensive threat-model context:

- **T1190 — Exploit Public-Facing Application**
- **T1210 — Exploitation of Remote Services**

Unsupported software can increase exposure to known weaknesses relevant to these techniques, especially when externally reachable. The mappings do **not** indicate that any sample asset has been compromised or exploited.

## Example assessment

[`reports/example-assessment.md`](reports/example-assessment.md) shows how the synthetic dataset can be summarized for stakeholders. It highlights an internet-exposed critical EOL asset, an unowned legacy system, a time-bound risk exception, and a lower-priority endpoint lifecycle issue.

## CI/CD security and quality checks

The GitHub Actions workflow uses read-only repository permissions and validates:

- Python source/test compilation
- the complete unit-test suite
- an end-to-end CLI smoke test
- creation of a non-empty assessment report
- presence of expected report content

No workflow step needs cloud credentials, repository write permission, production data, or external scanning access.

## Limitations

- Vendor lifecycle dates are supplied in the input dataset rather than fetched from vendor APIs.
- The scoring model is illustrative rather than statistically calibrated.
- CVE/KEV/EPSS intelligence is intentionally outside this repository's scope.
- Asset ownership and exposure are trusted inventory attributes; production implementations should preserve source lineage.
- No network discovery or remote interrogation is implemented.

## Roadmap

- lifecycle-reference provenance fields
- configurable enterprise risk weights
- CSV/JSON schema validation
- trend reporting for EOL backlog reduction
- exception-expiry alerts
- optional enrichment interface for authoritative lifecycle sources
- unit normalization for product/version naming
- policy-as-code support for lifecycle SLAs

## Safety boundary

This repository is deliberately defensive. It contains no exploit code, credential collection, vulnerability exploitation, active network scanning, production targeting, employer/client data, or real credentials. All included assets and vendor/product names are synthetic examples.

## Recruiter view

The project is intended to demonstrate practical security-engineering judgment: lifecycle risk is not treated as a simple "EOL yes/no" field. The implementation combines data validation, contextual prioritization, risk acceptance, ownership, remediation, revalidation, reporting, and CI into a small but complete vulnerability-management workflow.