# Cloud_Project
 
Image and Python code files for Term Project of Cloud Computing Class.

# RDPSO Cloud Workflow Scheduling Visualization

This repository contains the Python code for visualizing the scheduling of tasks in a cloud environment using the Revised Discrete Particle Swarm Optimization (RDPSO) algorithm. The RDPSO is designed to efficiently schedule tasks while taking into account both data transmission costs and computation costs.

## Overview

The RDPSO algorithm is an optimization method that schedules a set of tasks to various service instances with the objective of minimizing the overall cost. This repository includes a Python script that simulates the RDPSO algorithm and generates a visual representation of the optimal task-service mapping.

## Features

- Simulation of cloud workflow scheduling using RDPSO.
- Visualization of task to service instance assignments.
- Calculation of the best cost for the given task-service mapping.
- Export of the visualized graph to a specified output folder.

## Installation

To run the script, you will need to have Python installed on your system. Additionally, you will need to install the following Python libraries:

```bash
pip install matplotlib networkx