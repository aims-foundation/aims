# How to Create AIMS Chapter Videos

Step-by-step guide for producing 3Blue1Brown-style animated videos for each chapter of the AIMS textbook. Based on the workflow used for Chapter 1.

---

## Overview

Each chapter video is assembled from:

1. **Content animations** — Manim scenes illustrating key concepts (one `.py` file per concept)
2. **Section title cards** — Short branded interstitials (chapter opening, part titles, closing)
3. **A narration script** — Timestamped text with `[ANIMATION]` cues for syncing
4. **A stitch script** — ffmpeg pipeline that concatenates everything with crossfades

```
animations/
├── HOWTO.md                  ← this file
├── animation.md              ← Chapter 1 animation plan
├── script.md                 ← Chapter 1 narration script
├── stitch.sh                 ← ffmpeg stitching (edit CLIPS array per chapter)
├── section_titles.py         ← Chapter 1 title cards
├── icc_models.py             ← Content animation
├── response_matrix.py        ← Content animation
├── ...                       ← etc.
└── chapter1.mp4              ← Final output
```

---

## 1. Environment Setup

### Prerequisites

- **Python 3.10+** with Manim Community Edition
- **ffmpeg** (for rendering and stitching)
- **LaTeX** (for MathTex; usually bundled with Manim)

### Installation (on the Stanford cluster)

```bash
# Activate conda with system libs (pango, cairo, ffmpeg)
export PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH"

# Install Manim (one-time)
conda install -y -c conda-forge pango cairo pkg-config ffmpeg
pip install manim
```

### Verify

```bash
PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
  manim -qh --disable_caching -o /dev/null - <<'PY'
from manim import *
class Test(Scene):
    def construct(self):
        self.play(FadeIn(Text("OK")))
PY
```

---

## 2. Design System

All chapter videos share a consistent visual identity. Use these tokens in every animation file.

### Colors

```python
# ── design tokens (copy to top of every animation file) ────────
ACCENT  = "#FFD966"        # gold — formulas, highlights, accent lines
BG      = "#0f0f0f"        # near-black background
TEXT2   = "#aaaaaa"        # secondary / muted text
AXIS_CLR = "#888888"       # axis lines, tick marks
PAL = [                    # 5-color palette for data series
    "#5B8DEE",             # blue
    "#45BF7C",             # green
    "#F0A35C",             # orange
    "#E8637A",             # red-pink
    "#B07CD8",             # purple
]
```

### Typography

- **Titles:** `font_size=44`, `color=WHITE`, `weight=BOLD`
- **Subtitles:** `font_size=24`, `color=TEXT2`
- **Formulas:** `MathTex(..., color=ACCENT)` at `font_size=32`
- **Body text / notes:** `font_size=20–22`, `color=TEXT2`
- **Source line:** `font_size=18`, `color=ManimColor("#444444")`

### Layout Rules

- Set `self.camera.background_color = BG` in every `construct()`
- Pin headers at `to_edge(UP, buff=0.35)` or `to_edge(UP, buff=0.4)`
- Position axes at `center=DOWN * 0.55` to leave headroom
- Bottom notes at `to_edge(DOWN, buff=0.25)`
- Accent lines: `Line(LEFT * 2.5, RIGHT * 2.5, color=ACCENT, stroke_width=1.5)`

### Rendering Target

- **Resolution:** 1080p60 (`-qh` flag = 1920×1080 at 60fps)
- **Codec:** H.264 (Manim default)

---

## 3. Planning a New Chapter

### Step 1: Identify animation candidates

Read through the chapter `.qmd` file and list concepts that benefit from animation:

- Mathematical relationships (curves, surfaces, parameter spaces)
- Step-by-step algebra (cancellations, derivations)
- Sorting / reordering operations
- Before/after comparisons
- Simulations with dynamics over time

Aim for **5–8 content animations** per chapter.

### Step 2: Create an animation plan

Create `animations/chapterN_plan.md` (see `animation.md` for the Chapter 1 example). For each animation, specify:

- **File name** and **Scene name**
- **Target duration** (30–60s each)
- **Storyboard** with acts, content description, and timing
- **Key Manim elements** to use

### Step 3: Write the narration script

Create `animations/chapterN_script.md` (see `script.md` for Chapter 1). Include:

- Full narrator text organized by Part / Section
- `[ANIMATION: file.py — SceneName]` cues marking when each animation plays
- `Cue:` lines for specific moments within an animation
- `[pause]` (~1s) and `[beat]` (~0.5s) pacing markers
- An **Animation-Scene Mapping** table at the end
- A **batch render command** at the end

---

## 4. Building Animations

### File structure

Each animation lives in its own `.py` file with a single Scene class:

```python
"""
AIMS Chapter N Animation: <Title>
<Description>

Run with:
    PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
    manim -qh --disable_caching animations/<file>.py <SceneName>
"""

from manim import *
import numpy as np

# ── design tokens ────────────────────────────────────────────
ACCENT  = "#FFD966"
BG      = "#0f0f0f"
TEXT2   = "#aaaaaa"
PAL     = ["#5B8DEE", "#45BF7C", "#F0A35C", "#E8637A", "#B07CD8"]
AXIS_CLR = "#888888"


class MyScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.play_title()
        self.play_main_content()
        self.play_takeaway()

    def play_title(self):
        t = Text("Animation Title", font_size=44,
                 color=WHITE, weight=BOLD)
        st = Text("Subtitle here", font_size=24, color=TEXT2)
        st.next_to(t, DOWN, buff=0.35)
        line = Line(LEFT * 2.5, RIGHT * 2.5, color=ACCENT,
                    stroke_width=1.5)
        line.next_to(st, DOWN, buff=0.3)
        g = VGroup(t, st, line)
        self.play(FadeIn(t, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(st), Create(line), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(g, shift=UP * 0.4), run_time=0.7)

    def play_main_content(self):
        ...  # your acts here

    def play_takeaway(self):
        ...  # closing message + source line
```

### Common patterns

**Axes with curves:**
```python
axes = Axes(
    x_range=[-4, 4, 1], y_range=[0, 1.05, 0.25],
    x_length=9, y_length=4.2,
    axis_config={"color": AXIS_CLR, "stroke_width": 1.5},
)
axes.move_to(DOWN * 0.55)
labels = axes.get_axis_labels(
    MathTex(r"\theta", color=TEXT2),
    MathTex(r"P", color=TEXT2),
)
```

**Formula with header:**
```python
header = Text("The Rasch Model (1PL)", font_size=30,
              color=WHITE, weight=BOLD)
header.to_edge(UP, buff=0.35)
formula = MathTex(
    r"P(Y_{ij}=1) = \sigma(\theta_i - \beta_j)",
    font_size=32, color=ACCENT,
)
formula.next_to(header, DOWN, buff=0.25)
```

**Animated parameter change (ValueTracker):**
```python
param = ValueTracker(1.0)
curve = always_redraw(lambda: axes.plot(
    lambda x: sigmoid(param.get_value() * x),
    color=PAL[0],
))
self.play(param.animate.set_value(2.5), run_time=2.0)
```

### MathTex gotchas

- **Keep each MathTex string self-contained.** Manim splits multiple string arguments into separate LaTeX fragments. An unmatched `\frac{...` in one string will cause a LaTeX error.
- **Use `\mathrm{}` instead of `\text{}` inside math mode** to avoid font issues.
- **Avoid `_` in `\text{}`** — use `\mathrm{odds}_{i}` not `\text{odds}_i`.

### Render a single scene

```bash
PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH" \
  manim -qh --disable_caching animations/<file>.py <SceneName>
```

Output goes to `media/videos/<file>/1080p60/<SceneName>.mp4`.

### Render all content animations (batch)

```bash
PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH"

for scene in \
  "file1.py Scene1" \
  "file2.py Scene2" \
  "file3.py Scene3"; do
  set -- $scene
  manim -qh --disable_caching animations/$1 $2
done
```

---

## 5. Section Title Cards

Each chapter needs a set of title card scenes for interstitials. Create a file like `animations/chapterN_titles.py` following the pattern in `section_titles.py`.

### Required scenes

| Scene | Purpose |
|-------|---------|
| `ChapterOpening` | Chapter number, title, subtitle, source URL |
| `Part1Title` ... `PartNTitle` | One per major section |
| `ChapterClosing` | Key takeaways list + closing quote + source |

### Base class pattern

```python
class _TitleBase(Scene):
    def construct(self):
        self.camera.background_color = BG

    def make_part_card(self, part_num, part_title, subtitle, color):
        part_lbl = Text(f"Part {part_num}", font_size=22, color=TEXT2)
        part_lbl.shift(UP * 0.8)
        title = Text(part_title, font_size=44, color=color, weight=BOLD)
        title.next_to(part_lbl, DOWN, buff=0.3)
        line = Line(LEFT * 2, RIGHT * 2, color=ACCENT, stroke_width=1.5)
        line.next_to(title, DOWN, buff=0.3)
        sub = Text(subtitle, font_size=22, color=TEXT2)
        sub.next_to(line, DOWN, buff=0.3)

        self.play(FadeIn(part_lbl, shift=DOWN * 0.1), run_time=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.7)
        self.play(Create(line), run_time=0.4)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(VGroup(part_lbl, title, line, sub)), run_time=0.7)
        self.wait(0.3)
```

### Render all title cards

```bash
PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH"

for scene in ChapterOpening Part1Title Part2Title Part3Title \
             Part4Title Part5Title ChapterClosing; do
  manim -qh --disable_caching animations/chapterN_titles.py $scene
done
```

---

## 6. Stitching the Final Video

### Edit the clip list

Open `animations/stitch.sh` and update the `CLIPS` array and `OUT` path for your chapter:

```bash
OUT="$ROOT/animations/chapterN.mp4"

CLIPS=(
    "chapterN_titles/1080p60/ChapterOpening.mp4"

    "chapterN_titles/1080p60/Part1Title.mp4"
    "content_anim_1/1080p60/Scene1.mp4"

    "chapterN_titles/1080p60/Part2Title.mp4"
    "content_anim_2/1080p60/Scene2.mp4"
    # ... etc.

    "chapterN_titles/1080p60/ChapterClosing.mp4"
)
```

The paths are relative to `media/videos/`.

### Run the stitch

```bash
cd /lfs/skampere2/0/sttruong/aims

# Crossfade version (0.5s fades between clips)
bash animations/stitch.sh

# Hard-cut version (faster, lossless)
bash animations/stitch.sh --simple
```

### Output

The script:
1. Validates all clips exist
2. Concatenates them with crossfade transitions (or hard cuts)
3. Outputs `animations/chapterN.mp4`
4. Prints a segment duration breakdown

---

## 7. Adding Background Music

The stitch script supports a `--music` flag to mix a background track under the video.

### Where to find royalty-free classical music

| Source | License | Notes |
|--------|---------|-------|
| [Musopen](https://musopen.org/) | Public domain / CC | Classical recordings performed specifically for free distribution. High quality. |
| [IMSLP](https://imslp.org/) | Public domain | Huge archive; check individual recording licenses (some are CC, some PD) |
| [Free Music Archive](https://freemusicarchive.org/) | CC | Search by genre "Classical". Filter by license. |
| [Pixabay Music](https://pixabay.com/music/) | Pixabay License (free) | Search "classical piano", "orchestral". No attribution required. |
| [YouTube Audio Library](https://studio.youtube.com/channel/audio) | Free to use | Filter by genre and mood. Some require attribution. |

Good pieces for math/science videos: Bach (Cello Suites, Goldberg Variations), Debussy (Clair de Lune, Arabesques), Satie (Gymnopedies), Chopin (Nocturnes).

### Usage

```bash
# Download a track (example: from Musopen or Pixabay)
# Place it in animations/music/

# Stitch with background music (default volume: 12%)
bash animations/stitch.sh --music animations/music/bach_cello_suite.mp3

# Adjust volume (0.0 = silent, 1.0 = full volume)
bash animations/stitch.sh --music animations/music/track.mp3 --music-volume 0.08

# Works with both modes
bash animations/stitch.sh --simple --music animations/music/track.mp3
```

The script automatically:
- Fades the music in over 2 seconds at the start
- Fades the music out over 3 seconds at the end
- Trims the music to match the video duration
- Encodes audio as AAC 192kbps

### Recommended volume levels

| Scenario | Volume |
|----------|--------|
| Music only (no narration) | `0.10–0.15` |
| Music under narration | `0.05–0.08` |
| Music during transitions only | Edit in a video editor |

---

## 8. Adding Narration

The animations are silent by default. To produce a narrated video:

1. **Record narration** following `chapterN_script.md`, using `[ANIMATION]` and `Cue:` markers for timing
2. **Sync in a video editor** (DaVinci Resolve, Premiere, or ffmpeg) — align narration audio to the corresponding animation segments
3. Alternatively, use TTS (e.g., ElevenLabs) to generate narration from the script
4. If using both narration and background music, lower the music volume to `0.05–0.08` so it doesn't compete with the voice

---

## 9. Checklist for a New Chapter

```
[ ] Read chapter .qmd and identify 5-8 animation candidates
[ ] Create animations/chapterN_plan.md with storyboards
[ ] Write animations/chapterN_script.md with narration + cues
[ ] Create content animation .py files (one per concept)
[ ] Render and review each animation individually
[ ] Create animations/chapterN_titles.py with title card scenes
[ ] Render all title cards
[ ] Update CLIPS array in stitch.sh (or create chapterN_stitch.sh)
[ ] Run stitch.sh to produce chapterN.mp4
[ ] Review final video, adjust timing/content as needed
[ ] (Optional) Add background music: --music animations/music/<track>.mp3
[ ] (Optional) Record/generate narration and sync
```

---

## 10. Chapter 1 Reference

Chapter 1 produced **14 clips** (7 content + 7 title cards) totaling ~5 minutes of animation:

| # | File | Scene | Duration |
|---|------|-------|----------|
| 1 | `section_titles.py` | `ChapterOpening` | ~6s |
| 2 | `section_titles.py` | `Part1Title` | ~5s |
| 3 | `response_matrix.py` | `ResponseMatrixSort` | ~42s |
| 4 | `section_titles.py` | `Part2Title` | ~5s |
| 5 | `icc_models.py` | `ICCModels` | ~66s |
| 6 | `section_titles.py` | `Part3Title` | ~5s |
| 7 | `sufficiency.py` | `Sufficiency` | ~37s |
| 8 | `specific_objectivity.py` | `SpecificObjectivity` | ~43s |
| 9 | `section_titles.py` | `Part4Title` | ~5s |
| 10 | `elo_dynamics.py` | `EloDynamics` | ~40s |
| 11 | `latent_vs_network.py` | `LatentVsNetwork` | ~38s |
| 12 | `section_titles.py` | `Part5Title` | ~5s |
| 13 | `factor_model.py` | `FactorModel` | ~42s |
| 14 | `section_titles.py` | `ChapterClosing` | ~18s |

---

## Tips

- **Iterate fast:** Use `-ql` (480p15) for quick previews, `-qh` (1080p60) for final renders
- **Disable caching:** Always use `--disable_caching` to avoid stale frames
- **Keep scenes modular:** One concept per file, one Scene class per file. This makes re-rendering fast.
- **Test LaTeX early:** MathTex errors are the most common failure. Render a minimal scene with your formulas first.
- **Consistent timing:** Title cards ~5s, content acts 6-10s each, total content animation 30-65s
- **Fade everything:** Use `FadeIn`/`FadeOut` with slight `shift` for polish. Avoid hard cuts within a scene.
