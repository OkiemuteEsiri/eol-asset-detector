"""Defensive end-of-life asset assessment toolkit."""

from .engine import assess_asset, assess_inventory, posture_score
from .models import Asset, Criticality, Finding

__all__ = ["Asset", "Criticality", "Finding", "assess_asset", "assess_inventory", "posture_score"]
