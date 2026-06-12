import numpy as np
import matplotlib.pyplot as plt
import random

# پارامترهای استخراج شده از جدول 3 و 4 مقاله [cite: 1100, 1116]
LOAD = np.array([40, 50, 60, 75, 85, 92, 98, 95, 90, 85, 80, 82, 82, 80, 85, 90, 95, 98, 92, 85, 75, 60, 50, 40])
GRID_PRICE = np.array([0.12, 0.12, 0.25, 0.35, 0.55, 0.55, 0.55, 0.55, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.55, 0.55, 0.55, 0.55, 0.35, 0.25, 0.12, 0.12])
SOLAR_PROFILE = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 0.9, 0.8, 0.6, 0.3, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

# ضرایب هزینه و آلایندگی مطابق جدول 3 مقاله 
PARAMS = {
    'MT': {'min': 10, 'max': 60, 'cost': 0.45, 'em': 0.72},
    'FC': {'min': 10, 'max': 40, 'cost': 0.35, 'em': 0.45},
    'WT': {'min': 0, 'max': 50, 'cost': 0.0, 'em': 0.0},
    'PV': {'min': 0, 'max': 40, 'cost': 0.0, 'em': 0.0},
    'GRID': {'min': -100, 'max': 100, 'em': 0.85}
}

def repair_and_calc(pos):
    """تابع هدف منطبق با فرمول F1 و F2 در صفحه 8 مقاله """
    pos_reshaped = pos.reshape((24, 5))
    total_cost, total_em = 0.0, 0.0
    for t in range(24):
        # اعمال محدودیت‌های نسل (Generation Constraints) [cite: 494]
        P_MT = np.clip(pos_reshaped[t,0], PARAMS['MT']['min'], PARAMS['MT']['max'])
        P_FC = np.clip(pos_reshaped[t,1], PARAMS['FC']['min'], PARAMS['FC']['max'])
        P_WT = np.clip(pos_reshaped[t,2], PARAMS['WT']['min'], PARAMS['WT']['max'])
        P_PV = np.clip(pos_reshaped[t,3], PARAMS['PV']['min'], PARAMS['PV']['max'] * SOLAR_PROFILE[t])
        
        # تراز توان (Power Balance) [cite: 493]
        P_GRID = LOAD[t] - (P_MT + P_FC + P_WT + P_PV)
        P_GRID = np.clip(P_GRID, PARAMS['GRID']['min'], PARAMS['GRID']['max'])
        
        # محاسبه هزینه‌ها و آلایندگی با مقیاس صحیح
        total_cost += (P_MT*PARAMS['MT']['cost'] + P_FC*PARAMS['FC']['cost'] + P_GRID*GRID_PRICE[t]) * 24 
        total_em += (P_MT*PARAMS['MT']['em'] + P_FC*PARAMS['FC']['em'] + (P_GRID if P_GRID>0 else 0)*PARAMS['GRID']['em']) * 24
    return total_cost, total_em

# اجرای اصلی MOCSO
class Cat:
    def __init__(self):
        self.pos = np.random.uniform(0, 40, 120)
        self.cost, self.em = repair_and_calc(self.pos)
        self.vel = np.zeros(120)

def run_mocso(N=100, T=100):
    pop = [Cat() for _ in range(N)]
    archive = []
    for _ in range(T):
        combined = pop + archive
        # استخراج جبهه پارتو
        archive = [c1 for i, c1 in enumerate(combined) if not any(
            (combined[j].cost <= c1.cost and combined[j].em <= c1.em) and (combined[j].cost < c1.cost or combined[j].em < c1.em)
            for j in range(len(combined)) if i != j)]
        archive = archive[:100]
        # به‌روزرسانی گربه‌ها
        g_best = random.choice(archive).pos if archive else pop[0].pos
        for cat in pop:
            cat.vel = 0.5 * cat.vel + 2.0 * random.random() * (g_best - cat.pos)
            cat.pos = np.clip(cat.pos + cat.vel, 0, 60)
            cat.cost, cat.em = repair_and_calc(cat.pos)
    return archive

# نمایش خروجی
archive = run_mocso()
plt.scatter([c.cost for c in archive], [c.em for c in archive], c='green', marker='*')
plt.title('Optimal Pareto Fronts for Microgrid Energy Management')
plt.xlabel('Operational Cost ($/day)')
plt.ylabel('Emissions (kg/day)')
plt.grid(True)
plt.show()
