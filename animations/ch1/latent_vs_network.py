"""
AIMS Chapter 1 Animation #6: Latent Variable vs. Network Models
Contrasts two explanations for why benchmark items correlate.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch1 animations/ch1/latent_vs_network.py LatentVsNetwork
"""

from manim import *
import numpy as np

# ── design tokens ───────────────────────────────────────────────────
ACCENT = "#FFD966"
BG = "#0f0f0f"
TEXT2 = "#aaaaaa"
PAL = ["#5B8DEE", "#45BF7C", "#F0A35C", "#E8637A", "#B07CD8"]
AXIS_CLR = "#888888"
EDGE_CLR = "#444444"
LATENT_CLR = PAL[0]
NETWORK_CLR = PAL[2]


class LatentVsNetwork(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.play_title()
        self.play_observation()
        self.play_latent_variable()
        self.play_network()
        self.play_side_by_side()
        self.play_takeaway()

    # ── title ───────────────────────────────────────────────────────
    def play_title(self):
        t = Text("Two Theories of Measurement", font_size=44,
                 color=WHITE, weight=BOLD)
        st = Text("Latent variable vs. network models",
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

    # ── helpers ─────────────────────────────────────────────────────
    def make_item_nodes(self, center, radius=1.6, n=5, color=TEXT2):
        """Create n item nodes arranged in a circle."""
        nodes = VGroup()
        labels = VGroup()
        angles = [PI / 2 + i * 2 * PI / n for i in range(n)]
        for i, angle in enumerate(angles):
            pos = center + radius * np.array([
                np.cos(angle), np.sin(angle), 0,
            ])
            circ = Circle(
                radius=0.3, fill_color=BG, fill_opacity=1,
                stroke_color=color, stroke_width=2,
            )
            circ.move_to(pos)
            lbl = MathTex(rf"X_{i+1}", font_size=22, color=color)
            lbl.move_to(pos)
            nodes.add(circ)
            labels.add(lbl)
        return nodes, labels

    def make_edges(self, nodes, color=EDGE_CLR, width=1.5):
        """Create edges between all pairs of nodes."""
        edges = VGroup()
        n = len(nodes)
        for i in range(n):
            for j in range(i + 1, n):
                edge = Line(
                    nodes[i].get_center(), nodes[j].get_center(),
                    color=color, stroke_width=width, stroke_opacity=0.5,
                )
                edges.add(edge)
        return edges

    # ── observation: items are correlated ───────────────────────────
    def play_observation(self):
        header = Text("Observation: Items are Correlated",
                      font_size=30, color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.6)

        center = DOWN * 0.3
        nodes, labels = self.make_item_nodes(center)
        edges = self.make_edges(nodes, color="#555555", width=1.5)

        self.play(*[Create(n) for n in nodes],
                  *[FadeIn(l) for l in labels], run_time=1.0)
        self.play(*[Create(e) for e in edges], run_time=1.2)

        question = Text("Why do items correlate?", font_size=24,
                        color=ACCENT)
        question.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(question, shift=UP * 0.1), run_time=0.6)
        self.wait(5.5)  # narrator poses the question: why do items correlate?

        self.obs_group = VGroup(header, nodes, labels, edges, question)
        self.play(FadeOut(self.obs_group), run_time=0.7)

    # ── latent variable explanation ─────────────────────────────────
    def play_latent_variable(self):
        header = Text("Explanation 1: Common Cause",
                      font_size=30, color=LATENT_CLR, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.6)

        center = DOWN * 0.5
        nodes, labels = self.make_item_nodes(center, radius=1.8)

        # Show items first
        self.play(*[Create(n) for n in nodes],
                  *[FadeIn(l) for l in labels], run_time=0.8)

        # Central latent node
        theta_node = Circle(
            radius=0.4, fill_color=LATENT_CLR, fill_opacity=0.3,
            stroke_color=LATENT_CLR, stroke_width=2.5,
        )
        theta_node.move_to(center)
        theta_lbl = MathTex(r"\theta", font_size=30, color=LATENT_CLR)
        theta_lbl.move_to(center)

        self.play(Create(theta_node), FadeIn(theta_lbl), run_time=0.8)

        # Arrows from θ to each item
        arrows = VGroup()
        for node in nodes:
            arr = Arrow(
                theta_node.get_center(),
                node.get_center(),
                color=LATENT_CLR, stroke_width=2,
                buff=0.4,
                max_tip_length_to_length_ratio=0.12,
            )
            arrows.add(arr)
        self.play(*[Create(a) for a in arrows], run_time=1.0)

        note = Text(
            "A hidden factor \u03b8 causes all responses",
            font_size=20, color=TEXT2,
        )
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(5.0)  # narrator explains common cause explanation

        # Remove one item — others unaffected
        self.play(FadeOut(note), run_time=0.3)
        remove_note = Text(
            "Remove item X\u2083 \u2014 other correlations unchanged",
            font_size=20, color=TEXT2,
        )
        remove_note.to_edge(DOWN, buff=0.25)

        self.play(
            FadeOut(nodes[2]), FadeOut(labels[2]),
            FadeOut(arrows[2]),
            FadeIn(remove_note),
            run_time=0.8,
        )
        self.wait(5.5)  # narrator: removing item doesn't affect others

        self.latent_group = VGroup(
            header, nodes, labels, theta_node, theta_lbl,
            arrows, remove_note,
        )
        self.play(FadeOut(self.latent_group), run_time=0.7)

    # ── network explanation ─────────────────────────────────────────
    def play_network(self):
        header = Text("Explanation 2: Direct Connections",
                      font_size=30, color=NETWORK_CLR, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.6)

        center = DOWN * 0.5
        nodes, labels = self.make_item_nodes(center, radius=1.8,
                                             color=NETWORK_CLR)

        self.play(*[Create(n) for n in nodes],
                  *[FadeIn(l) for l in labels], run_time=0.8)

        # Direct edges with varying thickness
        np.random.seed(12)
        edges = VGroup()
        n = len(nodes)
        for i in range(n):
            for j in range(i + 1, n):
                w = np.random.uniform(0.5, 3.0)
                edge = Line(
                    nodes[i].get_center(), nodes[j].get_center(),
                    color=NETWORK_CLR, stroke_width=w,
                    stroke_opacity=0.6,
                )
                edges.add(edge)
        self.play(*[Create(e) for e in edges], run_time=1.2)

        note = Text(
            "Items directly cause each other \u2014 no hidden factor",
            font_size=20, color=TEXT2,
        )
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(5.0)  # narrator explains direct connections model

        # Remove item 3 — some edges disappear, correlations weaken
        self.play(FadeOut(note), run_time=0.3)
        remove_note = Text(
            "Remove X\u2083 \u2014 some connections lost, "
            "correlations weaken",
            font_size=20, color=TEXT2,
        )
        remove_note.to_edge(DOWN, buff=0.25)

        # Find edges connected to node 2
        edges_to_remove = VGroup()
        edge_idx = 0
        for i in range(n):
            for j in range(i + 1, n):
                if i == 2 or j == 2:
                    edges_to_remove.add(edges[edge_idx])
                edge_idx += 1

        # Remaining edges get thinner (weakened)
        remaining_anims = []
        edge_idx = 0
        for i in range(n):
            for j in range(i + 1, n):
                if i != 2 and j != 2:
                    remaining_anims.append(
                        edges[edge_idx].animate.set_stroke(opacity=0.3)
                    )
                edge_idx += 1

        self.play(
            FadeOut(nodes[2]), FadeOut(labels[2]),
            FadeOut(edges_to_remove),
            *remaining_anims,
            FadeIn(remove_note),
            run_time=1.0,
        )
        self.wait(5.5)  # narrator: removing item weakens remaining connections

        self.network_group = VGroup(
            header, nodes, labels, edges, remove_note,
        )
        self.play(FadeOut(self.network_group), run_time=0.7)

    # ── side-by-side comparison ─────────────────────────────────────
    def play_side_by_side(self):
        header = Text("Side-by-Side Comparison", font_size=30,
                      color=WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.5)

        # Left: latent variable
        left_center = LEFT * 3.2 + UP * 0.3
        l_nodes, l_labels = self.make_item_nodes(
            left_center, radius=1.1, n=4, color=LATENT_CLR,
        )
        l_theta = Circle(
            radius=0.3, fill_color=LATENT_CLR, fill_opacity=0.3,
            stroke_color=LATENT_CLR, stroke_width=2,
        )
        l_theta.move_to(left_center)
        l_theta_lbl = MathTex(r"\theta", font_size=24, color=LATENT_CLR)
        l_theta_lbl.move_to(left_center)

        l_arrows = VGroup()
        for node in l_nodes:
            arr = Arrow(
                l_theta.get_center(), node.get_center(),
                color=LATENT_CLR, stroke_width=1.5, buff=0.32,
                max_tip_length_to_length_ratio=0.15,
            )
            l_arrows.add(arr)

        l_title = Text("Latent Variable", font_size=20,
                       color=LATENT_CLR, weight=BOLD)
        l_title.next_to(VGroup(l_nodes, l_theta), DOWN, buff=0.3)

        # Right: network
        right_center = RIGHT * 3.2 + UP * 0.3
        r_nodes, r_labels = self.make_item_nodes(
            right_center, radius=1.1, n=4, color=NETWORK_CLR,
        )

        np.random.seed(42)
        r_edges = VGroup()
        for i in range(4):
            for j in range(i + 1, 4):
                w = np.random.uniform(0.8, 2.5)
                edge = Line(
                    r_nodes[i].get_center(), r_nodes[j].get_center(),
                    color=NETWORK_CLR, stroke_width=w, stroke_opacity=0.6,
                )
                r_edges.add(edge)

        r_title = Text("Network", font_size=20,
                       color=NETWORK_CLR, weight=BOLD)
        r_title.next_to(VGroup(r_nodes), DOWN, buff=0.3)

        # Divider
        divider = DashedLine(
            UP * 2.5, DOWN * 2.5,
            color="#333333", stroke_width=1, dash_length=0.1,
        )

        # Show left
        self.play(
            *[Create(n) for n in l_nodes],
            *[FadeIn(l) for l in l_labels],
            Create(l_theta), FadeIn(l_theta_lbl),
            *[Create(a) for a in l_arrows],
            FadeIn(l_title),
            Create(divider),
            run_time=1.2,
        )

        # Show right
        self.play(
            *[Create(n) for n in r_nodes],
            *[FadeIn(l) for l in r_labels],
            *[Create(e) for e in r_edges],
            FadeIn(r_title),
            run_time=1.2,
        )

        # Comparison table
        table_lines = VGroup(
            Text("Common cause     vs.  Direct connections",
                 font_size=18, color=TEXT2),
            Text("Removing an item: no effect  vs.  weakens others",
                 font_size=18, color=TEXT2),
            Text("\u03b8 exists and causes responses  vs.  "
                 "\u03b8 is just a summary",
                 font_size=18, color=TEXT2),
        )
        table_lines.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        table_lines.to_edge(DOWN, buff=0.2)

        for tl in table_lines:
            self.play(FadeIn(tl, shift=UP * 0.05), run_time=0.5)
        self.wait(7.0)  # narrator walks through the side-by-side comparison

        everything = VGroup(
            header, l_nodes, l_labels, l_theta, l_theta_lbl,
            l_arrows, l_title, r_nodes, r_labels, r_edges, r_title,
            divider, table_lines,
        )
        self.play(FadeOut(everything), run_time=0.7)

    # ── takeaway ────────────────────────────────────────────────────
    def play_takeaway(self):
        q = Text(
            "Are AI capabilities caused by a common factor,",
            font_size=26, color=WHITE,
        )
        q2 = Text(
            "or are they a network of distinct skills?",
            font_size=26, color=WHITE,
        )
        q.shift(UP * 0.5)
        q2.next_to(q, DOWN, buff=0.3)

        both = Text(
            "Both views may be partially correct.",
            font_size=22, color=TEXT2,
        )
        both.next_to(q2, DOWN, buff=0.5)

        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(q2, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(both), run_time=0.5)
        self.wait(7.0)  # narrator: both views may be partially correct
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
