from enum import Enum, unique, auto
from functools import reduce
from typing import List


@unique
class Difficulty(Enum):
    easy = auto()
    medium = auto()
    hard = auto()
    deadly = auto()

    def __str__(self):
        return self.name.upper()


class CR:
    label: str
    xp: int

    def __init__(self, label, xp):
        self.label = label
        self.xp = xp

    def __str__(self):
        return f"CR-{self.label}"


class XpThresholds:
    easy: int
    medium: int
    hard: int
    deadly: int

    def __init__(self, easy, medium, hard, deadly):
        self.easy = easy
        self.medium = medium
        self.hard = hard
        self.deadly = deadly

    def __add__(self, other):
        return XpThresholds(
            other.easy + self.easy,
            other.medium + self.medium,
            other.hard + self.hard,
            other.deadly + self.deadly
        )

    def __eq__(self, other):
        if isinstance(other, XpThresholds):
            return self.easy == other.easy \
                and self.medium == other.medium \
                and self.hard == other.hard \
                and self.deadly == other.deadly
        else:
            return False

    def __str__(self):
        return f"XpThresholds({self.easy}, {self.medium}, {self.hard}, {self.deadly})"

    def __repr__(self):
        return self.__str__()

    def resolve(self, xp: int) -> Difficulty:
        if xp <= self.easy:
            return Difficulty.easy
        elif self.easy < xp <= self.medium:
            return Difficulty.medium
        elif self.medium < xp <= self.hard:
            return Difficulty.hard
        else:
            return Difficulty.deadly


_crs: List[CR] = [
    CR("0", 10),
    CR("1/8", 25),
    CR("1/4", 50),
    CR("1/2", 100),
    CR("1", 200),
    CR("2", 450),
    CR("3", 700),
    CR("4", 1100),
    CR("5", 1800),
    CR("6", 2300),
    CR("7", 2900),
    CR("8", 3900),
    CR("9", 5000),
    CR("10", 5900),
    CR("11", 7200),
    CR("12", 8400),
    CR("13", 10000),
    CR("14", 11500),
    CR("15", 13000),
    CR("16", 15000),
    CR("17", 18000),
    CR("18", 20000),
    CR("19", 22000),
    CR("20", 25000),
    CR("21", 33000),
    CR("22", 41000),
    CR("23", 50000),
    CR("24", 62000),
    CR("25", 75000),
    CR("26", 90000),
    CR("27", 105000),
    CR("28", 120000),
    CR("29", 135000),
    CR("30", 155000)
]
_thresholds = [
    XpThresholds(25, 50, 75, 100),
    XpThresholds(50, 100, 150, 200),
    XpThresholds(75, 150, 225, 400),
    XpThresholds(125, 250, 375, 500),
    XpThresholds(250, 500, 750, 1100),
    XpThresholds(300, 600, 900, 1400),
    XpThresholds(350, 750, 1100, 1700),
    XpThresholds(450, 900, 1400, 2100),
    XpThresholds(550, 1100, 1600, 2400),
    XpThresholds(600, 1200, 1900, 2800),
    XpThresholds(800, 1600, 2400, 3600),
    XpThresholds(1000, 2000, 3000, 4500),
    XpThresholds(1100, 2200, 3400, 5100),
    XpThresholds(1250, 2500, 3800, 5700),
    XpThresholds(1400, 2800, 4300, 6400),
    XpThresholds(1600, 3200, 4800, 7200),
    XpThresholds(2000, 3900, 5900, 8800),
    XpThresholds(2100, 4200, 6300, 9500),
    XpThresholds(2400, 4900, 7300, 10900),
    XpThresholds(2800, 5700, 8500, 12700),
]


def calculate_difficulty(party: str, monsters: str) -> Difficulty:
    """Calculates the difficulty rating for the given party (levels) against the specified group of monsters
    (number@CR)."""
    # calculate the threshold for party levels
    party_levels = [int(lvl) for lvl in party.split(',')]
    party_size = len(party_levels)
    party_thresholds = _calculate_party_thresholds(party_levels)

    # calculate the challenge XP
    monster_xp = _calculate_monster_xp(party_size, monsters)

    # resolve the difficulty
    return party_thresholds.resolve(monster_xp)


def _calculate_party_thresholds(levels: List[int]) -> XpThresholds:
    return reduce(lambda a, b: a + b, map(_thresholds_for_level, levels))


def _thresholds_for_level(level: int) -> XpThresholds:
    return _thresholds[level - 1]


def _count_monsters(monsters: str) -> int:
    return sum(map(_to_count, monsters.split(',')))


def _calculate_monster_xp(party_size: int, monsters: str) -> int:
    monster_count = _count_monsters(monsters)
    monsters_total_xp = sum(map(_to_xp, monsters.split(',')))

    return round(monsters_total_xp * _multiplier(party_size, monster_count))


def _to_xp(num_at_cr: str) -> int:
    n_cr = num_at_cr.split('@')
    return int(n_cr[0]) * _cr_from_label(n_cr[1].strip()).xp


def _cr_from_label(label: str) -> CR:
    return list(filter(lambda c: c.label == label, _crs))[0]


def _to_count(num_at_cr: str) -> int:
    return int(num_at_cr.split('@')[0])


_MULTIPLIERS = [1.0, 1.5, 2, 2.5, 3.0, 4.0]


def _multiplier(party_size: int, monster_count: int) -> float:
    index = 1
    if monster_count == 1:
        index = 0
    elif monster_count == 2:
        index = 1
    elif 3 <= monster_count <= 6:
        index = 2
    elif 7 <= monster_count <= 10:
        index = 3
    elif 11 <= monster_count <= 14:
        index = 4
    else:
        index = 5

    # apply the party size adjustment
    if party_size < 3:
        index += 1
    elif party_size >= 6:
        index -= 1

    # make sure the index is in bounds
    index = max(min(index, 5), 0)

    return _MULTIPLIERS[index]
