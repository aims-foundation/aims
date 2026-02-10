"""
AIMS Chapter 2 Animation: Opening Hook
Bridge from Chapter 1 (models) to Chapter 2 (estimation).
Poses the question: "You have the model — now learn the parameters."

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch2 animations/ch2/opening_hook.py OpeningHook
"""

from manim import *
import numpy as np

# ── design tokens ────────────────────────────────────────────────
ACCENT = "#FFD966"
BG = "#0f0f0f"
TEXT2 = "#aaaaaa"
PAL = ["#5B8DEE", "#45BF7C", "#F0A35C", "#E8637A", "#B07CD8"]
AXIS_CLR = "#888888"


def sigmoid(x):
    return np.where(x >= 0,
                    1 / (1 + np.exp(-x)),
                    np.exp(x) / (1 + np.exp(x)))


class OpeningHook(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.play_recap()
        self.play_question()
        self.play_landscape_preview()

    # ================================================================
    #  Act 1: Recap from Chapter 1
    # ================================================================
    def play_recap(self):
        # Rasch formula
        formula = MathTex(
            r"P(Y_{ij}=1)",
            r"=",
            r"\sigma(",
            r"\theta_i",
            r"-",
            r"\beta_j",
            r")",
            font_size=34,
        )
        formula[0].set_color(WHITE)
        formula[3].set_color(PAL[0])  # theta
        formula[5].set_color(PAL[2])  # beta
        formula.shift(UP * 1.5)

        context = Text("Chapter 1: We defined the models",
                        font_size=22, color=TEXT2)
        context.next_to(formula, UP, buff=0.4)

        self.play(FadeIn(context, shift=DOWN * 0.1), run_time=0.6)
        self.play(Write(formula), run_time=1.2)
        self.wait(2.0)

        # Small response matrix
        np.random.seed(42)
        n_rows, n_cols = 6, 10
        theta_t = np.linspace(1.5, -1.5, n_rows)
        beta_t = np.linspace(-1.5, 1.5, n_cols)
        probs = sigmoid(theta_t[:, None] - beta_t[None, :])
        Y = (np.random.random((n_rows, n_cols)) < probs).astype(int)

        cell_size = 0.22
        grid = VGroup()
        for i in range(n_rows):
            for j in range(n_cols):
                sq = Square(side_length=cell_size, stroke_width=0.5,
                            stroke_color="#333333")
                if Y[i, j] == 1:
                    sq.set_fill(PAL[0], opacity=0.6)
                else:
                    sq.set_fill("#1c1c1c", opacity=0.6)
                sq.move_to(
                    RIGHT * (j - n_cols / 2 + 0.5) * cell_size
                    + DOWN * (i - n_rows / 2 + 0.5) * cell_size
                )
                grid.add(sq)

        grid.shift(DOWN * 0.8)
        grid_label = Text("Response matrix Y", font_size=16,
                          color=TEXT2)
        grid_label.next_to(grid, DOWN, buff=0.2)

        self.play(FadeIn(grid, lag_ratio=0.01), run_time=1.0)
        self.play(FadeIn(grid_label), run_time=0.3)
        self.wait(3.0)

        self.play(FadeOut(VGroup(context, formula, grid, grid_label)),
                  run_time=0.8)

    # ================================================================
    #  Act 2: The question — theta and beta are unknown
    # ================================================================
    def play_question(self):
        formula = MathTex(
            r"P(Y_{ij}=1)",
            r"=",
            r"\sigma(",
            r"\theta_i",
            r"-",
            r"\beta_j",
            r")",
            font_size=36,
        )
        formula[3].set_color(PAL[0])
        formula[5].set_color(PAL[2])
        formula.shift(UP * 1.0)

        self.play(Write(formula), run_time=0.8)
        self.wait(1.0)

        # Pulse theta and beta with question marks
        q1 = Text("?", font_size=30, color=ACCENT, weight=BOLD)
        q1.next_to(formula[3], UP, buff=0.1)
        q2 = Text("?", font_size=30, color=ACCENT, weight=BOLD)
        q2.next_to(formula[5], UP, buff=0.1)

        self.play(
            Indicate(formula[3], color=ACCENT, scale_factor=1.3),
            Indicate(formula[5], color=ACCENT, scale_factor=1.3),
            run_time=0.8,
        )
        self.play(FadeIn(q1, scale=1.5), FadeIn(q2, scale=1.5),
                  run_time=0.5)
        self.wait(1.5)

        # The core question
        line1 = Text("These parameters are unknown.",
                     font_size=26, color=WHITE)
        line1.next_to(formula, DOWN, buff=0.7)
        self.play(FadeIn(line1, shift=DOWN * 0.1), run_time=0.6)
        self.wait(1.5)

        line2 = Text("How do we learn them from data?",
                     font_size=28, color=ACCENT, weight=BOLD)
        line2.next_to(line1, DOWN, buff=0.4)
        self.play(FadeIn(line2, shift=DOWN * 0.1), run_time=0.7)
        self.wait(4.0)

        self.play(FadeOut(VGroup(formula, q1, q2, line1, line2)),
                  run_time=0.8)

    # ================================================================
    #  Act 3: Likelihood landscape preview
    # ================================================================
    def play_landscape_preview(self):
        header = Text("Find the peak of the likelihood",
                      font_size=26, color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        # Axes for theta vs beta
        ax = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=6, y_length=5,
            axis_config={"color": AXIS_CLR, "font_size": 18,
                         "include_numbers": True},
            tips=False,
        )
        ax.shift(DOWN * 0.3)
        x_lab = MathTex(r"\theta", font_size=24, color=PAL[0])
        x_lab.next_to(ax, RIGHT, buff=0.1).shift(DOWN * 0.3)
        y_lab = MathTex(r"\beta", font_size=24, color=PAL[2])
        y_lab.next_to(ax, UP, buff=0.1).shift(LEFT * 0.3)

        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab), run_time=0.7)

        # Contour ellipses centered at the optimum
        opt_x, opt_y = 1.0, -0.5
        contours = VGroup()
        for r, opacity in [(2.5, 0.15), (2.0, 0.2), (1.5, 0.3),
                           (1.0, 0.45), (0.5, 0.7)]:
            ellipse = Ellipse(
                width=r * 1.6, height=r * 1.2,
                stroke_color=ACCENT, stroke_width=1.5,
                stroke_opacity=opacity, fill_opacity=0,
            )
            ellipse.move_to(ax.c2p(opt_x, opt_y))
            ellipse.rotate(0.3)
            contours.add(ellipse)

        self.play(
            *[Create(c) for c in contours],
            run_time=1.5,
        )

        # Gradient ascent path
        # Pre-compute path points
        path_points = []
        x, y = -2.0, 2.0
        lr = 0.15
        for _ in range(20):
            # Gradient toward optimum (simplified)
            gx = -(x - opt_x)
            gy = -(y - opt_y)
            x += lr * gx
            y += lr * gy
            path_points.append(ax.c2p(x, y))

        # Start point
        start_pos = ax.c2p(-2.0, 2.0)
        start_dot = Dot(start_pos, color=TEXT2, radius=0.08)
        start_lbl = Text("start", font_size=14, color=TEXT2)
        start_lbl.next_to(start_dot, UP + LEFT, buff=0.1)
        self.play(FadeIn(start_dot), FadeIn(start_lbl), run_time=0.4)

        # Animate the path
        path_line = VMobject(color=PAL[0], stroke_width=2.5)
        path_line.set_points_smoothly([start_pos] + path_points)

        moving_dot = Dot(start_pos, color=ACCENT, radius=0.1)
        self.add(moving_dot)
        self.play(
            Create(path_line),
            MoveAlongPath(moving_dot, path_line),
            run_time=3.0, rate_func=smooth,
        )

        # MLE label at end
        mle_lbl = Text("MLE", font_size=18, color=ACCENT, weight=BOLD)
        mle_lbl.next_to(moving_dot, DOWN + RIGHT, buff=0.1)
        self.play(FadeIn(mle_lbl, scale=1.2), run_time=0.4)
        self.wait(2.0)

        note = Text(
            "Find the parameters that make the data most probable",
            font_size=20, color=TEXT2,
        )
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.4)
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
