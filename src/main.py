"""
This project is an implementation of the paper Local Wealth Redistribution
Promotes Cooperation in Multiagent Systems: https://arxiv.org/pdf/1802.01730.

Authored by Flavio L. Pinherio and Fernando P. Santos.
"""

from dilemma import Dilemma
from enum import Enum
from typing import TypedDict
import random


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

    def __init__(self, num_nodes: int, dilemma: Dilemma=Dilemma()):
        self.num_nodes = num_nodes
        self.dilemma = dilemma
        self.graph: dict[int, Node] = {
            i: {
                "strategy": Strategy.COOPERATE if i % 2 == 0 else Strategy.DEFECT,  # even = cooperate, odd = defect
                "utility": 0,
                "surplus": 0,
                "neighbors": set()  # neighbors will be added later according to different graph structures
            }
            for i in range(num_nodes)
        }
        self.edges: set[frozenset] = set()  # edges can be represented as frozensets within this set to be immutable while avoiding repeats


    def __add_edge(self, node_0: int, node_1: int) -> bool:
        """
        Helper function for adding an edge to the graph
        """
        if frozenset((node_0, node_1)) in self.edges:
            return False
        self.graph[node_0]["neighbors"].add(node_1)
        self.graph[node_1]["neighbors"].add(node_0)
        self.edges.add(frozenset((node_0, node_1)))
        return True

    def build_HRG(self, degree: int=4, attempts: int=10):
        """
        Homogenous Random Graph: adds edges to self.graph with an even distribution
        this is a relaxed implementation where one node often ends up with with degree - 1 
        or degree - 2 becuase it's much simpler to implement and will serve the same purpose for 
        this simulation
        
        degree (int): degree of each node. degree < self.num_nodes
        attempts (int): stop building after this many consecutive failed attempts to create a new edge
        """
        if len(self.edges) > 0:
            print("This graph has already been populated")
            return
        
        assert degree < self.num_nodes

        available_nodes = set(range(self.num_nodes))
        unsuccessful = 0
        while len(available_nodes) > 1:
            node_0 = random.choice(list(available_nodes))
            node_1 = random.choice(list(available_nodes.difference({node_0})))
            if self.__add_edge(node_0, node_1):
                if len(self.graph[node_0]["neighbors"]) == degree:
                    available_nodes.remove(node_0)
                if len(self.graph[node_1]["neighbors"]) == degree:
                    available_nodes.remove(node_1)
                unsuccessful = 0
            else:
                unsuccessful += 1

            if unsuccessful == attempts:
                print(f"Quit building HRG after {attempts} consecutive failed attempts")
                return



    def build_PAG(self, edges_new: int=2):
        """
        Preferential Attachment Graph: adds edges to self.graph using preferential attachment

        edges_new (int): number of edges created when a new node enters the graph
        """
        if len(self.edges) > 0:
            print("This graph has already been populated")
            return
        
        assert edges_new < self.num_nodes

        available_nodes = []

        # create the smallest possible starting graph (edges_new + 1 complete graph)
        for node_0 in range(edges_new):
            for node_1 in range(node_0 + 1, edges_new + 1):
                self.__add_edge(node_0, node_1)
                available_nodes += [node_0, node_1]

        # add the rest of the nodes using preferential attachment
        for node_0 in range(edges_new + 1, self.num_nodes):
            for _ in range(edges_new):
                node_1 = random.choice(available_nodes)
                self.__add_edge(node_0, node_1)
                available_nodes += [node_0, node_1]


    def play(self): 
        """
        Every node plays every neighbor in a single round of the Prisoner's Dilemma.

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
        for edge in self.edges:
            edge = tuple(edge)
            node_0 = self.graph[edge[0]]
            node_1 = self.graph[edge[1]]
            rewards = self.dilemma.play(node_0["strategy"].value, node_1["strategy"].value)
            node_0["utility"] += rewards[0]
            node_1["utility"] += rewards[1]




    def calc_surplus(self, threshold: float=1):
        """
        for each node, if the utility exceeds the threshold, move the surplus amount to self.graph[node]["surplus"]
        """
        for node in self.graph.values():
            if node["utility"] > threshold:
                node["surplus"] += node["utility"] - threshold
                node["utility"] = threshold



    def distribute_tax(self, tax_rate: float=0.1, radius: int = 1, rand: bool = False):
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


    def get_num_cooperate(self) -> int:
        """
        gets the number of cooperating nodes in the graph
        """
        num_cooperate = 0
        for node in self.graph.values():
            if node["strategy"] == Strategy.COOPERATE:
                num_cooperate += 1

        return num_cooperate
    

    def is_done(self) -> Strategy:
        """
        checks if the graph has converged to all cooperate or all defect
        returns the winning policy if done else None
        """
        num_cooperate = self.get_num_cooperate()
        if num_cooperate == 0:
            return Strategy.DEFECT
        elif num_cooperate == self.num_nodes:
            return Strategy.COOPERATE
    

    def run(self):
        """
        defines the main loop for the simulation
        """        
        while True:
            self.play()
            self.calc_surplus()
            self.distribute_tax()
            self.update_strategies()
            self.reset_payoffs()
            winning_stragety = self.is_done()
            if winning_stragety is not None:
                return winning_stragety


if __name__ == "__main__":
    sh = Dilemma("staghunt", m=1.1)
    print(sh)
    # sim = Simulation(1000)
    # sim.build_HRG()
    # # or
    # # sim.build_PAG()
    # sim.run()