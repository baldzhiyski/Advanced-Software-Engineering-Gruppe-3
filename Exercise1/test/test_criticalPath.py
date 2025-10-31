import os
import sys

# Ensure the module path points to the Exercise1 folder for imports
THIS_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(os.path.join(THIS_DIR, os.pardir))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from critical_path import Activity, CriticalPathAnalyzer

def test_critical_path():
    activities = [
        Activity("A1", 3),
        Activity("A2", 2, ["A1"]),
        Activity("A3", 4, ["A1"]),
        Activity("A4", 3, ["A2", "A3"])
    ]
    cpa = CriticalPathAnalyzer(activities)
    critical_path = cpa.get_critical_path()
    assert critical_path == ["A1", "A3", "A4"]
