# Tentative Homework 1 Problems

> **Status:** Superseded by the student-facing draft in
> `lecturebook/homework/homework-01.ipynb`. Retained only as an early planning
> record.

This planning draft is intentionally outside the published Jupyter Book. The
student-facing notebook now contains the full review draft.

The tentative problems use only Lectures 1--4 and emphasize handwritten
reasoning. Code may be used to check arithmetic, but it would not replace the
required derivations, diagrams, or interpretations.

## 1. Predictive-modeling formulation

For a small engineering system, draw a causal diagram and write a corresponding
set of structural equations. Identify which uncertain quantities are aleatory
and which are epistemic. State one uncertainty-propagation question and one
calibration question for the system.

## 2. Probability rules

Consider a two-stage inspection experiment in which components are sampled
without replacement. Enumerate the outcomes and compute specified joint,
conditional, complement, and union probabilities using the sum and product
rules. Show every step.

## 3. A discrete random variable

Let

\[
p_X(x) = c(x+1), \qquad x \in \{0,1,2,3\}.
\]

Find the normalizing constant, make the probability-mass table, and compute a
tail probability, $\mathbb{E}[X]$, $\operatorname{Var}(X)$, and
$\mathbb{E}[g(X)]$ for a specified function $g$. Perform the calculations by
hand and include a reasonableness check.

## 4. A continuous random variable

Let

\[
f_X(x) = cx, \qquad 0 \leq x \leq 2,
\]

and let the density be zero elsewhere. Find the normalizing constant, derive
the full piecewise cumulative distribution function, and compute a specified
interval probability, $\mathbb{E}[X]$, and $\operatorname{Var}(X)$ by
integration. Sketch both the density and cumulative distribution by hand and
check their units and limiting values.
