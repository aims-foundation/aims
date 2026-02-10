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

In the last chapter, we defined the measurement models — the Rasch model,
the 2PL, factor models — that describe how latent abilities generate
observed responses.

[beat]

But knowing the *form* of a model is not enough. To actually *use* these
models for AI evaluation, we must estimate their parameters from data.

> [ANIMATION: opening_hook.py — OpeningHook]
> Cue: Rasch formula with response matrix grid

Think of it this way. The Rasch model says: the probability of a correct
response is the sigmoid of theta minus beta. Beautiful. But theta and beta
are *unknown*. They are the hidden quantities we are trying to measure.

> Cue: Question marks pulse on theta and beta

So the central problem of this chapter is: given a matrix of zeros and ones
— right and wrong answers — find the parameter values that best explain
the data.

> Cue: Likelihood landscape with gradient ascent path

This is an optimization problem. We need to climb the likelihood landscape
to find its peak. And the tools for doing that are the subject of this chapter.

[pause]

### 1.2 Maximum Likelihood

**NARRATOR:**

> [ANIMATION: likelihood_landscape.py — LikelihoodLandscape]
> Cue: Single-item likelihood visualization

Maximum likelihood estimation starts with a simple principle: find the
parameter values that make the observed data *most probable*.

For a single item, the likelihood depends on whether the model answered
correctly. If it did, we want the predicted probability to be high. If it
didn't, we want it low. The likelihood measures how well our parameters
explain what we saw.

> Cue: Gradient intuition and convergence curve

The gradient has a beautiful interpretation. It is simply the sum of
*residuals* — observed minus predicted. If a model performs better than
expected, the residuals are positive, and we increase its ability. If worse,
we decrease it.

[beat]

This is gradient ascent. At each step, we nudge the parameters in the
direction that most improves the likelihood. After a few hundred iterations,
the estimates converge.

> Cue: Parameter recovery scatter plots

And when we compare the estimated parameters to the true values — on
synthetic data where we know ground truth — the recovery is remarkably
good. Correlations above 0.98 are typical for well-behaved datasets.

[pause]

Maximum likelihood estimation is the foundation. But it comes with a
subtle trap.

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

When we treat person abilities as *latent variables* rather than fixed
parameters, we need a different approach. The EM algorithm — Expectation-
Maximization — is the standard tool.

It alternates between two steps in a cycle that is guaranteed to improve
the likelihood at every iteration.

> Cue: E-step — posterior over abilities

In the E-step, we compute the posterior distribution over each model's
ability, given its responses and the current item parameters. We start
with a prior — a standard normal — and the data shift and sharpen it
into a posterior.

[beat]

The posterior tells us what we believe about this model's ability, given
everything we know so far.

> Cue: M-step — bar chart adjustment

In the M-step, we update the item parameters so that the *expected* number
of correct responses matches the *observed* number. Each item difficulty
adjusts to close the gap between prediction and reality.

> Cue: Iteration counter and convergence

Then we repeat. Each cycle is guaranteed to increase the marginal
likelihood. After ten or twenty iterations, the algorithm converges.

[pause]

The EM algorithm is the workhorse behind most IRT software. It is slower
than direct gradient methods, but it handles latent variables naturally
and is very stable.

---

## PART 4 — THE BAYESIAN PERSPECTIVE (~2:00)

### 4.1 Prior, Likelihood, Posterior

**NARRATOR:**

> [ANIMATION: bayesian_inference.py — BayesianInference]
> Cue: Prior bell curve

The Bayesian approach adds one more ingredient: a *prior distribution*
that encodes what we believe about the parameters before seeing any data.

For abilities, the standard choice is a normal distribution centered at
zero. This says: most models are roughly average, with a few unusually
strong or weak.

> Cue: Likelihood curve appears

The likelihood tells us what the data say. Its peak — the MLE — is
the data's best guess for the parameter.

> Cue: Posterior curve with MAP and MLE marked

The posterior is the product: prior times likelihood. Its peak — the
MAP estimate — is a compromise between the prior and the data.

Notice: the MAP is pulled toward zero compared to the MLE. This is
*Bayesian shrinkage*. The prior acts as a regularizer, pulling extreme
estimates back toward the center.

> Cue: Extreme case — perfect score, MLE diverges

And here is where it really matters. When a model answers every question
correctly, the MLE goes to *infinity*. But the MAP stays finite. The
prior prevents absurd estimates.

[beat]

For AI benchmarks where some models achieve near-perfect scores on easy
subsets, this regularization is not just elegant — it is essential.

---

## PART 5 — ADAPTIVE TESTING (~2:30)

### 5.1 Fisher Information and CAT

**NARRATOR:**

> [ANIMATION: cat_simulation.py — CATSimulation]
> Cue: Fisher information curves

Everything we have discussed so far is *passive learning* — we have a
fixed dataset and estimate parameters from it. But what if we could
*choose* which questions to ask?

This is Computerized Adaptive Testing. The key insight: not all questions
are equally informative for all test-takers.

[beat]

Fisher information quantifies this. Each item has an information curve
that peaks where the item difficulty matches the ability. The most
informative item is always the one closest in difficulty to the current
ability estimate.

A genius gains nothing from a trivial question. A beginner gains nothing
from an impossible one.

> Cue: CAT step-by-step simulation

So CAT works like this. Start with a prior estimate — say, average
ability. Select the most informative item. Observe the response. Update
the estimate. Repeat.

Watch the confidence interval shrink with each well-chosen question. The
estimate zeroes in on the true ability rapidly.

> Cue: CAT vs random comparison chart

Compared to random item selection, CAT is dramatically more efficient.
The same measurement precision is achieved with roughly *half* as many
questions.

[pause]

For AI evaluation, where each benchmark question costs an API call, this
is not just elegant — it is practical. CAT lets us evaluate models
faster, cheaper, and with less risk of benchmark contamination.

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
