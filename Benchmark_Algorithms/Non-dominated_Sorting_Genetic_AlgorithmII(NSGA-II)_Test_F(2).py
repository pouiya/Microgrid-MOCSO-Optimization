import random
import numpy as np
import matplotlib.pyplot as plt

# Define the objective functions
def objective_function_1(x1, x2):
    return -(x1)**2 + x2

def objective_function_2(x1, x2):
    return 0.5*x1 + x2 + 1

# Define the NSGA-II algorithm
class NSGA2:
    def __init__(self, objective_function_1, objective_function_2, num_generations, population_size):
        self.objective_function_1 = objective_function_1
        self.objective_function_2 = objective_function_2
        self.num_generations = num_generations
        self.population_size = population_size
        self.population = []
    
    def initialize_population(self):
        for _ in range(self.population_size):
            x1 = random.uniform(-10, 10)
            x2 = random.uniform(-10, 10)
            self.population.append([x1, x2])
    
    def evaluate_population(self):
        evaluated_population = []
        for solution in self.population:
            x1, x2 = solution
            f1 = self.objective_function_1(x1, x2)
            f2 = self.objective_function_2(x1, x2)
            evaluated_population.append([solution, [f1, f2]])
        return evaluated_population
    
    def fast_non_dominated_sort(self, evaluated_population):
        population_size = len(evaluated_population)
        S = [[] for _ in range(population_size)]
        frontiers = [[]]
        n = [0] * population_size
        rank = [0] * population_size

        for p in range(population_size):
            for q in range(population_size):
                if p != q:
                    if evaluated_population[p][1][0] > evaluated_population[q][1][0] and evaluated_population[p][1][1] > evaluated_population[q][1][1]:
                        if q not in S[p]:
                            S[p].append(q)
                    elif evaluated_population[p][1][0] < evaluated_population[q][1][0] and evaluated_population[p][1][1] < evaluated_population[q][1][1]:
                        n[p] += 1
            if n[p] == 0:
                rank[p] = 0
                if p not in frontiers[0]:
                    frontiers[0].append(p)

        i = 0
        while frontiers[i]:
            next_frontier = []
            for p in frontiers[i]:
                for q in S[p]:
                    n[q] -= 1
                    if n[q] == 0:
                        rank[q] = i + 1
                        if q not in next_frontier:
                            next_frontier.append(q)
            i += 1
            frontiers.append(next_frontier)

        return frontiers[:-1]

    def crowding_distance_assignment(self, evaluated_population, frontier):
        population_size = len(frontier)
        distances = [0] * population_size
        f1_values = [evaluated_population[i][1][0] for i in frontier]
        f2_values = [evaluated_population[i][1][1] for i in frontier]
        f1_sorted_indices = np.argsort(f1_values)
        f2_sorted_indices = np.argsort(f2_values)

        distances[f1_sorted_indices[0]] = np.inf
        distances[f1_sorted_indices[-1]] = np.inf
        distances[f2_sorted_indices[0]] = np.inf
        distances[f2_sorted_indices[-1]] = np.inf

        f1_range = max(f1_values) - min(f1_values)
        f2_range = max(f2_values) - min(f2_values)

        if f1_range == 0 or f2_range == 0:
            return distances

        for i in range(1, population_size-1):
            distances[f1_sorted_indices[i]] += (f1_values[f1_sorted_indices[i+1]] - f1_values[f1_sorted_indices[i-1]]) / f1_range
            distances[f2_sorted_indices[i]] += (f2_values[f2_sorted_indices[i+1]] - f2_values[f2_sorted_indices[i-1]]) / f2_range

        return distances
    
    def select_parents(self, evaluated_population, frontier):
        population_size = len(frontier)
        parents = []
        distances = self.crowding_distance_assignment(evaluated_population, frontier)
        
        for _ in range(2):
            max_distance_index = distances.index(max(distances))
            parents.append(frontier[max_distance_index])
            distances[max_distance_index] = -1
        
        return parents
    
    def crossover(self, parents):
        alpha = random.uniform(0, 1)
        child = [alpha * parents[0][0] + (1 - alpha) * parents[1][0],
                 alpha * parents[0][1] + (1 - alpha) * parents[1][1]]
        return child
    
    def mutation(self, child):
        mutation_rate = 0.1
        mutated_child = []
        
        for gene in child:
            if random.uniform(0, 1) < mutation_rate:
                mutated_gene = gene + random.uniform(-1, 1)
                mutated_child.append(mutated_gene)
            else:
                mutated_child.append(gene)
        
        return mutated_child
    
    def generate_offspring(self, evaluated_population, frontiers):
        offspring = []
        
        for frontier in frontiers:
            while len(offspring) < self.population_size:
                if random.uniform(0, 1) < 0.9:
                    parents = self.select_parents(evaluated_population, frontier)
                    child = self.crossover([evaluated_population[p][0] for p in parents])
                    mutated_child = self.mutation(child)
                    offspring.append(mutated_child)
                else:
                    random_solution = random.choice(frontier)
                    offspring.append(evaluated_population[random_solution][0])
        
        return offspring
    
    def run(self):
        self.initialize_population()
        
        for _ in range(self.num_generations):
            evaluated_population = self.evaluate_population()
            frontiers = self.fast_non_dominated_sort(evaluated_population)
            
            if len(frontiers) == 1:
                break
            
            self.population = self.generate_offspring(evaluated_population, frontiers)
        
        return evaluated_population

# Define the main function
def main():
    nsga2 = NSGA2(objective_function_1, objective_function_2, num_generations=100, population_size=100)
    evaluated_population = nsga2.run()
    
    f1_values = [evaluated_solution[1][0] for evaluated_solution in evaluated_population]
    f2_values = [evaluated_solution[1][1] for evaluated_solution in evaluated_population]
    
    plt.scatter(f1_values, f2_values)
    plt.xlabel('Objective Function 1')
    plt.ylabel('Objective Function 2')
    plt.title('Pareto Optimal Solutions')
    plt.show()

# Run the main function
if __name__ == '__main__':
    main()
