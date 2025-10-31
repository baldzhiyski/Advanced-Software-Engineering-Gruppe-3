from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Literal

Boundary = Literal["bounded", "torus"]


@dataclass(slots=True)
class GameOfLife:
    """
    Conway's Game of Life on a finite 2D grid.

    Boundary behavior:
      - 'bounded': Cells outside the grid are considered dead.
      - 'torus'  : The grid wraps around (top <-> bottom, left <-> right).

    """

    width: int
    height: int
    boundary: Boundary = "bounded"
    alive_char: str = "O"
    dead_char: str = "."
    _grid: list[list[bool]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """
        Initialize the internal grid.
        Raises ValueError if width or height are non-positive.
        """

        if self.width <= 0 or self.height <= 0:
            raise ValueError("width and height must be positive")
        self._grid: list[list[bool]] = [[False] * self.width for _ in range(self.height)]

    # ---------- Construction / Serialization ----------

    @classmethod
    def from_string(
            cls,
            s: str,
            *,
            alive_char: str = "O",
            dead_char: str = ".",
            boundary: Boundary = "bounded",
    ) -> "GameOfLife":
        """
        Create a world from multi-line string. All non-empty lines must have equal length.
        Example:
            ....
            .O..
            ..O.
            OOO.
        """
        lines = cls._normalize_and_validate_lines(s)
        cls._validate_characters(lines, alive_char, dead_char)
        grid = cls._build_grid(lines, alive_char)
        obj = cls(len(lines[0]), len(lines), boundary=boundary,
                  alive_char=alive_char, dead_char=dead_char)
        obj._grid = grid
        return obj

    def to_string(self) -> str:
        """
        Convert the current grid state into a multi-line string representation.
        Alive cells are represented by `alive_char`, dead cells by `dead_char`.
        """
        return "\n".join(
            "".join(self.alive_char if self._grid[y][x] else self.dead_char for x in range(self.width))
            for y in range(self.height)
        )

    # ---------- Public API ----------

    def set_alive(self, x: int, y: int, alive: bool = True) -> None:
        """
        Set cell state.
        Raises IndexError if out-of-bounds in 'bounded' or 'torus' (writing).
        """
        self._require_in_bounds(x, y)
        self._grid[y][x] = alive

    def is_alive(self, x: int, y: int) -> bool:
        """
        Returns cell state. For 'bounded' boundary: off-grid is dead.
        For 'torus': off-grid indices wrap around (but we still clamp writes).
        """
        if self.boundary == "bounded":
            return self._grid[y][x] if self._in_bounds(x, y) else False
        # torus: wrap read indices
        xw = x % self.width
        yh = y % self.height
        return self._grid[yh][xw]

    def tick(self) -> None:
        """
        Advance one generation using the 4 classic rules.
        We compute into a new grid to avoid read/write conflicts.
        """
        next_grid = [[False] * self.width for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                alive = self._grid[y][x]
                neighbors = self._alive_neighbors(x, y)
                next_grid[y][x] = (alive and neighbors in (2, 3)) or (not alive and neighbors == 3)
        self._grid = next_grid

    def live_cells(self) -> Iterable[tuple[int, int]]:
        """
        Iterate over coordinates of living cells (useful in tests or instrumentation).
        """
        for y in range(self.height):
            for x in range(self.width):
                if self._grid[y][x]:
                    yield (x, y)

    # ---------- Internals ----------

    def _alive_neighbors(self, x: int, y: int) -> int:
        """
        Count live neighbors in Moore neighborhood (8 surrounding cells).
        Boundary rules:
          - bounded: off-grid counts as dead
          - torus  : indices wrap around
        """

        def cell(nx, ny):
            if self.boundary == "torus":
                return self._grid[ny % self.height][nx % self.width]
            return self._grid[ny][nx] if self._in_bounds(nx, ny) else False

        return sum(
            cell(x + dx, y + dy)
            for dy in (-1, 0, 1)
            for dx in (-1, 0, 1)
            if not (dx == 0 and dy == 0)
        )

    def _in_bounds(self, x: int, y: int) -> bool:
        """
        Return true if (x, y) is within grid bounds.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def _require_in_bounds(self, x: int, y: int) -> None:
        """
        Raise IndexError if (x, y) is out of bounds.
        """
        if not self._in_bounds(x, y):
            raise IndexError(f"cell out of bounds: {(x, y)} in {self.width}x{self.height}")

    @staticmethod
    def _normalize_and_validate_lines(s: str) -> list[str]:
        """Clean input string and ensure all lines have equal length."""
        lines = [line.strip() for line in s.splitlines() if line.strip()]
        if not lines:
            raise ValueError("empty world")

        width = len(lines[0])
        if any(len(line) != width for line in lines):
            raise ValueError("inconsistent line lengths")
        return lines

    @staticmethod
    def _validate_characters(lines: list[str], alive_char: str, dead_char: str) -> None:
        """Ensure all characters are valid (raise ValueError if not)."""
        allowed = {alive_char, dead_char}
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch not in allowed:
                    raise ValueError(f"unexpected char '{ch}' at {(x, y)}; "f"expected '{alive_char}' or '{dead_char}'")

    @staticmethod
    def _build_grid(lines: list[str], alive_char: str) -> list[list[bool]]:
        """Convert string lines into a boolean grid (True = alive)."""
        return [[ch == alive_char for ch in line] for line in lines]
