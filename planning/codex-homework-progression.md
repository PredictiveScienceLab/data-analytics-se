# Codex progression across Homework 1--13

This is an instructor-facing plan. The published homework notebooks remain
title-only until each assignment is written. Each homework should contain at
most one **Codex laboratory** problem; the remaining problems should continue
to emphasize manual mathematical work.

The progression follows the actual course sequence and treats mathematical
knowledge as the verification layer for agent-produced work. Students should
not receive credit merely because code runs or a dashboard looks convincing.

Official background for the course materials:

- [`AGENTS.md` project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex skills and `SKILL.md`](https://learn.chatgpt.com/docs/build-skills)
- [Interactive Visualizations in ChatGPT](https://learn.chatgpt.com/docs/visualizations)

## Common structure

Students maintain one cumulative, private course repository. The instructor
provides a Python 3.11 starter project with `pyproject.toml`, `uv.lock`, and one
documented command for each operation. Python dependencies and commands use
`uv`; no public repository or public dashboard deployment is required.

The graded dashboard path should be repository-native and reproducible, such
as an instructor-selected `ipywidgets` or local Streamlit template. The
in-product `@Visualize` experience can be demonstrated as an optional route,
but it should not be required because availability and rendering differ by
account and Codex surface.

Every Codex laboratory problem produces the following small evidence bundle:

1. `agent_task.md`: the final bounded task specification given to Codex;
2. the source code or notebook produced and then reviewed by the student;
3. an executable verification harness, invoked with one documented `uv run`
   command;
4. `verification.md`: a short mathematical oracle, one failed or rejected
   output, the repair, and a conclusion; and
5. `AI_USE.md`: tool, date, task, and the material human changes, without a
   full conversation transcript.

Here, **harness** means the reproducible environment, tests, reference cases,
mathematical invariants, fixed stochastic seeds where appropriate, and a
single command that decides whether the artifact satisfies its specification.
It is not a visual demonstration and it is not Codex saying that its own work
is correct.

## Homework sequence

| HW | Due | Course material | Codex laboratory problem | Mathematical verification gate | Main artifact |
|---:|---:|---|---|---|---|
| 1 | Aug. 30 | Lectures 1--4: predictive modeling; probability; discrete and continuous random variables | **Codex as a fallible calculator.** After doing a small normalization/CDF/moment calculation by hand, ask Codex to write a checker. Inspect its patch and identify at least one test that had to come from the mathematics rather than the generated code. | PMF/PDF normalization, CDF endpoint and monotonicity checks, and hand-computed moments. | A small checker plus the first `verification.md`; no `AGENTS.md` authoring yet. |
| 2 | Sept. 6 | Lectures 5--6: collections of random variables and random vectors | **Write the first `AGENTS.md`.** Specify setup/test commands, files Codex may edit, course notation, mathematical invariants, and the definition of done. Then ask Codex to implement joint-distribution, marginalization, and covariance utilities. | A hand-worked finite joint distribution; marginals must normalize; covariance must be symmetric and positive semidefinite. | Root `AGENTS.md`, implementation, and instructor-provided tests. |
| 3 | Sept. 13 | Lectures 7--10: sampling, Monte Carlo estimation, and Monte Carlo uncertainty | **Build the first real harness.** Students write tests and analytic reference values before asking Codex to implement Monte Carlo estimators and uncertainty estimates. Include deterministic smoke tests and stochastic property tests. | For \(U\sim U(0,1)\), derive \(E[U^2]=1/3\) and \(\operatorname{Var}(U^2)=4/45\); test the \(N^{-1/2}\) error rate and repeated-trial coverage within stated tolerances. | `tests/`, seeded simulation, and `uv run pytest -q`. |
| 4 | Sept. 20 | Lectures 11--12: prior information and analytical Bayesian inference | **First nontrivial repo task and first reusable skill.** Author `.agents/skills/conjugate-bayes-audit/SKILL.md`, then give Codex a bounded task to build and audit a multi-file conjugate Bayesian tool under the existing `AGENTS.md` and harness. Review the diff and reject at least one unsupported claim or implementation choice. | Beta\((2,3)\) with seven successes and three failures must produce Beta\((9,6)\), posterior-predictive probability \(9/15\), and correct prior- and data-dominated limits. A hidden second case prevents hard-coding. | Skill, Bayesian tool, tests, task specification, and audit. This is the first integration milestone. |
| 5 | Sept. 27 | Lectures 13--15: least squares, Bayesian linear regression, ARD, and posterior diagnostics | **Build the first interactive dashboard.** Codex creates a local regression/prior explorer, while all numerical work remains in pure tested functions and the UI is a thin wrapper. | For \(x=(-1,0,1)\), \(y=(-1,1,3)\), verify OLS weights \((1,2)\); with a standard-normal prior and unit noise, verify posterior mean \((3/4,4/3)\) and covariance \(\operatorname{diag}(1/4,1/3)\). | Tested regression core, local dashboard, and one screenshot for smoke-checking only. |
| 6 | Oct. 11 | Lectures 16--17: classification, decision making, clustering, and density estimation | **Teach scoped instructions and independent review.** Add a homework-level `AGENTS.md` that specializes the root instructions. Use separate implementer and verifier passes to build and audit a classifier or clustering analysis. | Hand-computed confusion-matrix metrics and comparison with a base-rate rule; clustering conclusions must be invariant to label permutation. | Nested `AGENTS.md`, model code, evaluator, and hidden metric tests. |
| 7 | Oct. 18 | Lecture 18: dimensionality reduction | **Red-team a visual result.** Codex builds a PCA explorer, but students must validate its numerical core and supply a counterexample to any interpretation inferred from appearance alone. | For covariance \(\begin{bmatrix}2&1\\1&2\end{bmatrix}\), verify eigenvalues \(3,1\), explained-variance fractions \(3/4,1/4\), orthonormal directions, and monotone reconstruction error. | Refined thin dashboard, PCA core, property tests, and one rejected visual claim. |
| 8 | Oct. 25 | Lectures 19--20: state-space models and Kalman filters | **Use a dashboard as an experiment, not as proof.** Build a local Kalman-filter explorer with process/measurement-noise controls. Require Codex to connect every control to a tested model parameter. | For prior \(N(0,2)\), observation \(y=2\), and \(R=2\), verify \(K=1/2\), posterior mean \(1\), and posterior variance \(1\); also test covariance symmetry/PSD and \(R\to0\), \(Q\to0\) limits. | Tested filter core plus a thin interactive dashboard and an interpretation card. |
| 9 | Nov. 1 | Lectures 21--22: Gaussian-process priors and conditioning | **Reuse and improve the skill/harness pattern.** Extend the probabilistic-model audit skill, then use Codex to build a kernel/posterior explorer. Test the numerical core independently of the UI. | Kernel symmetry/PSD, noiseless interpolation, the conditioning equations, and posterior variance no larger than prior variance for fixed hyperparameters. Include one small hand-computed GP posterior. | Revised audit skill, tested GP core, and dashboard. |
| 10 | Nov. 15 | Lecture 23 and model-calibration material: Bayesian global optimization and calibration | **Decompose bounded agentic work.** Run separate planning, implementation, and skeptical-review passes for an acquisition-function or calibration tool. Enforce an objective-call/runtime budget. The workflow must work even if a student's interface has no subagent feature. | Acquisition values on a hand-specified GP state, domain/boundary checks, budget compliance, and recovery on a synthetic calibration case with known truth. | Three short task records, decision trace, implementation, and a red-team test set. |
| 11 | Nov. 22 | Lectures 24--25: deep neural networks for regression and classification | **Build a resource-aware harness.** Put runtime/data limits and smoke-test commands in `AGENTS.md`. Codex must implement a finite-difference gradient check, a tiny-overfit test, and a cheap baseline before any full training run or learning-curve dashboard. | Manual parameter count, one hand-derived gradient, central finite-difference agreement, a leak-free split, and successful overfit of a tiny batch. | Fast/full run modes, gradient tests, training record, and learning-curve explorer. |
| 12 | Nov. 29 | Lecture 26 and PIV material: physics-informed neural networks | **Use physics as the oracle.** Ask Codex to implement a PINN residual and residual/boundary-condition explorer only after the student supplies the equations, units, and manufactured solution. Keep the task short for Thanksgiving week. | For \(u(x)=\sin(\pi x)\), verify \(u''+\pi^2u=0\) and \(u(0)=u(1)=0\); also require dimensional consistency and held-out residual checks. | Tested residual functions, PINN experiment, and thin dashboard. |
| 13 | Dec. 6 | Lectures 27--28: sampling methods and variational inference | **Capstone verification task.** Use the accumulated `AGENTS.md`, skill, harness, and dashboard patterns to compare MCMC and VI first on a diagonal Gaussian with an exact answer, then on a correlated or bimodal stress test. | Hand-check one Metropolis--Hastings ratio; compare MCMC error with its Monte Carlo standard error; verify exact VI recovery on the simple target and demonstrate under-dispersion or mode failure on the stress test. | Compact comparison package, local diagnostic dashboard, and one-page “math warranty.” |

## Milestones

By the end of Homework 4, a student should be able to:

- turn a mathematical problem into a bounded repository task;
- write useful project instructions in `AGENTS.md`;
- require a one-command harness and define acceptance tests before coding;
- inspect the patch rather than accepting a narrative claim; and
- use a hand derivation, limiting case, or invariant to reject incorrect output.

Later homeworks refine and reuse skills, scoped instructions, thin dashboards,
task decomposition, computational budgets, and domain-specific scientific
oracles.

## Scalable grading

Use the same 20-point rubric for the single Codex laboratory problem in every
homework:

- 8 points: public and hidden executable tests;
- 4 points: required repository/artifact structure, checked automatically;
- 2 points: clean reproduction from the documented `uv run` command;
- 4 points: the concise mathematical verification card; and
- 2 points: a specific rejected output, repair, and AI-use disclosure.

Do not grade prompt eloquence, dashboard aesthetics, or the length of the chat
transcript. Autograde the first 14 points. The two TAs only inspect the six-point
verification/audit card, using a three-level checklist. At roughly 45 seconds
per submission, the human pass is about two hours total for 160 students.

## Instructor preparation

- Confirm that every student has an institutionally acceptable route to Codex;
  provide an equivalent access path before making the strand required.
- Use synthetic or public course data only; prohibit uploading private,
  sponsored-research, or personally identifiable data.
- Supply a cumulative private starter repository and accept a zip snapshot or
  institutionally supported private-repository submission.
- Publish public tests and keep a small hidden bank of mathematical property
  tests with randomized parameters.
- Provide a dashboard skeleton in Homework 5 so UI plumbing does not displace
  regression learning.
- Revisit the Codex-specific instructions immediately before Fall 2026 because
  product interfaces and feature availability can change.
