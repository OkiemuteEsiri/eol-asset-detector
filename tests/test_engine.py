import unittest
from datetime import date

from src.eol_detector.engine import assess_asset, assess_inventory, posture_score
from src.eol_detector.models import Asset, Criticality


class EngineTests(unittest.TestCase):
    def make_asset(self, **overrides):
        values = dict(
            asset_id="AST-1",
            hostname="host-1",
            product="ExampleOS",
            version="1",
            vendor="ExampleVendor",
            end_of_support=date(2025, 1, 1),
            criticality=Criticality.HIGH,
            internet_exposed=False,
            owner="Platform",
            exception_until=None,
        )
        values.update(overrides)
        return Asset(**values)

    def test_supported_asset_has_no_finding(self):
        asset = self.make_asset(end_of_support=date(2027, 1, 1))
        self.assertIsNone(assess_asset(asset, date(2026, 9, 10)))

    def test_eol_asset_has_finding(self):
        finding = assess_asset(self.make_asset(), date(2026, 9, 10))
        self.assertIsNotNone(finding)
        self.assertGreater(finding.days_past_eol, 0)

    def test_internet_exposure_increases_risk(self):
        internal = assess_asset(self.make_asset(asset_id="A"), date(2026, 9, 10))
        exposed = assess_asset(self.make_asset(asset_id="B", internet_exposed=True), date(2026, 9, 10))
        self.assertGreater(exposed.risk_score, internal.risk_score)

    def test_missing_owner_increases_risk(self):
        owned = assess_asset(self.make_asset(asset_id="A"), date(2026, 9, 10))
        orphan = assess_asset(self.make_asset(asset_id="B", owner=None), date(2026, 9, 10))
        self.assertGreater(orphan.risk_score, owned.risk_score)

    def test_active_exception_remains_a_finding(self):
        finding = assess_asset(
            self.make_asset(exception_until=date(2026, 12, 31)), date(2026, 9, 10)
        )
        self.assertEqual("accepted-risk", finding.status)

    def test_duplicate_asset_ids_fail_closed(self):
        with self.assertRaises(ValueError):
            assess_inventory(
                [self.make_asset(), self.make_asset(hostname="host-2")], date(2026, 9, 10)
            )

    def test_findings_sorted_by_risk(self):
        findings = assess_inventory(
            [self.make_asset(asset_id="A"), self.make_asset(asset_id="B", internet_exposed=True)],
            date(2026, 9, 10),
        )
        self.assertEqual("B", findings[0].asset_id)

    def test_posture_score_is_bounded(self):
        assets = [
            self.make_asset(asset_id="A"),
            self.make_asset(asset_id="B", internet_exposed=True),
        ]
        findings = assess_inventory(assets, date(2026, 9, 10))
        self.assertGreaterEqual(posture_score(assets, findings), 0)
        self.assertLessEqual(posture_score(assets, findings), 100)


if __name__ == "__main__":
    unittest.main()
