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

# Define the Simulated Annealing algorithm parameters
initial_temperature = 100
final_temperature = 0.1
cooling_rate = 0.95
num_iterations = 1000

# Define the Simulated Annealing class
class SimulatedAnnealing:
    def __init__(self, initial_temperature, final_temperature, cooling_rate, num_iterations):
        self.initial_temperature = initial_temperature
        self.final_temperature = final_temperature
        self.cooling_rate = cooling_rate
        self.num_iterations = num_iterations
        self.best_solution = None
        self.best_fitness = math.inf

    def acceptance_probability(self, current_fitness, new_fitness, temperature):
        if np.all(new_fitness < current_fitness):
            return 1.0
        else:
            return math.exp(-abs(current_fitness[0] - new_fitness[0]) / temperature)

    def simulated_annealing(self):
        current_solution = np.array([np.random.uniform(x1_min, x1_max), np.random.uniform(x2_min, x2_max)])
        current_fitness = np.array([f1(current_solution), f2(current_solution)])
        self.best_solution = current_solution
        self.best_fitness = current_fitness

        temperature = self.initial_temperature

        for iteration in range(self.num_iterations):
            new_solution = np.array([np.random.uniform(x1_min, x1_max), np.random.uniform(x2_min, x2_max)])
            new_fitness = np.array([f1(new_solution), f2(new_solution)])

            probability = self.acceptance_probability(current_fitness, new_fitness, temperature)
            if np.random.random() < probability:
                current_solution = new_solution
                current_fitness = new_fitness

            if np.all(new_fitness < self.best_fitness):
                self.best_solution = new_solution
                self.best_fitness = new_fitness

            temperature *= self.cooling_rate

            print(f"Iteration: {iteration + 1}, Best Fitness: {self.best_fitness}")

        return [self.best_fitness]

sa = SimulatedAnnealing(initial_temperature, final_temperature, cooling_rate, num_iterations)
pareto_set = sa.simulated_annealing()

print("\nPareto Optimal Solutions:")
for solution in pareto_set:
    print(f"f1: {solution[0]}, f2: {solution[1]}")