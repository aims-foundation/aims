"""
AIMS Chapter 1 — Section title cards & chapter bookends.
These short clips are stitched between the content animations.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch1 animations/ch1/section_titles.py <Scene>

Scenes (render in order):
    ChapterOpening
    Part1Title
    Part2Title
    Part3Title
    Part4Title
    Part5Title
    ChapterClosing
"""

from manim import *

# ── shared design tokens ────────────────────────────────────────────
ACCENT = "#FFD966"
BG = "#0f0f0f"
TEXT2 = "#aaaaaa"
PAL = ["#5B8DEE", "#45BF7C", "#F0A35C", "#E8637A", "#B07CD8"]


class _TitleBase(Scene):
    """Base class for consistent styling."""

    def construct(self):
        self.camera.background_color = BG

    def make_part_card(self, part_num, part_title, subtitle, color):
        """Animate a 'Part N' title card with accent line."""
        part_lbl = Text(
            f"Part {part_num}", font_size=22, color=TEXT2,
        )
        part_lbl.shift(UP * 0.8)

        title = Text(
            part_title, font_size=44, color=color, weight=BOLD,
        )
        title.next_to(part_lbl, DOWN, buff=0.3)

        line = Line(LEFT * 2, RIGHT * 2, color=ACCENT, stroke_width=1.5)
        line.next_to(title, DOWN, buff=0.3)

        sub = Text(subtitle, font_size=22, color=TEXT2)
        sub.next_to(line, DOWN, buff=0.3)

        # Animate in
        self.play(FadeIn(part_lbl, shift=DOWN * 0.1), run_time=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.7)
        self.play(Create(line), run_time=0.4)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)
        self.wait(1.5)

        # Animate out
        group = VGroup(part_lbl, title, line, sub)
        self.play(FadeOut(group), run_time=0.7)
        self.wait(0.3)


# ════════════════════════════════════════════════════════════════════
#  CHAPTER OPENING
# ════════════════════════════════════════════════════════════════════

class ChapterOpening(_TitleBase):
    def construct(self):
        super().construct()

        # Chapter number
        ch = Text("Chapter 1", font_size=24, color=TEXT2)
        ch.shift(UP * 1.2)

        # Title
        title = Text(
            "Foundations of Measurement",
            font_size=52, color=WHITE, weight=BOLD,
        )
        title.next_to(ch, DOWN, buff=0.35)

        # Accent line
        line = Line(LEFT * 3, RIGHT * 3, color=ACCENT, stroke_width=2)
        line.next_to(title, DOWN, buff=0.35)

        # Subtitle
        sub = Text(
            "AI Measurement Science",
            font_size=28, color=ACCENT,
        )
        sub.next_to(line, DOWN, buff=0.35)

        # Animate
        self.play(FadeIn(ch, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=1.0)
        self.play(Create(line), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.7)
        self.wait(2.5)
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.8,
        )
        self.wait(0.5)


# ════════════════════════════════════════════════════════════════════
#  PART TITLE CARDS
# ════════════════════════════════════════════════════════════════════

class Part1Title(_TitleBase):
    def construct(self):
        super().construct()
        self.make_part_card(
            1, "The Problem",
            "Scoring vs. measuring",
            PAL[0],
        )


class Part2Title(_TitleBase):
    def construct(self):
        super().construct()
        self.make_part_card(
            2, "The Models",
            "Item Response Theory: 1PL, 2PL, 3PL",
            PAL[1],
        )


class Part3Title(_TitleBase):
    def construct(self):
        super().construct()
        self.make_part_card(
            3, "Why Rasch Is Special",
            "Sufficiency and specific objectivity",
            PAL[2],
        )


class Part4Title(_TitleBase):
    def construct(self):
        super().construct()
        self.make_part_card(
            4, "Beyond Item Response",
            "Paired comparisons and network models",
            PAL[3],
        )


class Part5Title(_TitleBase):
    def construct(self):
        super().construct()
        self.make_part_card(
            5, "Multidimensionality",
            "Factor models and benchmark heterogeneity",
            PAL[4],
        )


# ════════════════════════════════════════════════════════════════════
#  CHAPTER CLOSING
# ════════════════════════════════════════════════════════════════════

class ChapterClosing(_TitleBase):
    def construct(self):
        super().construct()

        # Key takeaways
        heading = Text("Key Takeaways", font_size=38,
                       color=WHITE, weight=BOLD)
        heading.to_edge(UP, buff=0.8)
        self.play(FadeIn(heading, shift=DOWN * 0.15), run_time=1.0)
        self.wait(6.0)  # narrator introduces the key takeaways

        takeaways = [
            "Measurement requires more than scoring",
            "The Rasch model guarantees sufficiency\n"
            "    and specific objectivity",
            "Richer models (2PL, 3PL, factor) capture\n"
            "    complexity at the cost of those guarantees",
            "Benchmarks are rarely unidimensional\n"
            "    \u2014 mean scores can be misleading",
        ]

        prev = heading
        items = []
        for i, text in enumerate(takeaways):
            bullet = Text(
                f"{i+1}.", font_size=22, color=ACCENT, weight=BOLD,
            )
            body = Text(
                text, font_size=20, color=TEXT2, line_spacing=1.2,
            )
            row = VGroup(bullet, body).arrange(RIGHT, buff=0.2,
                                                aligned_edge=UP)
            row.next_to(prev, DOWN, buff=0.35, aligned_edge=LEFT)
            row.shift(RIGHT * 0.5)
            items.append(row)
            prev = row
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.5)
            self.wait(6.0)  # narrator explains each takeaway

        self.wait(22.0)  # narrator wraps up takeaways + philosophical discussion

        # Closing line — appears when narrator is about to say these words
        line = Line(LEFT * 3, RIGHT * 3, color=ACCENT, stroke_width=1.5)
        line.next_to(items[-1], DOWN, buff=0.5)

        closing = Text(
            "The tools have existed for a century.\n"
            "It's time we applied them to AI.",
            font_size=24, color=WHITE, line_spacing=1.4,
        )
        closing.next_to(line, DOWN, buff=0.4)

        self.play(Create(line), run_time=0.4)
        self.play(FadeIn(closing, shift=UP * 0.1), run_time=0.8)
        self.wait(5.0)  # narrator delivers the final line
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.5)
