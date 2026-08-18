# Fall 2026 homework redesign: ten-assignment blueprint

Status: **instructor review; not yet student-facing**

This is the active homework plan for the revised ten-assignment schedule. It
replaces the earlier thirteen-assignment and Codex-oriented plans. There are no
Codex, agent, prompt-writing, or AI-tool exercises in this sequence.

## Common design

Each completed homework is one Google Colab notebook with exactly two numbered
problems:

1. **Manual mathematics (25 points).** One coherent, multi-part calculation or
   derivation using only material available by the assignment deadline.
2. **Computational scientific study (75 points).** One scaffolded application
   with supplied data loading, helper code, and expensive boilerplate. The
   final part asks for a concise scientific interpretation and at least one
   limitation or failure mode.

The target workload is 3--4 hours and the target runtime is under five minutes
on a fresh, CPU-only Colab runtime. Every released notebook must use a fixed
random seed, avoid Google Drive and absolute paths, identify data provenance,
and run from beginning to end without additional package installation.

Homework is assigned on the dates in the syllabus. It is not described as a
weekly sequence because assignments are omitted around holidays, breaks, and
exam weeks.

## Ten-assignment schedule

| Homework | Due | Coverage | Current draft |
|---|---|---|---|
| 1 | Aug. 30 | Lectures 1--4 | Probability and mechanical reliability; complete |
| 2 | Sept. 13 | Lectures 5--10 | Random vectors plus Monte Carlo propagation; complete merged draft |
| 3 | Sept. 20 | Lectures 11--12 | Prior information and Bayesian earthquake rates; complete |
| 4 | Sept. 27 | Lectures 13--15 | Least squares and Bayesian elastic-modulus inference; complete |
| 5 | Oct. 18 | Lectures 16--18 | Classification, clustering, and dimensionality reduction; consolidation pending |
| 6 | Oct. 25 | Lectures 19--20 | State-space models and Kalman filtering; complete |
| 7 | Nov. 1 | Lectures 21--22 | GP prediction with NIST Chwirut1; complete |
| 8 | Nov. 15 | Lecture 23 and model-calibration material | Bayesian optimization for calibration; pending |
| 9 | Nov. 22 | Lectures 24--25 | Deep neural-network regression; complete |
| 10 | Dec. 6 | Lectures 26--28 | Physics-informed modeling plus sampling/VI; consolidation pending |

The skipped Week 2 material is assessed in Homework 2, the skipped pre-Fall
Break material is assessed in Homework 5, and the Thanksgiving-week material
is assessed in Homework 10.

## Assignment designs

### Homework 1 -- Probability and mechanical reliability

- **Manual problem:** Bayes' rule, diagnostic-test predictive values, and a
  false-positive-rate design inequality.
- **Computational study:** fit and audit a two-parameter Weibull model for eight
  gear failure times, calculate reliability quantities, and make a bounded
  replacement decision.

### Homework 2 -- Random vectors and Monte Carlo propagation

This assignment deliberately merges selected pieces of the former Homework 2
and Homework 3 rather than concatenating two 100-point assignments.

- **Manual problem:** joint PMF, marginals, conditional probability, covariance,
  correlation, independence, and a linear combination of random variables.
- **Computational study:** propagate uncertain stiffness and damping through a
  supplied damped-oscillator evaluator; estimate a mean, standard error,
  exceedance probability, and quantile; demonstrate estimator variability
  proportional to $N^{-1/2}$.

The former B--H computational study and inverse-sampling mathematics are kept
in the instructor homework bank as optional material.

### Homework 3 -- Prior information and Bayesian earthquake rates

- **Manual problem:** Gamma--Poisson conjugacy, posterior summaries, and a
  posterior-predictive zero-count probability.
- **Computational study:** use the frozen Southern California USGS snapshot to
  compare priors, calculate predictive counts, and communicate ten- and
  twenty-year event risk.

### Homework 4 -- Least squares and Bayesian elastic-modulus inference

- **Manual problem:** zero-intercept least squares and its sampling variance.
- **Computational study:** determine the largest strain range for which a
  Bayesian Hooke's-law model is defensible using residual and predictive
  diagnostics.

### Homework 5 -- Classification, clustering, and dimensionality reduction

This notebook remains a placeholder until one bounded study covers all three
topics. The completed steel-plate classification/clustering draft is preserved
in the homework bank and should be shortened before a PCA component is added.

The unresolved data/application choices are:

- reuse the steel-plate data and perform PCA before supervised and
  unsupervised comparisons;
- use the UCI robot force/torque traces for PCA and keep a smaller steel-plate
  classification component; or
- use MRI or B--H data only if the assignment can remain one coherent study.

### Homework 6 -- State-space models and Kalman filtering

- **Manual problem:** one complete Kalman prediction/update step.
- **Computational study:** filter a hidden forced oscillator, validate against
  known truth, and diagnose process-noise misspecification with innovations.

### Homework 7 -- Gaussian-process prediction

- **Manual problem:** GP conditioning with latent and noisy predictive
  variances.
- **Computational study:** download and checksum NIST Chwirut1, hold out entire
  replicated distance levels, compare squared-exponential and Matern-3/2
  kernels, and evaluate interpolation separately from extrapolation.

### Homework 8 -- Bayesian optimization for model calibration

This notebook remains a placeholder. The preferred design uses a supplied
catalytic-reaction solver and expected improvement under a fixed evaluation
budget. A Forrester-function study remains the safe fallback. The assignment
must be self-contained and may not assume that any new video will be recorded.

### Homework 9 -- Deep neural-network regression

- **Manual problem:** one small neural-network forward pass and SGD update.
- **Computational study:** compare a linear baseline with a compact neural
  network on UCI Airfoil Self-Noise using train/validation/test discipline,
  early stopping, and a sparse-support trust check.

### Homework 10 -- Physics-informed modeling and posterior characterization

This notebook remains a placeholder because it must combine Lecture 26 with
the sampling and variational material from Lectures 27--28 without becoming two
independent assignments. The completed Challenger MCMC/VI draft and the former
Lecture-26 design notes are preserved in the homework bank. The final design
must not assume PIV material, a PIV application, or new videos.

## Data and link constraints

- Keep the existing artifact filenames such as `hw04_...`, `hw11_...`, and
  `hw13_...` even when their assignment numbers change. They are provenance
  identifiers and changing them would create unnecessary raw-link churn.
- Before release, replace moving `master` data URLs with an immutable course
  release tag or commit.
- The active book navigation, source directory, and Brightspace list contain
  Homework 1--10 only.
- The affected thirteen-assignment source drafts are preserved under
  `planning/homework-bank/2026-08-18-13-set/` and are not part of the book.

## Remaining authoring decisions

Only three assignments require substantive follow-up:

1. consolidate classification, clustering, and dimensionality reduction for
   Homework 5;
2. choose the calibrated-model or Forrester route for Homework 8; and
3. design one coherent Lecture 26--28 assignment for Homework 10 without PIV.
