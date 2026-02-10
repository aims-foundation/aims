# Foundations of Measurement — Video Script

**Chapter 1 of AI Measurement Science (AIMS)**
Target length: ~12 minutes
Format: Narrated animation (3Blue1Brown style)

---

## Production Notes

- **Animations** are in `animations/*.py` (Manim, 1080p60). Each scene listed
  below corresponds to a rendered `.mp4` in `media/videos/`.
- **Narration** should be recorded separately and synced in a video editor.
  The `[ANIMATION]` cues mark when each Manim scene plays.
- **Pacing markers:** `[pause]` = ~1 s beat. `[beat]` = ~0.5 s.

---

## PART 1 — THE PROBLEM (~2:30)

### 1.1 Opening Hook

**NARRATOR:**

Imagine you've just evaluated a hundred language models on a thousand
benchmark questions. You compute each model's accuracy, rank them from best to
worst, and publish a leaderboard.

[beat]

But here's a question that should bother you: have you actually *measured*
anything?

[pause]

You've certainly *scored* the models — you assigned numbers to them. But
measurement, in the scientific sense, requires something more. It requires
that those numbers correspond to some underlying property — a *latent
construct* — in a principled way.

Think of temperature. The height of mercury in a thermometer is a score.
We trust it as a *measurement* because we understand the causal relationship
between thermal energy and mercury expansion. When GPT-4 scores 86% on MMLU
and Claude scores 84%, what is the "thermal energy" behind those numbers?

[pause]

This is the measurement problem in AI. And it turns out, psychologists and
educators solved it — or at least developed very good tools for it — over a
century ago. This chapter introduces those tools.

### 1.2 The Response Matrix

**NARRATOR:**

Everything starts with the *response matrix*.

> [ANIMATION: `response_matrix.py` — `ResponseMatrixSort`]
> Cue: Show the random grid appear

Each row is a model. Each column is a benchmark question. Each cell is zero or
one — wrong or right. The naive approach just averages across each row and
ranks models by accuracy.

But watch what happens when we sort.

> Cue: Row sort animation

We sort the rows by total score — strongest models on top.

> Cue: Column sort animation

And the columns by difficulty — easiest questions on the left.

> Cue: Diagonal reveal

A diagonal structure appears. High-ability models answer most questions right.
Easy questions get answered by almost everyone. This isn't guaranteed — it
depends on the data satisfying certain assumptions — but when it appears, it
suggests that a simple probabilistic model might describe the data well.

[pause]

That model is called the *Rasch model*.

---

## PART 2 — THE MODELS (~4:00)

### 2.1 The Rasch Model (1PL)

**NARRATOR:**

> [ANIMATION: `icc_models.py` — `ICCModels`]
> Cue: Act 1 — Rasch header + formula

The Rasch model says: the probability that model i answers question j
correctly is the logistic sigmoid of the difference between the model's
ability theta-i and the question's difficulty beta-j.

> Cue: First ICC curve draws

This S-shaped curve is called the *Item Characteristic Curve*. When theta
equals beta, the probability is exactly one half — a coin flip. As ability
increases, the probability rises toward one.

> Cue: Remaining ICC curves appear

Different items have different difficulties, but notice — every curve has
exactly the same shape. They're just shifted left or right on the ability
axis. This is the Rasch model's defining feature: all items discriminate
equally.

### 2.2 The 2PL Model

**NARRATOR:**

> Cue: Act 2 — 2PL header + formula

But what if some questions are better at distinguishing strong models from
weak ones? The two-parameter logistic model adds a *discrimination*
parameter, a-j, which controls the slope of the curve.

> Cue: Discrimination morphing animation (a = 1 → 2.5 → 0.3)

Watch the curve. High discrimination — steep slope — means a small
difference in ability produces a big change in the probability of getting it
right. Low discrimination — flat slope — means the question barely
distinguishes between models at all.

> Cue: Multiple 2PL curves appear

Now items don't just differ in *where* the curve sits — they differ in
*how sharply* it rises.

### 2.3 The 3PL Model

**NARRATOR:**

> Cue: Act 3 — 3PL header + formula

One more refinement. On a multiple-choice test, even a model that knows
nothing can guess. The three-parameter model adds a *guessing* parameter,
c-j, which sets a floor — a minimum probability of getting the answer right.

> Cue: Lower asymptote lifting (c = 0 → 0.25 → 0.50)

For a four-option multiple-choice question, we'd expect a floor around 0.25.
For true-false, around 0.50. The curve can never drop below this floor.

> Cue: Side-by-side comparison (Act 4)

Here are all three models together. The 1PL is the simplest — one parameter
per item. The 2PL adds a slope. The 3PL adds a floor. Each parameter tells
you something different about the question.

> Cue: Closing card (Act 5)

Beta tells you how hard it is. A tells you how sharply it discriminates.
C tells you whether you can guess the answer.

---

## PART 3 — WHY RASCH IS SPECIAL (~3:00)

### 3.1 Sufficiency of Sum Scores

**NARRATOR:**

Now, here's a deep question. When you compute a model's accuracy — the
total number of correct answers — are you throwing away information?

> [ANIMATION: `sufficiency.py` — `Sufficiency`]
> Cue: Three patterns appear

Consider these three response patterns. All three have a sum score of three
out of five. But the *patterns* are different. Does the pattern matter, or
does the sum score tell you everything you need to know?

> Cue: Rasch merge animation

Under the Rasch model, the answer is remarkable. The sum score is a
*sufficient statistic* for ability. This means: once you know the total,
knowing *which* questions were answered correctly adds zero additional
information about the model's ability. All three patterns are equally likely.

> Cue: 2PL break animation

But under the 2PL model — where items have different discriminations —
this breaks down. The pattern where the high-discrimination items are
answered correctly is more informative. The sum score is no longer sufficient.
The pattern matters.

This is why the choice of model has consequences. If you trust accuracy as
your metric, you're implicitly assuming Rasch. If Rasch doesn't hold, you
should be weighting some questions more than others.

### 3.2 Specific Objectivity

**NARRATOR:**

> [ANIMATION: `specific_objectivity.py` — `SpecificObjectivity`]
> Cue: Setup — two models on number line

The other property that makes Rasch special is *specific objectivity*. This
is arguably Georg Rasch's deepest contribution — not the mathematical model
itself, but this philosophical principle.

> Cue: Odds ratio algebra

Here's the idea. Take two models, i and k, and compute the odds ratio — how
much more likely is model i to answer correctly, compared to model k?

> Cue: Beta cancellation

Watch the item difficulty, beta-j. It appears in the numerator *and* the
denominator... and it cancels completely.

> Cue: Result box

The odds ratio depends only on the *difference* in abilities. It doesn't
matter which question you use to make the comparison.

> Cue: Visual proof — all bars equal

This is specific objectivity: person comparisons are *independent* of the
items used. You could compare two models on any subset of questions, and —
if the Rasch model holds — you'd get the same answer.

> Cue: 2PL counterexample — bars differ

Under the 2PL, this breaks. The comparison *depends* on which questions
you pick. High-discrimination items amplify the difference; low-discrimination
items shrink it.

This is why Rasch is sometimes called *the* measurement model. It's the only
model where comparisons are truly item-free — just like comparing two
temperatures doesn't depend on whether you use a mercury or alcohol
thermometer.

---

## PART 4 — BEYOND ITEM RESPONSE (~2:00)

### 4.1 Paired Comparisons: Elo and Bradley-Terry

**NARRATOR:**

Not all evaluation data comes as correct-or-incorrect. Sometimes we have
*pairwise comparisons*: which model is better?

> [ANIMATION: `elo_dynamics.py` — `EloDynamics`]
> Cue: BT formula

The Bradley-Terry model says: the probability that model i beats model j is
the sigmoid of the difference in their strengths. Sound familiar? It's the
same math as Rasch — but instead of a model answering a question, two
models compete against each other.

> Cue: Elo arena simulation

The Elo rating system turns this into an online algorithm. Models start with
equal ratings. After each match, the winner's rating goes up and the loser's
goes down — by an amount that depends on how surprising the outcome was. An
upset causes a bigger swing.

> Cue: Fast-forward convergence

After many matches, the ratings converge toward true strengths.

This is exactly how the Chatbot Arena works. When a user prefers one model's
response over another, it's a "match." The Elo ratings that result implement
the same mathematics that Thurstone proposed in 1927 for measuring subjective
preferences.

### 4.2 What Causes the Correlations?

**NARRATOR:**

All the models we've seen so far share an assumption: there's a hidden
variable — ability, strength, quality — that *causes* the observed
responses. But there's an alternative.

> [ANIMATION: `latent_vs_network.py` — `LatentVsNetwork`]
> Cue: Observation — correlated items

Benchmark items are correlated. Models that answer one question correctly
tend to answer similar questions correctly. Why?

> Cue: Latent variable explanation

The *latent variable* view says: because a hidden factor, theta, causes all
the responses. The correlations are a byproduct of this common cause. Remove
one item, and nothing changes — the others still share the same factor.

> Cue: Network explanation

The *network* view says: because the items directly influence each other.
Knowing one skill helps with another. There's no hidden factor — the
correlations arise from these direct connections. Remove an item, and the
remaining correlations can actually change.

> Cue: Side-by-side comparison

These aren't just two parameterizations of the same thing — they make
different claims about the structure of the world. And for AI evaluation,
the question is real: are capabilities like reasoning, knowledge, and
language understanding driven by a common factor? Or are they a network of
distinct but connected skills?

Both views may be partially correct.

---

## PART 5 — MULTIDIMENSIONALITY (~1:30)

### 5.1 Factor Models and Benchmark Heterogeneity

**NARRATOR:**

> [ANIMATION: `factor_model.py` — `FactorModel`]
> Cue: One-factor model

If a benchmark truly measures one thing, a single-factor model should
describe it well. Every item loads on the same factor, and the model's
accuracy captures everything.

> Cue: Two-factor model

But in practice, benchmarks often measure multiple things. A question might
test reasoning, or factual recall, or language understanding — and these
aren't the same capability. A two-factor model lets items load on different
factors with different strengths.

> Cue: Loading space scatter plot

When we plot items in their *loading space*, clusters emerge. Each cluster
represents a different capability that the benchmark is secretly measuring.
Most benchmarks, it turns out, are not homogeneous.

> Cue: Two models, same score, different profiles

And this leads to a striking consequence. Two models can have the *exact
same* mean accuracy — and yet excel at completely different things. Model A
is strong at reasoning but weak on facts. Model B is the opposite. The mean
score hides this entirely.

This is why measurement science matters. A single number — accuracy — can
be deeply misleading when the benchmark is multidimensional.

---

## PART 6 — CLOSING (~1:00)

### 6.1 Summary

**NARRATOR:**

> [On screen: key takeaways, clean text on dark background]

Let's step back and see the full picture.

Measurement is more than scoring. It requires a theory connecting observed
responses to latent constructs. The Rasch model occupies a special place
because it guarantees two properties — sufficiency and specific objectivity —
that no other model provides. These properties are what make it possible to
compare models fairly across different test items.

But real benchmarks are rarely so clean. Items have different discriminations.
Models can guess. Benchmarks measure multiple things at once. The richer
models — 2PL, 3PL, factor models — capture this complexity at the cost of
losing Rasch's elegant guarantees.

And there's a deeper question: do latent abilities even exist, or are
capabilities better understood as a network of connected skills? The answer
shapes how we interpret every leaderboard score.

These aren't abstract philosophical debates. They determine whether a
two-point accuracy difference between two models is meaningful — or noise.

[pause]

The tools to answer these questions have existed for a century. It's time
we applied them to AI.

> [On screen: "AIMS — AI Measurement Science" / "aimslab.stanford.edu"]

---

## Animation-Scene Mapping

| Script section | Animation file | Scene name |
|---------------|----------------|------------|
| 1.2 Response Matrix | `response_matrix.py` | `ResponseMatrixSort` |
| 2.1–2.3 ICC Models | `icc_models.py` | `ICCModels` |
| 3.1 Sufficiency | `sufficiency.py` | `Sufficiency` |
| 3.2 Specific Objectivity | `specific_objectivity.py` | `SpecificObjectivity` |
| 4.1 Elo / Bradley-Terry | `elo_dynamics.py` | `EloDynamics` |
| 4.2 Latent vs. Network | `latent_vs_network.py` | `LatentVsNetwork` |
| 5.1 Factor Model | `factor_model.py` | `FactorModel` |

## Rendering All Animations

```bash
PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH"

for scene in \
  "response_matrix.py ResponseMatrixSort" \
  "icc_models.py ICCModels" \
  "sufficiency.py Sufficiency" \
  "specific_objectivity.py SpecificObjectivity" \
  "elo_dynamics.py EloDynamics" \
  "latent_vs_network.py LatentVsNetwork" \
  "factor_model.py FactorModel"; do
  set -- $scene
  manim -qh --disable_caching animations/$1 $2
done
```
