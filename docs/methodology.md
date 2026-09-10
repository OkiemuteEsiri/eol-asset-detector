# Assessment Methodology

## Scope

This lab demonstrates a defensive, inventory-driven process for identifying unsupported operating systems, runtimes, databases, browsers, and other technology components.

## Workflow

1. **Normalize inventory** — require a stable asset ID, hostname, product, version, vendor, support-end date, business criticality, exposure state, owner, and optional exception date.
2. **Validate data quality** — reject duplicate asset IDs and malformed dates before risk calculation.
3. **Classify lifecycle** — compare the vendor support-end date with the explicit assessment date.
4. **Contextualize risk** — weight time past EOL, business criticality, internet exposure, and missing ownership.
5. **Prioritize** — map bounded scores to P0–P3 queues without hiding accepted risk.
6. **Remediate** — prefer upgrade, migration, or retirement. When that cannot occur immediately, reduce attack surface and use documented, time-bound risk acceptance.
7. **Revalidate** — re-inventory the asset and verify that the installed version is supported on the new validation date; confirm ownership and exposure records are current.

## Risk interpretation

| Priority | Score | Typical handling |
|---|---:|---|
| P0 | 85–100 | Immediate engineering and risk-owner attention |
| P1 | 70–84 | Accelerated remediation plan |
| P2 | 45–69 | Planned remediation within normal governance |
| P3 | 0–44 | Track and address proportionately |

The score is illustrative and deterministic. Enterprise implementations should calibrate weights against risk appetite, asset taxonomy, exploit intelligence, compensating controls, and policy-defined SLAs.

## ATT&CK context

Unsupported services can increase exposure to techniques such as **T1190 – Exploit Public-Facing Application** and **T1210 – Exploitation of Remote Services**. These mappings are defensive threat-model context only; they do not indicate that any sample asset was exploited.

## Evidence standard

A finding should be considered actionable only when product/version identity and the relevant support-end date can be substantiated. Production programs should preserve vendor lifecycle references and inventory-source lineage alongside each finding.

## Safety

All included data is synthetic. No discovery, exploitation, credential use, or live-environment targeting is part of the project.