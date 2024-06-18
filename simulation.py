#!/usr/bin/env wolframscript
import time

import matplotlib.pyplot as plt
import numpy as np
from memory_profiler import memory_usage

m = 30  # mass [kg]
k = 50  # spring constant [N/m]
g = 9.81  # gravitational acceleration [m/s^2]
mu = 0.05  # coefficient of friction
x0_initial = 6  # initial stretch [m]
N_cyc = 5  # total number of cycles


def solve_quadratic(A, B, C):
    discriminant = B**2 - 4 * A * C
    if discriminant < 0:
        msg = "Discriminant is negative. No real roots."
        raise ValueError(msg)
    root1 = (-B + np.sqrt(discriminant)) / (2 * A)
    root2 = (-B - np.sqrt(discriminant)) / (2 * A)
    return root1, root2


def simulate_spring_mass_system(N_cyc):
    results = []
    x0 = x0_initial
    for cycle in range(1, N_cyc + 1):
        A = 0.5 * k
        B = m * g * mu
        C0 = m * g * mu * x0 - 0.5 * k * x0**2
        x1_1, x1_2 = solve_quadratic(A, B, C0)
        x1 = x1_1 if 0 < x1_1 < x0 else x1_2

        C1 = m * g * mu * x1 - 0.5 * k * x1**2
        x2_1, x2_2 = solve_quadratic(A, B, C1)
        x2 = x2_1 if 0 < x2_1 < x1 else x2_2

        results.append((cycle - 0.5, abs(x0), abs(x1)))
        results.append((cycle, abs(x1), abs(x2)))

        x0 = x2

    return results


cycle_counts = list(range(100, 100000, 100))
times_taken = []
memory_used = []

for N_cyc in cycle_counts:
    start_time = time.time()
    mem_usage = memory_usage((simulate_spring_mass_system, (N_cyc,)))
    end_time = time.time()

    times_taken.append(end_time - start_time)
    memory_used.append(max(mem_usage) - min(mem_usage))

fig, ax1 = plt.subplots(figsize=(12, 6))

color = "tab:red"
ax1.set_xlabel("Number of Cycles")
ax1.set_ylabel("Time Taken (seconds)", color=color)
ax1.plot(cycle_counts, times_taken, color=color)
ax1.tick_params(axis="y", labelcolor=color)

ax2 = ax1.twinx()
color = "tab:blue"
ax2.set_ylabel("Memory Usage (MiB)", color=color)
ax2.plot(cycle_counts, memory_used, color=color)
ax2.tick_params(axis="y", labelcolor=color)

fig.tight_layout()
plt.title("Time and Memory Complexity of Spring-Mass System Simulation")
plt.grid(True)
plt.savefig("time_memory_complexity.pgf")
plt.show()
