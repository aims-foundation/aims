# Learning — Video Script

**Chapter 2 of AI Measurement Science (AIMS)**
Target length: ~10-12 minutes
Format: Narrated animation (3Blue1Brown style)

---

## Production Notes

- **Animations** are in `animations/ch2/*.py` (Manim, 1080p60). Each scene listed
  below corresponds to a rendered `.mp4` in `media/ch2/videos/`.
- **Narration** generated via edge-tts, synced via `stitch_narrated.sh`.
- **Pacing markers:** `[pause]` = ~1 s beat. `[beat]` = ~0.5 s.

---

## PART 1 — THE ESTIMATION PROBLEM (~3:30)

### 1.1 Opening Hook

**NARRATOR:**

In the last chapter, we defined measurement models — Rasch, 2PL, factor
models — that describe how latent abilities generate observed responses.

[beat]

But knowing the form of a model is not enough. To use these models,
we must estimate their parameters from data.

> [ANIMATION: opening_hook.py — OpeningHook]
> Cue: Rasch formula with response matrix grid

The Rasch model says the probability of a correct response depends on
theta minus beta. But theta and beta are *unknown* — the hidden
quantities we want to measure.

> Cue: Question marks pulse on theta and beta

Given a matrix of right and wrong answers, find the parameters that
best explain the data.

> Cue: Likelihood landscape with gradient ascent path

This is an optimization problem — climbing the likelihood landscape
to find its peak.

[pause]

### 1.2 Maximum Likelihood

**NARRATOR:**

> [ANIMATION: likelihood_landscape.py — LikelihoodLandscape]
> Cue: Single-item likelihood visualization

Maximum likelihood estimation starts with a simple principle: find the
parameters that make the observed data most probable.

For a single item, the likelihood measures how well our parameters
explain what we saw — high predicted probability for correct responses,
low for incorrect.

> Cue: Gradient intuition and convergence curve

The gradient has an elegant interpretation: it is the sum of residuals —
observed minus predicted. Gradient ascent nudges the parameters toward
higher likelihood until the estimates converge.

> Cue: Parameter recovery scatter plots

When we compare estimates to true values on synthetic data, the recovery
is remarkably good — correlations above 0.98 are typical.

[pause]

Maximum likelihood is the foundation. But it comes with a subtle trap.

---

## PART 2 — MAXIMUM LIKELIHOOD (~1:30)

### 2.1 The Identifiability Problem

**NARRATOR:**

> [ANIMATION: identifiability.py — Identifiability]
> Cue: Number line with models and items

The Rasch model has an *identifiability problem*.

Watch what happens when we add the same constant to every ability and every
difficulty simultaneously.

> Cue: All parameters slide right by +c

The differences don't change. The probabilities don't change. The likelihood
doesn't change. The model cannot tell these solutions apart.

> Cue: Algebraic cancellation

Mathematically, the plus-c appears in both theta and beta — and cancels
perfectly. There are *infinitely many* parameter settings that produce the
exact same likelihood.

> Cue: Sum-to-zero constraint

The standard fix is to anchor the scale. We constrain the parameters to
sum to zero. Now there is a unique solution, and a model with ability zero
is, by convention, average.

[pause]

This may seem like a technicality. But without addressing identifiability,
your optimizer will wander forever without converging.

---

## PART 3 — THE EM ALGORITHM (~2:00)

### 3.1 The EM Framework

**NARRATOR:**

> [ANIMATION: em_algorithm.py — EMAlgorithm]
> Cue: E-step / M-step cycle diagram

When abilities are *latent variables*, we need a different approach.
The EM algorithm — Expectation-Maximization — alternates between two
steps, guaranteed to improve the likelihood each iteration.

> Cue: E-step — posterior over abilities

In the E-step, we compute the posterior over each model's ability.
A prior — a standard normal — gets shifted and sharpened by the data.

> Cue: M-step — bar chart adjustment

In the M-step, we update item parameters so expected correct responses
match observed ones. Each difficulty adjusts to close the gap.

> Cue: Iteration counter and convergence

Then we repeat. After ten or twenty iterations, the algorithm converges.

[pause]

The EM algorithm is the workhorse behind most IRT software — stable
and natural for latent variable models.

---

## PART 4 — THE BAYESIAN PERSPECTIVE (~2:00)

### 4.1 Prior, Likelihood, Posterior

**NARRATOR:**

> [ANIMATION: bayesian_inference.py — BayesianInference]
> Cue: Prior bell curve

The Bayesian approach adds a *prior* — what we believe before seeing data.
A standard normal says most models are roughly average.

> Cue: Likelihood curve appears

The likelihood is what the data say. Its peak is the MLE.

> Cue: Posterior curve with MAP and MLE marked

The posterior is prior times likelihood. Its peak — the MAP — compromises
between prior and data, pulled toward zero. This is *Bayesian shrinkage*.

> Cue: Extreme case — perfect score, MLE diverges

When a model answers everything correctly, the MLE diverges to infinity.
The MAP stays finite — the prior prevents absurd estimates.

[beat]

For AI benchmarks with near-perfect scores, this is essential.

---

## PART 5 — ADAPTIVE TESTING (~2:30)

### 5.1 Fisher Information and CAT

**NARRATOR:**

> [ANIMATION: cat_simulation.py — CATSimulation]
> Cue: Fisher information curves

Everything so far has been *passive learning* — estimating from a fixed
dataset. But what if we could *choose* which questions to ask?

This is Computerized Adaptive Testing.

[beat]

Fisher information tells us how much we learn from each item. It peaks
where item difficulty matches ability. A genius learns nothing from a
trivial question; a beginner learns nothing from an impossible one.

> Cue: CAT step-by-step simulation

CAT works like this: start with an average estimate, select the most
informative item, observe the response, update, and repeat.

Watch the confidence interval shrink with each well-chosen question.

> Cue: CAT vs random comparison chart

Compared to random selection, CAT achieves the same precision with
roughly *half* as many questions.

[pause]

For AI evaluation, where each question costs an API call, adaptive
testing means faster, cheaper evaluation with less contamination risk.

---

## PART 6 — CLOSING (~1:00)

### 6.1 Summary

**NARRATOR:**

> [On screen: key takeaways, clean text on dark background]

Let us step back.

This chapter covered the bridge from theory to practice. The models from
Chapter 1 become useful only when we can estimate their parameters from data.

[pause]

Maximum likelihood finds the peak of the likelihood — the parameters that
make the data most probable. The gradient is simply observed minus predicted
— a beautiful interpretation.

The EM algorithm handles the case where abilities are latent variables,
alternating between expectation and maximization in a guaranteed-convergent
cycle.

Bayesian inference adds regularization through priors. This prevents
absurd estimates for extreme data and naturally quantifies uncertainty.

And adaptive testing turns estimation on its head: instead of passively
analyzing a fixed dataset, we actively choose what to measure, achieving
the same precision with far fewer questions.

[pause]

The tools to estimate these models are the bridge between theory and practice.

> [On screen: "AIMS — AI Measurement Science" / "aimslab.stanford.edu"]

---

## Animation-Scene Mapping

| Script section | Animation file | Scene name |
|----------------|----------------|------------|
| 1.1 Opening Hook | `opening_hook.py` | `OpeningHook` |
| 1.2 MLE | `likelihood_landscape.py` | `LikelihoodLandscape` |
| 2.1 Identifiability | `identifiability.py` | `Identifiability` |
| 3.1 EM Algorithm | `em_algorithm.py` | `EMAlgorithm` |
| 4.1 Bayesian Inference | `bayesian_inference.py` | `BayesianInference` |
| 5.1 CAT | `cat_simulation.py` | `CATSimulation` |

## Rendering All Animations

```bash
PATH="/lfs/local/0/sttruong/miniconda3/bin:$PATH"

for scene in \
  "opening_hook.py OpeningHook" \
  "likelihood_landscape.py LikelihoodLandscape" \
  "identifiability.py Identifiability" \
  "em_algorithm.py EMAlgorithm" \
  "bayesian_inference.py BayesianInference" \
  "cat_simulation.py CATSimulation"; do
  set -- $scene
  manim -qh --disable_caching --media_dir media/ch2 animations/ch2/$1 $2
done
```
