# Multi-Objective Microgrid Energy Management Optimization

This repository contains the complete Python source code for the paper:
**"A Comparative Analysis of Metaheuristic Algorithms for Multi-Objective Optimization in Microgrid Energy Management"**

## Repository Structure
* `MOCSO_Microgrid.py`: The core implementation of the proposed Multi-Objective Cat Swarm Optimization (MOCSO) algorithm. It dynamically schedules the 24-hour operation of a grid-connected microgrid (incorporating MT, FC, WT, PV, and Main Grid) to minimize operational cost and environmental emissions simultaneously.
* `Benchmark_Algorithms/`: Contains the Python scripts for standard NSGA-II, PSO, and Gradient Ascent algorithms applied to the multi-objective benchmark functions (Deb's Test Functions) as evaluated in Section 4.1 of the manuscript.

## Dependencies
* Python 3.8+
* NumPy
* Matplotlib

## Execution
Run `MOCSO_Microgrid.py` to generate the Pareto optimal front for the microgrid energy management problem (Cost vs. Emissions).
