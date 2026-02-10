"""
AIMS Chapter 2 Animation: Bayesian Inference for IRT
Prior × Likelihood = Posterior, MAP vs MLE shrinkage, extreme case.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch2 animations/ch2/bayesian_inference.py BayesianInference
"""

from manim import *
import numpy as np

# ── design tokens ────────────────────────────────────────────────
ACCENT = "#FFD966"
BG = "#0f0f0f"
TEXT2 = "#aaaaaa"
PAL = ["#5B8DEE", "#45BF7C", "#F0A35C", "#E8637A", "#B07CD8"]
AXIS_CLR = "#888888"


def gauss(x, mu, sigma):
    return np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (
        sigma * np.sqrt(2 * np.pi)
    )


class BayesianInference(Scene):
    """Bayesian triptych: Prior × Likelihood = Posterior."""

    def construct(self):
        self.camera.background_color = BG
        self.play_title()
        self.play_triptych()
        self.play_extreme_case()
        self.play_takeaway()

    # ================================================================
    #  Title
    # ================================================================
    def play_title(self):
        title = Text("Bayesian Inference for IRT", font_size=44,
                     color=WHITE, weight=BOLD)
        formula = MathTex(
            r"p(\theta \mid Y)",
            r"\propto",
            r"p(Y \mid \theta)",
            r"\cdot",
            r"p(\theta)",
            font_size=32, color=ACCENT,
        )
        formula.next_to(title, DOWN, buff=0.4)
        line = Line(LEFT * 2.5, RIGHT * 2.5, color=ACCENT,
                    stroke_width=1.5)
        line.next_to(formula, DOWN, buff=0.35)
        group = VGroup(title, formula, line)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.8)
        self.play(Write(formula), Create(line), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(group, shift=UP * 0.4), run_time=0.7)

    # ================================================================
    #  Main triptych: Prior → Likelihood → Posterior
    # ================================================================
    def play_triptych(self):
        header = Text("Combining Prior and Data", font_size=28,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        # Axes
        ax = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.55, 0.1],
            x_length=9, y_length=4.2,
            axis_config={
                "color": AXIS_CLR, "include_numbers": True,
                "font_size": 22,
            },
            tips=False,
        )
        x_lab = ax.get_x_axis_label(
            MathTex(r"\theta", font_size=28, color=AXIS_CLR),
            edge=RIGHT, direction=DOWN,
        )
        y_lab = ax.get_y_axis_label(
            Text("density", font_size=18, color=AXIS_CLR),
            edge=UP, direction=LEFT,
        )
        ax_group = VGroup(ax, x_lab, y_lab)
        ax_group.move_to(DOWN * 0.55)
        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab), run_time=0.8)

        # ── Prior: N(0, 1) ──
        prior_curve = ax.plot(
            lambda x: gauss(x, 0, 1),
            x_range=[-4, 4, 0.05], color=PAL[4], stroke_width=3,
        )
        prior_lbl = Text("Prior: N(0,1)", font_size=18, color=PAL[4])
        prior_lbl.next_to(ax.c2p(0, gauss(0, 0, 1)), UP + LEFT,
                          buff=0.15)

        self.play(Create(prior_curve), FadeIn(prior_lbl), run_time=1.2)
        self.wait(3.0)

        # ── Likelihood ──
        lik_mu, lik_sigma = 1.8, 0.7
        # Scale to roughly match prior height for visual clarity
        lik_scale = gauss(0, 0, 1) / gauss(lik_mu, lik_mu, lik_sigma)
        lik_curve = ax.plot(
            lambda x: gauss(x, lik_mu, lik_sigma) * lik_scale,
            x_range=[-4, 4, 0.05], color=PAL[0], stroke_width=3,
        )
        lik_lbl = Text("Likelihood", font_size=18, color=PAL[0])
        lik_peak_y = gauss(lik_mu, lik_mu, lik_sigma) * lik_scale
        lik_lbl.next_to(ax.c2p(lik_mu, lik_peak_y), UP + RIGHT,
                        buff=0.15)

        # MLE marker
        mle_line = DashedLine(
            ax.c2p(lik_mu, 0), ax.c2p(lik_mu, lik_peak_y),
            color=PAL[0], stroke_width=1.5, dash_length=0.06,
        )
        mle_dot = Dot(ax.c2p(lik_mu, 0), color=PAL[0], radius=0.06,
                      fill_opacity=0, stroke_color=PAL[0],
                      stroke_width=2)
        mle_lbl = MathTex(r"\hat{\theta}_{\mathrm{MLE}}",
                          font_size=18, color=PAL[0])
        mle_lbl.next_to(mle_dot, DOWN, buff=0.15)

        self.play(Create(lik_curve), FadeIn(lik_lbl), run_time=1.0)
        self.play(Create(mle_line), FadeIn(mle_dot),
                  FadeIn(mle_lbl), run_time=0.6)
        self.wait(3.0)

        # ── Posterior ──
        post_mu, post_sigma = 1.1, 0.55
        post_scale = gauss(0, 0, 1) / gauss(post_mu, post_mu, post_sigma) * 1.1
        post_curve = ax.plot(
            lambda x: gauss(x, post_mu, post_sigma) * post_scale,
            x_range=[-4, 4, 0.05], color=PAL[1], stroke_width=3,
        )
        post_lbl = Text("Posterior", font_size=18, color=PAL[1])
        post_peak_y = gauss(post_mu, post_mu, post_sigma) * post_scale
        post_lbl.next_to(ax.c2p(post_mu, post_peak_y), UP, buff=0.15)

        # MAP marker
        map_dot = Dot(ax.c2p(post_mu, 0), color=PAL[1], radius=0.08)
        map_lbl = MathTex(r"\hat{\theta}_{\mathrm{MAP}}",
                          font_size=18, color=PAL[1])
        map_lbl.next_to(map_dot, DOWN, buff=0.15)

        self.play(Create(post_curve), FadeIn(post_lbl), run_time=1.0)
        self.play(FadeIn(map_dot), FadeIn(map_lbl), run_time=0.5)
        self.wait(1.5)

        # Shrinkage arrow from MLE to MAP
        shrink_arrow = Arrow(
            ax.c2p(lik_mu, -0.04), ax.c2p(post_mu, -0.04),
            color=ACCENT, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.2,
            buff=0.05,
        )
        shrink_lbl = Text("shrinkage", font_size=16, color=ACCENT)
        shrink_lbl.next_to(shrink_arrow, DOWN, buff=0.08)

        self.play(Create(shrink_arrow), FadeIn(shrink_lbl), run_time=0.7)
        self.wait(4.0)

        # Store everything for cleanup
        self.triptych_group = VGroup(
            header, ax_group, prior_curve, prior_lbl,
            lik_curve, lik_lbl, mle_line, mle_dot, mle_lbl,
            post_curve, post_lbl, map_dot, map_lbl,
            shrink_arrow, shrink_lbl,
        )
        self.play(FadeOut(self.triptych_group), run_time=0.8)

    # ================================================================
    #  Extreme case: perfect score
    # ================================================================
    def play_extreme_case(self):
        header = Text("Extreme Case: Perfect Score", font_size=28,
                      color=PAL[3], weight=BOLD)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.6)

        # Axes
        ax = Axes(
            x_range=[-4, 5, 1], y_range=[0, 0.5, 0.1],
            x_length=9, y_length=3.8,
            axis_config={
                "color": AXIS_CLR, "include_numbers": True,
                "font_size": 22,
            },
            tips=False,
        )
        x_lab = ax.get_x_axis_label(
            MathTex(r"\theta", font_size=28, color=AXIS_CLR),
            edge=RIGHT, direction=DOWN,
        )
        ax_group = VGroup(ax, x_lab)
        ax_group.move_to(DOWN * 0.6)
        self.play(Create(ax), FadeIn(x_lab), run_time=0.7)

        # Prior
        prior_curve = ax.plot(
            lambda x: gauss(x, 0, 1),
            x_range=[-4, 5, 0.05], color=PAL[4], stroke_width=2.5,
        )
        prior_lbl = Text("Prior", font_size=16, color=PAL[4])
        prior_lbl.next_to(ax.c2p(-1.5, gauss(-1.5, 0, 1)), UP,
                          buff=0.1)
        self.play(Create(prior_curve), FadeIn(prior_lbl), run_time=0.8)

        # MLE goes to infinity
        mle_arrow = Arrow(
            ax.c2p(3.5, 0.15), ax.c2p(5.0, 0.15),
            color=PAL[0], stroke_width=2.5,
        )
        mle_lbl = MathTex(
            r"\hat{\theta}_{\mathrm{MLE}} \to \infty",
            font_size=22, color=PAL[0],
        )
        mle_lbl.next_to(mle_arrow, UP, buff=0.1)

        self.play(Create(mle_arrow), FadeIn(mle_lbl), run_time=0.8)
        self.wait(2.0)

        # MAP stays finite
        map_mu = 2.2
        map_curve = ax.plot(
            lambda x: gauss(x, map_mu, 0.5) * 0.8,
            x_range=[-4, 5, 0.05], color=PAL[1], stroke_width=3,
        )
        map_dot = Dot(ax.c2p(map_mu, 0), color=PAL[1], radius=0.08)
        map_lbl = MathTex(
            r"\hat{\theta}_{\mathrm{MAP}} = 2.2",
            font_size=20, color=PAL[1],
        )
        map_lbl.next_to(
            ax.c2p(map_mu, gauss(map_mu, map_mu, 0.5) * 0.8),
            UP, buff=0.15,
        )

        self.play(Create(map_curve), FadeIn(map_dot),
                  FadeIn(map_lbl), run_time=1.0)
        self.wait(1.5)

        note = Text("The prior prevents infinite estimates",
                     font_size=22, color=ACCENT)
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(3.5)

        self.play(FadeOut(VGroup(
            header, ax_group, prior_curve, prior_lbl,
            mle_arrow, mle_lbl,
            map_curve, map_dot, map_lbl, note,
        )), run_time=0.8)

    # ================================================================
    #  Takeaway
    # ================================================================
    def play_takeaway(self):
        heading = Text("Bayesian = Regularized MLE", font_size=36,
                       color=WHITE, weight=BOLD)
        heading.shift(UP * 0.8)

        rows = []
        items = [
            ("Prior", PAL[4], "belief before seeing data"),
            ("Likelihood", PAL[0], "what the data say"),
            ("Posterior", PAL[1], "updated belief = prior \u00d7 likelihood"),
        ]
        for label, color, desc in items:
            lbl = Text(label, font_size=26, color=color, weight=BOLD)
            dash = Text("\u2014", font_size=24, color=TEXT2)
            desc_mob = Text(desc, font_size=22, color=TEXT2)
            row = VGroup(lbl, dash, desc_mob).arrange(RIGHT, buff=0.2)
            rows.append(row)

        row_group = VGroup(*rows).arrange(DOWN, buff=0.45,
                                          aligned_edge=LEFT)
        row_group.next_to(heading, DOWN, buff=0.6)

        line = Line(LEFT * 2, RIGHT * 2, color=ACCENT, stroke_width=1.5)
        line.next_to(row_group, DOWN, buff=0.5)

        self.play(FadeIn(heading, shift=DOWN * 0.15), run_time=0.7)
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.5)
            self.wait(0.4)
        self.play(Create(line), run_time=0.5)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
