from __future__ import annotations

from game_of_life.core import GameOfLife
from game_of_life.patterns import list_patterns, pattern_cells


def test_patterns_exist_and_loadable():
    names = set(list_patterns())
    assert {"block", "blinker", "glider"}.issubset(names)
    cells = pattern_cells("block", offset_x=5, offset_y=7)
    assert (5, 7) in cells and (6, 8) in cells


def test_glider_moves_diagonally_on_torus():
    # Small board, place glider, ensure it "travels" diagonally over a few ticks.
    g = GameOfLife(10, 10, boundary="torus")
    for (x, y) in pattern_cells("glider", offset_x=2, offset_y=2):
        g.set_alive(x, y, True)

    # Track centroid rough movement; over 4 steps, it should have shifted down-right
    def centroid():
        cells = list(g.live_cells())
        cx = sum(x for x, _ in cells) / len(cells)
        cy = sum(y for _, y in cells) / len(cells)
        return (cx, cy)

    c0 = centroid()
    for _ in range(4):
        g.tick()
    c1 = centroid()
    assert c1[0] > c0[0] and c1[1] > c0[1]
