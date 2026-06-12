# Multi-Objective Microgrid Energy Management Optimization

This repository contains the complete Python source code for the research paper: **"A Comparative Analysis of Metaheuristic Algorithms for Multi-Objective Optimization in Microgrid Energy Management"**.

## Overview
This project implements the **Multi-Objective Cat Swarm Optimization (MOCSO)** algorithm, along with benchmark algorithms (NSGA-II, PSO, SA, Gradient Ascent), to solve the multi-objective microgrid scheduling problem of minimizing daily operational costs ($F_1$) and pollutant emissions ($F_2$).

## Simulation & Reproducibility
The implementation uses the technical and economic parameters defined in **Table 3** and **Table 4** of the manuscript. 
* **Results:** The provided code reproduces the optimization trends, Pareto curvature, and performance behaviors reported in Section 4.2.
* **Reproducibility:** All simulations were conducted in Python. Minor variations in absolute values may occur due to the stochastic nature of metaheuristic algorithms across different execution environments.

## Repository Structure
* `MOCSO_Microgrid.py`: Core implementation of the proposed MOCSO algorithm.
* `Benchmark_Algorithms/`: Implementations for NSGA-II, PSO, SA, and Gradient Ascent for performance validation.

## License
This code is provided for research purposes. If you use this implementation, please cite our manuscript.
