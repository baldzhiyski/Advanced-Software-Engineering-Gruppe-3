from __future__ import annotations

import pytest
from game_of_life.core import GameOfLife


def world(s: str, boundary: str = "bounded") -> GameOfLife:
    return GameOfLife.from_string(s, boundary=boundary)

def test_from_to_string_roundtrip():
    s = """
....
.O..
..O.
OOO.
"""
    g = world(s)
    assert g.to_string() == "....\n.O..\n..O.\nOOO."


def test_set_and_get_alive_and_bounds():
    g = GameOfLife(3, 2)
    g.set_alive(1, 0, True)
    assert g.is_alive(1, 0) is True
    assert g.is_alive(0, 0) is False
    with pytest.raises(IndexError):
        g.set_alive(-1, 0, True)
    with pytest.raises(IndexError):
        g.set_alive(3, 0, True)


def test_rules_under_over_and_birth():
    g = GameOfLife(3, 3)
    # Cross pattern: center has 4 neighbors -> dies (overpopulation)
    g.set_alive(1, 1, True)
    g.set_alive(0, 1, True)
    g.set_alive(2, 1, True)
    g.set_alive(1, 0, True)
    g.set_alive(1, 2, True)
    g.tick()
    assert g.is_alive(1, 1) is False  # dies
    # corners are born due to exactly 3 neighbors
    assert g.is_alive(0, 0) is True
    assert g.is_alive(2, 0) is True
    assert g.is_alive(0, 2) is True
    assert g.is_alive(2, 2) is True


def test_still_life_block_is_stable():
    s = """
....
.OO.
.OO.
....
"""
    g = world(s)
    before = g.to_string()
    for _ in range(4):
        g.tick()
        assert g.to_string() == before


def test_oscillator_blinker_period_2():
    start = """
.....
..O..
..O..
..O..
.....
"""
    g = world(start)
    g.tick()
    assert g.to_string() == "\n".join([".....", ".....", ".OOO.", ".....", "....."])
    g.tick()
    # back to start
    assert g.to_string() == "\n".join([line for line in start.splitlines() if line.strip() != ""])


def test_bounded_edges_outside_are_dead():
    s = """
O..
...
..O
"""
    g = world(s, boundary="bounded")
    g.tick()
    # single live cells with <2 neighbors die
    assert all(not g.is_alive(x, y) for y in range(g.height) for x in range(g.width))


def test_torus_wraps_reads():
    s = """
.O.
...
...
"""
    # With torus, the cell at (1,0) has neighbors wrapping; but on empty world it still dies.
    g = world(s, boundary="torus")
    g.tick()
    # A single cell has 0 neighbors on torus as well -> dies
    assert all(not g.is_alive(x, y) for y in range(g.height) for x in range(g.width))

