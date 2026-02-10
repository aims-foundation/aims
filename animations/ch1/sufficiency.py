"""
AIMS Chapter 1 Animation #4: Sufficiency of Sum Scores
Shows that under Rasch, different response patterns with the same sum
give identical information about theta. Under 2PL, pattern matters.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch1 animations/ch1/sufficiency.py Sufficiency
"""

from manim import *
import numpy as np

# ── design tokens ───────────────────────────────────────────────────
ACCENT = "#FFD966"
BG = "#0f0f0f"
TEXT2 = "#aaaaaa"
PAL = ["#5B8DEE", "#45BF7C", "#F0A35C", "#E8637A", "#B07CD8"]
CELL_ON = "#5B8DEE"
CELL_OFF = "#1c1c1c"
CELL_BORDER = "#2a2a2a"
AXIS_CLR = "#888888"

M = 5  # number of items
CELL_SIZE = 0.55


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class Sufficiency(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.play_title()
        self.play_patterns()
        self.play_rasch_merge()
        self.play_2pl_break()
        self.play_takeaway()

    # ── title ───────────────────────────────────────────────────────
    def play_title(self):
        t = Text("Sufficiency of Sum Scores", font_size=44,
                 color=WHITE, weight=BOLD)
        st = Text("When does the total score tell the whole story?",
                  font_size=24, color=TEXT2)
        st.next_to(t, DOWN, buff=0.35)
        line = Line(LEFT * 2.5, RIGHT * 2.5, color=ACCENT,
                    stroke_width=1.5)
        line.next_to(st, DOWN, buff=0.3)
        g = VGroup(t, st, line)
        self.play(FadeIn(t, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(st), Create(line), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(g, shift=UP * 0.4), run_time=0.7)

    # ── helper: build a row of cells ────────────────────────────────
    def make_row(self, pattern, y_offset=0, label=None):
        row = VGroup()
        for j, val in enumerate(pattern):
            color = CELL_ON if val == 1 else CELL_OFF
            sq = Square(
                side_length=CELL_SIZE,
                fill_color=color, fill_opacity=1.0,
                stroke_color=CELL_BORDER, stroke_width=1,
            )
            sq.move_to(np.array([
                j * (CELL_SIZE + 0.06) - (M - 1) * (CELL_SIZE + 0.06) / 2,
                y_offset, 0,
            ]))
            # number inside
            num = Text(str(val), font_size=20,
                       color=WHITE if val == 1 else "#444444")
            num.move_to(sq.get_center())
            row.add(VGroup(sq, num))
        if label is not None:
            lbl = MathTex(label, font_size=22, color=TEXT2)
            lbl.next_to(row, LEFT, buff=0.3)
            row.add(lbl)
        return row

    # ── show three patterns with same sum ───────────────────────────
    def play_patterns(self):
        header = Text("Three Patterns, Same Sum Score",
                      font_size=30, color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.6)

        patterns = [
            [1, 1, 1, 0, 0],
            [1, 0, 1, 0, 1],
            [0, 1, 0, 1, 1],
        ]

        # Item headers
        item_headers = VGroup()
        for j in range(M):
            lbl = MathTex(rf"q_{j+1}", font_size=20, color=AXIS_CLR)
            lbl.move_to(np.array([
                j * (CELL_SIZE + 0.06) - (M - 1) * (CELL_SIZE + 0.06) / 2,
                1.8, 0,
            ]))
            item_headers.add(lbl)
        self.play(FadeIn(item_headers), run_time=0.5)

        rows = []
        sum_labels = []
        for i, pat in enumerate(patterns):
            y = 1.0 - i * 0.9
            row = self.make_row(pat, y_offset=y)
            rows.append(row)

            s = sum(pat)
            sl = MathTex(rf"S = {s}", font_size=24, color=ACCENT)
            sl.next_to(row, RIGHT, buff=0.4)
            sum_labels.append(sl)

            self.play(FadeIn(row), FadeIn(sl), run_time=0.7)
            self.wait(0.2)

        note = Text("All three patterns have S = 3",
                     font_size=20, color=TEXT2)
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.4)
        self.wait(6.0)  # narrator explains the three patterns and their shared sum

        self.patterns_data = patterns
        self.pattern_rows = rows
        self.pattern_sums = sum_labels
        self.item_headers = item_headers
        self.pattern_header = header
        self.pattern_note = note

    # ── Rasch: patterns merge ───────────────────────────────────────
    def play_rasch_merge(self):
        self.play(FadeOut(self.pattern_note), run_time=0.3)

        rasch_title = Text("Under the Rasch Model", font_size=26,
                           color=PAL[0], weight=BOLD)
        rasch_title.move_to(DOWN * 1.0)
        self.play(FadeIn(rasch_title, shift=DOWN * 0.1), run_time=0.5)

        # Show factorization
        factor = MathTex(
            r"L(\theta) = \exp(\theta \cdot S)",
            r"\times h(Y, \boldsymbol{\beta})",
            font_size=26, color=ACCENT,
        )
        factor.next_to(rasch_title, DOWN, buff=0.35)
        self.play(Write(factor), run_time=1.2)
        self.wait(1.5)

        explain = Text(
            "Likelihood depends on \u03b8 only through S",
            font_size=20, color=TEXT2,
        )
        explain.next_to(factor, DOWN, buff=0.25)
        self.play(FadeIn(explain), run_time=0.5)
        self.wait(4.0)  # narrator explains likelihood depends on θ only through S

        # Animate all three rows merging into one "S = 3" box
        # First, create the target: a single merged bar
        merge_target = RoundedRectangle(
            width=3.5, height=0.7, corner_radius=0.15,
            fill_color=PAL[0], fill_opacity=0.3,
            stroke_color=PAL[0], stroke_width=2,
        )
        merge_target.move_to(UP * 0.55)
        merge_label = MathTex(r"S = 3", font_size=32, color=ACCENT)
        merge_label.move_to(merge_target.get_center())

        # Animate rows moving to center
        self.play(
            *[row.animate.move_to(merge_target.get_center()).set_opacity(0)
              for row in self.pattern_rows],
            *[sl.animate.move_to(merge_target.get_center()).set_opacity(0)
              for sl in self.pattern_sums],
            FadeOut(self.item_headers),
            run_time=1.5,
        )
        self.play(FadeIn(merge_target), FadeIn(merge_label), run_time=0.6)

        arrow = Arrow(
            merge_target.get_bottom() + DOWN * 0.1,
            merge_target.get_bottom() + DOWN * 0.8,
            color=TEXT2, stroke_width=2,
        )
        arrow_lbl = Text("no information lost", font_size=18, color=TEXT2)
        arrow_lbl.next_to(arrow, RIGHT, buff=0.15)
        self.play(Create(arrow), FadeIn(arrow_lbl), run_time=0.6)
        self.wait(6.0)  # narrator: "no information lost" — key Rasch property

        self.rasch_group = VGroup(
            self.pattern_header, rasch_title, factor, explain,
            merge_target, merge_label, arrow, arrow_lbl,
            *self.pattern_rows, *self.pattern_sums,
        )
        self.play(FadeOut(self.rasch_group), run_time=0.7)

    # ── 2PL: patterns diverge ──────────────────────────────────────
    def play_2pl_break(self):
        header = Text("Under the 2PL Model", font_size=30,
                      color=PAL[3], weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        # Discrimination values
        discrims = [2.0, 0.5, 1.5, 0.8, 1.2]
        disc_row = VGroup()
        for j, a in enumerate(discrims):
            lbl = MathTex(rf"a_{j+1}\!=\!{a}", font_size=18, color=TEXT2)
            lbl.move_to(np.array([
                j * (CELL_SIZE + 0.06) - (M - 1) * (CELL_SIZE + 0.06) / 2,
                2.0, 0,
            ]))
            disc_row.add(lbl)
        self.play(FadeIn(disc_row), run_time=0.5)

        patterns = self.patterns_data
        betas = [0.0] * M  # all same difficulty for clarity

        # Rebuild rows with likelihood values
        rows = []
        likelihoods = []
        for i, pat in enumerate(patterns):
            y = 1.2 - i * 1.0
            row = self.make_row(pat, y_offset=y)
            rows.append(row)

            # Compute log-likelihood at theta=1.0 under 2PL
            theta_eval = 1.0
            ll = 0
            for j in range(M):
                p = sigmoid(discrims[j] * (theta_eval - betas[j]))
                ll += pat[j] * np.log(p + 1e-10) + (1 - pat[j]) * np.log(
                    1 - p + 1e-10)
            ll_lbl = MathTex(
                rf"\ell(\theta\!=\!1) = {ll:.2f}",
                font_size=20, color=PAL[3],
            )
            ll_lbl.next_to(row, RIGHT, buff=0.35)
            likelihoods.append(ll_lbl)

            self.play(FadeIn(row), FadeIn(ll_lbl), run_time=0.6)
            self.wait(0.15)

        note = Text("Same S = 3, but different likelihoods!",
                     font_size=22, color=PAL[3])
        note.shift(DOWN * 1.6)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)

        explain = Text(
            "Pattern (1,1,1,0,0) gets the high-discrimination items right",
            font_size=18, color=TEXT2,
        )
        explain.next_to(note, DOWN, buff=0.25)
        self.play(FadeIn(explain), run_time=0.5)
        self.wait(6.5)  # narrator explains why pattern matters under 2PL

        everything = VGroup(
            header, disc_row, note, explain, *rows, *likelihoods,
        )
        self.play(FadeOut(everything), run_time=0.7)

    # ── takeaway ────────────────────────────────────────────────────
    def play_takeaway(self):
        l1 = Text("Under Rasch:", font_size=30, color=PAL[0], weight=BOLD)
        l2 = Text("Sum score = sufficient statistic", font_size=26,
                  color=ACCENT)
        l3 = Text("Under 2PL:", font_size=30, color=PAL[3], weight=BOLD)
        l4 = Text("The response pattern matters", font_size=26,
                  color=TEXT2)

        group = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.4)
        group.move_to(UP * 0.3)

        self.play(FadeIn(l1, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(l2, shift=DOWN * 0.1), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(l3, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(l4, shift=DOWN * 0.1), run_time=0.5)
        self.wait(7.0)  # narrator delivers the sufficiency takeaway
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
