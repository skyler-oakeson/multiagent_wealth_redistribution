"""
This project is an implementation of the paper Local Wealth Redistribution
Promotes Cooperation in Multiagent Systems: https://arxiv.org/pdf/1802.01730.

Authored by Flavio L. Pinherio and Fernando P. Santos.
"""

from dilemma import Dilemma
from enum import Enum
from typing import TypedDict
import math
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
    id: int
    neighbors: set[int]
    strategy: Strategy
    benefit: float
    surplus: float
    utility: float


class Simulation():
    def __init__(self, 
                 num_nodes: int,
                 temptation: float = 1.1, 
                 taxation: float = 0.1,
                 threshold: float = 1,
                 intensity: float = 1.0,
                 dilemma: None | Dilemma = None
                 ):

        self.num_nodes: int  = num_nodes
        self.dilemma: Dilemma = Dilemma(m=temptation) if not dilemma else dilemma
        self.temptation: float = temptation
        self.taxation: float = taxation
        self.intensity: float = intensity
        self.edges: set[frozenset[int]] = set()  # edges can be represented as frozensets within this set to be immutable while avoiding repeats
        self.graph: dict[int, Node] = {
            i: {
                "id": i,
                "strategy": Strategy.COOPERATE if i % 2 == 0 else Strategy.DEFECT,  # even = cooperate, odd = defect
                "utility": 0,
                "benefit": 0,
                "surplus": 0,
                "neighbors": set()  # neighbors will be added later according to different graph structures
            }
            for i in range(num_nodes)
        }


    def print_graph(self):
        """
        prints the graph with each node on a new line
        """
        for node, vals in self.graph.items():
            print(f"{node}: {vals}")


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

        available_nodes: list[int] = []

        # create the smallest possible starting graph (edges_new + 1 complete graph)
        for node_0 in range(edges_new):
            for node_1 in range(node_0 + 1, edges_new + 1):
                _ = self.__add_edge(node_0, node_1)
                available_nodes += [node_0, node_1]

        # add the rest of the nodes using preferential attachment
        for node_0 in range(edges_new + 1, self.num_nodes):
            edges_to_add = edges_new
            while edges_to_add > 0:
                node_1 = node_0
                while node_1 == node_0:
                    node_1 = random.choice(available_nodes)
                if self.__add_edge(node_0, node_1):
                    available_nodes += [node_0, node_1]
                    edges_to_add -= 1

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

        ∏_i = The accumulated payoff over all interactions agent i participates in.
        ∏_i = n_Ci * T - σ_i(1 - T) * (n_Di + n_Ci)
            where
                i = The agent
                n = Neighbors
                n_Ci = The number of neighbors that cooperate
                n_Di = The number of neighbors that defect
                σ_i = 1 if i is cooperator 0 if defector
                T = The temptation parameter
        """
        for edge in self.edges:
            edge = tuple(edge)
            node_0 = self.graph[edge[0]]
            node_1 = self.graph[edge[1]]
            rewards = self.dilemma.play(node_0["strategy"].value, node_1["strategy"].value)
            node_0["utility"] += rewards[0]
            node_1["utility"] += rewards[1]


    def random_node(self) -> int:
        return random.choice(list(self.graph.keys()))


    def random_neighbor(self, id: int) -> int:
        return random.choice(list(self.graph[id]["neighbors"]))


    def calc_surplus(self, threshold: float=1):
        """
        for each node, if the utility exceeds the threshold, move the surplus amount to self.graph[node]["surplus"]
        """
        for node in self.graph.values():
            if node["utility"] > threshold:
                node["surplus"] += node["utility"] - threshold
                node["utility"] = threshold


    def distribute_tax(self, radius: int = 1, rand: bool = False):
        """
        for each node, remove tax_rate * surplus from the surplus and distribute evenly to the neighbors in beneficiary radius

        radius: number of steps to create the beneficiary radius (e.g 1 = immediate neighbors only, 2 = neighbors and neighbors of neighbors)
        rand: if True, distribute the taxed surplus to a random set of nodes equal in size to the calculated beneficiary radius
        """
        for node in self.graph.values():
            if node['surplus'] > 0:
                beneficiary_set = [id for id in node["neighbors"] if self.graph[id]['surplus'] == 0]
                if len(beneficiary_set) == 0:
                    continue

                tax = node["surplus"] * self.taxation
                node["surplus"] -= tax
                share = tax / len(beneficiary_set)
                for neighbor in beneficiary_set:
                    self.graph[neighbor]["benefit"] += share

        # RANDOM
        #     nodes = list(self.graph.values())
        #     random.shuffle(nodes)




    def update_strategies(self, num_updates: int = 2):
        """
        This must run AFTER payoff and tax have been distributed.

        Update the strategy of a random set of nodes. The paper does this step like so:

            Pick a random agent and a random neighbor:
                - If the neighbor’s fitness (post-tax utility + beneifits) is higher,
                - The agent may switch to the neighbor’s strategy (probabilistically)
                - there is a formula for calculating this probability outlined in the paper



            This means if j is performing much better than i, then i updates
            his/her strategy adopting the strategy of j. Conversely, if j is
            performing much worse, i does not update the strategy -- Section 3.5
        """
        for update in range(num_updates):
            i = self.random_node()
            j = self.random_neighbor(i)
            fi = self.calculate_fitness(i)
            fj = self.calculate_fitness(j)
            p = self.calculate_mimicry_probablity(fi, fj)
            swap = random.choices([True, False], weights=[p, 1-p], k=1)
            if swap:
                self.graph[i]["strategy"] = self.graph[j]["strategy"]



    def calculate_mimicry_probablity(self, fi: float, fj: float) -> float:
        """
        p = The probability of agent i adopting agent j's strategy.
        p = 1 / 1 + Exp(-ß(f_i - f_j))
            where
                ß = Intensity of selection, a learning rate.
        """
        try:
            p = 1 / (1 + math.exp(-self.intensity * (fj - fi)))
            return p
        except:
            self.print_graph()
            raise Exception(f"Evaluation failed with {fi}, {fj}")



    def calculate_fitness(self, id: int) -> float:
        """
        f_i = Calculated by adding the money recived after taxation and beneifits have been distributed.
        f_i = (1 - α)(∏_i - θ) + Σ_j^Z (ơ_i,j * (α * (∏_j - θ))/ |B_j|)
            where
                f_i = Fitness of agent i.
                α = Taxation rate.
                θ = Surplus threshold.
                ∏_i = The accumulated payoff over all interactions agent i participates in.
                Σ_j^Z = Summation from j to Z.
                Z = The population size or amount of nodes.
                ơ_i,j = Is equal to one if i is part of the beneficiary set towards which j contributes 0 otherwise.
                |B_j| = The size of the beneficiary set j is a part of.

        (1 - α)(∏_i - θ) = Surplus AFTER tax.
        Σ_j^Z (ơ_i,j * (α * (∏_j - θ))/ |B_j|) = Total beneifits recived from the beneficiary sets i is a part of.

        The fitness of agent i comes from subtracting from their accumulated
        payoff (utility + surplus) their contributions plus the share they
        obtain from all beneficiary sets they participate in.
        """
        node = self.graph[id]
        return node['utility'] + node['surplus'] + node['benefit']


    def reset_payoffs(self):
        """
        reset payoffs so the simulation can be repeated
        """
        for node in self.graph.values():
            node['utility'] = 0
            node['surplus'] = 0
            node['benefit'] = 0


    def get_num_cooperate(self) -> int:
        """
        gets the number of cooperating nodes in the graph
        """
        num_cooperate = 0
        for node in self.graph.values():
            if node["strategy"] == Strategy.COOPERATE:
                num_cooperate += 1

        return num_cooperate


    def strategy_distribution(self) -> tuple[float, float]:
        """
        checks if the graph has converged to all cooperate or all defect
        returns the winning policy if done else None

        Returns
            tuple[float, float] = (cooperator %, defector %)
        """
        num_cooperate = self.get_num_cooperate()
        num_defect = self.num_nodes - num_cooperate
        return (num_cooperate / self.num_nodes, num_defect / self.num_nodes)


    def run(self, iterations: int) -> tuple[float, float]:
        """
        defines the main loop for the simulation
        """        
        for iter in range(iterations):
            print(f"Iteration: {iter}", end="\r")


            self.play()
            self.calc_surplus()
            self.distribute_tax()
            self.update_strategies()
            self.reset_payoffs()

            if iter % 1000 == 0:
                print(self.strategy_distribution())

        print(f"\rCompleted {iterations} rounds.")

        return self.strategy_distribution()


if __name__ == "__main__":
    sim = Simulation(10**3, temptation=1.6, taxation=0.7, threshold=.7, intensity=1.0)
    sim.build_PAG()
    print(sim.run(10**4))
