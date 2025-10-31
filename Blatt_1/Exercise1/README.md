# Exercise 1 – Critical Path

This folder contains a small, reusable implementation to compute the Critical Path (CPM) for arbitrary activity networks.

## Files
- `critical_path.py` – Implementation of `Activity` and `CriticalPathAnalyzer` (forward/backward pass with ES/EF/LS/LF and slack).
- `main.py` – Example using the assignment network (A01..A16). Prints the critical path and all timing values.
- `test/` – Pytest-based unit tests for a toy example and the assignment network.

## How to run

From the repository root:

```powershell
# (Optional) activate the venv that VS Code created
# . .venv/Scripts/Activate.ps1

# Run the example script
python Exercise1\main.py

# Run tests
python -m pytest -q Exercise1/test
```

On success, you should see the critical path for the assignment network as:

```
A01 → A05 → A12 → A14
```

and a total project duration of 21 days.
