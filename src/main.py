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
                 dilemma: None | Dilemma = None
                 ):

        self.num_nodes: int  = num_nodes
        self.beneficiary_sets: dict[int, set[int]] = {} # this is used to memoize collecting the sets
        self.edges: set[frozenset[int]] = set()  # edges can be represented as frozensets within this set to be immutable while avoiding repeats
        self.graph: dict[int, Node] = {
            i: {
                'id': i,
                'strategy': Strategy.COOPERATE if i % 2 == 0 else Strategy.DEFECT,  # even = cooperate, odd = defect
                'utility': 0,
                'benefit': 0,
                'surplus': 0,
                'neighbors': set()  # neighbors will be added later according to different graph structures
            }
            for i in range(num_nodes)
        }


    def print_graph(self):
        """
        Prints the graph with each node on a new line
        """
        for node, vals in self.graph.items():
            print(f'{node}: {vals}')


    def __add_edge(self, node_0: int, node_1: int) -> bool:
        """
        Helper function for adding an edge to the graph
        """
        if frozenset((node_0, node_1)) in self.edges:
            return False
        self.graph[node_0]['neighbors'].add(node_1)
        self.graph[node_1]['neighbors'].add(node_0)
        self.edges.add(frozenset((node_0, node_1)))
        return True


    def build_HRG(self, degree: int=4, attempts: int=10):
        """
        Homogenous Random Graph: adds edges to self.graph with an even distribution
        this is a relaxed implementation where one node often ends up with with degree - 1 
        or degree - 2 becuase it's much simpler to implement and will serve the same purpose for 
        this simulation

        Parameters
        ----------
            degree : int 
                Degree of each node. (degree < self.num_nodes)

            attempts : int
                Stop building after this many consecutive failed attempts to create a new edge.
        """
        if len(self.edges) > 0:
            print('This graph has already been populated')
            return
        
        assert degree < self.num_nodes

        available_nodes = set(range(self.num_nodes))
        unsuccessful = 0
        while len(available_nodes) > 1:
            node_0 = random.choice(list(available_nodes))
            node_1 = random.choice(list(available_nodes.difference({node_0})))
            if self.__add_edge(node_0, node_1):
                if len(self.graph[node_0]['neighbors']) == degree:
                    available_nodes.remove(node_0)
                if len(self.graph[node_1]['neighbors']) == degree:
                    available_nodes.remove(node_1)
                unsuccessful = 0
            else:
                unsuccessful += 1

            if unsuccessful == attempts:
                print(f'Quit building HRG after {attempts} consecutive failed attempts')
                return


    def build_PAG(self, edges_new: int=2):
        """
        Preferential Attachment Graph: adds edges to self.graph using preferential attachment

        Parameters
        ----------
        edges_new : int 
            Number of edges created when a new node enters the graph.
        """
        if len(self.edges) > 0:
            print('This graph has already been populated')
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

    def play(self, temptation: float = 1.5, dtype: str ='prisoners'): 
        """
        Every node plays every neighbor in a single round of the Prisoner's Dilemma.

        R:	Reward both players cooperate
        T:	Temptation defect while the other cooperates
        S:	Sucker's payoff	cooperate while other defects
        P:	Punishment mutual defection

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

        ∏_i = the accumulated payoff over all interactions agent i participates in.
        ∏_i = n_Ci * T - σ_i(1 - T) * (n_Di + n_Ci)
            where
                i    = the agent
                n_Ci = the number of neighbors that cooperate
                n_Di = the number of neighbors that defect
                σ_i  = 1 if i is cooperator 0 if defector
                T    = the temptation parameter
        """
        dilemma = Dilemma(m=temptation, type=dtype)
        for edge in self.edges:
            edge = tuple(edge)
            node_0 = self.graph[edge[0]]
            node_1 = self.graph[edge[1]]
            row, col = dilemma.play(node_0['strategy'].value, node_1['strategy'].value)
            node_0['utility'] += row
            node_1['utility'] += col


    def random_node(self) -> int:
        return random.choice(list(self.graph.keys()))


    def random_neighbor(self, id: int) -> int:
        return random.choice(list(self.graph[id]["neighbors"]))


    def calc_surplus(self, threshold: float = 1.0):
        """
        For each node, if the utility exceeds the threshold, move the surplus
        amount to self.graph[node]["surplus"]
        """
        for node in self.graph.values():
            if node['utility'] > threshold:
                node['surplus'] += node['utility'] - threshold
                node['utility'] = threshold


    def distribute_tax(self, taxation: float = .5, radius: int = 1, rand: bool = False) -> None:
        """
        For each node, tax from the surplus and distribute the tax evenly to
        the neighbors in beneficiary radius.

        Parameters
        ----------
        radius : int 
            Number of steps to create the beneficiary radius 
            (e.g 1 = immediate neighbors only, 2 = neighbors and neighbors of neighbors)

        rand: bool 
            If True, distribute the taxed surplus to a random set of nodes
            equal in size to the calculated beneficiary radius.
        """

        for id, node in self.graph.items():
            if node['surplus'] > 0:
                beneficiary_set = self.collect_random_beneficiary_set(id) if rand else self.collect_beneficiary_set(id, radius)
                if len(beneficiary_set) == 0:
                    continue

                tax = node['surplus'] * taxation
                node['surplus'] -= tax
                share = tax / len(beneficiary_set)
                for neighbor in beneficiary_set:
                    self.graph[neighbor]['benefit'] += share


    def collect_beneficiary_set(self, center: int, radius: int) -> set[int]:
        if center in self.beneficiary_sets:
            return self.beneficiary_sets[center]

        stack = [(0, center)]
        visted: set[int] = set()
        while stack:
            dist, curr = stack.pop(0)
            visted.add(curr)
            if dist < radius:
                for next in self.graph[curr]['neighbors']:
                    stack.insert(0, (dist+1, next))
        visted.remove(center)
        self.beneficiary_sets[center] = visted

        return visted


    def collect_random_beneficiary_set(self, id: int) -> set[int]:
        if id in self.beneficiary_sets:
            return self.beneficiary_sets[id]
        degree = len(self.graph[id]['neighbors'])
        random_set: set[int] = set()
        for _ in range(degree):
            random_set.add(random.randint(0, self.num_nodes - 1))
        self.beneficiary_sets[id] = random_set

        return random_set


    def update_strategies(self, intensity: float = 1.0, num_updates: int = 1):
        """
        Update the strategy of a random set of nodes. The paper does this step like so:

            Pick a random agent and a random neighbor:
                - If the neighbor’s fitness (post-tax utility + beneifits) is higher,
                - The agent may switch to the neighbor’s strategy (probabilistically)
                - There is a formula for calculating this probability outlined
                  in the paper

        If j is performing much better than i, then i updates
        his/her strategy adopting the strategy of j. Conversely, if j is
        performing much worse, i does not update the strategy.

        p = the probability of agent i adopting agent j's strategy
        p = 1 / 1 + Exp(-ß(f_i - f_j))
            where
                ß = intensity of selection, a learning rate.
                    * large ß means they will update at minor differences
                    * small ß means they are prone to make immitation mistakes
        """
        for _ in range(num_updates):
            i = self.random_node()
            j = self.random_neighbor(i)
            fi = self.calculate_fitness(i)
            fj = self.calculate_fitness(j)
            p = 1 / (1 + math.exp(-intensity * (fj - fi)))
            if random.choices([True, False], weights=[p, 1-p], k=1):
                self.graph[i]['strategy'] = self.graph[j]['strategy']



    def calculate_fitness(self, id: int) -> float:
        """
        The fitness of agent i comes from subtracting their taxes from their
        accumulated payoff (surplus + beneifits)
        
        f_i = calculated by adding the utility recived after taxation and
              beneifits have been distributed.
        f_i = (1 - α)(∏_i - θ) + Σ_j^Z (ơ_i,j * (α * (∏_j - θ))/ |B_j|)
            where
                f_i   = fitness of agent i
                α     = taxation rate
                θ     = surplus threshold
                ∏_i   = the accumulated payoff over all interactions agent i
                        participates in
                Σ_j^Z = summation overall nodes in the graph
                Z     = the population size or amount of nodes
                ơ_i,j = is equal to one if i is part of the beneficiary set
                        towards which j contributes 0 otherwise
                |B_j| = the size of the beneficiary set j is a part of

        Parameters
        ----------
        id : int
            The id of the agent.
        """
        node = self.graph[id]
        return node['surplus'] + node['benefit']


    def reset_payoffs(self):
        """
        Reset payoffs so the simulation can be repeated
        """
        for node in self.graph.values():
            node['utility'] = 0
            node['surplus'] = 0
            node['benefit'] = 0


    def get_num_cooperate(self) -> int:
        """
        Gets the number of cooperating nodes in the graph

        Returns
        -------
        int : The number of cooperators.
        """
        num_cooperate = 0
        for node in self.graph.values():
            if node['strategy'] == Strategy.COOPERATE:
                num_cooperate += 1

        return num_cooperate


    def strategy_distribution(self) -> tuple[float, float]:
        """
        Calculates the distribution of cooperators and defectors.

        Returns
        -------
        tuple[float, float]
            The percentage of cooperators and defectors (cooperator %, defector %).
        """
        num_cooperate = self.get_num_cooperate()
        num_defect = self.num_nodes - num_cooperate
        return num_cooperate / self.num_nodes, num_defect / self.num_nodes


    def run(self, iterations: int) -> tuple[float, float]:
        """
        Defines the main loop for the simulation
        """        
        for iter in range(iterations):
            print("Iteration:", iter, end="\r")
            self.play(temptation=1.2)
            self.calc_surplus(threshold=1.0)
            self.distribute_tax(taxation=.7, radius=2)
            self.update_strategies(intensity=1.0, num_updates=1)
            self.reset_payoffs()
            if iter % 1000 == 0:
                print(iter, ":", self.strategy_distribution())

        print(f"\rCompleted {iterations} rounds.")

        return self.strategy_distribution()
    


    def average_degree(self) -> float:
        return sum(len(node['neighbors']) for node in self.graph.values()) / self.num_nodes



if __name__ == '__main__':
    sim = Simulation(10**3)
    sim.build_HRG()
    coop, defect = sim.run(10**4)
    print(f"Percentage of Cooperators: {coop * 100}% \nPercentage of Defectors:   {defect * 100}%")
