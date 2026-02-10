"""
AIMS Chapter 1 Animation: Opening Hook
Visualizes the measurement problem: leaderboard → thermometer analogy → question.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch1 animations/ch1/opening_hook.py OpeningHook
"""

from manim import *
import numpy as np

ACCENT = "#FFD966"
BG = "#0f0f0f"
TEXT2 = "#aaaaaa"
PAL = ["#5B8DEE", "#45BF7C", "#F0A35C", "#E8637A", "#B07CD8"]
AXIS_CLR = "#888888"


class OpeningHook(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.play_leaderboard()
        self.play_question()
        self.wait(5.0)  # narrator: "scored the models... latent construct"
        self.play_thermometer()
        self.play_measurement_problem()

    def play_leaderboard(self):
        """Show a mock AI leaderboard appearing."""
        header = Text("AI Model Leaderboard", font_size=34,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.5)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.8)
        self.wait(0.5)

        # Mock leaderboard data
        models = [
            ("GPT-4o", 88.7, PAL[0]),
            ("Claude 3.5", 86.4, PAL[1]),
            ("Gemini Pro", 83.1, PAL[2]),
            ("Llama 3", 79.8, PAL[3]),
            ("Mistral", 76.2, PAL[4]),
        ]

        rows = VGroup()
        for i, (name, score, color) in enumerate(models):
            rank = Text(f"#{i+1}", font_size=22, color=AXIS_CLR)
            model_name = Text(name, font_size=22, color=color)
            bar = Rectangle(
                width=score / 100 * 5.0, height=0.28,
                fill_color=color, fill_opacity=0.6,
                stroke_width=0,
            )
            score_lbl = Text(f"{score}%", font_size=20, color=color)

            rank.move_to(LEFT * 5.5)
            model_name.move_to(LEFT * 3.5)
            bar.move_to(RIGHT * 0.5)
            bar.align_to(LEFT * 1.8, LEFT)
            score_lbl.next_to(bar, RIGHT, buff=0.15)

            row = VGroup(rank, model_name, bar, score_lbl)
            row.shift(DOWN * (0.6 * i - 0.5))
            rows.add(row)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.5)
            self.wait(0.2)

        self.wait(2.0)

        # Accuracy label
        acc_note = Text("Accuracy on MMLU benchmark",
                        font_size=18, color=AXIS_CLR)
        acc_note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(acc_note), run_time=0.4)
        self.wait(2.5)

        self.play(FadeOut(VGroup(header, rows, acc_note)), run_time=0.8)

    def play_question(self):
        """The central question: have you measured anything?"""
        q1 = Text("You've scored the models.", font_size=30, color=WHITE)
        q1.shift(UP * 0.8)
        self.play(FadeIn(q1, shift=DOWN * 0.1), run_time=0.8)
        self.wait(1.5)

        q2 = Text("But have you actually", font_size=30, color=WHITE)
        q3 = Text("measured", font_size=36, color=ACCENT, weight=BOLD,
                   slant=ITALIC)
        q4 = Text("anything?", font_size=30, color=WHITE)
        q_line = VGroup(q2, q3, q4).arrange(RIGHT, buff=0.15)
        q_line.next_to(q1, DOWN, buff=0.5)
        self.play(FadeIn(q2), run_time=0.5)
        self.play(FadeIn(q3, scale=1.2), run_time=0.7)
        self.play(FadeIn(q4), run_time=0.4)
        self.wait(3.0)

        self.play(FadeOut(VGroup(q1, q_line)), run_time=0.8)

    def play_thermometer(self):
        """Thermometer analogy: mercury height is a score, temperature is measurement."""
        # Left side: thermometer (score)
        therm_label = Text("Score", font_size=26, color=PAL[3])
        therm_label.shift(LEFT * 3 + UP * 2.2)

        # Simple thermometer visual
        bulb = Circle(radius=0.3, fill_color="#E8637A",
                      fill_opacity=0.8, stroke_color=WHITE,
                      stroke_width=1.5)
        bulb.shift(LEFT * 3 + DOWN * 1.5)
        tube = Rectangle(width=0.25, height=2.5, fill_color="#E8637A",
                         fill_opacity=0.6, stroke_color=WHITE,
                         stroke_width=1.5)
        tube.next_to(bulb, UP, buff=-0.15)
        thermometer = VGroup(bulb, tube)

        mercury_lbl = Text("Mercury height = 86%",
                           font_size=16, color=TEXT2)
        mercury_lbl.next_to(thermometer, RIGHT, buff=0.3)

        # Right side: measurement
        measure_label = Text("Measurement", font_size=26, color=PAL[0])
        measure_label.shift(RIGHT * 3 + UP * 2.2)

        temp_text = Text("T = 37.2\u00b0C", font_size=26,
                         color=PAL[0])
        temp_text.shift(RIGHT * 3 + UP * 0.3)

        causal = Text("Causal relationship:\nthermal energy \u2192 expansion",
                       font_size=16, color=TEXT2, line_spacing=1.3)
        causal.shift(RIGHT * 3 + DOWN * 0.8)

        # Arrow
        arrow = Arrow(LEFT * 0.8, RIGHT * 0.8, color=ACCENT,
                      stroke_width=2)
        arrow.shift(UP * 0.3)
        arrow_lbl = Text("requires theory", font_size=16, color=ACCENT)
        arrow_lbl.next_to(arrow, UP, buff=0.1)

        # Divider
        divider = DashedLine(UP * 2.5, DOWN * 2.5, color="#333333",
                             stroke_width=1, dash_length=0.1)

        self.play(FadeIn(therm_label), run_time=0.4)
        self.play(Create(thermometer), FadeIn(mercury_lbl), run_time=1.0)
        self.wait(1.5)

        self.play(Create(divider), run_time=0.3)
        self.play(FadeIn(measure_label), run_time=0.4)
        self.play(Write(temp_text), run_time=0.8)
        self.play(FadeIn(causal), run_time=0.5)
        self.wait(1.5)

        self.play(Create(arrow), FadeIn(arrow_lbl), run_time=0.6)
        self.wait(3.0)

        self.play(FadeOut(VGroup(
            therm_label, thermometer, mercury_lbl,
            measure_label, temp_text, causal,
            divider, arrow, arrow_lbl,
        )), run_time=0.8)

    def play_measurement_problem(self):
        """The measurement problem in AI."""
        line1 = Text("When GPT-4 scores 86% and Claude scores 84%,",
                     font_size=24, color=WHITE)
        line1.shift(UP * 1.0)
        self.play(FadeIn(line1, shift=DOWN * 0.1), run_time=0.8)
        self.wait(1.5)

        line2 = Text('what is the "thermal energy" behind those numbers?',
                     font_size=24, color=ACCENT)
        line2.next_to(line1, DOWN, buff=0.4)
        self.play(FadeIn(line2, shift=DOWN * 0.1), run_time=0.8)
        self.wait(5.0)  # narrator explains "thermal energy" behind numbers

        line3 = Text("This is the measurement problem in AI.",
                     font_size=28, color=WHITE, weight=BOLD)
        line3.next_to(line2, DOWN, buff=0.6)
        self.play(FadeIn(line3, shift=DOWN * 0.1), run_time=0.8)
        self.wait(2.0)

        line4 = Text("Psychologists solved it a century ago.",
                     font_size=22, color=TEXT2)
        line4.next_to(line3, DOWN, buff=0.4)
        self.play(FadeIn(line4), run_time=0.6)
        self.wait(5.0)  # narrator finishes: "introduces those tools"

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
