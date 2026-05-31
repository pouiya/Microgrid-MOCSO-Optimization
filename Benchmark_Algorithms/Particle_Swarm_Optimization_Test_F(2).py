import numpy as np
import matplotlib.pyplot as plt

class Particle:
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

def update_particle(particle, global_best_position, w, c1, c2):
    r1 = np.random.random(particle.position.shape)
    r2 = np.random.random(particle.position.shape)
    particle.velocity = w * particle.velocity + c1 * r1 * (particle.best_position - particle.position) + c2 * r2 * (global_best_position - particle.position)
    particle.position = particle.position + particle.velocity
    particle.position = np.clip(particle.position, -5, 5)

def find_pareto_optimal_solutions(population):
    pareto_front = []
    for i, particle in enumerate(population):
        is_dominated = False
        for j, other_particle in enumerate(population):
            if i != j and dominates(other_particle.best_fitness, particle.best_fitness):
                is_dominated = True
                break
        if not is_dominated:
            pareto_front.append(particle)
    return pareto_front

def run_pso(num_particles, num_iterations):
    num_dimensions = 2
    w = 0.7
    c1 = 1.4
    c2 = 1.4
    population = [Particle(num_dimensions) for _ in range(num_particles)]
    global_best_position = population[0].position.copy()

    for _ in range(num_iterations):
        for particle in population:
            fitness1 = objective_function1(particle.position)
            fitness2 = objective_function2(particle.position)
            if particle.best_fitness is None or dominates([fitness1, fitness2], particle.best_fitness):
                particle.best_position = particle.position.copy()
                particle.best_fitness = [fitness1, fitness2]
            if dominates([fitness1, fitness2], global_best_position):
                global_best_position = particle.position.copy()
        for particle in population:
            update_particle(particle, global_best_position, w, c1, c2)
    
    pareto_optimal_solutions = find_pareto_optimal_solutions(population)
    return pareto_optimal_solutions

pareto_solutions = run_pso(num_particles=50, num_iterations=100)

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