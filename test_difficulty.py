from typing import List

import pytest

from difficulty import _calculate_party_thresholds, XpThresholds, _calculate_monster_xp, _multiplier, _count_monsters, \
    Difficulty, calculate_difficulty


@pytest.mark.parametrize(
    "party_levels, expected_thresholds",
    [
        ([1], XpThresholds(25, 50, 75, 100)),
        ([1, 1], XpThresholds(50, 100, 150, 200)),
        ([1, 2, 3], XpThresholds(150, 300, 450, 700)),
        ([20, 19, 10], XpThresholds(5800, 11800, 17700, 26400))
    ]
)
def test_calculate_party_thresholds(party_levels: List[int], expected_thresholds: XpThresholds):
    assert _calculate_party_thresholds(party_levels) == expected_thresholds


@pytest.mark.parametrize(
    "party_size, monster_count, expected_multiplier",
    [
        (1, 1, 1.5),
        (4, 1, 1.0),
        (4, 2, 1.5),
        (4, 3, 2.0),
        (4, 7, 2.5),
        (4, 11, 3.0),
        (4, 15, 4.0),
        (6, 15, 3.0),
        (7, 1, 1.0),
    ]
)
def test_multiplier(party_size: int, monster_count: int, expected_multiplier: float):
    assert _multiplier(party_size, monster_count) == expected_multiplier


@pytest.mark.parametrize(
    "monsters, expected_count",
    [
        ("1@1", 1),
        ("1@1,2@3", 3),
        ("3@1,1@3, 2@5", 6),
    ]
)
def test_count_monsters(monsters: str, expected_count: int):
    assert _count_monsters(monsters) == expected_count


@pytest.mark.parametrize(
    "party_size, monsters, expected_xp",
    [
        (1, "1@1", 300),
        (4, "3@1, 1@3", 2600),
        (7, "3@5, 1@10", 16950)
    ]
)
def test_calculate_monster_xp(party_size: int, monsters: str, expected_xp: int):
    assert _calculate_monster_xp(party_size, monsters) == expected_xp


@pytest.mark.parametrize(
    "thresholds, monsters_xp, expected_difficulty",
    [
        (XpThresholds(25, 50, 75, 100), 10, Difficulty.EASY),
        (XpThresholds(25, 50, 75, 100), 30, Difficulty.MEDIUM),
        (XpThresholds(25, 50, 75, 100), 60, Difficulty.HARD),
        (XpThresholds(25, 50, 75, 100), 79, Difficulty.DEADLY),
        (XpThresholds(800, 1600, 2400, 3600), 125, Difficulty.EASY),
        (XpThresholds(800, 1600, 2400, 3600), 1000, Difficulty.MEDIUM),
        (XpThresholds(800, 1600, 2400, 3600), 2400, Difficulty.HARD),
        (XpThresholds(800, 1600, 2400, 3600), 3000, Difficulty.DEADLY),
        (XpThresholds(800, 1600, 2400, 3600), 5000, Difficulty.DEADLY),
    ]
)
def test_resolve_difficulty(thresholds: XpThresholds, monsters_xp: int, expected_difficulty: Difficulty):
    assert thresholds.resolve(monsters_xp) == expected_difficulty


@pytest.mark.parametrize(
    "party, monsters, expected_difficulty",
    [
        ("1,1,1,1", "1@1", Difficulty.MEDIUM),
        ("1,1,1,1", "3@1", Difficulty.DEADLY),
        ("1,1,1,1,2,2,2", "7@1", Difficulty.DEADLY),
        ("1,1,1,1,2,2,2", "7@1/8", Difficulty.MEDIUM),
    ]
)
def test_calculate_difficulty(party: str, monsters: str, expected_difficulty: Difficulty):
    assert calculate_difficulty(party, monsters) == expected_difficulty
