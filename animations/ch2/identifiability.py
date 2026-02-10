"""
AIMS Chapter 2 Animation: The Identifiability Problem
Shows that shifting all parameters by +c leaves the likelihood unchanged,
then introduces the sum-to-zero constraint.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch2 animations/ch2/identifiability.py Identifiability
"""

from manim import *
import numpy as np

# ── design tokens ────────────────────────────────────────────────
ACCENT = "#FFD966"
BG = "#0f0f0f"
TEXT2 = "#aaaaaa"
PAL = ["#5B8DEE", "#45BF7C", "#F0A35C", "#E8637A", "#B07CD8"]
AXIS_CLR = "#888888"


class Identifiability(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.play_title()
        self.play_number_line_shift()
        self.play_algebra()
        self.play_solution()

    # ================================================================
    #  Title
    # ================================================================
    def play_title(self):
        title = Text("The Identifiability Problem", font_size=44,
                     color=WHITE, weight=BOLD)
        subtitle = Text("When infinitely many solutions look the same",
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
    #  Number line shift
    # ================================================================
    def play_number_line_shift(self):
        header = Text("Parameters on a shared scale", font_size=28,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.6)

        # Build number line
        nline = NumberLine(
            x_range=[-4, 5, 1], length=10,
            color=AXIS_CLR, include_numbers=True,
            font_size=18,
            decimal_number_config={"num_decimal_places": 0},
        )
        nline.shift(DOWN * 0.2)
        self.play(Create(nline), run_time=0.8)

        # Model dots (abilities)
        theta_vals = [-1.0, 0.5, 2.0]
        theta_labels = [r"\theta_1", r"\theta_2", r"\theta_3"]
        model_dots = VGroup()
        model_lbls = VGroup()
        for val, lbl_tex in zip(theta_vals, theta_labels):
            dot = Dot(nline.n2p(val), color=PAL[0], radius=0.1)
            lbl = MathTex(lbl_tex, font_size=20, color=PAL[0])
            lbl.next_to(dot, UP, buff=0.15)
            model_dots.add(dot)
            model_lbls.add(lbl)

        # Item triangles (difficulties)
        beta_vals = [-0.5, 1.0, 2.5]
        beta_labels = [r"\beta_1", r"\beta_2", r"\beta_3"]
        item_markers = VGroup()
        item_lbls = VGroup()
        for val, lbl_tex in zip(beta_vals, beta_labels):
            tri = Triangle(fill_color=PAL[2], fill_opacity=0.8,
                           stroke_width=0).scale(0.12).rotate(PI)
            tri.move_to(nline.n2p(val) + DOWN * 0.25)
            lbl = MathTex(lbl_tex, font_size=20, color=PAL[2])
            lbl.next_to(tri, DOWN, buff=0.15)
            item_markers.add(tri)
            item_lbls.add(lbl)

        self.play(
            *[FadeIn(d, scale=1.3) for d in model_dots],
            *[FadeIn(l) for l in model_lbls],
            run_time=0.8,
        )
        self.play(
            *[FadeIn(t, scale=1.3) for t in item_markers],
            *[FadeIn(l) for l in item_lbls],
            run_time=0.8,
        )

        # Show a gap annotation between theta_1 and beta_1
        gap_start = nline.n2p(theta_vals[0])
        gap_end = nline.n2p(beta_vals[0])
        brace = BraceBetweenPoints(
            gap_start + UP * 0.5, gap_end + UP * 0.5,
            direction=UP, color=ACCENT,
        )
        brace_lbl = Text("0.5", font_size=18, color=ACCENT)
        brace_lbl.next_to(brace, UP, buff=0.1)
        self.play(Create(brace), FadeIn(brace_lbl), run_time=0.6)
        self.wait(2.0)

        # ── Shift everything by +c ──
        c = 1.5
        shift_amount = nline.n2p(c) - nline.n2p(0)  # scene units

        shift_label = Text("Shift everything by +c", font_size=24,
                           color=ACCENT)
        shift_label.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(shift_label, shift=UP * 0.1), run_time=0.5)

        # Group all markers and labels (not the number line itself)
        all_params = VGroup(
            model_dots, model_lbls, item_markers, item_lbls,
            brace, brace_lbl,
        )
        self.play(all_params.animate.shift(shift_amount), run_time=2.0,
                  rate_func=smooth)
        self.wait(1.0)

        # Show gaps unchanged
        unchanged_note = Text("Differences unchanged!",
                              font_size=22, color=PAL[1], weight=BOLD)
        unchanged_note.next_to(brace_lbl, RIGHT, buff=0.8)
        unchanged_note.shift(shift_amount)
        self.play(FadeIn(unchanged_note, scale=1.1), run_time=0.6)
        self.wait(3.0)

        # Clean up
        self.play(FadeOut(VGroup(
            header, nline, all_params, shift_label, unchanged_note,
        )), run_time=0.8)

    # ================================================================
    #  Algebraic cancellation
    # ================================================================
    def play_algebra(self):
        header = Text("The Cancellation", font_size=28,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.5)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.6)

        # Show the full equation with colored parts
        eq = MathTex(
            r"\sigma(",
            r"\theta_i + c",
            r" - ",
            r"\beta_j + c",
            r")",
            r" = ",
            r"\sigma(",
            r"\theta_i",
            r" - ",
            r"\beta_j",
            r")",
            font_size=34,
        )
        # Color the parameter terms
        eq[1].set_color(PAL[0])  # theta_i + c
        eq[3].set_color(PAL[2])  # beta_j + c
        eq[7].set_color(PAL[0])  # theta_i
        eq[9].set_color(PAL[2])  # beta_j

        self.play(Write(eq), run_time=1.5)
        self.wait(2.0)

        # Highlight the +c portions
        # Create boxes around just the "+c" in theta_i + c and beta_j + c
        box1 = SurroundingRectangle(eq[1], color=PAL[3], buff=0.05,
                                     stroke_width=2)
        box2 = SurroundingRectangle(eq[3], color=PAL[3], buff=0.05,
                                     stroke_width=2)
        cancel_text = Text("The +c cancels!", font_size=24,
                           color=PAL[3])
        cancel_text.next_to(eq, DOWN, buff=0.6)

        self.play(Create(box1), Create(box2), run_time=0.6)
        self.wait(1.0)
        self.play(FadeIn(cancel_text, shift=UP * 0.1), run_time=0.5)
        self.wait(1.5)

        # Draw strikethrough lines
        strike1 = Line(
            box1.get_corner(DL), box1.get_corner(UR),
            color=PAL[3], stroke_width=3,
        )
        strike2 = Line(
            box2.get_corner(DL), box2.get_corner(UR),
            color=PAL[3], stroke_width=3,
        )
        self.play(Create(strike1), Create(strike2), run_time=0.5)
        self.wait(1.0)

        # Show the consequence
        consequence = Text(
            "Infinitely many solutions give the same likelihood",
            font_size=22, color=TEXT2,
        )
        consequence.next_to(cancel_text, DOWN, buff=0.5)
        self.play(FadeIn(consequence), run_time=0.6)
        self.wait(4.0)

        self.play(FadeOut(VGroup(
            header, eq, box1, box2, strike1, strike2,
            cancel_text, consequence,
        )), run_time=0.8)

    # ================================================================
    #  Sum-to-zero solution
    # ================================================================
    def play_solution(self):
        header = Text("Solution: Sum-to-Zero Constraint",
                      font_size=28, color=PAL[1], weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.6)

        # Build a clean number line
        nline = NumberLine(
            x_range=[-3, 3, 1], length=8,
            color=AXIS_CLR, include_numbers=True,
            font_size=18,
            decimal_number_config={"num_decimal_places": 0},
        )
        nline.shift(DOWN * 0.2)
        self.play(Create(nline), run_time=0.6)

        # Anchor line at zero
        anchor = DashedLine(
            nline.n2p(0) + UP * 0.8,
            nline.n2p(0) + DOWN * 0.6,
            color=ACCENT, stroke_width=2, dash_length=0.08,
        )
        anchor_lbl = Text("anchor", font_size=16, color=ACCENT)
        anchor_lbl.next_to(anchor, UP, buff=0.1)
        self.play(Create(anchor), FadeIn(anchor_lbl), run_time=0.5)

        # Place dots at un-centered positions
        raw_vals = [0.5, 2.0, 3.5]  # mean = 2.0, so need to shift by -2
        mean_val = np.mean(raw_vals)
        centered_vals = [v - mean_val for v in raw_vals]

        dots = VGroup()
        labels = VGroup()
        for i, val in enumerate(raw_vals):
            dot = Dot(nline.n2p(val), color=PAL[0], radius=0.1)
            lbl = MathTex(rf"\theta_{i+1}", font_size=20, color=PAL[0])
            lbl.next_to(dot, UP, buff=0.15)
            dots.add(dot)
            labels.add(lbl)

        self.play(
            *[FadeIn(d, scale=1.3) for d in dots],
            *[FadeIn(l) for l in labels],
            run_time=0.7,
        )
        self.wait(1.5)

        # Show the constraint
        constraint = MathTex(
            r"\sum_i \theta_i = 0",
            font_size=28, color=ACCENT,
        )
        constraint.next_to(header, DOWN, buff=0.3)
        self.play(Write(constraint), run_time=0.8)
        self.wait(1.5)

        # Animate centering: shift dots to centered positions
        anims = []
        for i, (dot, lbl) in enumerate(zip(dots, labels)):
            new_pos = nline.n2p(centered_vals[i])
            anims.append(dot.animate.move_to(new_pos))
            anims.append(lbl.animate.next_to(
                Dot(new_pos), UP, buff=0.15,
            ))

        self.play(*anims, run_time=2.0, rate_func=smooth)
        self.wait(1.0)

        # Note
        note = Text(
            'A model with \u03b8 = 0 is "average" by convention',
            font_size=20, color=TEXT2,
        )
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
