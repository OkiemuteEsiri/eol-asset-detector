from __future__ import annotations

import hashlib
from datetime import date

from .models import Asset, Criticality, Finding


CRITICALITY_WEIGHT = {
    Criticality.LOW: 5,
    Criticality.MEDIUM: 10,
    Criticality.HIGH: 18,
    Criticality.CRITICAL: 25,
}


def _finding_id(asset: Asset) -> str:
    digest = hashlib.sha256(f"{asset.asset_id}|{asset.product}|{asset.version}|eol".encode()).hexdigest()[:12]
    return f"EOL-{digest.upper()}"


def _priority(score: int) -> tuple[str, str]:
    if score >= 85:
        return "critical", "P0"
    if score >= 70:
        return "high", "P1"
    if score >= 45:
        return "medium", "P2"
    return "low", "P3"


def assess_asset(asset: Asset, as_of: date) -> Finding | None:
    if asset.end_of_support > as_of:
        return None

    days_past = (as_of - asset.end_of_support).days
    age_weight = min(35, 5 + days_past // 30 * 3)
    exposure_weight = 25 if asset.internet_exposed else 0
    ownership_weight = 10 if not asset.owner else 0
    score = min(100, age_weight + CRITICALITY_WEIGHT[asset.criticality] + exposure_weight + ownership_weight)

    exception_active = asset.exception_until is not None and asset.exception_until >= as_of
    status = "accepted-risk" if exception_active else "open"
    severity, priority = _priority(score)

    evidence = [
        f"{asset.product} {asset.version} support ended {asset.end_of_support.isoformat()}",
        f"{days_past} days past end-of-support",
        f"business criticality={asset.criticality.value}",
        f"internet_exposed={str(asset.internet_exposed).lower()}",
    ]
    if not asset.owner:
        evidence.append("no remediation owner recorded")
    if exception_active:
        evidence.append(f"risk exception active until {asset.exception_until.isoformat()}")

    return Finding(
        finding_id=_finding_id(asset),
        asset_id=asset.asset_id,
        severity=severity,
        priority=priority,
        risk_score=score,
        status=status,
        days_past_eol=days_past,
        evidence=tuple(evidence),
        remediation=(
            "Upgrade or replace the unsupported product with a vendor-supported release; "
            "where immediate replacement is not feasible, reduce exposure and document a time-bound exception."
        ),
        validation=(
            "Re-inventory the asset and verify the installed release has a support end date after the validation date; "
            "confirm exposure and ownership records are current."
        ),
    )


def assess_inventory(assets: list[Asset], as_of: date) -> list[Finding]:
    ids = [asset.asset_id for asset in assets]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate asset_id detected")
    findings = [finding for asset in assets if (finding := assess_asset(asset, as_of))]
    return sorted(findings, key=lambda f: (-f.risk_score, f.asset_id))


def posture_score(assets: list[Asset], findings: list[Finding]) -> int:
    if not assets:
        return 100
    penalty = sum(f.risk_score for f in findings) / (len(assets) * 100)
    return max(0, round(100 * (1 - min(1.0, penalty))))
