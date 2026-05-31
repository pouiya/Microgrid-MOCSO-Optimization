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

# Define the Gradient Ascent algorithm parameters
learning_rate = 0.01
max_iterations = 100

# Define the GradientAscent class
class GradientAscent:
    def __init__(self, max_iterations):
        self.max_iterations = max_iterations
        self.best_solution = None
        self.best_fitness = [np.inf, np.inf]
        self.pareto_set = []

    def update_fitness(self, solution):
        fitness = [f1(solution), f2(solution)]

        if all(f <= bf for f, bf in zip(fitness, self.best_fitness)):
            self.best_solution = solution.copy()
            self.best_fitness = fitness

        if all(all(f <= fi for f, fi in zip(solution, fitness)) for solution in self.pareto_set):
            self.pareto_set.append(fitness)

    def gradient_ascent(self):
        solution = [np.random.uniform(x1_min, x1_max), np.random.uniform(x2_min, x2_max)]

        for iteration in range(self.max_iterations):
            self.update_fitness(solution)

            gradient = [f1(solution), f2(solution)]

            # Update the solution using gradient ascent
            solution[0] += learning_rate * gradient[0]
            solution[1] += learning_rate * gradient[1]

            # Clip the solution to the feasible space
            solution[0] = max(min(solution[0], x1_max), x1_min)
            solution[1] = max(min(solution[1], x2_max), x2_min)

            print(f"Iteration: {iteration + 1}, Best Fitness: {self.best_fitness}")

        return self.best_solution

gradient_ascent = GradientAscent(max_iterations)
best_solution = gradient_ascent.gradient_ascent()

print("\nBest Solution:")
print(f"x1: {best_solution[0]}, x2: {best_solution[1]}")
print("Best Fitness:")
print(f"f1: {f1(best_solution)}, f2: {f2(best_solution)}")

print("\nPareto Optimal Solutions:")
for solution in gradient_ascent.pareto_set:
    print(f"f1: {solution[0]}, f2: {solution[1]}")