import numpy as np
import matplotlib.pyplot as plt

# Constants
m = 30  # mass [kg]
k = 50  # spring constant [N/m]
g = 9.81  # gravitational acceleration [m/s^2]
mu = 0.05  # coefficient of friction
x0_initial = 6  # initial stretch [m]
N_cyc = 5  # total number of cycles

def solve_quadratic(A, B, C):
    discriminant = B**2 - 4 * A * C
    if discriminant < 0: raise ValueError("Discriminant is negative. No real roots.")
    root1 = (-B + np.sqrt(discriminant)) / (2 * A)
    root2 = (-B - np.sqrt(discriminant)) / (2 * A)
    return root1, root2

results = []
x0 = x0_initial
for cycle in range(1, N_cyc + 1):
    A, B = 0.5 * k, m * g * mu
    C0 = m * g * mu * x0 - 0.5 * k * x0**2
    x1_1, x1_2 = solve_quadratic(A, B, C0)
    x1 = x1_1 if 0 < x1_1 < x0 else x1_2

    C1 = m * g * mu * x1 - 0.5 * k * x1**2
    x2_1, x2_2 = solve_quadratic(A, B, C1)
    x2 = x2_1 if 0 < x2_1 < x1 else x2_2

    results.append((cycle - 0.5, abs(x0), abs(x1)))
    results.append((cycle, abs(x1), abs(x2)))

    x0 = x2

for i in range(len(results)):
    if i % 2 == 0: results[i] = (results[i][0], results[i][1], -results[i][2])
    else: results[i] = (results[i][0], -results[i][1], results[i][2])

cycle_numbers = []
positions = []
for cycle, start, end in results:
    cycle_numbers.append(cycle)
    positions.append(start)
    cycle_numbers.append(cycle)
    positions.append(end)

plt.figure(figsize=(10, 6))
plt.plot(cycle_numbers, positions, marker='o')
plt.title('Position of Mass Block Over Cycles')
plt.xlabel('Cycle')
plt.ylabel('Position [m]')
plt.grid(True)
plt.show()

def compute_velocity_profile(x0, x, m, k, g, mu):
    return np.sqrt(np.maximum(0, (-k x**2 + 2 (k x0 - m g mu) x) / m))

velocities = [compute_velocity_profile(x0_initial, x, m, k, g, mu) for x in positions]

plt.figure(figsize=(10, 6))
plt.plot(cycle_numbers, velocities, marker='x')
plt.title('Velocity Profile of Mass Block Over Cycles')
plt.xlabel('Cycle')
plt.ylabel('Velocity [m/s]')
plt.grid(True)
plt.show()
Notebook[{}]
