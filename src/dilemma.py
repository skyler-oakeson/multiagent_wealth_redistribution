""" 
This module implements the different social dilemmas possible. Each dilemma
is a sub class of the base class Dilemma. Dilemma implements all the behavior
of a game and the subclasses insure we are following the rules for each game.
Every dilemma has 4 reward arguments required. Each subclass implements their
constructor to take the biggest reward first descending. 

Prisoners(4, 3, 2, 1)
StagHunt(4, 3, 2, 1)
"""

from abc import ABC, abstractmethod
from typing import override

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

        self._reward: int = reward
        self._punishment: int = punishment
        self._sucker: int = sucker
        self._temptation: int = temptation

        self._board: dict[Choices, Rewards] = {
         (True, True): (reward, reward),
         (True, False): (sucker, temptation),
         (False, True): (temptation, sucker) ,
         (False, False): (punishment, punishment),
         }

    @abstractmethod
    def assert_values(self):
        """
        Abstract method to ensures that a dilemmas values are correct.
        """

    def play(self, r_move: bool, c_move: bool) -> Rewards:
        """ 
        Takes two bools representing a row and col player choice.
        Returns the utility values for both in a tuple (R, C).
        """

        return self._board[(r_move, c_move)]

    @property
    def reward(self):
        """ Reward property getter """
        return self._reward

    @reward.setter
    def reward(self, reward: int):
        """ Reward property setter """
        self._reward = reward
        self.assert_values()
        self._board[(True,True)] = (self._reward, self._reward)

    @property
    def sucker(self):
        """ Sucker property getter """
        return self._sucker

    @sucker.setter
    def sucker(self, sucker: int):
        """ Sucker property setter """
        self._sucker = sucker
        self.assert_values()
        self._board[(True,False)] = (self._sucker, self._temptation)
        self._board[(False,True)] = (self._temptation, self._sucker)

    @property
    def punishment(self):
        """ Punishment property getter """
        return self._punishment

    @punishment.setter
    def punishment(self, punishment: int):
        """ Punishment property setter """
        self._punishment = punishment
        self.assert_values()
        self._board[(False,False)] = (self._punishment, self._punishment)

    @property
    def temptation(self):
        """ Temptation property getter """
        return self._temptation

    @temptation.setter
    def temptation(self, temptation: int):
        """ Temptation property setter """
        self._temptation = temptation
        self.assert_values()
        self._board[(True,False)] = (self._sucker, self._temptation)
        self._board[(False,True)] = (self._temptation, self._sucker)

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
        super().__init__(reward, punishment, sucker, temptation)
        self.assert_values()

    @override
    def assert_values(self):
        assert self.temptation > self.reward > self.punishment > self.sucker


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
        super().__init__(reward, punishment, sucker, temptation)
        self.assert_values()

    @override
    def assert_values(self):
        assert self.reward > self.temptation > self.punishment > self.sucker


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
        assert temptation > reward > sucker > punishment
        super().__init__(reward, punishment, sucker, temptation)

    @override
    def assert_values(self):
        assert self.temptation > self.reward > self.sucker > self.punishment


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
        super().__init__(reward, punishment, sucker, temptation)
        self.assert_values()

    @override
    def assert_values(self):
        assert self.reward > self.temptation > self.sucker > self.punishment


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
        super().__init__(reward, punishment, sucker, temptation)
        self.assert_values()

    @override
    def assert_values(self):
        assert self.temptation > self.punishment > self.reward > self.sucker
