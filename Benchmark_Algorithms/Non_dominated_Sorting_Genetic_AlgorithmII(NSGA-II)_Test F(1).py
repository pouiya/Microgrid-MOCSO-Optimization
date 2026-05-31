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

# Define the NSGA-II algorithm parameters
population_size = 100
max_iterations = 100
tournament_size = 2
crossover_rate = 0.9
mutation_rate = 0.1

# Define the Individual class
class Individual:
    def __init__(self, x):
        self.x = x
        self.objective_values = [f1(x), f2(x)]
        self.rank = None
        self.dominated_count = 0
        self.dominated_set = []

    def dominates(self, other):
        return all(f1_self <= f1_other and f2_self <= f2_other for f1_self, f2_self, f1_other, f2_other in zip(self.objective_values, other.objective_values, other.objective_values, other.objective_values))

# Define the NSGA-II class
class NSGA2:
    def __init__(self, population_size, max_iterations, tournament_size, crossover_rate, mutation_rate):
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.tournament_size = tournament_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population = []

    def initialize_population(self):
        self.population = []
        for _ in range(self.population_size):
            x = [np.random.uniform(x1_min, x1_max), np.random.uniform(x2_min, x2_max)]
            individual = Individual(x)
            self.population.append(individual)

    def non_dominated_sort(self):
        fronts = [[]]
        for individual in self.population:
            individual.dominated_set = []
            individual.dominated_count = 0

            for other in self.population:
                if individual.dominates(other):
                    individual.dominated_set.append(other)
                elif other.dominates(individual):
                    individual.dominated_count += 1

            if individual.dominated_count == 0:
                individual.rank = 0
                fronts[0].append(individual)

        current_rank = 0
        while len(fronts[current_rank]) > 0:
            next_front = []
            for individual in fronts[current_rank]:
                for other in individual.dominated_set:
                    other.dominated_count -= 1
                    if other.dominated_count == 0:
                        other.rank = current_rank + 1
                        next_front.append(other)
            current_rank += 1
            fronts.append(next_front)

        return fronts[:-1]

    def crowding_distance_assignment(self, front):
        num_objectives = len(front[0].objective_values)
        for individual in front:
            individual.distance = 0

        for m in range(num_objectives):
            front = sorted(front, key=lambda individual: individual.objective_values[m])
            front[0].distance = np.inf
            front[-1].distance = np.inf
            objective_range = front[-1].objective_values[m] - front[0].objective_values[m]
            if objective_range == 0:
                continue
            for i in range(1, len(front) - 1):
                front[i].distance += (front[i + 1].objective_values[m] - front[i - 1].objective_values[m]) / objective_range

    def selection(self, fronts):
        mating_pool = []
        fronts.sort(key=lambda front: front[0].rank)
        current_size = 0

        for front in fronts:
            if current_size + len(front) > self.population_size:
                self.crowding_distance_assignment(front)
                front.sort(key=lambda individual: individual.distance, reverse=True)
                mating_pool.extend(front[:self.population_size - current_size])
                break
            else:
                mating_pool.extend(front)
                current_size += len(front)

        return mating_pool

    def crossover(self, parent1, parent2):
        if np.random.random() < self.crossover_rate:
            x1_child = []
            x2_child = []

            for i in range(len(parent1.x)):
                if np.random.random() < 0.5:
                    x1_child.append(parent1.x[i])
                    x2_child.append(parent2.x[i])
                else:
                    x1_child.append(parent2.x[i])
                    x2_child.append(parent1.x[i])

            child1 = Individual(x1_child)
            child2 = Individual(x2_child)
            return child1, child2
        else:
            return parent1, parent2

    def mutation(self, individual):
        x_mutated = []

        for i in range(len(individual.x)):
            if np.random.random() < self.mutation_rate:
                x_mutated.append(np.random.uniform(x1_min, x1_max))
            else:
                x_mutated.append(individual.x[i])

        individual_mutated = Individual(x_mutated)
        return individual_mutated

    def create_offspring(self, mating_pool):
        offspring = []

        while len(offspring) < self.population_size:
            parent1 = np.random.choice(mating_pool)
            parent2 = np.random.choice(mating_pool)
            child1, child2 = self.crossover(parent1, parent2)
            child1_mutated = self.mutation(child1)
            child2_mutated = self.mutation(child2)
            offspring.extend([child1_mutated, child2_mutated])

        return offspring[:self.population_size]

    def nsga2(self):
        self.initialize_population()

        for iteration in range(self.max_iterations):
            fronts = self.non_dominated_sort()
            mating_pool = self.selection(fronts)
            self.population = self.create_offspring(mating_pool)

            print(f"Iteration: {iteration + 1}, Number of Pareto Optimal Solutions: {len(fronts[0])}")

        pareto_set = [individual.objective_values for individual in fronts[0]]
        return pareto_set

nsga2 = NSGA2(population_size, max_iterations, tournament_size, crossover_rate, mutation_rate)
pareto_set = nsga2.nsga2()

print("\nPareto Optimal Solutions:")
for solution in pareto_set:
    print(f"f1: {solution[0]}, f2: {solution[1]}")