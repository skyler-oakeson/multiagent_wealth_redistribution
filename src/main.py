"""
This project is an implementation of the paper Local Wealth Redistribution
Promotes Cooperation in Multiagent Systems: https://arxiv.org/pdf/1802.01730.

Authored by Flavio L. Pinherio and Fernando P. Santos.
"""

from dilemma import Dilemma
from enum import Enum
from typing import TypedDict


class Strategy(Enum):
    """
    Decisions of agents.
    """
    COOPERATE = True
    DEFECT = False


class Node(TypedDict):
    """
    Represents an agent in the network.
    """
    strategy: Strategy
    utility: int
    surplus: int
    neighbors: set[int]


class Simulation():
    graph = {}
    edges: set[int] = set()  # edges can be represented as frozensets within this set to be immutable while avoiding repeats
    tax_threshold: float = 1  # default is 1 in the paper
    tax_rate: float = 0.1  # 0.0 - 1.0

    def __init__(self, num_nodes: int):
        self.graph: dict[int, Node] = {
            i: {
                "strategy": Strategy.COOPERATE if i % 2 == 0 else Strategy.DEFECT,  # even = cooperate, odd = defect
                "utility": 0,
                "surplus": 0,
                "neighbors": set()  # neighbors will be added later according to different graph structures
            }
            for i in range(num_nodes)
        }


    def build_HRG(self, degree: int):
        """
        Homogenous Random Graph: adds edges to self.graph with an even distribution
        
        degree (int): degree of each node
        """
        pass


    def build_PAG(self, avg_degree: int):
        """
        Preferential Attachment Graph: adds edges to self.graph using preferential attachment

        avg_degree (int): multiply by number of nodes in the graph to get total edges
        (we could alternativly pass in total edges to this function if that's easier)
        """
        pass


    def play(self, T: float=1.5):
        """
        Every node plays every other node in a single round of the Prisoner's Dilemma.

        R:	Reward	Both players Cooperate
        T:	Temptation	Defect while the other cooperates
        S:	Sucker's payoff	Cooperate while other defects
        P:	Punishment	Mutual Defection

        To be a real PD, payoffs must follow:

            T > R > P > S

        and also:

            2R > T+S

        for normalized PD where R = 1, P = 0, and S = 1 - T:
        
            1 < T < 2

        The game takes the form:

           |  C  |  D
        ---|-----|-----
         C | R,R | S,T
         D | T,S | P,P

        """
        pass


    def get_surplus(self, threshold: float = tax_threshold):
        """
        for each node, if the utility exceeds the threshold, move the surplus amount to self.graph[node]["surplus"]
        """
        pass


    def distribute_tax(self, tax_rate: float = tax_rate, radius: int = 1, rand: bool = False):
        """
        for each node, remove tax_rate * surplus from the surplus and distribute evenly to the neighbors in beneficiary radius

        radius: number of steps to create the beneficiary radius (e.g 1 = immediate neighbors only, 2 = neighbors and neighbors of neighbors)
        rand: if True, distribute the taxed surplus to a random set of nodes equal in size to the calculated beneficiary radius
        """
        pass


    def update_strategies(self, num_updates: int = 1):
        """
        update the strategy of a random set of nodes. The paper does this step like so:

            Pick a random agent and a random neighbor:
                - If the neighbor’s fitness (post-tax utility + any remaining surplus) is higher,
                - The agent may switch to the neighbor’s strategy (probabilistically)
                - there is a formula for calculating this probability outlined in the paper
        """
        pass


    def reset_payoffs(self):
        """
        reset payoffs so the simulation can be repeated
        """

        for node in self.graph.values():
            node['utility'] = 0
            node['surplus'] = 0


    def is_done(self):
        """
        checks if the graph has converged to all cooperate or all defect
        returns the winning policy if done else False
        """
        pass


    def run(self):
        """
        defines the main loop for the simulation
        """

        while True:
            self.play()
            self.get_surplus()
            self.distribute_tax()
            self.update_strategies()
            self.reset_payoffs()
            winning_stragety = self.is_done()
            if winning_stragety:
                return winning_stragety


if __name__ == "__main__":
    prisoners = Dilemma("prisoners", t=1.2)
    print(prisoners.play(True, False))
    # sim = Simulation(1000)
    # sim.build_HRG()
    # # or
    # # sim.build_PAG()
    # sim.run()
