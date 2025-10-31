import os
import sys

THIS_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(os.path.join(THIS_DIR, os.pardir))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from critical_path import Activity, CriticalPathAnalyzer


def test_given_network_critical_path_and_duration():
    activities = [
        Activity("A01", 3),
        Activity("A02", 4),
        Activity("A03", 5),
        Activity("A04", 4, ["A01"]),
        Activity("A05", 9, ["A01"]),
        Activity("A06", 4, ["A02"]),
        Activity("A07", 2, ["A03"]),
        Activity("A08", 4, ["A04"]),
        Activity("A09", 2, ["A06"]),
        Activity("A10", 3, ["A06"]),
        Activity("A11", 3, ["A07"]),
        Activity("A12", 2, ["A05", "A08"]),
        Activity("A13", 4, ["A10", "A11"]),
        Activity("A14", 7, ["A09", "A12"]),
        Activity("A15", 2, ["A09", "A12"]),
        Activity("A16", 4, ["A13", "A15"]),
    ]
    cpa = CriticalPathAnalyzer(activities)
    cp = cpa.get_critical_path()
    # Expected path from the manual solution
    assert cp == ["A01", "A05", "A12", "A14"]
    # Project duration is the maximum earliest finish
    project_duration = max(a.earliest_finish for a in cpa.activities.values())
    assert project_duration == 21
