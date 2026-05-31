import numpy as np
import matplotlib.pyplot as plt
import random

"""
Multi-Objective Cat Swarm Optimization (MOCSO) for Microgrid Energy Management
This script optimizes the 24-hour scheduling of a Grid-Connected Microgrid.
"""

# ==========================================
# 1. Microgrid Parameters & 24-Hour Data
# ==========================================
LOAD = np.array([35, 32, 30, 32, 38, 50, 65, 75, 80, 85, 88, 85,
                 82, 80, 85, 90, 95, 98, 92, 85, 75, 60, 50, 40])

GRID_PRICE = np.array([0.12, 0.12, 0.12, 0.12, 0.12, 0.25, 0.35, 0.55, 0.55, 0.55, 0.35, 0.35,
                       0.35, 0.35, 0.35, 0.35, 0.55, 0.55, 0.55, 0.55, 0.35, 0.25, 0.12, 0.12])

PARAMS = {
    'MT': {'min': 10, 'max': 60, 'cost': 0.45, 'em': 0.72},
    'FC': {'min': 10, 'max': 40, 'cost': 0.35, 'em': 0.45},
    'WT': {'min': 0,  'max': 50, 'cost': 0.00, 'em': 0.00},
    'PV': {'min': 0,  'max': 40, 'cost': 0.00, 'em': 0.00},
    'GRID': {'min': -100, 'max': 100, 'em': 0.85} 
}

HOURS = 24
DIMENSIONS = 5 * HOURS

# ==========================================
# 2. Repair Mechanism & Objective Functions
# ==========================================
def repair_solution(pos):
    """Repairs the position to strictly satisfy capacity and power balance constraints."""
    repaired = np.copy(pos)
    for t in range(HOURS):
        idx = t * 5
        # Enforce Min/Max bounds for DGs
        repaired[idx]   = np.clip(repaired[idx], PARAMS['MT']['min'], PARAMS['MT']['max'])
        repaired[idx+1] = np.clip(repaired[idx+1], PARAMS['FC']['min'], PARAMS['FC']['max'])
        repaired[idx+2] = np.clip(repaired[idx+2], PARAMS['WT']['min'], PARAMS['WT']['max'])
        repaired[idx+3] = np.clip(repaired[idx+3], PARAMS['PV']['min'], PARAMS['PV']['max'])
        
        # Grid acts as slack variable to balance the load exactly
        dg_total = repaired[idx] + repaired[idx+1] + repaired[idx+2] + repaired[idx+3]
        required_grid = LOAD[t] - dg_total
        repaired[idx+4] = np.clip(required_grid, PARAMS['GRID']['min'], PARAMS['GRID']['max'])
    return repaired

def calculate_objectives(position):
    total_cost = 0.0
    total_emission = 0.0
    penalty = 0.0
    schedule = position.reshape((HOURS, 5))
    
    for t in range(HOURS):
        P_MT, P_FC, P_WT, P_PV, P_GRID = schedule[t]
        
        # Check power balance (should be 0 after repair, but just in case)
        mismatch = abs((P_MT + P_FC + P_WT + P_PV + P_GRID) - LOAD[t])
        penalty += mismatch * 1000 
        
        total_cost += (P_MT * PARAMS['MT']['cost'] + P_FC * PARAMS['FC']['cost'] + 
                       P_WT * PARAMS['WT']['cost'] + P_PV * PARAMS['PV']['cost'] + 
                       P_GRID * GRID_PRICE[t])
        
        total_emission += (P_MT * PARAMS['MT']['em'] + P_FC * PARAMS['FC']['em'] + 
                           P_WT * PARAMS['WT']['em'] + P_PV * PARAMS['PV']['em'] + 
                           (P_GRID if P_GRID > 0 else 0) * PARAMS['GRID']['em'])

    return total_cost + penalty, total_emission + penalty

def dominates(obj1, obj2):
    return (obj1[0] <= obj2[0] and obj1[1] <= obj2[1]) and (obj1[0] < obj2[0] or obj1[1] < obj2[1])

# ==========================================
# 3. MOCSO Algorithm Core
# ==========================================
class Cat:
    def __init__(self):
        self.position = np.random.uniform(-50, 100, DIMENSIONS)
        self.position = repair_solution(self.position)
        self.velocity = np.zeros(DIMENSIONS)
        self.cost, self.emission = calculate_objectives(self.position)
        self.objectives = [self.cost, self.emission]

def run_mocso(N=100, T_max=100):
    MR = 0.2  
    SMP = 5   
    c1 = 2.0  
    
    population = [Cat() for _ in range(N)]
    archive = []

    print("Starting MOCSO Optimization for Microgrid...")
    for iteration in range(T_max):
        # Update Archive
        combined = population + archive
        new_archive = []
        for i, c1_cat in enumerate(combined):
            is_dominated = False
            for j, c2_cat in enumerate(combined):
                if i != j and dominates(c2_cat.objectives, c1_cat.objectives):
                    is_dominated = True
                    break
            if not is_dominated:
                new_archive.append(c1_cat)
        
        # Remove duplicates based on fitness
        unique_archive = []
        seen = set()
        for cat in new_archive:
            obj_tuple = (round(cat.objectives[0], 2), round(cat.objectives[1], 2))
            if obj_tuple not in seen:
                seen.add(obj_tuple)
                unique_archive.append(cat)
                
        archive = unique_archive[:100] 
        g_best = random.choice(archive).position if archive else population[0].position

        # Evolve Population
        for cat in population:
            if random.random() < MR:
                # Seeking Mode
                best_clone_pos = cat.position.copy()
                best_clone_obj = cat.objectives
                for _ in range(SMP):
                    clone_pos = cat.position + np.random.uniform(-5, 5, DIMENSIONS)
                    clone_pos = repair_solution(clone_pos)
                    clone_obj = calculate_objectives(clone_pos)
                    if dominates(clone_obj, best_clone_obj):
                        best_clone_pos = clone_pos
                        best_clone_obj = clone_obj
                cat.position = best_clone_pos
            else:
                # Tracing Mode
                r = random.random()
                cat.velocity = cat.velocity + c1 * r * (g_best - cat.position)
                cat.position = cat.position + cat.velocity
                cat.position = repair_solution(cat.position)

            cat.cost, cat.emission = calculate_objectives(cat.position)
            cat.objectives = [cat.cost, cat.emission]

        if iteration % 10 == 0 or iteration == T_max - 1:
            print(f"Iteration {iteration+1}/{T_max} - Pareto Archive Size: {len(archive)}")

    return archive

# ==========================================
# 4. Execution & Plotting
# ==========================================
if __name__ == '__main__':
    pareto_front = run_mocso(N=100, T_max=100)
    
    costs = [cat.cost for cat in pareto_front]
    emissions = [cat.emission for cat in pareto_front]
    
    print("\nSample Optimal Pareto Solutions (Cost, Emissions):")
    for i in range(min(5, len(costs))):
        print(f"Solution {i+1}: Cost = {costs[i]:.2f}/day | Emissions = {emissions[i]:.2f} kg/day")
    
    plt.figure(figsize=(9, 6))
    plt.scatter(costs, emissions, color='green', marker='*', s=80, alpha=0.8, label='MOCSO (Extended CSO)')
    plt.title('Optimal Pareto Fronts for Microgrid Energy Management (MOCSO)', fontsize=14, fontweight='bold')
    plt.xlabel('Operational Cost (/day)', fontsize=12, fontweight='bold')
    plt.ylabel('Emissions (kg/day)', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()