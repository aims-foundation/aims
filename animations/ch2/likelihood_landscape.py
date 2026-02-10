"""
AIMS Chapter 2 Animation: Maximum Likelihood Estimation
Likelihood function, gradient = observed - predicted, gradient ascent
convergence, and parameter recovery scatter plots.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch2 animations/ch2/likelihood_landscape.py LikelihoodLandscape
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


class LikelihoodLandscape(Scene):
    """MLE visualization: likelihood, gradient intuition, convergence."""

    def construct(self):
        self.camera.background_color = BG
        self.play_title()
        self.play_single_item_likelihood()
        self.play_gradient_convergence()
        self.play_parameter_recovery()

    # ================================================================
    #  Helpers (matching ch1 icc_models.py style)
    # ================================================================
    def make_axes(self, x_range=(-4, 4, 1), y_range=(0, 1.05, 0.25),
                  x_length=9, y_length=4.2):
        ax = Axes(
            x_range=x_range, y_range=y_range,
            x_length=x_length, y_length=y_length,
            axis_config={
                "color": AXIS_CLR,
                "include_numbers": True,
                "font_size": 22,
            },
            tips=False,
        )
        return ax

    def bottom_note(self, text_str):
        note = Text(text_str, font_size=20, color=TEXT2,
                    line_spacing=1.3)
        note.to_edge(DOWN, buff=0.25)
        return note

    # ================================================================
    #  Title
    # ================================================================
    def play_title(self):
        title = Text("Maximum Likelihood Estimation", font_size=44,
                     color=WHITE, weight=BOLD)
        subtitle = Text("Finding the peak of the likelihood",
                        font_size=24, color=TEXT2)
        subtitle.next_to(title, DOWN, buff=0.4)
        line = Line(LEFT * 2.5, RIGHT * 2.5, color=ACCENT,
                    stroke_width=1.5)
        line.next_to(subtitle, DOWN, buff=0.35)
        group = VGroup(title, subtitle, line)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.15),
                  Create(line), run_time=0.7)
        self.wait(2.5)
        self.play(FadeOut(group, shift=UP * 0.4), run_time=0.7)

    # ================================================================
    #  Act 1: Single-item likelihood intuition
    # ================================================================
    def play_single_item_likelihood(self):
        header = Text("Likelihood for One Item", font_size=30,
                      color=PAL[0], weight=BOLD)
        header.to_edge(UP, buff=0.35)

        formula = MathTex(
            r"\ell = Y \log P + (1-Y) \log(1-P)",
            font_size=28, color=ACCENT,
        )
        formula.next_to(header, DOWN, buff=0.2)

        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.6)
        self.play(Write(formula), run_time=1.0)

        # Axes
        ax = self.make_axes(y_range=(0, 1.05, 0.25))
        x_lab = ax.get_x_axis_label(
            MathTex(r"\theta", font_size=28, color=AXIS_CLR),
            edge=RIGHT, direction=DOWN,
        )
        y_lab = ax.get_y_axis_label(
            MathTex(r"P", font_size=26, color=AXIS_CLR),
            edge=UP, direction=LEFT,
        )
        ax_group = VGroup(ax, x_lab, y_lab)
        ax_group.move_to(DOWN * 0.55)

        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab), run_time=0.8)

        # ICC curve for one item (beta=0)
        beta = 0.0
        icc = ax.plot(
            lambda t: float(sigmoid(t - beta)),
            x_range=[-4, 4, 0.05], color=PAL[0], stroke_width=3,
        )
        beta_dot = Dot(ax.c2p(beta, 0.5), color=PAL[0], radius=0.06)
        beta_lbl = MathTex(r"\beta=0", font_size=18, color=PAL[0])
        beta_lbl.next_to(beta_dot, DOWN + RIGHT, buff=0.1)

        self.play(Create(icc), FadeIn(beta_dot), FadeIn(beta_lbl),
                  run_time=1.2)

        # ValueTracker for theta position
        theta_t = ValueTracker(-2.5)

        # Tracking dot on curve
        tracking_dot = always_redraw(
            lambda: Dot(
                ax.c2p(theta_t.get_value(),
                       float(sigmoid(theta_t.get_value() - beta))),
                color=ACCENT, radius=0.08,
            )
        )
        # Vertical dashed line
        vert_line = always_redraw(
            lambda: DashedLine(
                ax.c2p(theta_t.get_value(), 0),
                ax.c2p(theta_t.get_value(),
                       float(sigmoid(theta_t.get_value() - beta))),
                color=ACCENT, stroke_width=1.5, dash_length=0.06,
            )
        )

        self.add(vert_line, tracking_dot)
        self.play(FadeIn(tracking_dot), FadeIn(vert_line), run_time=0.4)

        # Show Y=1 scenario
        y1_text = Text("Y = 1: want P high \u2191", font_size=20,
                       color=PAL[1])
        y1_text.next_to(ax, RIGHT, buff=0.3).shift(UP * 0.8)
        self.play(FadeIn(y1_text), run_time=0.4)
        self.play(theta_t.animate.set_value(2.0), run_time=2.5,
                  rate_func=smooth)
        self.wait(2.0)

        # Show Y=0 scenario
        y0_text = Text("Y = 0: want P low \u2193", font_size=20,
                       color=PAL[3])
        y0_text.next_to(y1_text, DOWN, buff=0.3)
        self.play(FadeOut(y1_text), FadeIn(y0_text), run_time=0.5)
        self.play(theta_t.animate.set_value(-1.5), run_time=2.0,
                  rate_func=smooth)
        self.wait(2.0)

        note = self.bottom_note(
            "The likelihood measures how well parameters explain the data"
        )
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.4)
        self.wait(3.0)

        self.play(FadeOut(VGroup(
            header, formula, ax_group, icc, beta_dot, beta_lbl,
            tracking_dot, vert_line, y0_text, note,
        )), run_time=0.8)

    # ================================================================
    #  Act 2: Gradient and convergence
    # ================================================================
    def play_gradient_convergence(self):
        header = Text("Gradient Ascent", font_size=30,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.35)

        # Gradient formula
        grad_formula = MathTex(
            r"\frac{\partial \ell}{\partial \theta_i}",
            r"=",
            r"\sum_j",
            r"(",
            r"Y_{ij}",
            r"-",
            r"P_{ij}",
            r")",
            font_size=28,
        )
        grad_formula[0].set_color(ACCENT)
        grad_formula[4].set_color(PAL[1])  # Y observed
        grad_formula[6].set_color(PAL[3])  # P predicted
        grad_formula.next_to(header, DOWN, buff=0.2)

        interp = Text("gradient = observed \u2212 predicted",
                       font_size=18, color=TEXT2)
        interp.next_to(grad_formula, DOWN, buff=0.15)

        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)
        self.play(Write(grad_formula), run_time=1.2)
        self.play(FadeIn(interp), run_time=0.4)
        self.wait(3.0)

        # Left: convergence curve
        conv_ax = Axes(
            x_range=[0, 500, 100], y_range=[-3500, -2400, 250],
            x_length=5, y_length=3.2,
            axis_config={"color": AXIS_CLR, "font_size": 16,
                         "include_numbers": True},
            tips=False,
        )
        conv_ax.shift(LEFT * 3.0 + DOWN * 1.3)
        conv_x_lab = Text("Iteration", font_size=16, color=AXIS_CLR)
        conv_x_lab.next_to(conv_ax, DOWN, buff=0.15)
        conv_y_lab = Text("Log-lik", font_size=16, color=AXIS_CLR)
        conv_y_lab.next_to(conv_ax, LEFT, buff=0.15).shift(UP * 0.5)

        self.play(Create(conv_ax), FadeIn(conv_x_lab),
                  FadeIn(conv_y_lab), run_time=0.7)

        # Convergence curve (steep rise then plateau)
        conv_curve = conv_ax.plot(
            lambda x: -2500 - 950 * np.exp(-x / 60),
            x_range=[0, 500, 2], color=PAL[1], stroke_width=2.5,
        )
        self.play(Create(conv_curve), run_time=2.5)

        # Right: number line showing theta converging
        nline = NumberLine(
            x_range=[-3, 3, 1], length=4,
            color=AXIS_CLR, include_numbers=True, font_size=14,
            decimal_number_config={"num_decimal_places": 0},
        )
        nline.shift(RIGHT * 3.0 + DOWN * 1.0)
        nline_lbl = Text("Ability estimate", font_size=16,
                         color=AXIS_CLR)
        nline_lbl.next_to(nline, UP, buff=0.25)

        # True value star
        true_theta = 1.2
        true_star = Star(n=5, outer_radius=0.12, color=ACCENT,
                         fill_opacity=1)
        true_star.move_to(nline.n2p(true_theta))
        true_lbl = Text("true", font_size=14, color=ACCENT)
        true_lbl.next_to(true_star, UP, buff=0.1)

        # Estimate dot
        est_tracker = ValueTracker(0.0)
        est_dot = always_redraw(
            lambda: Dot(
                nline.n2p(est_tracker.get_value()),
                color=PAL[0], radius=0.1,
            )
        )

        self.play(Create(nline), FadeIn(nline_lbl), run_time=0.5)
        self.play(FadeIn(true_star), FadeIn(true_lbl), run_time=0.4)
        self.add(est_dot)
        self.play(FadeIn(est_dot), run_time=0.3)

        # Animate convergence
        self.play(est_tracker.animate.set_value(true_theta),
                  run_time=3.0, rate_func=smooth)
        self.wait(3.0)

        self.play(FadeOut(VGroup(
            header, grad_formula, interp,
            conv_ax, conv_x_lab, conv_y_lab, conv_curve,
            nline, nline_lbl, true_star, true_lbl, est_dot,
        )), run_time=0.8)

    # ================================================================
    #  Act 3: Parameter recovery scatter plots
    # ================================================================
    def play_parameter_recovery(self):
        header = Text("Parameter Recovery", font_size=30,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        np.random.seed(42)

        # Left scatter: abilities
        ax_left = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=4.2, y_length=4.2,
            axis_config={"color": AXIS_CLR, "font_size": 14,
                         "include_numbers": True},
            tips=False,
        )
        ax_left.shift(LEFT * 3.2 + DOWN * 0.4)
        lbl_xt = Text("True ability", font_size=16, color=AXIS_CLR)
        lbl_xt.next_to(ax_left, DOWN, buff=0.15)
        lbl_yt = Text("Estimated", font_size=16, color=AXIS_CLR)
        lbl_yt.next_to(ax_left, LEFT, buff=0.1).shift(UP * 0.3)
        title_left = Text("Abilities", font_size=20, color=PAL[0],
                          weight=BOLD)
        title_left.next_to(ax_left, UP, buff=0.2)

        # Right scatter: difficulties
        ax_right = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=4.2, y_length=4.2,
            axis_config={"color": AXIS_CLR, "font_size": 14,
                         "include_numbers": True},
            tips=False,
        )
        ax_right.shift(RIGHT * 3.2 + DOWN * 0.4)
        lbl_xd = Text("True difficulty", font_size=16, color=AXIS_CLR)
        lbl_xd.next_to(ax_right, DOWN, buff=0.15)
        lbl_yd = Text("Estimated", font_size=16, color=AXIS_CLR)
        lbl_yd.next_to(ax_right, LEFT, buff=0.1).shift(UP * 0.3)
        title_right = Text("Difficulties", font_size=20, color=PAL[2],
                           weight=BOLD)
        title_right.next_to(ax_right, UP, buff=0.2)

        self.play(
            Create(ax_left), FadeIn(lbl_xt), FadeIn(lbl_yt),
            FadeIn(title_left),
            Create(ax_right), FadeIn(lbl_xd), FadeIn(lbl_yd),
            FadeIn(title_right),
            run_time=0.8,
        )

        # Reference lines (y = x)
        ref_left = DashedLine(
            ax_left.c2p(-3, -3), ax_left.c2p(3, 3),
            color=AXIS_CLR, stroke_width=1, dash_length=0.08,
        )
        ref_right = DashedLine(
            ax_right.c2p(-3, -3), ax_right.c2p(3, 3),
            color=AXIS_CLR, stroke_width=1, dash_length=0.08,
        )
        self.play(Create(ref_left), Create(ref_right), run_time=0.4)

        # Generate scatter data
        n_points = 25
        true_t = np.linspace(-2.5, 2.5, n_points)
        est_t = true_t + np.random.normal(0, 0.18, n_points)
        true_d = np.linspace(-2.5, 2.5, n_points)
        est_d = true_d + np.random.normal(0, 0.2, n_points)

        dots_left = VGroup(*[
            Dot(ax_left.c2p(t, e), color=PAL[0], radius=0.05,
                fill_opacity=0.7)
            for t, e in zip(true_t, est_t)
        ])
        dots_right = VGroup(*[
            Dot(ax_right.c2p(t, e), color=PAL[2], radius=0.05,
                fill_opacity=0.7)
            for t, e in zip(true_d, est_d)
        ])

        self.play(
            FadeIn(dots_left, lag_ratio=0.03),
            FadeIn(dots_right, lag_ratio=0.03),
            run_time=1.5,
        )

        # Correlation labels
        corr_left = Text("r = 0.99", font_size=18, color=PAL[0])
        corr_left.next_to(ax_left, DOWN, buff=0.45)
        corr_right = Text("r = 0.98", font_size=18, color=PAL[2])
        corr_right.next_to(ax_right, DOWN, buff=0.45)
        self.play(FadeIn(corr_left), FadeIn(corr_right), run_time=0.4)

        note = self.bottom_note(
            "MLE recovers true parameters with high accuracy"
        )
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.4)
        self.wait(5.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
