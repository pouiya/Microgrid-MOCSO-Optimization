import numpy as np
import matplotlib.pyplot as plt

class Cat:
    def __init__(self, num_dimensions):
        self.position = np.random.uniform(-5, 5, num_dimensions)
        self.velocity = np.zeros(num_dimensions)
        self.best_position = self.position.copy()
        self.best_fitness = None

def objective_function1(x):
    return -(x[0]**2) + x[1]

def objective_function2(x):
    return 0.5 * x[0] + x[1] + 1

def dominates(fitness1, fitness2):
    return all(f1 >= f2 for f1, f2 in zip(fitness1, fitness2)) and any(f1 > f2 for f1, f2 in zip(fitness1, fitness2))

def update_cat(cat, global_best_position, w, c1, c2):
    r1 = np.random.random(cat.position.shape)
    r2 = np.random.random(cat.position.shape)
    cat.velocity = w * cat.velocity + c1 * r1 * (cat.best_position - cat.position) + c2 * r2 * (global_best_position - cat.position)
    cat.position = cat.position + cat.velocity
    cat.position = np.clip(cat.position, -5, 5)

def find_pareto_optimal_solutions(population):
    pareto_front = []
    for i, cat in enumerate(population):
        is_dominated = False
        for j, other_cat in enumerate(population):
            if i != j and dominates(other_cat.best_fitness, cat.best_fitness):
                is_dominated = True
                break
        if not is_dominated:
            pareto_front.append(cat)
    return pareto_front

def run_cso(num_cats, num_iterations):
    num_dimensions = 2
    w = 0.7
    c1 = 1.4
    c2 = 1.4
    population = [Cat(num_dimensions) for _ in range(num_cats)]
    global_best_position = population[0].position.copy()

    for _ in range(num_iterations):
        for cat in population:
            fitness1 = objective_function1(cat.position)
            fitness2 = objective_function2(cat.position)
            if cat.best_fitness is None or dominates([fitness1, fitness2], cat.best_fitness):
                cat.best_position = cat.position.copy()
                cat.best_fitness = [fitness1, fitness2]
            if dominates([fitness1, fitness2], global_best_position):
                global_best_position = cat.position.copy()
        for cat in population:
            update_cat(cat, global_best_position, w, c1, c2)
    
    pareto_optimal_solutions = find_pareto_optimal_solutions(population)
    return pareto_optimal_solutions

pareto_solutions = run_cso(num_cats=50, num_iterations=100)

# Print Pareto optimal solutions
print("Pareto Optimal Solutions:")
for solution in pareto_solutions:
    print("Fitness 1:", objective_function1(solution.position), "Fitness 2:", objective_function2(solution.position))

# Plot Pareto front
fitness1_values = [objective_function1(solution.position) for solution in pareto_solutions]
fitness2_values = [objective_function2(solution.position) for solution in pareto_solutions]
plt.scatter(fitness1_values, fitness2_values)
plt.xlabel("Fitness 1")
plt.ylabel("Fitness 2")
plt.title("Pareto Front")
plt.show()