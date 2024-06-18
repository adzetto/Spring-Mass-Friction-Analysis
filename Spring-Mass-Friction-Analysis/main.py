import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

m = 30
k = 50
mu_s = 0.05
mu_d = 0.05
x0 = 6
v0 = 0.0
T = 25
dt = 1e-4

g = 9.81
n = int(np.ceil(T / dt)) + 1
t = np.linspace(0, T, n)

x = np.zeros(n)
v = np.zeros(n)

x[0] = x0
v[0] = v0


def fr(x, v, m, g, k, mu_s, mu_d):
    if abs(v) > 1e-20:
        return mu_d * m * g * np.sign(v)
    else:
        return -min(mu_s * m * g, abs(k * x)) * np.sign(x)


for i in range(1, n):
    x[i] = x[i - 1] + dt * v[i - 1]
    v[i] = v[i - 1] + dt * (
        -1 / m * fr(x[i - 1], v[i - 1], m, g, k, mu_s, mu_d) - k / m * x[i - 1]
    )

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(t, x, label="$x(t)$")
plt.xlabel(r"Time $t$ [$\operatorname{s}$]")
plt.ylabel(r"Displacement $x$ [$\operatorname{m}$]")
plt.title("Displacement vs. Time")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(x, v, label="$v(t)$", color="r")
plt.xlabel(r"Displacement $x$ [$\operatorname{m}$]")
plt.ylabel(r"Velocity $v$ [$\operatorname{m}$/$\operatorname{s}$]")
plt.title("Velocity vs. Displacement")
plt.legend()

plt.tight_layout()
plt.savefig("1.pdf")

m = 30
k = 50
g = 9.81
mu = 0.05
x0_initial = 6
N_cyc = 5


def solve_quadratic(A, B, C):
    discriminant = B**2 - 4 * A * C
    if discriminant < 0:
        raise ValueError("Discriminant is negative. No real roots.")
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
    if i % 2 == 0:
        results[i] = (results[i][0], results[i][1], -results[i][2])
    else:
        results[i] = (results[i][0], -results[i][1], results[i][2])

cycle_numbers = []
positions = []

for cycle, start, end in results:
    cycle_numbers.append(cycle)
    positions.append(start)
    cycle_numbers.append(cycle)
    positions.append(end)

colors = plt.cm.viridis(np.linspace(0, 1, len(cycle_numbers)))

fig, ax = plt.subplots(figsize=(8, 6))

for i in range(0, len(cycle_numbers) - 1, 2):
    ax.plot(cycle_numbers[i : i + 2], positions[i : i + 2], marker="o", color=colors[i])

ax.set_title("Position of Mass Over Cycles", fontsize=16, weight="bold")
ax.set_xlabel("Cycle", fontsize=14)
ax.set_ylabel("Position [m]", fontsize=14)

ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
ax.yaxis.set_major_locator(ticker.MaxNLocator(10))

ax.grid(True, which="both", linestyle="--", linewidth=0.7, color="gray")
ax.set_facecolor("#f0f0f0")

for i, txt in enumerate(positions):
    if i % 2 == 0:
        ax.annotate(
            f"{txt:.4f}",
            (cycle_numbers[i], positions[i]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=10,
            color="black",
        )

sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=1, vmax=N_cyc))
sm.set_array([])

cbar = plt.colorbar(sm, ticks=range(1, N_cyc + 1), ax=ax)
cbar.set_label("Cycle Number", fontsize=12)

plt.tight_layout()
plt.savefig("2.pdf")


def compute_velocity_profile(x0, x, m, k, g, mu):
    return np.sqrt(np.maximum(0, (-k * x**2 + 2 * (k * x0 - m * g * mu) * x) / m))


velocities = [compute_velocity_profile(x0_initial, x, m, k, g, mu) for x in positions]

plt.figure(figsize=(10, 6))
plt.plot(cycle_numbers, velocities, marker="x")
plt.title("Velocity Profile of Mass Block Over Cycles")
plt.xlabel("Cycle")
plt.ylabel("Velocity [m/s]")
plt.grid(True)
plt.tight_layout()