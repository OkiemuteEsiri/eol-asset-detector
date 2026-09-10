from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


class Criticality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Asset:
    asset_id: str
    hostname: str
    product: str
    version: str
    vendor: str
    end_of_support: date
    criticality: Criticality
    internet_exposed: bool = False
    owner: str | None = None
    exception_until: date | None = None

    def __post_init__(self) -> None:
        required = (self.asset_id, self.hostname, self.product, self.version, self.vendor)
        if any(not value.strip() for value in required):
            raise ValueError("asset identity fields must be non-empty")


@dataclass(frozen=True)
class Finding:
    finding_id: str
    asset_id: str
    severity: str
    priority: str
    risk_score: int
    status: str
    days_past_eol: int
    evidence: tuple[str, ...]
    remediation: str
    validation: str
