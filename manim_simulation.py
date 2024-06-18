import numpy as np
from manim import *

# Input parameters
m = 30  # Block mass [kg]
k = 50  # Spring stiffness [N/m]
mu_s = 0.05  # Static dry friction coefficient
mu_d = 0.05  # Dynamic dry friction coefficient
x0 = 6  # Initial displacement [m]
v0 = 0.0  # Initial velocity [m/s]
T = 25  # Total simulation time [s]
dt = 1e-6  # Approximate simulation timestep [s]

g = 9.81  # Acceleration of gravity [m/s^2]
n = int(np.ceil(T / dt)) + 1  # Number of timesteps
t = np.linspace(0, T, n)  # Time vector

x = np.zeros(n)  # Solution vector for position
v = np.zeros(n)  # Solution vector for velocity

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


class MassSpringSystem(Scene):
    def construct(self) -> None:
        self.camera.frame_width = 24
        self.camera.frame_height = 14
        elapsed_time = ValueTracker(0)

        point_A = Dot((-10, 0, 0))
        point_O = Dot((0, 0, 0))
        point_B = Dot((10, 0, 0))

        wall_left = Line(
            point_A.get_center() + 3 * UP,
            point_A.get_center() + 3 * DOWN,
            color=WHITE,
            stroke_width=10,
        )
        wall_right = Line(
            point_B.get_center() + 3 * UP,
            point_B.get_center() + 3 * DOWN,
            color=WHITE,
            stroke_width=10,
        )

        label_A = Text("A", font_size=36).next_to(point_A, DOWN + LEFT, buff=0.1)
        label_O = Text("O", font_size=36).next_to(point_O, DOWN, buff=0.1)
        label_B = Text("B", font_size=36).next_to(point_B, DOWN + LEFT, buff=0.1)

        slider_box = Square(side_length=1, color=BLUE).move_to(
            point_O.get_center() + RIGHT * x[0]
        )

        slider_box.add_updater(
            lambda m: m.move_to(
                point_O.get_center() + RIGHT * x[int(elapsed_time.get_value() / dt)]
            )
        )

        rod = Line(
            start=point_A.get_center(),
            end=point_B.get_center(),
            color=GREY,
            stroke_width=20,
            stroke_opacity=0.8,
        )

        spring = always_redraw(
            lambda: self.create_spring(point_A.get_center(), slider_box.get_center())
        )

        position_vector = always_redraw(
            lambda: Arrow(
                start=point_O.get_center() + UP * 2,
                end=slider_box.get_center() + UP * 2,
                buff=0,
                color=YELLOW,
            ),
        )
        vector_label = always_redraw(
            lambda: MathTex(
                f"x = {x[int(elapsed_time.get_value() / dt)]:.4f} m"
            ).next_to(position_vector.get_end(), UP),
        )

        velocity_vector = always_redraw(
            lambda: Arrow(
                start=slider_box.get_bottom() - UP * 0.2,
                end=slider_box.get_bottom()
                - UP * 0.2
                + v[int(elapsed_time.get_value() / dt)] * RIGHT * 0.1,
                buff=0,
                color=RED,
            ),
        )
        velocity_label = always_redraw(
            lambda: MathTex(
                f"v = {v[int(elapsed_time.get_value() / dt)]:.4f} m/s"
            ).next_to(velocity_vector.get_end(), DOWN),
        )

        help_line = always_redraw(
            lambda: DashedLine(
                start=slider_box.get_center(),
                end=position_vector.get_end(),
                color=RED,
                stroke_width=2,
            ),
        )

        friction_force_vector = always_redraw(
            lambda: Arrow(
                start=slider_box.get_center() - DOWN * 0.5,
                end=slider_box.get_center()
                - DOWN * 0.5
                + fr(
                    x[int(elapsed_time.get_value() / dt)],
                    v[int(elapsed_time.get_value() / dt)],
                    m,
                    g,
                    k,
                    mu_s,
                    mu_d,
                )
                * LEFT
                * 0.01,
                buff=0,
                color=GREEN,
            ),
        )
        friction_force_label = always_redraw(
            lambda: MathTex(
                f"F_r = {-1 * fr(x[int(elapsed_time.get_value() / dt)], v[int(elapsed_time.get_value() / dt)], m, g, k, mu_s, mu_d):.4f} N"
            ).next_to(friction_force_vector.get_end(), DOWN + RIGHT),
        )

        spring_force_vector = always_redraw(
            lambda: Arrow(
                start=slider_box.get_center() + UP * 0.5,
                end=slider_box.get_center()
                + UP * 0.5
                + (-k * x[int(elapsed_time.get_value() / dt)]) * RIGHT * 0.01,
                buff=0,
                color=PURPLE,
            ),
        )
        spring_force_label = always_redraw(
            lambda: MathTex(
                f"F_s = {-k * x[int(elapsed_time.get_value() / dt)]:.4f} N"
            ).next_to(spring_force_vector.get_end(), UP),
        )

        self.add(help_line)

        self.add(
            wall_left,
            wall_right,
            label_A,
            label_O,
            label_B,
            rod,
            spring,
            slider_box,
            position_vector,
            vector_label,
            velocity_vector,
            velocity_label,
            friction_force_vector,
            friction_force_label,
            spring_force_vector,
            spring_force_label,
        )

        self.play(elapsed_time.animate.set_value(T), run_time=T, rate_func=linear)
        self.wait(1)

    def create_spring(self, start, end, coils=20, radius=0.2):
        def spring_func(t):
            return np.array(
                [
                    start[0] + t * (end[0] - start[0]),
                    radius * np.sin(2 * np.pi * coils * t),
                    0,
                ]
            )

        return ParametricFunction(spring_func, t_range=(0, 1, 0.01), color=WHITE)


#!/usr/bin/env wolframscript
