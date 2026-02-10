"""
AIMS Chapter 1 Animation: Item Characteristic Curves (ICC)
Rasch (1PL) -> 2PL -> 3PL progression

3Blue1Brown-style animation using Manim.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch1 animations/ch1/icc_models.py ICCModels
"""

from manim import *
import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# ── colour palette ──────────────────────────────────────────────────
ITEM_COLORS = ["#5B8DEE", "#45BF7C", "#F0A35C", "#E8637A", "#B07CD8"]
ACCENT = "#FFD966"          # warm gold for formulas
BG_COLOR = "#0f0f0f"        # near-black, modern/neutral
GRID_COLOR = "#2a2a2a"      # subtle grid
AXIS_COLOR = "#888888"      # muted axes
TEXT_SECONDARY = "#aaaaaa"  # secondary text


class ICCModels(Scene):
    """Full animation: Rasch -> 2PL -> 3PL with narration-style titles."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        self.play_title()
        self.play_rasch()
        self.play_2pl()
        self.play_3pl()
        self.play_comparison()
        self.play_closing()

    # ================================================================
    #  HELPERS
    # ================================================================

    def make_axes(self, x_range=(-4, 4, 1), y_range=(0, 1, 0.25),
                  x_length=9, y_length=4.2):
        """Compact axes that leave room for header and footer text."""
        ax = Axes(
            x_range=x_range, y_range=y_range,
            x_length=x_length, y_length=y_length,
            axis_config={
                "color": AXIS_COLOR,
                "include_numbers": True,
                "font_size": 22,
                "numbers_to_exclude": [],
            },
            tips=False,
        )
        x_label = ax.get_x_axis_label(
            MathTex(r"\theta", font_size=32, color=AXIS_COLOR),
            edge=RIGHT, direction=DOWN,
        )
        y_label = ax.get_y_axis_label(
            MathTex(r"P(Y=1)", font_size=26, color=AXIS_COLOR),
            edge=UP, direction=LEFT,
        )
        return ax, x_label, y_label

    def make_header_formula(self, header_text, header_color, formula_tex):
        """Create a header + formula group pinned to the top of the frame."""
        header = Text(header_text, font_size=36, color=header_color,
                      weight=BOLD)
        header.to_edge(UP, buff=0.35)
        formula = MathTex(formula_tex, font_size=32, color=ACCENT)
        formula.next_to(header, DOWN, buff=0.2)
        return header, formula

    def position_axes(self, ax, x_lab, y_lab):
        """Center axes in the middle-lower portion of the frame."""
        group = VGroup(ax, x_lab, y_lab)
        group.move_to(DOWN * 0.55)
        return group

    def bottom_note(self, text_str):
        """Create a note anchored safely below the axes."""
        note = Text(text_str, font_size=20, color=TEXT_SECONDARY,
                    line_spacing=1.3)
        note.to_edge(DOWN, buff=0.25)
        return note

    def icc_1pl(self, theta, beta):
        return sigmoid(theta - beta)

    def icc_2pl(self, theta, a, beta):
        return sigmoid(a * (theta - beta))

    def icc_3pl(self, theta, a, beta, c):
        return c + (1 - c) * sigmoid(a * (theta - beta))

    # ================================================================
    #  ACT 0 - Title
    # ================================================================

    def play_title(self):
        title = Text("Item Characteristic Curves", font_size=48,
                     color=WHITE, weight=BOLD)
        subtitle = Text("From the Rasch Model to the 3PL",
                        font_size=26, color=TEXT_SECONDARY)
        subtitle.next_to(title, DOWN, buff=0.4)

        # thin accent line
        line = Line(LEFT * 2.5, RIGHT * 2.5, color=ACCENT, stroke_width=1.5)
        line.next_to(subtitle, DOWN, buff=0.35)

        group = VGroup(title, subtitle, line)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2),
                  Create(line), run_time=0.8)
        self.wait(3.0)
        self.play(FadeOut(group, shift=UP * 0.5), run_time=0.8)

    # ================================================================
    #  ACT 1 - Rasch Model
    # ================================================================

    def play_rasch(self):
        header, formula = self.make_header_formula(
            "The Rasch Model (1PL)", ITEM_COLORS[0],
            r"P(Y_{ij}=1) = \sigma(\theta_i - \beta_j)"
        )
        self.play(FadeIn(header, shift=DOWN * 0.15), run_time=0.8)
        self.play(Write(formula), run_time=1.2)
        self.wait(2.0)

        ax, x_lab, y_lab = self.make_axes()
        ax_group = self.position_axes(ax, x_lab, y_lab)
        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab), run_time=1.0)

        # 0.5 reference line
        half_line = DashedLine(
            ax.c2p(-4, 0.5), ax.c2p(4, 0.5),
            color=GRID_COLOR, stroke_width=1, dash_length=0.08,
        )
        self.play(Create(half_line), run_time=0.4)

        # Draw curves for several items with different difficulties
        betas = [-2, -0.5, 0.5, 1.5]
        curves = []
        labels = []
        for i, beta in enumerate(betas):
            color = ITEM_COLORS[i]
            curve = ax.plot(
                lambda t, b=beta: self.icc_1pl(t, b),
                x_range=[-4, 4, 0.05], color=color, stroke_width=3,
            )
            dot = Dot(ax.c2p(beta, 0.5), color=color, radius=0.06)
            lbl = MathTex(rf"\beta={beta}", font_size=20, color=color)
            lbl.next_to(dot, UP + RIGHT, buff=0.1)
            curves.append(VGroup(curve, dot))
            labels.append(lbl)

        self.play(Create(curves[0]), FadeIn(labels[0]), run_time=1.5)
        self.wait(4.0)  # narrator: "S-shaped curve... coin flip"
        for j in range(1, len(curves)):
            self.play(Create(curves[j]), FadeIn(labels[j]), run_time=0.7)
        self.wait(1.5)

        note = self.bottom_note(
            "All curves have identical shape \u2014 only shifted by difficulty \u03b2"
        )
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(9.0)  # narrator: "all items discriminate equally"

        everything = VGroup(
            header, formula, ax_group, half_line, note,
            *curves, *labels,
        )
        self.play(FadeOut(everything), run_time=0.8)

    # ================================================================
    #  ACT 2 - 2PL  (introduce discrimination)
    # ================================================================

    def play_2pl(self):
        header, formula = self.make_header_formula(
            "The 2PL Model", ITEM_COLORS[1],
            r"P(Y_{ij}=1) = \sigma\!\bigl(a_j(\theta_i - \beta_j)\bigr)"
        )
        self.play(FadeIn(header, shift=DOWN * 0.15), run_time=0.8)
        self.play(Write(formula), run_time=1.2)
        self.wait(2.0)  # narrator: "adds discrimination parameter a_j"

        ax, x_lab, y_lab = self.make_axes()
        ax_group = self.position_axes(ax, x_lab, y_lab)
        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab), run_time=0.8)

        # Start with a Rasch curve (a=1) and morph it
        beta = 0.0
        a_tracker = ValueTracker(1.0)

        dynamic_curve = always_redraw(
            lambda: ax.plot(
                lambda t: self.icc_2pl(t, a_tracker.get_value(), beta),
                x_range=[-4, 4, 0.05],
                color=ITEM_COLORS[1], stroke_width=3,
            )
        )
        dynamic_label = always_redraw(
            lambda: MathTex(
                rf"a = {a_tracker.get_value():.2f}",
                font_size=28, color=ITEM_COLORS[1],
            ).next_to(ax, RIGHT, buff=0.3).shift(UP * 1.0)
        )

        self.play(Create(dynamic_curve), FadeIn(dynamic_label), run_time=1.0)
        self.wait(2.5)  # narrator: "Watch the curve"

        # Ramp up
        self.play(a_tracker.animate.set_value(2.5), run_time=2.5,
                  rate_func=smooth)
        self.wait(3.0)  # narrator: "steep slope means..."
        # Ramp down
        self.play(a_tracker.animate.set_value(0.3), run_time=2.0,
                  rate_func=smooth)
        self.wait(3.0)  # narrator: "flat slope means..."
        # Back to 1
        self.play(a_tracker.animate.set_value(1.0), run_time=1.0,
                  rate_func=smooth)
        self.wait(0.3)

        # Show several fixed curves at once
        self.remove(dynamic_curve, dynamic_label)

        discriminations = [0.5, 1.0, 1.5, 2.5]
        curves_2pl = []
        labels_2pl = []
        for i, a in enumerate(discriminations):
            color = ITEM_COLORS[i]
            c = ax.plot(
                lambda t, _a=a: self.icc_2pl(t, _a, beta),
                x_range=[-4, 4, 0.05], color=color, stroke_width=3,
            )
            lbl = MathTex(rf"a = {a}", font_size=20, color=color)
            # Stagger labels to the right of the curve at theta = 2.0
            x_pos = 2.0
            y_pos = self.icc_2pl(x_pos, a, beta)
            lbl.next_to(ax.c2p(x_pos, y_pos), RIGHT, buff=0.15)
            curves_2pl.append(c)
            labels_2pl.append(lbl)

        self.play(
            *[Create(c) for c in curves_2pl],
            *[FadeIn(l) for l in labels_2pl],
            run_time=1.2,
        )

        note = self.bottom_note(
            "Higher discrimination \u2192 steeper curve = better at "
            "distinguishing ability levels"
        )
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(7.0)  # narrator: "how sharply it rises"

        everything = VGroup(
            header, formula, ax_group, note,
            *curves_2pl, *labels_2pl,
        )
        self.play(FadeOut(everything), run_time=0.8)

    # ================================================================
    #  ACT 3 - 3PL  (introduce guessing)
    # ================================================================

    def play_3pl(self):
        header, formula = self.make_header_formula(
            "The 3PL Model", ITEM_COLORS[2],
            r"P(Y_{ij}=1) = c_j + (1 - c_j)\,"
            r"\sigma\!\bigl(a_j(\theta_i - \beta_j)\bigr)"
        )
        self.play(FadeIn(header, shift=DOWN * 0.15), run_time=0.8)
        self.play(Write(formula), run_time=1.4)
        self.wait(0.4)

        ax, x_lab, y_lab = self.make_axes()
        ax_group = self.position_axes(ax, x_lab, y_lab)
        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab), run_time=0.8)

        a, beta = 1.5, 0.0
        c_tracker = ValueTracker(0.0)

        dynamic_curve = always_redraw(
            lambda: ax.plot(
                lambda t: self.icc_3pl(t, a, beta, c_tracker.get_value()),
                x_range=[-4, 4, 0.05],
                color=ITEM_COLORS[2], stroke_width=3,
            )
        )
        c_label = always_redraw(
            lambda: MathTex(
                rf"c = {c_tracker.get_value():.2f}",
                font_size=28, color=ITEM_COLORS[2],
            ).next_to(ax, RIGHT, buff=0.3).shift(UP * 1.0)
        )

        # Dashed line for guessing level
        guess_line = always_redraw(
            lambda: DashedLine(
                ax.c2p(-4, c_tracker.get_value()),
                ax.c2p(4, c_tracker.get_value()),
                color="#E8637A", stroke_width=1.5, dash_length=0.1,
            )
        )
        guess_text = always_redraw(
            lambda: MathTex(
                rf"c = {c_tracker.get_value():.2f}",
                font_size=18, color="#E8637A",
            ).next_to(ax.c2p(-3.8, c_tracker.get_value()), UP, buff=0.08)
        )

        self.add(dynamic_curve, c_label, guess_line, guess_text)
        self.play(FadeIn(dynamic_curve), FadeIn(c_label), run_time=0.6)
        self.wait(3.0)  # narrator: "guessing parameter c_j... floor"

        # Animate guessing parameter rising
        self.play(c_tracker.animate.set_value(0.25), run_time=2.0,
                  rate_func=smooth)
        self.wait(0.4)

        note1 = self.bottom_note("c = 0.25 \u2192 4-option multiple choice")
        self.play(FadeIn(note1), run_time=0.4)
        self.wait(2.0)

        self.play(c_tracker.animate.set_value(0.5), run_time=1.5,
                  rate_func=smooth)
        self.play(FadeOut(note1), run_time=0.3)

        note2 = self.bottom_note(
            "c = 0.50 \u2192 true/false (coin flip floor)"
        )
        self.play(FadeIn(note2), run_time=0.4)
        self.wait(2.0)

        self.play(c_tracker.animate.set_value(0.20), run_time=1.5,
                  rate_func=smooth)
        self.play(FadeOut(note2), run_time=0.3)
        self.wait(0.3)

        note3 = self.bottom_note(
            "Even low-ability test-takers have a non-zero chance of "
            "answering correctly"
        )
        self.play(FadeIn(note3, shift=UP * 0.1), run_time=0.5)
        self.wait(5.0)  # narrator: "can never drop below this floor"

        everything = VGroup(
            header, formula, ax_group, dynamic_curve,
            c_label, guess_line, guess_text, note3,
        )
        self.play(FadeOut(everything), run_time=0.8)

    # ================================================================
    #  ACT 4 - Side-by-side comparison
    # ================================================================

    def play_comparison(self):
        header, _ = self.make_header_formula(
            "Comparing the Three Models", WHITE,
            ""  # no formula for this section
        )
        self.play(FadeIn(header, shift=DOWN * 0.15), run_time=0.8)
        self.wait(0.3)

        ax, x_lab, y_lab = self.make_axes()
        ax_group = self.position_axes(ax, x_lab, y_lab)
        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab), run_time=0.8)

        beta = 0.0

        # 1PL
        c1 = ax.plot(lambda t: self.icc_1pl(t, beta),
                     x_range=[-4, 4, 0.05],
                     color=ITEM_COLORS[0], stroke_width=3)
        l1 = MathTex(r"\text{1PL (Rasch)}", font_size=22,
                     color=ITEM_COLORS[0])
        l1.next_to(ax.c2p(3.0, self.icc_1pl(3.0, beta)), UP, buff=0.15)

        # 2PL: a=2
        c2 = ax.plot(lambda t: self.icc_2pl(t, 2.0, beta),
                     x_range=[-4, 4, 0.05],
                     color=ITEM_COLORS[1], stroke_width=3)
        l2 = MathTex(r"\text{2PL}\ (a\!=\!2)", font_size=22,
                     color=ITEM_COLORS[1])
        l2.next_to(ax.c2p(1.5, self.icc_2pl(1.5, 2.0, beta)),
                   RIGHT, buff=0.15)

        # 3PL: a=2, c=0.2
        c3 = ax.plot(lambda t: self.icc_3pl(t, 2.0, beta, 0.2),
                     x_range=[-4, 4, 0.05],
                     color=ITEM_COLORS[2], stroke_width=3)
        l3 = MathTex(r"\text{3PL}\ (a\!=\!2,\ c\!=\!0.2)", font_size=22,
                     color=ITEM_COLORS[2])
        l3.next_to(ax.c2p(-2.8, self.icc_3pl(-2.8, 2.0, beta, 0.2)),
                   UP, buff=0.15)

        g_line = DashedLine(
            ax.c2p(-4, 0.2), ax.c2p(4, 0.2),
            color="#E8637A", stroke_width=1, dash_length=0.08,
        )

        self.play(Create(c1), FadeIn(l1), run_time=1.0)
        self.wait(0.4)
        self.play(Create(c2), FadeIn(l2), run_time=1.0)
        self.wait(0.4)
        self.play(Create(c3), FadeIn(l3), Create(g_line), run_time=1.0)
        self.wait(1.0)

        # Annotation arrows
        arrow1 = Arrow(
            ax.c2p(0.8, 0.28), ax.c2p(0.2, 0.5),
            color=WHITE, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )
        ann1 = Text("steeper slope\n= higher discrimination",
                     font_size=16, color=TEXT_SECONDARY, line_spacing=1.2)
        ann1.next_to(arrow1.get_start(), DOWN, buff=0.1)

        arrow2 = Arrow(
            ax.c2p(-2.8, 0.38), ax.c2p(-3.3, 0.22),
            color=WHITE, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )
        ann2 = Text("non-zero floor\n= guessing", font_size=16,
                     color=TEXT_SECONDARY, line_spacing=1.2)
        ann2.next_to(arrow2.get_start(), UP, buff=0.1)

        self.play(Create(arrow1), FadeIn(ann1), run_time=0.8)
        self.wait(0.8)
        self.play(Create(arrow2), FadeIn(ann2), run_time=0.8)
        self.wait(7.0)  # narrator: "each parameter tells you something"

        everything = VGroup(
            header, ax_group, c1, c2, c3, l1, l2, l3,
            g_line, arrow1, ann1, arrow2, ann2,
        )
        self.play(FadeOut(everything), run_time=0.8)

    # ================================================================
    #  ACT 5 - Closing card
    # ================================================================

    def play_closing(self):
        heading = Text("Each parameter tells a story",
                       font_size=36, color=WHITE, weight=BOLD)
        heading.to_edge(UP, buff=1.2)

        rows = []
        params = [
            (r"\beta", ITEM_COLORS[0], "how hard is the item?"),
            (r"a", ITEM_COLORS[1], "how sharply does it discriminate?"),
            (r"c", ITEM_COLORS[2], "can you guess the answer?"),
        ]
        for sym, color, desc in params:
            sym_mob = MathTex(sym, font_size=40, color=color)
            dash = Text("\u2014", font_size=28, color=TEXT_SECONDARY)
            desc_mob = Text(desc, font_size=24, color=TEXT_SECONDARY)
            row = VGroup(sym_mob, dash, desc_mob).arrange(RIGHT, buff=0.25)
            rows.append(row)

        row_group = VGroup(*rows).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        row_group.next_to(heading, DOWN, buff=0.7)

        self.play(FadeIn(heading, shift=DOWN * 0.15), run_time=0.8)
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.6)
            self.wait(0.3)

        # accent line
        line = Line(LEFT * 2, RIGHT * 2, color=ACCENT, stroke_width=1.5)
        line.next_to(row_group, DOWN, buff=0.6)

        self.play(Create(line), run_time=0.6)
        self.wait(4.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
