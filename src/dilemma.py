""" 
This module implements different social dilemmas normal form games. Each
is generated from an ordering of utility values.
"""

from enum import Enum
from typing import assert_never, override

Rewards = tuple[float, float]
Choices = tuple[bool, bool]

class Dilemma:
    """
    Abstract base class for all social dilemmas to be built on.

    r (int): Reward utility value of both players cooperating.
    p (int): Punishment utility value of both players defecting.
    s (int): Sucker utility value of a player that cooperated while the other defected.
    t (int): Temptation utility value of a player that defected while the other cooperated.

    Dilemmas:
        prisoners: T > R > P > S
        harmony: R > T > S > P
        staghunt: R > T > P > S
        snowdrift: T > R > S > P
        deadlock: T > P > R > S
    """

    r: float
    p: float
    s: float
    t: float

    def __init__(self, dilemma: str = "prisoners", t: float = 1.5):
        assert 1 < t <= 2
        values = [t, 1, 0, 1 - t]

        if dilemma == "prisoners":
            self.t, self.r, self.p, self.s = values
        elif dilemma == "harmony":
            self.r, self.t, self.s, self.p = values
        elif dilemma == "staghunt":
            self.r, self.t, self.p, self.s = values
        elif dilemma == "snowdrift":
            self.t, self.r, self.s, self.p = values
        elif dilemma == "deadlock":
            self.t, self.p, self.r, self.s = values
        else:
            raise Exception("Dilemma not in [prisoners, harmony, staghunt, snowdrift, deadlock]")

        self._board: dict[Choices, Rewards] = {
         (True, True): (self.r, self.r),
         (True, False): (self.s, self.t),
         (False, True): (self.t, self.s) ,
         (False, False): (self.p, self.p),
         }

    @override
    def __repr__(self) -> str:
        board = "  "
        for i, col in enumerate(["C", "D"]):
            board += f"{col}" + " " * 9

        board += f"\n" 
        for row_label, row in zip(["C", "D"], [True, False]):
            board += row_label + " "
            for col in [True, False]:
                r_val, c_val = self._board[(row, col)]
                board += "(%.1f, %.1f)" % (r_val, c_val)
            board += f"\n" 
        return board


    def play(self, r_move: bool, c_move: bool) -> Rewards:
        """ 
        Takes two bools representing a row and col player choice.
        Returns the utility values for both in a tuple (R, C).
        """

        return self._board[(r_move, c_move)]
