import numpy as np
import math

# Define the objective functions
def f1(x):
    return x[0]

def f2(x):
    return x[0] * x[1]

# Define the constraint functions
def g(x):
    return 11 + x[1]**2 - 10 * math.cos(2 * math.pi * x[1])

def h(x):
    if f1(x) <= g(x):
        return 1 - f1(x) / g(x)
    else:
        return 0

# Define the bounds of the decision variables
x1_min = 0
x1_max = 1
x2_min = -30
x2_max = 30

# Define the CSO parameters
num_agents = 50
max_iterations = 100
w = 0.5
c1 = 2
c2 = 2

# Define the CSO class
class CSO:
    def __init__(self, num_agents, max_iterations):
        self.num_agents = num_agents
        self.max_iterations = max_iterations
        self.agents = []
        self.best_agent = None
        self.best_fitness = [np.inf, np.inf]
        self.pareto_set = []

    def initialize_agents(self):
        for _ in range(self.num_agents):
            x1 = np.random.uniform(x1_min, x1_max)
            x2 = np.random.uniform(x2_min, x2_max)
            agent = [x1, x2]
            self.agents.append(agent)

    def update_fitness(self):
        for agent in self.agents:
            fitness = [f1(agent), f2(agent)]
            agent.extend(fitness)

            if all(f <= bf for f, bf in zip(fitness, self.best_fitness)):
                self.best_agent = agent.copy()
                self.best_fitness = fitness

            if all(all(f <= fi for f, fi in zip(solution, fitness)) for solution in self.pareto_set):
                self.pareto_set.append(fitness)

    def update_agents(self, iteration):
        for agent in self.agents:
            r1 = np.random.random()
            r2 = np.random.random()

            velocity = [w * v + c1 * r1 * (self.best_agent[i] - agent[i]) + c2 * r2 * (self.best_agent[i] - agent[i])
                        for i, v in enumerate(agent[:2])]

            new_agent = [agent[i] + velocity[i] for i in range(2)]
            new_agent = self.check_boundary(new_agent)

            agent[:2] = new_agent

    def check_boundary(self, agent):
        agent[0] = max(min(agent[0], x1_max), x1_min)
        agent[1] = max(min(agent[1], x2_max), x2_min)
        return agent

    def run(self):
        self.initialize_agents()

        for iteration in range(self.max_iterations):
            self.update_fitness()
            self.update_agents(iteration)

            print(f"Iteration: {iteration + 1}, Best Fitness: {self.best_fitness}")

cso = CSO(num_agents, max_iterations)
cso.run()

print("\nPareto Optimal Solutions:")
for solution in cso.pareto_set:
    print(f"f1: {solution[0]}, f2: {solution[1]}")