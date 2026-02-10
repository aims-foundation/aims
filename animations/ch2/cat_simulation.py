"""
AIMS Chapter 2 Animation: Computerized Adaptive Testing
Fisher information curves, step-by-step CAT, CAT vs random comparison.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch2 animations/ch2/cat_simulation.py CATSimulation
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


class CATSimulation(Scene):
    """CAT animation: Fisher info, step-by-step selection, comparison."""

    def construct(self):
        self.camera.background_color = BG
        np.random.seed(42)
        self.play_title()
        self.play_fisher_information()
        self.play_cat_steps()
        self.play_comparison()
        self.play_takeaway()

    # ================================================================
    #  Title
    # ================================================================
    def play_title(self):
        title = Text("Computerized Adaptive Testing",
                     font_size=44, color=WHITE, weight=BOLD)
        subtitle = Text("Ask the right questions",
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
    #  Fisher information curves
    # ================================================================
    def play_fisher_information(self):
        header = Text("Fisher Information", font_size=30,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.35)

        formula = MathTex(
            r"I_j(\theta) = P_j(\theta) \cdot (1 - P_j(\theta))",
            font_size=28, color=ACCENT,
        )
        formula.next_to(header, DOWN, buff=0.2)

        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)
        self.play(Write(formula), run_time=1.0)

        # Axes
        ax = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.28, 0.05],
            x_length=9, y_length=3.5,
            axis_config={"color": AXIS_CLR, "font_size": 18,
                         "include_numbers": True},
            tips=False,
        )
        x_lab = MathTex(r"\theta", font_size=24, color=AXIS_CLR)
        x_lab.next_to(ax, RIGHT, buff=0.1).shift(DOWN * 0.3)
        y_lab = Text("Information", font_size=16, color=AXIS_CLR)
        y_lab.next_to(ax, LEFT, buff=0.1).shift(UP * 0.3)
        ax_group = VGroup(ax, x_lab, y_lab)
        ax_group.move_to(DOWN * 0.7)

        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab), run_time=0.7)

        # Information curves for items at different betas
        betas = [-2, -1, 0, 1, 2]
        curves = VGroup()
        labels = VGroup()
        for i, b in enumerate(betas):
            color = PAL[i % len(PAL)]
            curve = ax.plot(
                lambda t, _b=b: float(
                    sigmoid(t - _b) * (1 - sigmoid(t - _b))
                ),
                x_range=[-4, 4, 0.05], color=color, stroke_width=2.5,
            )
            # Label at peak
            lbl = MathTex(rf"\beta = {b}", font_size=14, color=color)
            peak_y = float(sigmoid(b - b) * (1 - sigmoid(b - b)))
            lbl.next_to(ax.c2p(b, peak_y), UP, buff=0.1)
            curves.add(curve)
            labels.add(lbl)

        for c, l in zip(curves, labels):
            self.play(Create(c), FadeIn(l), run_time=0.5)
        self.wait(1.5)

        # Highlight: information peaks where theta = beta
        note = Text(
            "Maximum information where \u03b8 = \u03b2 (50% chance)",
            font_size=18, color=TEXT2,
        )
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.4)
        self.wait(4.0)

        self.play(FadeOut(VGroup(
            header, formula, ax_group, curves, labels, note,
        )), run_time=0.8)

    # ================================================================
    #  CAT step-by-step simulation
    # ================================================================
    def play_cat_steps(self):
        header = Text("Adaptive Item Selection", font_size=28,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        # Number line for ability estimate
        nline = NumberLine(
            x_range=[-3, 3, 1], length=8,
            color=AXIS_CLR, include_numbers=True, font_size=14,
            decimal_number_config={"num_decimal_places": 0},
        )
        nline.shift(UP * 0.8)
        nline_lbl = Text("Ability estimate", font_size=16,
                         color=AXIS_CLR)
        nline_lbl.next_to(nline, UP, buff=0.2)
        self.play(Create(nline), FadeIn(nline_lbl), run_time=0.5)

        # True ability
        true_theta = 1.2
        true_star = Star(n=5, outer_radius=0.12, color=ACCENT,
                         fill_opacity=1)
        true_star.move_to(nline.n2p(true_theta))
        true_lbl = Text("true", font_size=12, color=ACCENT)
        true_lbl.next_to(true_star, UP, buff=0.08)
        self.play(FadeIn(true_star), FadeIn(true_lbl), run_time=0.4)

        # Estimate tracker
        est_val = ValueTracker(0.0)
        se_val = ValueTracker(1.0)

        est_dot = always_redraw(
            lambda: Dot(
                nline.n2p(est_val.get_value()),
                color=PAL[0], radius=0.1,
            )
        )

        # Confidence interval
        ci_left = always_redraw(
            lambda: Line(
                nline.n2p(est_val.get_value() - 1.96 * se_val.get_value())
                + UP * 0.15,
                nline.n2p(est_val.get_value() - 1.96 * se_val.get_value())
                + DOWN * 0.15,
                color=PAL[0], stroke_width=1.5, stroke_opacity=0.5,
            )
        )
        ci_right = always_redraw(
            lambda: Line(
                nline.n2p(est_val.get_value() + 1.96 * se_val.get_value())
                + UP * 0.15,
                nline.n2p(est_val.get_value() + 1.96 * se_val.get_value())
                + DOWN * 0.15,
                color=PAL[0], stroke_width=1.5, stroke_opacity=0.5,
            )
        )
        ci_bar = always_redraw(
            lambda: Line(
                nline.n2p(est_val.get_value() - 1.96 * se_val.get_value()),
                nline.n2p(est_val.get_value() + 1.96 * se_val.get_value()),
                color=PAL[0], stroke_width=1, stroke_opacity=0.3,
            )
        )

        self.add(ci_bar, ci_left, ci_right, est_dot)
        self.play(FadeIn(est_dot), run_time=0.3)

        # Item pool: 10 items as small squares
        item_betas = [-1.5, -1.0, -0.5, 0.0, 0.3, 0.6, 0.9, 1.2, 1.5, 2.0]
        item_squares = VGroup()
        item_beta_lbls = VGroup()
        for i, b in enumerate(item_betas):
            sq = Square(side_length=0.35, stroke_color=AXIS_CLR,
                        stroke_width=1.5, fill_opacity=0)
            sq.move_to(LEFT * 3.6 + RIGHT * i * 0.8 + DOWN * 0.6)
            item_squares.add(sq)
            lbl = Text(f"{b:.1f}", font_size=10, color=AXIS_CLR)
            lbl.next_to(sq, DOWN, buff=0.08)
            item_beta_lbls.add(lbl)

        pool_lbl = Text("Item pool (\u03b2 values):", font_size=14,
                        color=TEXT2)
        pool_lbl.next_to(item_squares, UP, buff=0.15).align_to(
            item_squares, LEFT)

        self.play(
            FadeIn(item_squares), FadeIn(item_beta_lbls),
            FadeIn(pool_lbl),
            run_time=0.6,
        )

        # Counter
        counter = Text("Items: 0", font_size=18, color=TEXT2)
        counter.shift(RIGHT * 5.5 + UP * 0.8)
        self.play(FadeIn(counter), run_time=0.3)

        # Pre-computed CAT steps:
        # (item_index, response, new_theta, new_SE)
        steps = [
            (3, 1, 0.55, 0.72),    # beta=0.0, correct
            (5, 1, 0.85, 0.58),    # beta=0.6, correct
            (7, 0, 0.65, 0.50),    # beta=1.2, incorrect
            (6, 1, 0.85, 0.44),    # beta=0.9, correct
            (8, 1, 1.05, 0.39),    # beta=1.5, correct
            (4, 1, 1.15, 0.35),    # beta=0.3, correct
        ]

        used_items = set()
        for step_idx, (item_idx, response, new_theta, new_se) in \
                enumerate(steps):
            speed = 1.2 if step_idx < 3 else 0.7

            # Highlight selected item
            self.play(
                item_squares[item_idx].animate.set_stroke(
                    color=ACCENT, width=3),
                run_time=speed * 0.3,
            )

            # Show response
            if response == 1:
                icon = Text("\u2713", font_size=18, color=PAL[1])
            else:
                icon = Text("\u2717", font_size=18, color=PAL[3])
            icon.move_to(item_squares[item_idx])

            self.play(FadeIn(icon, scale=1.3), run_time=speed * 0.2)

            # Update estimate and SE
            self.play(
                est_val.animate.set_value(new_theta),
                se_val.animate.set_value(new_se),
                run_time=speed * 0.5,
                rate_func=smooth,
            )

            # Update counter
            new_counter = Text(f"Items: {step_idx + 1}",
                               font_size=18, color=TEXT2)
            new_counter.move_to(counter)
            self.play(FadeOut(counter), FadeIn(new_counter),
                      run_time=0.1)
            counter = new_counter
            used_items.add(item_idx)

        self.wait(2.5)

        # Clean up
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ================================================================
    #  CAT vs Random comparison
    # ================================================================
    def play_comparison(self):
        header = Text("CAT vs Random Selection", font_size=28,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        # Axes
        ax = Axes(
            x_range=[0, 30, 5], y_range=[0, 1.05, 0.25],
            x_length=8, y_length=4.2,
            axis_config={"color": AXIS_CLR, "font_size": 18,
                         "include_numbers": True},
            tips=False,
        )
        x_lab = Text("Number of items", font_size=16, color=AXIS_CLR)
        x_lab.next_to(ax, DOWN, buff=0.15)
        y_lab = Text("Reliability", font_size=16, color=AXIS_CLR)
        y_lab.next_to(ax, LEFT, buff=0.1).shift(UP * 0.5)
        ax_group = VGroup(ax, x_lab, y_lab)
        ax_group.move_to(DOWN * 0.4)

        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab), run_time=0.7)

        # Threshold line
        thresh_line = DashedLine(
            ax.c2p(0, 0.95), ax.c2p(30, 0.95),
            color=TEXT2, stroke_width=1, dash_length=0.08,
        )
        thresh_lbl = Text("95% reliability", font_size=14, color=TEXT2)
        thresh_lbl.next_to(ax.c2p(30, 0.95), RIGHT, buff=0.15)
        self.play(Create(thresh_line), FadeIn(thresh_lbl), run_time=0.4)

        # CAT curve (faster rise)
        cat_curve = ax.plot(
            lambda x: 1 - np.exp(-0.22 * x),
            x_range=[0, 30, 0.2], color=PAL[1], stroke_width=3,
        )
        cat_lbl = Text("CAT", font_size=18, color=PAL[1], weight=BOLD)
        cat_lbl.next_to(ax.c2p(8, 0.85), RIGHT, buff=0.15)

        # Random curve (slower rise)
        random_curve = ax.plot(
            lambda x: 1 - np.exp(-0.10 * x),
            x_range=[0, 30, 0.2], color=PAL[0], stroke_width=3,
        )
        random_lbl = Text("Random", font_size=18, color=PAL[0],
                          weight=BOLD)
        random_lbl.next_to(ax.c2p(20, 0.82), RIGHT, buff=0.15)

        self.play(Create(random_curve), FadeIn(random_lbl), run_time=1.5)
        self.wait(0.5)
        self.play(Create(cat_curve), FadeIn(cat_lbl), run_time=1.5)
        self.wait(1.0)

        # Crossing points
        # CAT crosses 0.95 at: 1 - exp(-0.22*x) = 0.95 → x ≈ 13.6
        # Random crosses at: 1 - exp(-0.10*x) = 0.95 → x ≈ 30
        cat_cross = -np.log(0.05) / 0.22  # ~13.6
        random_cross = -np.log(0.05) / 0.10  # ~30

        # CAT vertical marker
        cat_vline = DashedLine(
            ax.c2p(cat_cross, 0), ax.c2p(cat_cross, 0.95),
            color=PAL[1], stroke_width=1.5, dash_length=0.06,
        )
        cat_items_lbl = Text(f"~{int(cat_cross)} items", font_size=14,
                             color=PAL[1])
        cat_items_lbl.next_to(ax.c2p(cat_cross, 0), DOWN, buff=0.15)

        self.play(Create(cat_vline), FadeIn(cat_items_lbl), run_time=0.5)

        # Random doesn't quite reach 0.95 in 30 items, show that
        random_note = Text("~30 items", font_size=14, color=PAL[0])
        random_note.next_to(ax.c2p(28, 0), DOWN, buff=0.15)
        self.play(FadeIn(random_note), run_time=0.3)

        # Big callout
        callout = Text("2\u00d7 more efficient!", font_size=28,
                       color=ACCENT, weight=BOLD)
        callout.shift(RIGHT * 3 + UP * 2.0)
        self.play(FadeIn(callout, scale=1.2), run_time=0.6)
        self.wait(4.0)

        self.play(FadeOut(VGroup(
            header, ax_group, thresh_line, thresh_lbl,
            cat_curve, cat_lbl, random_curve, random_lbl,
            cat_vline, cat_items_lbl, random_note, callout,
        )), run_time=0.8)

    # ================================================================
    #  Takeaway
    # ================================================================
    def play_takeaway(self):
        heading = Text("Adaptive Testing for AI Evaluation",
                       font_size=32, color=WHITE, weight=BOLD)
        heading.shift(UP * 0.8)

        rows = VGroup(
            Text("Fewer questions \u2192 lower evaluation cost",
                 font_size=22, color=TEXT2),
            Text("Better precision per question asked",
                 font_size=22, color=TEXT2),
            Text("Less risk of benchmark contamination",
                 font_size=22, color=TEXT2),
        )
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows.next_to(heading, DOWN, buff=0.5)

        line = Line(LEFT * 2, RIGHT * 2, color=ACCENT, stroke_width=1.5)
        line.next_to(rows, DOWN, buff=0.5)

        self.play(FadeIn(heading, shift=DOWN * 0.15), run_time=0.7)
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.4)
            self.wait(0.3)
        self.play(Create(line), run_time=0.4)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
