"""
AIMS Chapter 1 Animation #2: Response Matrix Sort
Shows how sorting a binary response matrix reveals diagonal structure.

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching --media_dir media/ch1 animations/ch1/response_matrix.py ResponseMatrixSort
"""

from manim import *
import numpy as np

# ── shared design tokens ────────────────────────────────────────────
ACCENT = "#FFD966"
BG = "#0f0f0f"
AXIS_CLR = "#888888"
TEXT2 = "#aaaaaa"
CELL_ON = "#5B8DEE"
CELL_OFF = "#1c1c1c"
CELL_BORDER = "#2a2a2a"

N_MODELS = 16
N_ITEMS = 32
CELL = 0.17  # cell side length


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class ResponseMatrixSort(Scene):
    def construct(self):
        self.camera.background_color = BG
        np.random.seed(42)

        # Generate Rasch data
        theta = np.random.normal(0, 1.0, N_MODELS)
        beta = np.random.normal(0, 1.2, N_ITEMS)
        prob = sigmoid(theta[:, None] - beta[None, :])
        Y = (np.random.random((N_MODELS, N_ITEMS)) < prob).astype(int)

        self.play_title()
        self.play_matrix_sort(Y, theta, beta)

    # ── title ───────────────────────────────────────────────────────
    def play_title(self):
        t = Text("The Response Matrix", font_size=44, color=WHITE,
                 weight=BOLD)
        st = Text("Sorting reveals hidden structure",
                  font_size=24, color=TEXT2)
        st.next_to(t, DOWN, buff=0.35)
        line = Line(LEFT * 2, RIGHT * 2, color=ACCENT, stroke_width=1.5)
        line.next_to(st, DOWN, buff=0.3)
        g = VGroup(t, st, line)
        self.play(FadeIn(t, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(st), Create(line), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(g, shift=UP * 0.4), run_time=0.7)

    # ── helpers ─────────────────────────────────────────────────────
    def build_grid(self, Y):
        """Create a VGroup of colored squares for the matrix."""
        rows, cols = Y.shape
        squares = []
        for i in range(rows):
            row = []
            for j in range(cols):
                color = CELL_ON if Y[i, j] == 1 else CELL_OFF
                sq = Square(
                    side_length=CELL,
                    fill_color=color, fill_opacity=1.0,
                    stroke_color=CELL_BORDER, stroke_width=0.3,
                )
                row.append(sq)
            squares.append(row)

        # arrange in grid
        grid = VGroup()
        for i, row in enumerate(squares):
            for j, sq in enumerate(row):
                sq.move_to(np.array([
                    j * CELL - (cols - 1) * CELL / 2,
                    -i * CELL + (rows - 1) * CELL / 2,
                    0.0,
                ]))
                grid.add(sq)
        return grid, squares

    def color_for(self, val):
        return CELL_ON if val == 1 else CELL_OFF

    # ── main sequence ───────────────────────────────────────────────
    def play_matrix_sort(self, Y, theta, beta):
        header = Text("Response Matrix", font_size=32, color=WHITE,
                      weight=BOLD)
        header.to_edge(UP, buff=0.35)
        formula = MathTex(
            r"Y \in \{0,1\}^{N \times M}",
            font_size=28, color=ACCENT,
        )
        formula.next_to(header, DOWN, buff=0.18)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.6)
        self.play(Write(formula), run_time=0.8)

        # ── show unsorted matrix ────────────────────────────────────
        grid, squares = self.build_grid(Y)
        grid.move_to(DOWN * 0.3)

        y_lbl = Text("Models", font_size=18, color=TEXT2)
        y_lbl.rotate(PI / 2).next_to(grid, LEFT, buff=0.2)
        x_lbl = Text("Questions", font_size=18, color=TEXT2)
        x_lbl.next_to(grid, DOWN, buff=0.2)

        self.play(FadeIn(grid), FadeIn(y_lbl), FadeIn(x_lbl), run_time=1.0)
        self.wait(3.0)

        note1 = Text("Unsorted: no obvious pattern",
                      font_size=20, color=TEXT2)
        note1.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(note1, shift=UP * 0.1), run_time=0.4)
        self.wait(2.0)
        self.play(FadeOut(note1), run_time=0.3)

        rows, cols = Y.shape

        # ── sort rows by sum score ──────────────────────────────────
        note2 = Text("Sort rows by model score (high ability on top)",
                      font_size=20, color=TEXT2)
        note2.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(note2, shift=UP * 0.1), run_time=0.4)

        row_order = np.argsort(Y.sum(axis=1))[::-1]
        Y_rsorted = Y[row_order]

        # Animate row permutation
        anims = []
        for new_i, old_i in enumerate(row_order):
            for j in range(cols):
                sq = squares[old_i][j]
                target_y = -new_i * CELL + (rows - 1) * CELL / 2
                target_x = j * CELL - (cols - 1) * CELL / 2
                target = grid.get_center() + np.array([target_x, target_y, 0])
                anims.append(sq.animate.move_to(target))
        self.play(*anims, run_time=2.0, rate_func=smooth)
        self.wait(1.5)
        self.play(FadeOut(note2), run_time=0.3)

        # Update color reference for column sort
        # rebuild squares mapping to match new row order
        squares_resorted = [[squares[old_i][j] for j in range(cols)]
                            for old_i in row_order]

        # ── sort columns by difficulty ──────────────────────────────
        note3 = Text("Sort columns by difficulty (easy questions on left)",
                      font_size=20, color=TEXT2)
        note3.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(note3, shift=UP * 0.1), run_time=0.4)

        col_order = np.argsort(Y_rsorted.sum(axis=0))[::-1]

        anims2 = []
        for i in range(rows):
            for new_j, old_j in enumerate(col_order):
                sq = squares_resorted[i][old_j]
                target_y = -i * CELL + (rows - 1) * CELL / 2
                target_x = new_j * CELL - (cols - 1) * CELL / 2
                target = grid.get_center() + np.array([target_x, target_y, 0])
                anims2.append(sq.animate.move_to(target))
        self.play(*anims2, run_time=2.0, rate_func=smooth)
        self.wait(1.5)
        self.play(FadeOut(note3), run_time=0.3)

        # ── highlight diagonal ──────────────────────────────────────
        Y_sorted = Y_rsorted[:, col_order]
        note4 = Text(
            "Diagonal structure emerges: ability and difficulty are revealed",
            font_size=20, color=TEXT2,
        )
        note4.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(note4, shift=UP * 0.1), run_time=0.5)

        # Draw a diagonal guide line across the grid
        grid_left = grid.get_center()[0] - (cols - 1) * CELL / 2
        grid_right = grid.get_center()[0] + (cols - 1) * CELL / 2
        grid_top = grid.get_center()[1] + (rows - 1) * CELL / 2
        grid_bot = grid.get_center()[1] - (rows - 1) * CELL / 2

        # Build a smooth boundary curve from the sorted matrix
        # For each row, find the column where the transition from 1→0 happens
        boundary_points = []
        for i in range(rows):
            row_data = Y_sorted[i]
            # find last 1
            ones = np.where(row_data == 1)[0]
            if len(ones) > 0:
                last_one = ones[-1]
            else:
                last_one = -1
            bx = grid_left + (last_one + 0.5) * CELL
            by = grid_top - i * CELL
            boundary_points.append(np.array([bx, by, 0]))

        if len(boundary_points) >= 3:
            boundary = VMobject(color=ACCENT, stroke_width=2.5)
            boundary.set_points_smoothly(boundary_points)
            self.play(Create(boundary), run_time=1.5)

        self.wait(9.0)  # narrator explains diagonal structure at length

        # ── Rasch overlay ───────────────────────────────────────────
        self.play(FadeOut(note4), run_time=0.3)
        note5 = Text(
            "This pattern is predicted by the Rasch model: "
            "P(Y=1) = \u03c3(\u03b8\u1d62 \u2212 \u03b2\u2c7c)",
            font_size=20, color=TEXT2,
        )
        note5.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(note5, shift=UP * 0.1), run_time=0.5)

        rasch_eq = MathTex(
            r"P(Y_{ij}=1) = \sigma(\theta_i - \beta_j)",
            font_size=30, color=ACCENT,
        )
        rasch_eq.next_to(grid, RIGHT, buff=0.5)
        self.play(Write(rasch_eq), run_time=1.0)
        self.wait(8.5)  # narrator: "That model is called the Rasch model"

        # ── clean up ────────────────────────────────────────────────
        all_objs = VGroup(header, formula, grid, y_lbl, x_lbl,
                          note5, rasch_eq)
        if len(boundary_points) >= 3:
            all_objs.add(boundary)
        self.play(FadeOut(all_objs), run_time=0.8)
