""" 
This module implements the different social dilemmas possible. Each dilemma
is a sub class of the base class Dilemma. Dilemma implements all the behavior
of a game and the subclasses insure we are following the rules for each game.
Every dilemma has 4 reward arguments required. Each subclass implements their
constructor to take the biggest reward first descending. 

Prisoners(4, 3, 2, 1)
StagHunt(4, 3, 2, 1)
"""

from abc import ABC

Rewards = tuple[int, int]
Choices = tuple[bool, bool]

class Dilemma(ABC):
    """
    Abstract base class for all social dilemmas to be built on.

    Parameters:
        reward (int): Utility value of both players cooperating.
        punishment (int): Utility value of both players defecting.
        sucker (int): Utility value of a player that cooperated while the other defected.
        temptation (int): Utility value of a player that defected while the other cooperated.
    """
    def __init__(self, reward: int, punishment: int, sucker: int, temptation: int):

        self.reward: int = reward
        self.punishment: int = punishment
        self.sucker: int = sucker
        self.temptation: int = temptation

        self._board: dict[Choices, Rewards] = {
         (True, True): (reward, reward),
         (True, False): (sucker, temptation),
         (False, True): (temptation, sucker) ,
         (False, False): (punishment, punishment),
         }


    def play(self, r_move: bool, c_move: bool) -> Rewards:
        """ 
        Takes two bools representing a row and col player choice.
        Returns the utility values for both in a tuple (R, C).
        """

        return self._board[(r_move, c_move)]


class Prisoners(Dilemma):
    """
    Canonical prisoners dilemma T > R > P > S

    Properties appear in order of greatest to smallest

    Properties:
        temptation: int, 
        reward: int,
        punishment: int,
        sucker: int
    """

    def __init__(self, temptation: int, reward: int, punishment: int, sucker: int):
        assert(temptation > reward > punishment > sucker)
        super().__init__(reward, punishment, sucker, temptation)


class StagHunt(Dilemma):
    """
    Stag hunt dilemma R > T > P > S

    Properties appear in order of greatest to smallest

    Properties:
        reward: int, 
        temptation: int,
        punishment: int,
        sucker: int
    """

    def __init__(self, reward: int, temptation: int, punishment: int, sucker: int):
        assert(reward > temptation > punishment > sucker)
        super().__init__(reward, punishment, sucker, temptation)


class Snowdrift(Dilemma):
    """
    Snowdrift dilemma T > R > S > P

    Properties:
        temptation: int, 
        reward: int,
        sucker: int,
        punishment: int
    """

    def __init__(self, temptation: int, reward: int, sucker: int, punishment: int):
        assert(temptation > reward > sucker > punishment)
        super().__init__(reward, temptation, sucker, punishment)


class Harmony(Dilemma):
    """
    Harmony dilemma R > T > S > P

    Properties appear in order of greatest to smallest

    Properties:
        reward: int, 
        temptation: int,
        sucker: int,
        punishment: int
    """

    def __init__(self, reward: int, temptation: int, sucker: int, punishment: int):
        assert(reward > temptation > sucker > punishment)
        super().__init__(reward, punishment, sucker, temptation)

class Deadlock(Dilemma):
    """
    Deadlock dilemma T > P > R > S

    Properties appear in order of greatest to smallest

    Properties:
        temptation: int, 
        punishment: int,
        reward: int,
        sucker: int
    """

    def __init__(self, temptation: int, punishment: int, reward: int, sucker: int):
        assert(temptation > punishment > reward > sucker)
        super().__init__(reward, punishment, sucker, temptation)

