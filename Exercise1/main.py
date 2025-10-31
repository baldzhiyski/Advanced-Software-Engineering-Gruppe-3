from critical_path import Activity, CriticalPathAnalyzer

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
    Activity("A16", 4, ["A13", "A15"])
]

cpa = CriticalPathAnalyzer(activities)
critical_path = cpa.get_critical_path()
project_duration = cpa.project_duration()

print("Kritischer Pfad:", " → ".join(critical_path))
print("Projektdauer:", project_duration)
for a in activities:
    print(f"{a.id}: ES={a.earliest_start}, EF={a.earliest_finish}, "
          f"LS={a.latest_start}, LF={a.latest_finish}, Slack={a.slack}")
