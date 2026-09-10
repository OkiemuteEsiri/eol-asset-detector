# Architecture

## Objective

`eol-asset-detector` converts a normalized technology inventory into explainable end-of-life exposure findings for vulnerability and exposure-management workflows.

## Data flow

```text
CSV inventory
    |
    v
Parser + validation
    |
    v
Immutable Asset model
    |
    v
Support-date evaluation
    |
    +--> supported -> no finding
    |
    v
Contextual risk engine
(age + business criticality + exposure + ownership)
    |
    v
Finding model
    |
    +--> deterministic priority / severity
    +--> evidence
    +--> remediation
    +--> revalidation criteria
    |
    v
Markdown report + posture score
```

## Engineering controls

- Fail closed on duplicate asset identifiers.
- Require non-empty identity fields.
- Parse dates with the standard library ISO-8601 parser.
- Bound finding scores to 0–100.
- Keep accepted risk visible instead of suppressing the exposure.
- Use deterministic finding identifiers for stable reporting.
- Keep the project offline and provider-neutral; no production discovery or credential use is implemented.

## Risk model

The score is intentionally transparent rather than statistical. It combines:

1. **Age beyond support** — risk increases as unsupported time grows, with a cap.
2. **Business criticality** — critical business services receive greater weight.
3. **Internet exposure** — externally reachable unsupported technology receives a material uplift.
4. **Ownership gap** — unowned exposures receive an operational-governance penalty.

This is a prioritization aid, not a substitute for vendor advisories, threat intelligence, CVE analysis, compensating-control review, or business risk acceptance.

## Security boundary

The repository consumes only supplied inventory. It does not scan networks, enumerate production assets, exploit unsupported software, collect credentials, or claim compromise.