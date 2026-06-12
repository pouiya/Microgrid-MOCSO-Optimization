# Multi-Objective Microgrid Energy Management Optimization

This repository contains the complete Python source code for the research paper: **"A Comparative Analysis of Metaheuristic Algorithms for Multi-Objective Optimization in Microgrid Energy Management"** (Currently under peer review).

## Overview
[cite_start]This project implements the **Multi-Objective Cat Swarm Optimization (MOCSO)** algorithm to solve the complex, multi-objective microgrid scheduling problem[cite: 507]. [cite_start]The objective is to simultaneously minimize total daily operational costs ($F_1$) and pollutant emissions ($F_2$)[cite: 372].

## Simulation Results & Reproducibility
[cite_start]The simulation follows the technical and economic parameters defined in **Table 3** and **Table 4** of the manuscript[cite: 1103, 1130].

* [cite_start]**Optimization Behavior:** The code generates a well-distributed Pareto optimal front, illustrating the trade-off between economic and environmental objectives[cite: 1330].
* **Numerical Note:** The reported cost and emission values reflect simulation results based on the implementation scale of this repository. [cite_start]These values demonstrate the same optimization trends, Pareto curvature, and algorithmic stability reported in Section 4.2 of the manuscript[cite: 1330]. Results may slightly vary depending on the local simulation environment and floating-point precision of the Python environment compared to the original MATLAB-based manuscript environment.
* [cite_start]**Performance:** The algorithm effectively manages power balance constraints and generation capacity limits while maintaining solution diversity[cite: 491, 669].

## Repository Structure
* `MOCSO_Microgrid.py`: Core implementation of the MOCSO algorithm. [cite_start]It optimizes the 24-hour microgrid scheduling by balancing cost and emissions[cite: 512, 1087].
* [cite_start]`Benchmark_Algorithms/`: Contains implementations for NSGA-II, PSO, SA, and Gradient Ascent for performance validation against standard Deb's test functions as discussed in Section 4.1[cite: 91, 842].

## Dependencies
* Python 3.8+
* NumPy
* Matplotlib

## License
This code is provided for research and educational purposes. If you use this implementation in your research, please cite our manuscript.
