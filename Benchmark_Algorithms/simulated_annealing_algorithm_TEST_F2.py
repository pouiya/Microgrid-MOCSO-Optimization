import numpy as np
import matplotlib.pyplot as plt

class Solution:
    def __init__(self, num_dimensions):
        self.position = np.random.uniform(-5, 5, num_dimensions)
        self.fitness = None

def objective_function1(x):
    return -(x[0]**2) + x[1]

def objective_function2(x):
    return 0.5 * x[0] + x[1] + 1

def dominates(fitness1, fitness2):
    return all(f1 >= f2 for f1, f2 in zip(fitness1, fitness2)) and any(f1 > f2 for f1, f2 in zip(fitness1, fitness2))

def update_solution(solution, temperature):
    new_position = solution.position + np.random.normal(0, temperature, solution.position.shape)
    new_position = np.clip(new_position, -5, 5)
    new_fitness = [objective_function1(new_position), objective_function2(new_position)]
    if solution.fitness is None or dominates(new_fitness, solution.fitness):
        solution.position = new_position.copy()
        solution.fitness = new_fitness.copy()

def find_pareto_optimal_solutions(population):
    pareto_front = []
    for i, solution in enumerate(population):
        is_dominated = False
        for j, other_solution in enumerate(population):
            if i != j and dominates(other_solution.fitness, solution.fitness):
                is_dominated = True
                break
        if not is_dominated:
            pareto_front.append(solution)
    return pareto_front

def run_sa(num_solutions, num_iterations, initial_temperature, final_temperature):
    num_dimensions = 2
    population = [Solution(num_dimensions) for _ in range(num_solutions)]
    global_best_solution = population[0]

    for iteration in range(num_iterations):
        temperature = initial_temperature * (final_temperature / initial_temperature) ** (iteration / num_iterations)
        for solution in population:
            update_solution(solution, temperature)
            if dominates(solution.fitness, global_best_solution.fitness):
                global_best_solution = solution
    
    pareto_optimal_solutions = find_pareto_optimal_solutions(population)
    return pareto_optimal_solutions

pareto_solutions = run_sa(num_solutions=50, num_iterations=100, initial_temperature=10, final_temperature=0.1)

# Print Pareto optimal solutions
print("Pareto Optimal Solutions:")
for solution in pareto_solutions:
    print("Fitness 1:", solution.fitness[0], "Fitness 2:", solution.fitness[1])

# Plot Pareto front
fitness1_values = [solution.fitness[0] for solution in pareto_solutions]
fitness2_values = [solution.fitness[1] for solution in pareto_solutions]
plt.scatter(fitness1_values, fitness2_values)
plt.xlabel("Fitness 1")
plt.ylabel("Fitness 2")
plt.title("Pareto Front")
plt.show()