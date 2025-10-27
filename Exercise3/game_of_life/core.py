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
        lines = [line.rstrip("\n") for line in s.splitlines() if line.strip() != ""]
        if not lines:
            raise ValueError("empty world")
        w = len(lines[0])
        if any(len(line) != w for line in lines):
            raise ValueError("inconsistent line lengths")
        g = cls(w, len(lines), boundary=boundary, alive_char=alive_char, dead_char=dead_char)
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch == alive_char:
                    g._grid[y][x] = True
                elif ch == dead_char:
                    g._grid[y][x] = False
                else:
                    msg = f"unexpected char '{ch}' at {(x, y)}; expected '{alive_char}' or '{dead_char}'"
                    raise ValueError(msg)
        return g

    def to_string(self) -> str:
        """Serialize the world to a multi-line string."""
        return "\n".join(
            "".join(self.alive_char if self._grid[y][x] else self.dead_char for x in range(self.width))
            for y in range(self.height)
        )

    # ---------- Public API ----------

    def set_alive(self, x: int, y: int, alive: bool = True) -> None:
        """Set cell state. Raises IndexError if out-of-bounds in 'bounded' or 'torus' (writing)."""
        self._require_in_bounds(x, y)
        self._grid[y][x] = alive

    def is_alive(self, x: int, y: int) -> bool:
        """
        Get cell state. For 'bounded' boundary: off-grid is dead.
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
        next_grid: list[list[bool]] = [[False] * self.width for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                alive = self._grid[y][x]
                neighbors = self._alive_neighbors(x, y)
                # Survival
                if alive and (neighbors == 2 or neighbors == 3):
                    next_grid[y][x] = True
                # Birth
                elif (not alive) and neighbors == 3:
                    next_grid[y][x] = True
                # Under/Overpopulation -> dead (default False)
        self._grid = next_grid

    def live_cells(self) -> Iterable[tuple[int, int]]:
        """Iterate over coordinates of living cells (useful in tests or instrumentation)."""
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
        cnt = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if self.boundary == "bounded":
                    if self._in_bounds(nx, ny) and self._grid[ny][nx]:
                        cnt += 1
                else:  # torus
                    nx %= self.width
                    ny %= self.height
                    if self._grid[ny][nx]:
                        cnt += 1
        return cnt

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def _require_in_bounds(self, x: int, y: int) -> None:
        if not self._in_bounds(x, y):
            raise IndexError(f"cell out of bounds: {(x, y)} in {self.width}x{self.height}")
