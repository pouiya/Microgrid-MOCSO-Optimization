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

# Define the PSO algorithm parameters
num_particles = 100
max_iterations = 100
w = 0.5  # inertia weight
c1 = 1.5  # cognitive weight
c2 = 1.5  # social weight

# Define the Particle class
class Particle:
    def __init__(self, x):
        self.x = x
        self.velocity = np.zeros_like(x)
        self.best_position = x
        self.best_fitness = math.inf

    def update_velocity(self, global_best_position):
        r1 = np.random.random()
        r2 = np.random.random()
        self.velocity = w * self.velocity + c1 * r1 * (self.best_position - self.x) + c2 * r2 * (global_best_position - self.x)

    def update_position(self):
        self.x = self.x + self.velocity
        self.check_boundary()

    def check_boundary(self):
        self.x[0] = np.clip(self.x[0], x1_min, x1_max)
        self.x[1] = np.clip(self.x[1], x2_min, x2_max)

    def evaluate_fitness(self):
        return f1(self.x), f2(self.x)

# Define the PSO class
class PSO:
    def __init__(self, num_particles, max_iterations):
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.particles = []
        self.global_best_position = np.zeros(2)
        self.global_best_fitness = math.inf

    def initialize_particles(self):
        self.particles = []
        for _ in range(self.num_particles):
            x = np.array([np.random.uniform(x1_min, x1_max), np.random.uniform(x2_min, x2_max)])
            particle = Particle(x)
            self.particles.append(particle)

    def update_global_best(self):
        for particle in self.particles:
            fitness = particle.evaluate_fitness()
            if all(f < self.global_best_fitness for f in fitness):
                self.global_best_fitness = min(self.global_best_fitness, *fitness)
                self.global_best_position = particle.x

    def update_particles(self):
        for particle in self.particles:
            particle.update_velocity(self.global_best_position)
            particle.update_position()

    def pso(self):
        self.initialize_particles()

        for iteration in range(self.max_iterations):
            self.update_global_best()
            self.update_particles()

            print(f"Iteration: {iteration + 1}, Best Fitness: {self.global_best_fitness}")

        pareto_set = [particle.evaluate_fitness() for particle in self.particles]
        return pareto_set

pso = PSO(num_particles, max_iterations)
pareto_set = pso.pso()

print("\nPareto Optimal Solutions:")
for solution in pareto_set:
    print(f"f1: {solution[0]}, f2: {solution[1]}")