"""UP8: Smoke test for KPI Dashboard XAML presence & key fragments.
Avoids GUI instantiation for CI portability.
"""
from pathlib import Path

XAML = (
    Path(__file__).resolve().parents[3]
    / 'interface'
    / 'AIOS.UI'
    / 'KPIDashboardWindow.xaml'
)


def test_dashboard_xaml_contains_expected_controls():
    assert XAML.exists(), 'KPIDashboardWindow.xaml missing'
    text = XAML.read_text(encoding='utf-8', errors='ignore')
    # basic UI element IDs added in UP6 enhancements
    for fragment in [
        'x:Class="AIOS.UI.KPIDashboardWindow"',
        'PassCount',
        'FailCount',
        'StreamingStatus',
    ]:
        assert fragment in text
