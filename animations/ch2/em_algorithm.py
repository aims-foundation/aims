"""
AIMS Chapter 2 Animation: The EM Algorithm
E-step / M-step cycle, posterior sharpening, item difficulty update,
iteration convergence.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch2 animations/ch2/em_algorithm.py EMAlgorithm
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


class EMAlgorithm(Scene):
    """EM algorithm visualization with E-step/M-step cycle."""

    def construct(self):
        self.camera.background_color = BG
        self.play_title()
        self.play_cycle_diagram()
        self.play_e_step()
        self.play_m_step()
        self.play_iteration()
        self.play_takeaway()

    # ================================================================
    #  Title
    # ================================================================
    def play_title(self):
        title = Text("The EM Algorithm", font_size=44,
                     color=WHITE, weight=BOLD)
        subtitle = Text("Expectation-Maximization for latent variables",
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
    #  Cycle diagram
    # ================================================================
    def play_cycle_diagram(self):
        header = Text("Two-Step Cycle", font_size=28,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        # E-step box
        e_box = RoundedRectangle(
            width=2.8, height=0.9, corner_radius=0.15,
            fill_color=PAL[0], fill_opacity=0.12,
            stroke_color=PAL[0], stroke_width=2,
        )
        e_box.shift(LEFT * 2.5)
        e_text = Text("E-step", font_size=24, color=PAL[0],
                      weight=BOLD)
        e_text.move_to(e_box)
        e_sub = Text("Estimate abilities", font_size=16, color=TEXT2)
        e_sub.next_to(e_box, DOWN, buff=0.15)

        # M-step box
        m_box = RoundedRectangle(
            width=2.8, height=0.9, corner_radius=0.15,
            fill_color=PAL[1], fill_opacity=0.12,
            stroke_color=PAL[1], stroke_width=2,
        )
        m_box.shift(RIGHT * 2.5)
        m_text = Text("M-step", font_size=24, color=PAL[1],
                      weight=BOLD)
        m_text.move_to(m_box)
        m_sub = Text("Update items", font_size=16, color=TEXT2)
        m_sub.next_to(m_box, DOWN, buff=0.15)

        # Arrows
        arrow_right = CurvedArrow(
            e_box.get_right() + UP * 0.05,
            m_box.get_left() + UP * 0.05,
            angle=-TAU / 6, color=AXIS_CLR,
        )
        arrow_left = CurvedArrow(
            m_box.get_left() + DOWN * 0.05,
            e_box.get_right() + DOWN * 0.05,
            angle=-TAU / 6, color=AXIS_CLR,
        )

        self.cycle_group = Group(
            e_box, e_text, e_sub, m_box, m_text, m_sub,
            arrow_right, arrow_left,
        )

        self.play(
            FadeIn(e_box), FadeIn(e_text), FadeIn(e_sub),
            FadeIn(m_box), FadeIn(m_text), FadeIn(m_sub),
            run_time=0.8,
        )
        self.play(Create(arrow_right), Create(arrow_left), run_time=0.6)

        # Formula
        formula = MathTex(
            r"\ell(\beta^{(t+1)}) \geq \ell(\beta^{(t)})",
            font_size=26, color=ACCENT,
        )
        formula.next_to(self.cycle_group, DOWN, buff=0.5)
        guarantee = Text("Guaranteed improvement at every step",
                         font_size=18, color=TEXT2)
        guarantee.next_to(formula, DOWN, buff=0.15)

        self.play(Write(formula), run_time=0.8)
        self.play(FadeIn(guarantee), run_time=0.4)
        self.wait(3.0)

        self.play(FadeOut(Group(
            header, self.cycle_group, formula, guarantee,
        )), run_time=0.8)

    # ================================================================
    #  E-step: posterior over abilities
    # ================================================================
    def play_e_step(self):
        header = Text("E-step: Posterior Over Abilities", font_size=28,
                      color=PAL[0], weight=BOLD)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        # Axes
        ax = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.65, 0.1],
            x_length=8, y_length=3.8,
            axis_config={"color": AXIS_CLR, "font_size": 18,
                         "include_numbers": True},
            tips=False,
        )
        x_lab = MathTex(r"\theta", font_size=24, color=AXIS_CLR)
        x_lab.next_to(ax, RIGHT, buff=0.1).shift(DOWN * 0.3)
        y_lab = Text("density", font_size=16, color=AXIS_CLR)
        y_lab.next_to(ax, LEFT, buff=0.1).shift(UP * 0.5)
        ax_group = VGroup(ax, x_lab, y_lab)
        ax_group.move_to(DOWN * 0.3)
        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab), run_time=0.7)

        # Prior curve
        mu_t = ValueTracker(0.0)
        sig_t = ValueTracker(1.0)

        curve = always_redraw(
            lambda: ax.plot(
                lambda x: gauss(x, mu_t.get_value(), sig_t.get_value()),
                x_range=[-4, 4, 0.05],
                color=PAL[4], stroke_width=3,
            )
        )
        prior_lbl = Text("Prior: N(0,1)", font_size=18, color=PAL[4])
        prior_lbl.next_to(ax.c2p(0, gauss(0, 0, 1)), UP + LEFT,
                          buff=0.15)

        self.add(curve)
        self.play(FadeIn(curve), FadeIn(prior_lbl), run_time=0.8)
        self.wait(1.5)

        # Response pattern icons
        responses = [1, 0, 1, 1, 0]
        resp_group = VGroup()
        for i, r in enumerate(responses):
            if r == 1:
                icon = Circle(radius=0.12, fill_color=PAL[1],
                              fill_opacity=0.8, stroke_width=0)
            else:
                icon = Circle(radius=0.12, fill_color=PAL[3],
                              fill_opacity=0.8, stroke_width=0)
            resp_group.add(icon)
        resp_group.arrange(RIGHT, buff=0.15)
        resp_group.next_to(ax, DOWN, buff=0.35)

        resp_label = Text("Responses: ", font_size=16, color=TEXT2)
        resp_label.next_to(resp_group, LEFT, buff=0.15)

        self.play(FadeIn(resp_group), FadeIn(resp_label), run_time=0.5)
        self.wait(1.5)

        # Morph prior → posterior
        post_lbl = Text("Posterior", font_size=18, color=PAL[0])
        post_lbl.next_to(ax.c2p(0.8, gauss(0.8, 0.8, 0.6)),
                         UP + RIGHT, buff=0.15)

        self.play(
            mu_t.animate.set_value(0.8),
            sig_t.animate.set_value(0.6),
            FadeOut(prior_lbl),
            run_time=2.5, rate_func=smooth,
        )
        # Recolor curve
        new_curve = ax.plot(
            lambda x: gauss(x, 0.8, 0.6),
            x_range=[-4, 4, 0.05], color=PAL[0], stroke_width=3,
        )
        self.remove(curve)
        self.add(new_curve)
        self.play(FadeIn(post_lbl), run_time=0.4)
        self.wait(3.0)

        note = Text(
            "Data sharpens our belief about each model's ability",
            font_size=18, color=TEXT2,
        )
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.4)
        self.wait(3.0)

        self.play(FadeOut(VGroup(
            header, ax_group, new_curve, post_lbl,
            resp_group, resp_label, note,
        )), run_time=0.8)

    # ================================================================
    #  M-step: update item difficulties
    # ================================================================
    def play_m_step(self):
        header = Text("M-step: Update Item Parameters", font_size=28,
                      color=PAL[1], weight=BOLD)
        header.to_edge(UP, buff=0.35)

        formula = MathTex(
            r"\sum_i \mathbb{E}[P_{ij}]",
            r"=",
            r"\sum_i Y_{ij}",
            font_size=26,
        )
        formula[0].set_color(PAL[1])  # expected
        formula[2].set_color(ACCENT)  # observed
        formula.next_to(header, DOWN, buff=0.2)

        interp = Text("expected correct = observed correct",
                       font_size=16, color=TEXT2)
        interp.next_to(formula, DOWN, buff=0.12)

        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)
        self.play(Write(formula), run_time=0.8)
        self.play(FadeIn(interp), run_time=0.3)
        self.wait(1.5)

        # Bar chart: 5 items
        n_items = 5
        current_betas = [0.5, -0.3, 1.2, -0.8, 0.1]
        target_betas = [0.8, -0.1, 0.9, -1.2, 0.3]

        bar_width = 0.4
        bar_spacing = 1.2
        base_y = -1.5

        # Baseline axis
        baseline = Line(
            LEFT * 3.2 + UP * base_y,
            RIGHT * 3.2 + UP * base_y,
            color=AXIS_CLR, stroke_width=1,
        )
        self.play(Create(baseline), run_time=0.3)

        bars = VGroup()
        targets = VGroup()
        labels = VGroup()

        for j in range(n_items):
            x = (j - 2) * bar_spacing
            # Current bar
            h = current_betas[j] * 1.2  # scale for visibility
            bar = Rectangle(
                width=bar_width, height=abs(h),
                fill_color=PAL[1], fill_opacity=0.6,
                stroke_color=PAL[1], stroke_width=1.5,
            )
            if h >= 0:
                bar.move_to(
                    RIGHT * x + UP * (base_y + abs(h) / 2)
                )
            else:
                bar.move_to(
                    RIGHT * x + UP * (base_y - abs(h) / 2)
                )
            bars.add(bar)

            # Target outline
            th = target_betas[j] * 1.2
            target = Rectangle(
                width=bar_width, height=abs(th),
                fill_opacity=0,
                stroke_color=ACCENT, stroke_width=2,
                stroke_opacity=0.6,
            )
            if th >= 0:
                target.move_to(
                    RIGHT * x + UP * (base_y + abs(th) / 2)
                )
            else:
                target.move_to(
                    RIGHT * x + UP * (base_y - abs(th) / 2)
                )
            targets.add(target)

            # Label
            lbl = MathTex(rf"\beta_{j+1}", font_size=16, color=TEXT2)
            lbl.next_to(bar, DOWN, buff=0.3)
            lbl.move_to(RIGHT * x + UP * (base_y - 0.5))
            labels.add(lbl)

        self.play(
            *[FadeIn(b) for b in bars],
            *[FadeIn(l) for l in labels],
            run_time=0.6,
        )
        self.wait(1.0)

        # Show targets
        target_lbl = Text("Target (from data)", font_size=14,
                          color=ACCENT)
        target_lbl.shift(RIGHT * 4 + UP * 0.2)
        self.play(
            *[FadeIn(t) for t in targets],
            FadeIn(target_lbl),
            run_time=0.6,
        )
        self.wait(2.0)

        # Animate bars adjusting to targets
        anims = []
        for j in range(n_items):
            x = (j - 2) * bar_spacing
            th = target_betas[j] * 1.2
            new_bar = Rectangle(
                width=bar_width, height=abs(th),
                fill_color=PAL[1], fill_opacity=0.6,
                stroke_color=PAL[1], stroke_width=1.5,
            )
            if th >= 0:
                new_bar.move_to(
                    RIGHT * x + UP * (base_y + abs(th) / 2)
                )
            else:
                new_bar.move_to(
                    RIGHT * x + UP * (base_y - abs(th) / 2)
                )
            anims.append(Transform(bars[j], new_bar))

        self.play(*anims, run_time=2.0, rate_func=smooth)
        self.wait(3.0)

        self.play(FadeOut(VGroup(
            header, formula, interp, baseline,
            bars, targets, labels, target_lbl,
        )), run_time=0.8)

    # ================================================================
    #  Iteration cycle with convergence
    # ================================================================
    def play_iteration(self):
        header = Text("Iterating to Convergence", font_size=28,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        # Recreate small cycle diagram
        e_box = RoundedRectangle(
            width=2.0, height=0.7, corner_radius=0.12,
            fill_color=PAL[0], fill_opacity=0.1,
            stroke_color=PAL[0], stroke_width=1.5,
        )
        e_box.shift(LEFT * 1.8 + UP * 0.3)
        e_text = Text("E", font_size=20, color=PAL[0], weight=BOLD)
        e_text.move_to(e_box)

        m_box = RoundedRectangle(
            width=2.0, height=0.7, corner_radius=0.12,
            fill_color=PAL[1], fill_opacity=0.1,
            stroke_color=PAL[1], stroke_width=1.5,
        )
        m_box.shift(RIGHT * 1.8 + UP * 0.3)
        m_text = Text("M", font_size=20, color=PAL[1], weight=BOLD)
        m_text.move_to(m_box)

        arr_r = Arrow(e_box.get_right(), m_box.get_left(),
                      color=AXIS_CLR, stroke_width=1.5, buff=0.1)
        arr_l = Arrow(m_box.get_bottom() + LEFT * 0.3,
                      e_box.get_bottom() + RIGHT * 0.3,
                      color=AXIS_CLR, stroke_width=1.5, buff=0.1)

        cycle = VGroup(e_box, e_text, m_box, m_text, arr_r, arr_l)
        self.play(FadeIn(cycle), run_time=0.5)

        # Iteration counter
        iter_label = Text("Iteration: ", font_size=22, color=TEXT2)
        iter_label.shift(LEFT * 5 + UP * 0.3)
        counter = Integer(0, font_size=28, color=ACCENT)
        counter.next_to(iter_label, RIGHT, buff=0.1)
        self.play(FadeIn(iter_label), FadeIn(counter), run_time=0.3)

        # Convergence curve (bottom half)
        conv_ax = Axes(
            x_range=[0, 20, 5], y_range=[-3500, -2400, 250],
            x_length=7, y_length=2.5,
            axis_config={"color": AXIS_CLR, "font_size": 14,
                         "include_numbers": True},
            tips=False,
        )
        conv_ax.shift(DOWN * 2.0)
        conv_x_lbl = Text("Iteration", font_size=14, color=AXIS_CLR)
        conv_x_lbl.next_to(conv_ax, DOWN, buff=0.1)
        conv_y_lbl = Text("Marginal log-lik", font_size=14,
                          color=AXIS_CLR)
        conv_y_lbl.next_to(conv_ax, LEFT, buff=0.1).shift(UP * 0.3)

        self.play(Create(conv_ax), FadeIn(conv_x_lbl),
                  FadeIn(conv_y_lbl), run_time=0.5)

        # Pre-compute convergence data
        ll_values = [-2500 - 950 * np.exp(-t / 4) for t in range(21)]

        # Animate iterations
        prev_point = None
        for t in range(1, 11):
            # Flash E then M
            self.play(
                Indicate(e_box, color=PAL[0], scale_factor=1.08),
                run_time=0.2,
            )
            self.play(
                Indicate(m_box, color=PAL[1], scale_factor=1.08),
                run_time=0.2,
            )

            # Update counter
            self.play(counter.animate.set_value(t), run_time=0.1)

            # Add point to convergence curve
            point = Dot(conv_ax.c2p(t, ll_values[t]),
                        color=PAL[1], radius=0.04)
            if prev_point is not None:
                seg = Line(
                    conv_ax.c2p(t - 1, ll_values[t - 1]),
                    conv_ax.c2p(t, ll_values[t]),
                    color=PAL[1], stroke_width=2,
                )
                self.add(seg)
            self.add(point)
            prev_point = point

        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.clear()
        self.camera.background_color = BG

    # ================================================================
    #  Takeaway
    # ================================================================
    def play_takeaway(self):
        heading = Text("EM: The workhorse of IRT estimation",
                       font_size=32, color=WHITE, weight=BOLD)
        heading.shift(UP * 0.5)

        bullets = VGroup(
            Text("Handles latent variables naturally",
                 font_size=22, color=TEXT2),
            Text("Guaranteed monotone convergence",
                 font_size=22, color=TEXT2),
            Text("Basis for most IRT software",
                 font_size=22, color=TEXT2),
        )
        bullets.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        bullets.next_to(heading, DOWN, buff=0.5)

        line = Line(LEFT * 2, RIGHT * 2, color=ACCENT, stroke_width=1.5)
        line.next_to(bullets, DOWN, buff=0.5)

        self.play(FadeIn(heading, shift=DOWN * 0.15), run_time=0.7)
        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT * 0.15), run_time=0.4)
            self.wait(0.3)
        self.play(Create(line), run_time=0.4)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
