from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from .models import Asset, Criticality, Finding


def load_csv(path: str | Path) -> list[Asset]:
    assets: list[Asset] = []
    with Path(path).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            assets.append(
                Asset(
                    asset_id=row["asset_id"],
                    hostname=row["hostname"],
                    product=row["product"],
                    version=row["version"],
                    vendor=row["vendor"],
                    end_of_support=date.fromisoformat(row["end_of_support"]),
                    criticality=Criticality(row["criticality"].lower()),
                    internet_exposed=row.get("internet_exposed", "false").lower() == "true",
                    owner=row.get("owner") or None,
                    exception_until=date.fromisoformat(row["exception_until"]) if row.get("exception_until") else None,
                )
            )
    return assets


def render_markdown(assets: list[Asset], findings: list[Finding], as_of: date, posture: int) -> str:
    lines = [
        "# End-of-Life Asset Assessment",
        "",
        f"Assessment date: **{as_of.isoformat()}**",
        f"Assets assessed: **{len(assets)}**",
        f"Unsupported assets: **{len(findings)}**",
        f"Posture score: **{posture}/100**",
        "",
        "## Prioritized findings",
        "",
        "| Priority | Asset | Risk | Status | Days past EOL |",
        "|---|---|---:|---|---:|",
    ]
    for finding in findings:
        lines.append(
            f"| {finding.priority} | {finding.asset_id} | {finding.risk_score} | {finding.status} | {finding.days_past_eol} |"
        )
    lines += ["", "## Remediation detail", ""]
    for finding in findings:
        lines += [
            f"### {finding.finding_id} — {finding.asset_id}",
            f"- Severity: **{finding.severity}**",
            f"- Priority: **{finding.priority}**",
            "- Evidence: " + "; ".join(finding.evidence),
            f"- Remediation: {finding.remediation}",
            f"- Validation: {finding.validation}",
            "",
        ]
    return "\n".join(lines)
