""" 
This module implements different social dilemma 2X2 normal form games. 
"""

from typing import override

Rewards = tuple[float, float]
Choices = tuple[bool, bool]

class Dilemma:
    """
    Class for 2x2 normal form social dilemmas to be built on.

    Fields
    ------
    r: (int)  Reward            Both players Cooperate  
    t: (int)  Temptation        Defect while the other cooperates  
    s: (int)  Sucker            Cooperate while other defects  
    p: (int)  Punishment        Mutual Defection
    """

    r: float
    p: float
    s: float
    t: float

    def __init__(self, type: str = "prisoners", m: float = 1.5):
        """
        Games take the form:
           |  C  |  D
        ---|-----|-----
         C | R,R | S,T
         D | T,S | P,P

        Parameters
        ----------
        dilemma : str
            "prisoners": T > R > P > S
            "harmony": R > T > S > P
            "staghunt": R > T > P > S
            "snowdrift": T > R > S > P
            "deadlock": T > P > R > S

        m : float
            The motivation value or the greatest value the game, must be between 1 < m <= 2, default = 1.5
        """
        assert 1 < m <= 2

        # ordered from greatest to smallest
        values = [m, 1, 0, 1 - m]

        if type == "prisoners":
            self.t, self.r, self.p, self.s = values
        elif type == "harmony":
            self.r, self.t, self.s, self.p = values
        elif type == "staghunt":
            self.r, self.t, self.p, self.s = values
        elif type == "snowdrift":
            self.t, self.r, self.s, self.p = values
        elif type == "deadlock":
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

        board += "\n"
        for row_label, row in zip(["C", "D"], [True, False]):
            board += row_label + " "
            for col in [True, False]:
                r_val, c_val = self._board[(row, col)]
                board += "(%.1f, %.1f)" % (r_val, c_val)
            board += "\n"
        return board


    def play(self, r_move: bool, c_move: bool) -> Rewards:
        """ 
        Takes two bools representing a row and column player choice.
        Returns the utility values for both in a tuple (R, C).

        Parameters
        ----------
        r_move : bool
            The choice of the row player to cooperate (True) or defect (False).
            
        c_move : bool
            The choice of the column player to cooperate (True) or defect (False).

        Returns
        -------
        tuple[int, int]
            The resulting utility of a row and column players moves (RU, CU)
        """

        return self._board[(r_move, c_move)]
