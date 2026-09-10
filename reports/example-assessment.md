# Example End-of-Life Asset Assessment

Assessment date: **2026-09-10**

This example uses only `data/synthetic_inventory.csv`. Values are illustrative and are not production observations.

## Executive summary

The synthetic inventory contains multiple unsupported technology components, including an internet-exposed critical asset and an unowned legacy system. The highest-risk items should be migrated or upgraded first because unsupported software reduces the availability of vendor fixes and can amplify exposure when combined with external reachability or weak ownership.

## Priority observations

| Asset | Condition | Risk driver | Recommended action |
|---|---|---|---|
| AST-001 | Unsupported critical web asset | Long EOL age + internet exposure + criticality | Upgrade/migrate urgently and reduce external exposure until complete |
| AST-004 | Unsupported legacy jump host | Long EOL age + high criticality + no owner | Assign accountable owner and retire or migrate |
| AST-002 | Unsupported application runtime | High criticality; active time-bound exception | Keep visible, enforce compensating controls, complete migration before exception expiry |
| AST-005 | Unsupported browser | Moderate criticality and aging | Move managed endpoints to a supported release |

## Governance observations

- An accepted-risk record does **not** remove the technical finding.
- Missing ownership increases operational risk because no accountable remediation path exists.
- Support dates must be validated against authoritative vendor lifecycle information in a production implementation.
- Remediation closure requires re-inventory and confirmation that the installed release is supported on the validation date.

## Defensive ATT&CK context

Potential exposure is contextualized against **T1190 – Exploit Public-Facing Application** and **T1210 – Exploitation of Remote Services**. These mappings are threat-model references only and are not evidence of exploitation.