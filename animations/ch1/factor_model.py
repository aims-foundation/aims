"""
AIMS Chapter 1 Animation #7: Factor Model & Benchmark Heterogeneity
Shows how items cluster in loading space, revealing multi-dimensionality.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch1 animations/ch1/factor_model.py FactorModel
"""

from manim import *
import numpy as np

# ── design tokens ───────────────────────────────────────────────────
ACCENT = "#FFD966"
BG = "#0f0f0f"
TEXT2 = "#aaaaaa"
PAL = ["#5B8DEE", "#45BF7C", "#F0A35C", "#E8637A", "#B07CD8"]
AXIS_CLR = "#888888"


class FactorModel(Scene):
    def construct(self):
        self.camera.background_color = BG
        np.random.seed(42)
        self.play_title()
        self.play_one_factor()
        self.play_two_factors()
        self.play_loading_space()
        self.play_heterogeneity()
        self.play_takeaway()

    # ── title ───────────────────────────────────────────────────────
    def play_title(self):
        t = Text("Factor Models &\nBenchmark Heterogeneity",
                 font_size=42, color=WHITE, weight=BOLD,
                 line_spacing=1.3)
        st = Text("What does a benchmark really measure?",
                  font_size=24, color=TEXT2)
        st.next_to(t, DOWN, buff=0.4)
        line = Line(LEFT * 2.5, RIGHT * 2.5, color=ACCENT,
                    stroke_width=1.5)
        line.next_to(st, DOWN, buff=0.3)
        g = VGroup(t, st, line)
        self.play(FadeIn(t, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(st), Create(line), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(g, shift=UP * 0.4), run_time=0.7)

    # ── helpers ─────────────────────────────────────────────────────
    def make_factor_node(self, label, pos, color):
        circ = Circle(
            radius=0.35, fill_color=color, fill_opacity=0.25,
            stroke_color=color, stroke_width=2.5,
        )
        circ.move_to(pos)
        lbl = MathTex(label, font_size=28, color=color)
        lbl.move_to(pos)
        return VGroup(circ, lbl)

    def make_item_node(self, label, pos, color=TEXT2):
        circ = Circle(
            radius=0.28, fill_color=BG, fill_opacity=1,
            stroke_color=color, stroke_width=1.5,
        )
        circ.move_to(pos)
        lbl = MathTex(label, font_size=20, color=color)
        lbl.move_to(pos)
        return VGroup(circ, lbl)

    # ── one-factor model ────────────────────────────────────────────
    def play_one_factor(self):
        header = Text("One-Factor Model", font_size=30,
                      color=PAL[0], weight=BOLD)
        header.to_edge(UP, buff=0.4)
        formula = MathTex(
            r"X_j = \lambda_j F + \varepsilon_j",
            font_size=28, color=ACCENT,
        )
        formula.next_to(header, DOWN, buff=0.2)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)
        self.play(Write(formula), run_time=0.8)

        # Factor at center top
        f_pos = UP * 0.4
        f_node = self.make_factor_node("F", f_pos, PAL[0])

        # 6 items in an arc below
        items = VGroup()
        item_labels_list = []
        for j in range(6):
            angle = PI + PI * (j / 5)  # semicircle below factor
            x = f_pos[0] + 2.8 * np.cos(angle)
            y = f_pos[1] + 2.0 * np.sin(angle) - 1.0
            pos = np.array([x, y, 0])
            node = self.make_item_node(rf"X_{j+1}", pos)
            items.add(node)

        self.play(Create(f_node), run_time=0.6)
        self.play(*[FadeIn(item) for item in items], run_time=0.8)

        # Arrows with equal loading (≈1)
        arrows = VGroup()
        for item in items:
            arr = Arrow(
                f_node.get_center(), item.get_center(),
                color=PAL[0], stroke_width=2, buff=0.38,
                max_tip_length_to_length_ratio=0.1,
            )
            arrows.add(arr)

        self.play(*[Create(a) for a in arrows], run_time=1.0)

        note = Text("All items load equally on one factor "
                     "\u2014 unidimensional",
                     font_size=20, color=TEXT2)
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(5.5)  # narrator explains one-factor / unidimensional model

        self.one_factor_group = VGroup(
            header, formula, f_node, items, arrows, note,
        )
        self.play(FadeOut(self.one_factor_group), run_time=0.7)

    # ── two-factor model ────────────────────────────────────────────
    def play_two_factors(self):
        header = Text("Two-Factor Model", font_size=30,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        # Two factors
        f1_pos = LEFT * 2.5 + UP * 0.5
        f2_pos = RIGHT * 2.5 + UP * 0.5
        f1 = self.make_factor_node("F_1", f1_pos, PAL[0])
        f2 = self.make_factor_node("F_2", f2_pos, PAL[1])

        self.play(Create(f1), Create(f2), run_time=0.8)

        # Items: 3 load on F1, 3 load on F2, 2 load on both
        item_configs = [
            # (label, pos, f1_weight, f2_weight)
            (r"X_1", LEFT * 4 + DOWN * 1.5, 0.9, 0.0),
            (r"X_2", LEFT * 2.5 + DOWN * 2.0, 0.8, 0.1),
            (r"X_3", LEFT * 1.0 + DOWN * 1.5, 0.7, 0.3),
            (r"X_4", LEFT * 0.0 + DOWN * 2.2, 0.4, 0.5),
            (r"X_5", RIGHT * 1.0 + DOWN * 1.5, 0.3, 0.7),
            (r"X_6", RIGHT * 2.5 + DOWN * 2.0, 0.1, 0.8),
            (r"X_7", RIGHT * 4 + DOWN * 1.5, 0.0, 0.9),
        ]

        items = VGroup()
        arrows_f1 = VGroup()
        arrows_f2 = VGroup()
        for label, pos, w1, w2 in item_configs:
            node = self.make_item_node(label, pos)
            items.add(node)

            if w1 > 0.15:
                arr = Arrow(
                    f1.get_center(), node.get_center(),
                    color=PAL[0], stroke_width=w1 * 3, buff=0.38,
                    max_tip_length_to_length_ratio=0.1,
                    stroke_opacity=w1,
                )
                arrows_f1.add(arr)
            if w2 > 0.15:
                arr = Arrow(
                    f2.get_center(), node.get_center(),
                    color=PAL[1], stroke_width=w2 * 3, buff=0.38,
                    max_tip_length_to_length_ratio=0.1,
                    stroke_opacity=w2,
                )
                arrows_f2.add(arr)

        self.play(*[FadeIn(item) for item in items], run_time=0.8)
        self.play(*[Create(a) for a in arrows_f1], run_time=0.8)
        self.play(*[Create(a) for a in arrows_f2], run_time=0.8)

        note = Text(
            "Arrow thickness = loading strength. "
            "Some items load on both factors.",
            font_size=20, color=TEXT2,
        )
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(6.0)  # narrator explains two-factor model and cross-loadings

        self.two_factor_group = VGroup(
            header, f1, f2, items, arrows_f1, arrows_f2, note,
        )
        self.play(FadeOut(self.two_factor_group), run_time=0.7)

    # ── loading space scatter ───────────────────────────────────────
    def play_loading_space(self):
        header = Text("Items in Loading Space", font_size=30,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        ax = Axes(
            x_range=[0, 1, 0.25], y_range=[0, 1, 0.25],
            x_length=5.5, y_length=5.0,
            axis_config={
                "color": AXIS_CLR, "include_numbers": True,
                "font_size": 18,
            },
            tips=False,
        )
        ax.shift(DOWN * 0.3)
        x_lbl = ax.get_x_axis_label(
            MathTex(r"\lambda_1", font_size=26, color=PAL[0]),
            edge=RIGHT, direction=DOWN,
        )
        y_lbl = ax.get_y_axis_label(
            MathTex(r"\lambda_2", font_size=26, color=PAL[1]),
            edge=UP, direction=LEFT,
        )

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.8)

        # Generate clustered items
        # Cluster 1: high λ1, low λ2 (reasoning)
        c1_pts = np.random.multivariate_normal(
            [0.75, 0.15], [[0.005, 0], [0, 0.005]], size=8,
        )
        # Cluster 2: low λ1, high λ2 (factual)
        c2_pts = np.random.multivariate_normal(
            [0.15, 0.75], [[0.005, 0], [0, 0.005]], size=8,
        )
        # Cluster 3: medium both (mixed)
        c3_pts = np.random.multivariate_normal(
            [0.5, 0.5], [[0.008, 0.003], [0.003, 0.008]], size=5,
        )

        clusters = [
            (c1_pts, PAL[0], "Reasoning"),
            (c2_pts, PAL[1], "Factual recall"),
            (c3_pts, PAL[2], "Mixed"),
        ]

        all_dots = VGroup()
        cluster_labels = VGroup()
        for pts, color, name in clusters:
            grp = VGroup()
            for pt in pts:
                pt = np.clip(pt, 0.02, 0.98)
                dot = Dot(ax.c2p(pt[0], pt[1]), color=color, radius=0.06)
                grp.add(dot)
            all_dots.add(grp)
            # Label near cluster center
            cx, cy = pts.mean(axis=0)
            lbl = Text(name, font_size=16, color=color)
            lbl.next_to(ax.c2p(cx, cy), UR, buff=0.15)
            cluster_labels.add(lbl)

        for i, (grp, lbl) in enumerate(zip(all_dots, cluster_labels)):
            self.play(FadeIn(grp), FadeIn(lbl), run_time=0.7)
            self.wait(0.2)

        note = Text(
            "Items cluster by what they measure \u2014 benchmarks "
            "are rarely homogeneous",
            font_size=20, color=TEXT2,
        )
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(6.0)  # narrator explains item clustering in loading space

        self.loading_group = VGroup(
            header, ax, x_lbl, y_lbl, all_dots, cluster_labels, note,
        )
        # Keep ax for next scene
        self.loading_ax = ax
        self.play(FadeOut(self.loading_group), run_time=0.7)

    # ── heterogeneity: two models, same score, different profiles ──
    def play_heterogeneity(self):
        header = Text("Same Score, Different Profiles", font_size=30,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        ax = Axes(
            x_range=[0, 1, 0.25], y_range=[0, 1, 0.25],
            x_length=5.5, y_length=5.0,
            axis_config={
                "color": AXIS_CLR, "include_numbers": True,
                "font_size": 18,
            },
            tips=False,
        )
        ax.shift(DOWN * 0.3)
        x_lbl = ax.get_x_axis_label(
            Text("Reasoning score", font_size=18, color=PAL[0]),
            edge=RIGHT, direction=DOWN,
        )
        y_lbl = ax.get_y_axis_label(
            Text("Factual score", font_size=18, color=PAL[1]),
            edge=UP, direction=LEFT,
        )
        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.8)

        # Model A: strong reasoning, weak factual
        a_pos = ax.c2p(0.85, 0.25)
        dot_a = Dot(a_pos, color=PAL[3], radius=0.12)
        lbl_a = Text("Model A", font_size=18, color=PAL[3])
        lbl_a.next_to(dot_a, RIGHT, buff=0.15)

        # Model B: weak reasoning, strong factual
        b_pos = ax.c2p(0.25, 0.85)
        dot_b = Dot(b_pos, color=PAL[4], radius=0.12)
        lbl_b = Text("Model B", font_size=18, color=PAL[4])
        lbl_b.next_to(dot_b, LEFT, buff=0.15)

        self.play(
            FadeIn(dot_a), FadeIn(lbl_a),
            FadeIn(dot_b), FadeIn(lbl_b),
            run_time=0.8,
        )
        self.wait(0.5)

        # Draw iso-score line (mean = 0.55)
        iso_start = ax.c2p(0.0, 0.55 * 2)
        iso_end = ax.c2p(0.55 * 2, 0.0)
        iso_line = DashedLine(
            iso_start, iso_end,
            color=ACCENT, stroke_width=1.5, dash_length=0.08,
        )
        iso_lbl = Text("Same mean score", font_size=16, color=ACCENT)
        iso_lbl.next_to(iso_line, DR, buff=0.1)
        self.play(Create(iso_line), FadeIn(iso_lbl), run_time=0.8)

        # Arrows from origin showing different profiles
        arrow_a = Arrow(
            ax.c2p(0, 0), a_pos,
            color=PAL[3], stroke_width=2, buff=0.05,
            max_tip_length_to_length_ratio=0.08,
        )
        arrow_b = Arrow(
            ax.c2p(0, 0), b_pos,
            color=PAL[4], stroke_width=2, buff=0.05,
            max_tip_length_to_length_ratio=0.08,
        )
        self.play(Create(arrow_a), Create(arrow_b), run_time=0.8)

        note = Text(
            "Mean scores hide multidimensional capability profiles",
            font_size=20, color=TEXT2,
        )
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(5.0)  # narrator explains same score, different profiles

        everything = VGroup(
            header, ax, x_lbl, y_lbl, dot_a, dot_b,
            lbl_a, lbl_b, iso_line, iso_lbl,
            arrow_a, arrow_b, note,
        )
        self.play(FadeOut(everything), run_time=0.7)

    # ── takeaway ────────────────────────────────────────────────────
    def play_takeaway(self):
        lines = VGroup(
            Text("Benchmarks are rarely homogeneous",
                 font_size=30, color=WHITE, weight=BOLD),
            Text("Items cluster into distinct capability groups",
                 font_size=24, color=ACCENT),
            Text("Mean scores can mask opposing strengths",
                 font_size=22, color=TEXT2),
        )
        lines.arrange(DOWN, buff=0.4)
        lines.move_to(UP * 0.3)

        for l in lines:
            self.play(FadeIn(l, shift=DOWN * 0.1), run_time=0.6)
            self.wait(0.3)
        self.wait(6.0)  # narrator delivers the factor model takeaway
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
