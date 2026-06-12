import numpy as np
import matplotlib.pyplot as plt
import random

"""
Multi-Objective Cat Swarm Optimization (MOCSO) for Microgrid Energy Management
* Includes Smart Repair & Tournament Selection to prevent Archive Collapse
"""

# ==========================================
# 1. Microgrid Parameters & 24-Hour Data
# ==========================================
LOAD = np.array([40, 50, 60, 75, 85, 92, 98, 95, 90, 85, 80, 82,
                 82, 80, 85, 90, 95, 98, 92, 85, 75, 60, 50, 40])

GRID_PRICE = np.array([0.12, 0.12, 0.25, 0.35, 0.55, 0.55, 0.55, 0.55, 0.35, 0.35, 0.35, 0.35,
                       0.35, 0.35, 0.35, 0.35, 0.55, 0.55, 0.55, 0.55, 0.35, 0.25, 0.12, 0.12])

SOLAR_PROFILE = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.6, 0.8, 1.0, 1.0, 1.0, 
                          1.0, 0.9, 0.8, 0.6, 0.3, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

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
# 2. Smart Repair Mechanism & Objective Functions
# ==========================================
def repair_solution(pos):
    """Smartly repairs bounds and curtails excess generation to prevent penalty explosions."""
    repaired = np.copy(pos)
    for t in range(HOURS):
        idx = t * 5
        repaired[idx]   = np.clip(repaired[idx], PARAMS['MT']['min'], PARAMS['MT']['max'])
        repaired[idx+1] = np.clip(repaired[idx+1], PARAMS['FC']['min'], PARAMS['FC']['max'])
        repaired[idx+2] = np.clip(repaired[idx+2], PARAMS['WT']['min'], PARAMS['WT']['max'])
        
        pv_max_t = PARAMS['PV']['max'] * SOLAR_PROFILE[t]
        repaired[idx+3] = np.clip(repaired[idx+3], PARAMS['PV']['min'], pv_max_t)
        
        # Calculate required grid
        dg_total = repaired[idx] + repaired[idx+1] + repaired[idx+2] + repaired[idx+3]
        req_grid = LOAD[t] - dg_total
        
        # SMART REPAIR: If over-generating beyond grid capacity, curtail renewable energy
        if req_grid < PARAMS['GRID']['min']:
            excess = PARAMS['GRID']['min'] - req_grid
            # Reduce WT and PV equally to balance the equation natively
            repaired[idx+2] = max(PARAMS['WT']['min'], repaired[idx+2] - (excess / 2))
            repaired[idx+3] = max(PARAMS['PV']['min'], repaired[idx+3] - (excess / 2))
            # Recalculate grid
            dg_total = repaired[idx] + repaired[idx+1] + repaired[idx+2] + repaired[idx+3]
            req_grid = LOAD[t] - dg_total

        repaired[idx+4] = np.clip(req_grid, PARAMS['GRID']['min'], PARAMS['GRID']['max'])
    return repaired

def calculate_objectives(position):
    total_cost = 0.0
    total_emission = 0.0
    penalty = 0.0
    schedule = position.reshape((HOURS, 5))
    
    for t in range(HOURS):
        P_MT, P_FC, P_WT, P_PV, P_GRID = schedule[t]
        
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
# 3. Crowding Distance Calculation
# ==========================================
def calculate_crowding_distance(archive):
    length = len(archive)
    if length == 0: return
    
    for cat in archive:
        cat.distance = 0.0
        
    for m in range(2): 
        archive.sort(key=lambda x: x.objectives[m])
        archive[0].distance = float('inf')
        archive[-1].distance = float('inf')
        obj_min = archive[0].objectives[m]
        obj_max = archive[-1].objectives[m]
        
        if obj_max == obj_min: continue
        
        for i in range(1, length - 1):
            archive[i].distance += (archive[i+1].objectives[m] - archive[i-1].objectives[m]) / (obj_max - obj_min)

# ==========================================
# 4. MOCSO Algorithm Core
# ==========================================
class Cat:
    def __init__(self):
        # Initialized safely to prevent initial massive penalties
        self.position = np.random.uniform(0, 40, DIMENSIONS)
        self.position = repair_solution(self.position)
        self.velocity = np.zeros(DIMENSIONS)
        self.cost, self.emission = calculate_objectives(self.position)
        self.objectives = [self.cost, self.emission]
        self.distance = 0.0

def run_mocso(N=100, T_max=100):
    MR = 0.2  
    SMP = 5   
    c1 = 2.0  
    
    population = [Cat() for _ in range(N)]
    archive = []

    print("Starting Multi-Objective Cat Swarm Optimization (MOCSO)...")
    for iteration in range(T_max):
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
        
        unique_archive = []
        seen = set()
        for cat in new_archive:
            obj_tuple = (round(cat.objectives[0], 1), round(cat.objectives[1], 1))
            if obj_tuple not in seen:
                seen.add(obj_tuple)
                unique_archive.append(cat)
                
        calculate_crowding_distance(unique_archive)
        unique_archive.sort(key=lambda x: x.distance, reverse=True)
        archive = unique_archive[:100] 
        
        # TOURNAMENT SELECTION: Guarantees diversity and prevents archive collapse!
        if len(archive) > 2:
            candidates = random.sample(archive, 3)
            g_best = max(candidates, key=lambda x: x.distance).position
        else:
            g_best = archive[0].position if archive else population[0].position

        for cat in population:
            if random.random() < MR:
                best_clone_pos = cat.position.copy()
                best_clone_obj = cat.objectives
                for _ in range(SMP):
                    mutation_step = np.random.uniform(-0.05, 0.05, DIMENSIONS) * 100 
                    clone_pos = cat.position + mutation_step
                    clone_pos = repair_solution(clone_pos)
                    clone_obj = calculate_objectives(clone_pos)
                    if dominates(clone_obj, best_clone_obj):
                        best_clone_pos = clone_pos
                        best_clone_obj = clone_obj
                cat.position = best_clone_pos
            else:
                r = random.random()
                cat.velocity = cat.velocity + c1 * r * (g_best - cat.position)
                cat.velocity = np.clip(cat.velocity, -15, 15) 
                cat.position = cat.position + cat.velocity
                cat.position = repair_solution(cat.position)

            cat.cost, cat.emission = calculate_objectives(cat.position)
            cat.objectives = [cat.cost, cat.emission]

        if iteration % 10 == 0 or iteration == T_max - 1:
            print(f"Iteration {iteration+1}/{T_max} - Pareto Archive Size: {len(archive)}")

    return archive

# ==========================================
# 5. Execution & Plotting
# ==========================================
if __name__ == '__main__':
    pareto_front = run_mocso(N=100, T_max=100)
    
    pareto_front.sort(key=lambda x: x.cost)
    costs = [cat.cost for cat in pareto_front]
    emissions = [cat.emission for cat in pareto_front]
    
    print("\nSample Diverse Optimal Pareto Solutions (Cost, Emissions):")
    step = max(1, len(costs) // 5)
    for i in range(0, len(costs), step):
        if i < len(costs):
            print(f"Solution: Cost = ${costs[i]:.2f}/day | Emissions = {emissions[i]:.2f} kg/day")
    
    plt.figure(figsize=(9, 6))
    plt.scatter(costs, emissions, color='green', marker='*', s=80, alpha=0.8, label='MOCSO (Extended CSO)')
    plt.title('Optimal Pareto Fronts for Microgrid Energy Management (MOCSO)', fontsize=14, fontweight='bold')
    plt.xlabel('Operational Cost ($/day)', fontsize=12, fontweight='bold')
    plt.ylabel('Emissions (kg/day)', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()
