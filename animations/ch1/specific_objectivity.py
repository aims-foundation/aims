"""
AIMS Chapter 1 Animation #3: Specific Objectivity
Shows how β_j cancels in the Rasch odds ratio.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch1 animations/ch1/specific_objectivity.py SpecificObjectivity
"""

from manim import *
import numpy as np

# ── design tokens ───────────────────────────────────────────────────
ACCENT = "#FFD966"
BG = "#0f0f0f"
AXIS_CLR = "#888888"
TEXT2 = "#aaaaaa"
PAL = ["#5B8DEE", "#45BF7C", "#F0A35C", "#E8637A", "#B07CD8"]
MODEL_I_CLR = PAL[0]
MODEL_K_CLR = PAL[1]
ITEM_CLR = PAL[2]
CANCEL_CLR = "#E8637A"


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class SpecificObjectivity(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.play_title()
        self.play_setup()
        self.play_algebra()
        self.play_visual_proof()
        self.play_counterexample()
        self.play_takeaway()

    # ── title ───────────────────────────────────────────────────────
    def play_title(self):
        t = Text("Specific Objectivity", font_size=44, color=WHITE,
                 weight=BOLD)
        st = Text("Item-free person comparisons",
                  font_size=24, color=TEXT2)
        st.next_to(t, DOWN, buff=0.35)
        line = Line(LEFT * 2, RIGHT * 2, color=ACCENT, stroke_width=1.5)
        line.next_to(st, DOWN, buff=0.3)
        g = VGroup(t, st, line)
        self.play(FadeIn(t, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(st), Create(line), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(g, shift=UP * 0.4), run_time=0.7)

    # ── setup: two models, one item ─────────────────────────────────
    def play_setup(self):
        header = Text("Setup: Two Models, One Item", font_size=30,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.6)

        # θ number line
        theta_line = NumberLine(
            x_range=[-3, 3, 1], length=8, color=AXIS_CLR,
            include_numbers=True, font_size=20,
        )
        theta_line.shift(UP * 0.8)
        theta_label = MathTex(r"\theta", font_size=28, color=AXIS_CLR)
        theta_label.next_to(theta_line, RIGHT, buff=0.2)

        # Model dots
        theta_i, theta_k = 1.5, -0.5
        dot_i = Dot(theta_line.n2p(theta_i), color=MODEL_I_CLR, radius=0.12)
        dot_k = Dot(theta_line.n2p(theta_k), color=MODEL_K_CLR, radius=0.12)
        lbl_i = MathTex(r"\theta_i", font_size=24, color=MODEL_I_CLR)
        lbl_i.next_to(dot_i, UP, buff=0.15)
        lbl_k = MathTex(r"\theta_k", font_size=24, color=MODEL_K_CLR)
        lbl_k.next_to(dot_k, UP, buff=0.15)

        self.play(
            Create(theta_line), FadeIn(theta_label),
            FadeIn(dot_i), FadeIn(dot_k),
            FadeIn(lbl_i), FadeIn(lbl_k),
            run_time=1.2,
        )

        # Rasch formula for each
        f_i = MathTex(
            r"P(Y_{ij}=1)", r"=", r"\sigma(",
            r"\theta_i", r"-", r"\beta_j", r")",
            font_size=26,
        )
        f_i.set_color_by_tex(r"\theta_i", MODEL_I_CLR)
        f_i.set_color_by_tex(r"\beta_j", ITEM_CLR)
        f_i.shift(DOWN * 0.5)

        f_k = MathTex(
            r"P(Y_{kj}=1)", r"=", r"\sigma(",
            r"\theta_k", r"-", r"\beta_j", r")",
            font_size=26,
        )
        f_k.set_color_by_tex(r"\theta_k", MODEL_K_CLR)
        f_k.set_color_by_tex(r"\beta_j", ITEM_CLR)
        f_k.next_to(f_i, DOWN, buff=0.35)

        self.play(Write(f_i), run_time=1.0)
        self.play(Write(f_k), run_time=1.0)
        self.wait(5.0)  # narrator explains the setup with two models and one item

        # store for later cleanup
        self.setup_group = VGroup(
            header, theta_line, theta_label,
            dot_i, dot_k, lbl_i, lbl_k, f_i, f_k,
        )
        self.play(FadeOut(self.setup_group), run_time=0.7)

    # ── algebra: odds ratio, β cancels ──────────────────────────────
    def play_algebra(self):
        header = Text("The Odds Ratio", font_size=30, color=WHITE,
                      weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        # Step 1: odds for each model
        odds_i = MathTex(
            r"\mathrm{odds}_{i}", r"=",
            r"\frac{P(Y_{ij}=1)}{P(Y_{ij}=0)}", r"=",
            r"\exp(", r"\theta_i", r"-", r"\beta_j", r")",
            font_size=26,
        )
        odds_i.set_color_by_tex(r"\theta_i", MODEL_I_CLR)
        odds_i.set_color_by_tex(r"\beta_j", ITEM_CLR)
        odds_i.shift(UP * 1.2)

        odds_k = MathTex(
            r"\mathrm{odds}_{k}", r"=",
            r"\frac{P(Y_{kj}=1)}{P(Y_{kj}=0)}", r"=",
            r"\exp(", r"\theta_k", r"-", r"\beta_j", r")",
            font_size=26,
        )
        odds_k.set_color_by_tex(r"\theta_k", MODEL_K_CLR)
        odds_k.set_color_by_tex(r"\beta_j", ITEM_CLR)
        odds_k.next_to(odds_i, DOWN, buff=0.45)

        self.play(Write(odds_i), run_time=1.2)
        self.play(Write(odds_k), run_time=1.2)
        self.wait(4.0)  # narrator explains the odds for each model

        # Step 2: form the ratio — keep LaTeX fragments self-contained
        ratio = MathTex(
            r"\frac{\mathrm{odds}_{i}}{\mathrm{odds}_{k}}",
            r"=",
            r"\frac{ \exp(\theta_i - \beta_j) }{ \exp(\theta_k - \beta_j) }",
            font_size=28,
        )
        ratio.shift(DOWN * 0.6)
        self.play(Write(ratio), run_time=1.2)
        self.wait(2.5)

        # Step 3: highlight all β_j in red, then cross out
        # Find the β_j glyphs inside ratio[2] (the fraction)
        beta_indices = []
        frac_part = ratio[2]
        for idx, submob in enumerate(frac_part):
            # β is the glyph for \beta
            pass

        # Simpler approach: overlay a highlight + cross on the fraction
        # Create red "β_j cancels" note instead of glyph-level coloring
        cancel_note = MathTex(
            r"\beta_j \text{ cancels!}",
            font_size=26, color=CANCEL_CLR,
        )
        cancel_note.next_to(ratio, RIGHT, buff=0.4)
        self.play(FadeIn(cancel_note, shift=LEFT * 0.2), run_time=0.6)
        self.wait(4.0)  # narrator explains why β_j cancels in the ratio

        # Step 4: result
        result = MathTex(
            r"= \exp(\theta_i - \theta_k)",
            font_size=30, color=ACCENT,
        )
        result.next_to(ratio, DOWN, buff=0.5)
        self.play(Write(result), run_time=1.0)

        box = SurroundingRectangle(result, color=ACCENT, buff=0.15,
                                   stroke_width=2, corner_radius=0.1)
        self.play(Create(box), run_time=0.6)

        note = Text("Item difficulty cancels completely!",
                     font_size=22, color=TEXT2)
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(7.0)  # narrator elaborates on item difficulty cancelling

        self.algebra_group = VGroup(
            header, odds_i, odds_k, ratio, cancel_note, result, box, note,
        )
        self.play(FadeOut(self.algebra_group), run_time=0.7)

    # ── visual: odds ratio bars across items ────────────────────────
    def play_visual_proof(self):
        header = Text("Rasch: Same Comparison, Any Item", font_size=30,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        theta_i, theta_k = 1.5, -0.5
        true_diff = theta_i - theta_k  # = 2.0

        betas = [-2, -1, 0, 1, 2]
        bar_width = 0.5
        bar_max_len = 3.5

        # Axes-like layout: items on y-axis, odds ratio length on x-axis
        items_label = Text("Item", font_size=20, color=TEXT2)
        items_label.to_edge(LEFT, buff=0.6).shift(UP * 0.3)

        bars = VGroup()
        labels = VGroup()
        for idx, b in enumerate(betas):
            # Under Rasch, odds ratio = exp(theta_i - theta_k) for all items
            ratio_val = np.exp(true_diff)
            bar_len = (true_diff / 3.0) * bar_max_len  # scale

            y_pos = 1.5 - idx * 0.8
            bar = Rectangle(
                width=bar_len, height=bar_width,
                fill_color=PAL[0], fill_opacity=0.7,
                stroke_color=PAL[0], stroke_width=1,
            )
            bar.move_to(np.array([bar_len / 2 - 2.0, y_pos, 0]))

            lbl = MathTex(rf"\beta_j = {b}", font_size=20, color=TEXT2)
            lbl.next_to(bar, LEFT, buff=0.2)
            val_lbl = MathTex(
                rf"\exp({true_diff:.1f}) = {ratio_val:.2f}",
                font_size=18, color=ACCENT,
            )
            val_lbl.next_to(bar, RIGHT, buff=0.15)

            bars.add(VGroup(bar, val_lbl))
            labels.add(lbl)

        # Animate bars one by one
        for i in range(len(betas)):
            self.play(
                FadeIn(bars[i]), FadeIn(labels[i]),
                run_time=0.6,
            )
            self.wait(0.2)

        note = Text("All bars are identical \u2014 the comparison is item-free",
                     font_size=20, color=TEXT2)
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(7.0)  # narrator: bars are identical — comparison is item-free

        self.visual_group = VGroup(header, bars, labels, items_label, note)
        self.play(FadeOut(self.visual_group), run_time=0.7)

    # ── counterexample: 2PL breaks objectivity ──────────────────────
    def play_counterexample(self):
        header = Text("2PL: Comparison Depends on the Item",
                      font_size=30, color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        formula = MathTex(
            r"\mathrm{Under\ 2PL{:}}\ ",
            r"\frac{\mathrm{odds}_{i}}{\mathrm{odds}_{k}}",
            r"= \exp\!\bigl(", r"a_j", r"(\theta_i - \theta_k)\bigr)",
            font_size=26, color=ACCENT,
        )
        formula.set_color_by_tex(r"a_j", CANCEL_CLR)
        formula.next_to(header, DOWN, buff=0.3)
        self.play(Write(formula), run_time=1.0)

        theta_i, theta_k = 1.5, -0.5
        diff = theta_i - theta_k

        discrims = [0.5, 0.8, 1.0, 1.5, 2.5]
        bar_max_len = 3.5

        bars = VGroup()
        labels = VGroup()
        for idx, a in enumerate(discrims):
            ratio_val = np.exp(a * diff)
            bar_len = (a * diff / 6.0) * bar_max_len
            bar_len = min(bar_len, 5.0)

            y_pos = 1.0 - idx * 0.7
            bar = Rectangle(
                width=bar_len, height=0.45,
                fill_color=CANCEL_CLR, fill_opacity=0.6,
                stroke_color=CANCEL_CLR, stroke_width=1,
            )
            bar.move_to(np.array([bar_len / 2 - 2.0, y_pos, 0]))

            lbl = MathTex(rf"a_j = {a}", font_size=20, color=TEXT2)
            lbl.next_to(bar, LEFT, buff=0.2)
            val_lbl = MathTex(
                rf"{ratio_val:.1f}",
                font_size=18, color=TEXT2,
            )
            val_lbl.next_to(bar, RIGHT, buff=0.15)

            bars.add(VGroup(bar, val_lbl))
            labels.add(lbl)

        self.play(
            *[FadeIn(b) for b in bars],
            *[FadeIn(l) for l in labels],
            run_time=1.2,
        )

        note = Text("Bars differ \u2014 the comparison depends on "
                     "which item is used",
                     font_size=20, color=TEXT2)
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(7.5)  # narrator explains 2PL counterexample at length

        self.counter_group = VGroup(header, formula, bars, labels, note)
        self.play(FadeOut(self.counter_group), run_time=0.7)

    # ── takeaway ────────────────────────────────────────────────────
    def play_takeaway(self):
        lines = VGroup(
            Text("Specific objectivity", font_size=34,
                 color=WHITE, weight=BOLD),
            Text("= item-free person comparison", font_size=28,
                 color=ACCENT),
            Text("Only the Rasch model guarantees this property.",
                 font_size=22, color=TEXT2),
        )
        lines.arrange(DOWN, buff=0.4)

        self.play(FadeIn(lines[0], shift=DOWN * 0.15), run_time=0.7)
        self.play(FadeIn(lines[1], shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(lines[2], shift=DOWN * 0.1), run_time=0.5)
        self.wait(6.0)  # narrator delivers the specific objectivity takeaway
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
