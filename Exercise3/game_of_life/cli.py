from __future__ import annotations

import argparse
import os
import sys
import time
from typing import Optional

from .core import GameOfLife
from .patterns import list_patterns, pattern_cells


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Conway's Game of Life (Exercise3)")
    parser.add_argument("--width", type=int, default=20, help="grid width")
    parser.add_argument("--height", type=int, default=10, help="grid height")
    parser.add_argument("--pattern", type=str, default="blinker", choices=list_patterns())
    parser.add_argument("--steps", type=int, default=30, help="number of steps to run")
    parser.add_argument("--torus", action="store_true", help="use torus boundary (wrap around)")
    parser.add_argument("--sleep", type=float, default=0.12, help="delay between steps (seconds)")
    parser.add_argument("--offset-x", type=int, default=2, help="pattern offset x")
    parser.add_argument("--offset-y", type=int, default=2, help="pattern offset y")
    args = parser.parse_args(argv)

    boundary = "torus" if args.torus else "bounded"
    g = GameOfLife(args.width, args.height, boundary=boundary)

    # Place pattern
    for (x, y) in pattern_cells(args.pattern, offset_x=args.offset_x, offset_y=args.offset_y):
        if 0 <= x < g.width and 0 <= y < g.height:
            g.set_alive(x, y, True)

    for step in range(args.steps + 1):
        _render(g, step)
        if step == args.steps:
            break
        g.tick()
        time.sleep(max(args.sleep, 0.0))

    return 0


def _render(g: GameOfLife, step: int) -> None:
    # Clear terminal (cross-platform best-effort)
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Step: {step}  |  boundary={g.boundary}  |  size={g.width}x{g.height}")
    print(g.to_string())


if __name__ == "__main__":
    sys.exit(main())
