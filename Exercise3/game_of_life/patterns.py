from __future__ import annotations

from typing import Dict, Iterable, Tuple


# Simple built-in patterns via coordinate sets (x, y)
# Coordinates are relative;
PATTERNS: Dict[str, set[Tuple[int, int]]] = {
    "block": {(0, 0), (1, 0), (0, 1), (1, 1)},  # still life
    "blinker": {(0, 0), (0, 1), (0, 2)},        # oscillator (period 2)
    "glider": {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)},  # spaceship
}


def list_patterns() -> Iterable[str]:
    return sorted(PATTERNS.keys())


def pattern_cells(name: str, *, offset_x: int = 0, offset_y: int = 0) -> set[tuple[int, int]]:
    """
    Return a set of absolute coordinates for a named pattern placed at an offset.
    Raises KeyError for unknown patterns.
    """
    base = PATTERNS[name]
    return {(x + offset_x, y + offset_y) for (x, y) in base}
