"""
AIMS Chapter 1 Animation #5: Bradley-Terry & Elo Dynamics
Shows pairwise comparisons and Elo rating updates.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch1 animations/ch1/elo_dynamics.py EloDynamics
"""

from manim import *
import numpy as np

# ── design tokens ───────────────────────────────────────────────────
ACCENT = "#FFD966"
BG = "#0f0f0f"
TEXT2 = "#aaaaaa"
PAL = ["#5B8DEE", "#45BF7C", "#F0A35C", "#E8637A", "#B07CD8"]
AXIS_CLR = "#888888"

K_FACTOR = 32  # Elo K factor


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class EloDynamics(Scene):
    def construct(self):
        self.camera.background_color = BG
        np.random.seed(7)

        self.play_title()
        self.play_bt_formula()
        self.play_elo_arena()
        self.play_takeaway()

    # ── title ───────────────────────────────────────────────────────
    def play_title(self):
        t = Text("Paired Comparisons", font_size=44,
                 color=WHITE, weight=BOLD)
        st = Text("Bradley-Terry & Elo Rating Systems",
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

    # ── BT formula ──────────────────────────────────────────────────
    def play_bt_formula(self):
        header = Text("The Bradley-Terry Model", font_size=32,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.6)

        bt = MathTex(
            r"P(i \succ j) = \sigma(\theta_i - \theta_j)",
            font_size=34, color=ACCENT,
        )
        bt.next_to(header, DOWN, buff=0.4)
        self.play(Write(bt), run_time=1.2)
        self.wait(4.0)  # narrator explains the Bradley-Terry formula

        note = Text(
            "Same math as Rasch \u2014 but now two models compete "
            "instead of model vs. item",
            font_size=20, color=TEXT2,
        )
        note.next_to(bt, DOWN, buff=0.4)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.wait(3.0)

        # Elo update
        elo_header = Text("Elo Update Rule", font_size=26,
                          color=PAL[1], weight=BOLD)
        elo_header.next_to(note, DOWN, buff=0.5)
        elo_eq = MathTex(
            r"R_i^{\mathrm{new}} = R_i + K(S_i - E_i)",
            font_size=30, color=PAL[1],
        )
        elo_eq.next_to(elo_header, DOWN, buff=0.25)
        self.play(FadeIn(elo_header), run_time=0.5)
        self.play(Write(elo_eq), run_time=1.0)
        self.wait(4.5)  # narrator explains the Elo update rule

        self.play(FadeOut(VGroup(header, bt, note, elo_header, elo_eq)),
                  run_time=0.7)

    # ── Elo arena simulation ────────────────────────────────────────
    def play_elo_arena(self):
        header = Text("Elo Ratings in Action", font_size=32,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        # 5 models with true strengths
        names = ["A", "B", "C", "D", "E"]
        true_elo = np.array([1700, 1600, 1500, 1400, 1300])
        n_models = len(names)

        # Rating number line (vertical)
        rating_line = NumberLine(
            x_range=[1200, 1800, 100], length=5.5,
            rotation=PI / 2, color=AXIS_CLR,
            include_numbers=True, font_size=18,
            label_direction=LEFT,
        )
        rating_line.shift(LEFT * 3)
        rl_label = Text("Rating", font_size=18, color=AXIS_CLR)
        rl_label.next_to(rating_line, UP, buff=0.2)

        self.play(Create(rating_line), FadeIn(rl_label), run_time=0.8)

        # True rating dashed lines
        true_lines = VGroup()
        for i in range(n_models):
            y = rating_line.n2p(true_elo[i])[1]
            dl = DashedLine(
                np.array([-1.5, y, 0]), np.array([4.5, y, 0]),
                color=PAL[i], stroke_width=0.8, dash_length=0.06,
            )
            true_lines.add(dl)
        # Show true lines faintly
        self.play(
            *[Create(dl) for dl in true_lines],
            run_time=0.8,
        )

        # Initialize all models at 1500
        ratings = np.full(n_models, 1500.0)
        trackers = [ValueTracker(1500.0) for _ in range(n_models)]

        # Model dots
        dots = VGroup()
        labels = VGroup()
        for i in range(n_models):
            dot = always_redraw(
                lambda idx=i: Dot(
                    np.array([
                        -1.0 + idx * 1.2,
                        rating_line.n2p(trackers[idx].get_value())[1],
                        0,
                    ]),
                    color=PAL[idx], radius=0.12,
                )
            )
            lbl = always_redraw(
                lambda idx=i: Text(
                    names[idx], font_size=20, color=PAL[idx],
                ).next_to(
                    np.array([
                        -1.0 + idx * 1.2,
                        rating_line.n2p(trackers[idx].get_value())[1],
                        0,
                    ]),
                    UP, buff=0.15,
                )
            )
            dots.add(dot)
            labels.add(lbl)

        self.play(FadeIn(dots), FadeIn(labels), run_time=0.8)
        self.wait(0.5)

        # Run matches
        def elo_expected(r_a, r_b):
            return 1.0 / (1.0 + 10 ** ((r_b - r_a) / 400.0))

        def run_match(i, j, true_str):
            """Simulate a match and return winner index."""
            p_i_wins = sigmoid((true_str[i] - true_str[j]) / 200.0)
            winner = i if np.random.random() < p_i_wins else j
            return winner

        # Phase 1: slow matches (one at a time)
        match_pairs = [
            (0, 2), (1, 3), (0, 4), (2, 4), (1, 2),
            (3, 4), (0, 1), (2, 3),
        ]

        match_label = Text("", font_size=20, color=TEXT2)
        match_label.to_edge(DOWN, buff=0.25)

        for mi, (a, b) in enumerate(match_pairs):
            winner = run_match(a, b, true_elo)
            loser = b if winner == a else a

            e_a = elo_expected(ratings[a], ratings[b])
            e_b = 1 - e_a
            s_a = 1.0 if winner == a else 0.0
            s_b = 1.0 - s_a

            new_a = ratings[a] + K_FACTOR * (s_a - e_a)
            new_b = ratings[b] + K_FACTOR * (s_b - e_b)
            ratings[a] = new_a
            ratings[b] = new_b

            # Clamp to axis range
            ratings = np.clip(ratings, 1210, 1790)

            result_str = f"{names[winner]} beats {names[loser]}"
            new_match_lbl = Text(result_str, font_size=20, color=TEXT2)
            new_match_lbl.to_edge(DOWN, buff=0.25)

            speed = 0.8 if mi < 3 else 0.5
            self.play(
                trackers[a].animate.set_value(ratings[a]),
                trackers[b].animate.set_value(ratings[b]),
                FadeOut(match_label),
                FadeIn(new_match_lbl),
                run_time=speed,
            )
            match_label = new_match_lbl
            if mi < 3:
                self.wait(0.3)

        self.play(FadeOut(match_label), run_time=0.3)

        # Phase 2: fast-forward many more matches
        ff_label = Text("Fast-forward: 50 more matches...",
                        font_size=20, color=TEXT2)
        ff_label.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(ff_label), run_time=0.4)

        for _ in range(50):
            a, b = np.random.choice(n_models, 2, replace=False)
            winner = run_match(a, b, true_elo)
            loser = b if winner == a else a
            e_a = elo_expected(ratings[a], ratings[b])
            s_a = 1.0 if winner == a else 0.0
            ratings[a] += K_FACTOR * (s_a - e_a)
            ratings[b] += K_FACTOR * ((1 - s_a) - (1 - e_a))
            ratings = np.clip(ratings, 1210, 1790)

        self.play(
            *[trackers[i].animate.set_value(ratings[i])
              for i in range(n_models)],
            run_time=2.5, rate_func=smooth,
        )
        self.wait(0.5)

        self.play(FadeOut(ff_label), run_time=0.3)
        converge_note = Text(
            "Ratings converge toward true strengths",
            font_size=20, color=ACCENT,
        )
        converge_note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(converge_note, shift=UP * 0.1), run_time=0.5)
        self.wait(7.0)  # narrator explains convergence to true strengths

        everything = VGroup(
            header, rating_line, rl_label, true_lines,
            dots, labels, converge_note,
        )
        self.play(FadeOut(everything), run_time=0.7)

    # ── takeaway ────────────────────────────────────────────────────
    def play_takeaway(self):
        lines = VGroup(
            Text("Elo / Bradley-Terry", font_size=34,
                 color=WHITE, weight=BOLD),
            Text("= Rasch model for pairwise comparisons",
                 font_size=26, color=ACCENT),
            Text("Chatbot Arena uses exactly this system",
                 font_size=22, color=TEXT2),
            Text("to rank LLMs from human preferences.",
                 font_size=22, color=TEXT2),
        )
        lines.arrange(DOWN, buff=0.35)
        lines.move_to(UP * 0.2)

        for l in lines:
            self.play(FadeIn(l, shift=DOWN * 0.1), run_time=0.5)
            self.wait(0.2)
        self.wait(6.5)  # narrator delivers the Elo/BT takeaway
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
