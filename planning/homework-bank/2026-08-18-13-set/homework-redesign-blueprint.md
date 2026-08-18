# Fall 2026 homework redesign: instructor blueprint

Status: **for instructor review; not yet student-facing**

This redesign replaces the earlier Codex-oriented drafts. There are no Codex,
agent, prompt-writing, or AI-tool exercises in this homework sequence.

## Common design for all 13 sets

Each homework is one Colab notebook with exactly two numbered problems:

1. **Manual mathematics (25 points).** One coherent, multi-part derivation or
   calculation using only material assigned that week. Students must show the
   mathematical steps in Markdown/LaTeX or insert legible handwritten work.
2. **Computational scientific study (75 points).** One application with a
   supplied data-loading cell, starter code, and any expensive solver or helper
   machinery. The final 10 of these 75 points are for a short scientific
   interpretation, including one limitation or failure mode.

Target workload is 3--4 hours and target Colab runtime is under 5 minutes.
Homework 11 and 12 may use up to 10 minutes, but both must have a CPU-only
smoke-test mode. Homework 12, due immediately after Thanksgiving break, should
be the lightest assignment in the second half of the course.

Every released notebook should include:

- one setup cell that imports standard Colab packages and downloads at most one
  small, frozen data artifact;
- an instructor-controlled URL, retrieval date, license/provenance note, and
  SHA-256 checksum for external data;
- a fixed random seed and a `FAST_MODE` switch while students develop;
- no absolute paths and no dependence on a student's Google Drive;
- supplied plotting style, solver, and expensive boilerplate so the homework
  assesses modeling rather than environment setup;
- a final `Run all` check that completes in a fresh Colab runtime.

The old assignments provide the style: a real engineering or scientific
question, visualization, a probabilistic model, validation, uncertainty, and a
short decision. The old assignments do **not** provide the appropriate weekly
scope: old HW4--HW8 each contained several largely independent studies.

## Schedule and detailed problem designs

### HW1 -- Probability and mechanical reliability

**Coverage:** Lectures 1--4<br>
**Due:** Sunday, August 30, 11:59 p.m. ET<br>
**Legacy material retained:** diagnostic-testing reasoning and gear-lifetime
data from old HW1.

#### Problem 1 -- Manual mathematics: Bayes and test design (25 points)

For disease prevalence \(P(D)=0.004\), sensitivity \(P(+\mid D)=0.80\), and
specificity \(P(-\mid D^c)=0.90\):

1. draw the two-stage probability tree;
2. derive and calculate \(P(D\mid +)\) and \(P(D\mid -)\);
3. explain, using the calculation rather than intuition alone, why a positive
   result can still have a low positive predictive value;
4. with prevalence fixed at 0.004 and sensitivity fixed at 0.99, derive the
   maximum false-positive rate that would make \(P(D\mid +)\geq 0.90\).

This keeps the strongest part of old HW1 but turns the open-ended test-design
question into a single gradeable inequality.

#### Problem 2 -- Colab study: Weibull gear reliability (75 points)

Use the corrected eight failure times from the old assignment. The supplied
cell fits `scipy.stats.weibull_min` with location fixed at zero; fitting theory
is not assessed yet. The notebook supplies the Weibull PDF, CDF, survival,
mean, and quantile formulas because the assigned lectures use Uniform and
Gaussian examples rather than teaching Weibull fitting. Students:

1. plot the observations, empirical survival curve, and fitted survival curve;
2. report fitted shape and scale with units;
3. calculate mean life, median life, \(P(8<T<10)\), and the first-percentile
   failure time;
4. verify numerically that the fitted density integrates to one and that its
   CDF and survival function are complements at specified times;
5. answer a reliability decision: whether a proposed replacement interval
   meets a specified maximum pre-replacement failure probability;
6. state one reason that eight run-to-failure observations are insufficient for
   a high-consequence reliability decision.

No external data file is needed. The wording is corrected from "ten gears" to
eight, and the old `exponweib.fit(..., loc=0)` call is replaced by the intended
two-parameter Weibull fit with `floc=0`.

---

### HW2 -- Dependence and random vectors in engineering data

**Coverage:** Lectures 5--6<br>
**Due:** Sunday, September 6, 11:59 p.m. ET<br>
**Legacy material retained:** joint-PMF reasoning and the ensemble of B--H
curves from old HW2.

#### Problem 1 -- Manual mathematics: a joint probability table (25 points)

For \(X\in\{-1,0,2\}\), \(Y\in\{0,1\}\), and

\[
p_{X,Y}=\begin{array}{c|cc}
 &Y=0&Y=1\\\hline
X=-1&0.10&0.15\\
X=0 &0.20&0.10\\
X=2 &0.15&0.30
\end{array},
\]

students calculate both marginals, \(p_{X\mid Y=1}\),
\(E[X]\), \(E[Y]\), the covariance matrix of \((X,Y)^T\), the correlation,
and determine whether \(X\) and \(Y\) are independent. The final subpart asks
them to calculate the mean and variance of \(2X-Y\) two ways.

#### Problem 2 -- Colab study: an ensemble as a random vector (75 points)

The recommended default is the legacy B--H curve ensemble, with the field grid
downsampled before covariance calculations. Students:

1. load the frozen data and plot a reproducible subset of curves;
2. compute and plot the pointwise sample mean and standard deviation;
3. choose 25 supplied field locations and form the corresponding random vector;
4. visualize its covariance and correlation matrices and interpret two strong
   dependencies;
5. define two supplied linear functionals (an average response and a fixed
   quadrature-weighted path integral), predict their means/covariances using
   matrix formulas, and verify them from the ensemble;
6. compare dependence between two nearby field locations with dependence
   between two widely separated locations and give a physical interpretation.

The notebook directly supplies the downsampled vector representation. It does
not ask students to reason about covariance rank or SVD before Lecture 18.

**Dataset decision D2:**

- **D2-A (legacy/default): B--H curves.** Best alignment with random vectors
  and closest to the old homework. Before release, document the origin and
  redistribution status of `B_data.csv`.
- **D2-B (modern/open): UCI gas-turbine CO/NOx emissions.** CC BY 4.0,
  DOI 10.24432/C5WC95. Use one yearly CSV and treat selected sensor/emissions
  columns as a random vector. This is easier to document but loses the
  function-valued engineering example.

---

### HW3 -- Monte Carlo uncertainty propagation

**Coverage:** Lectures 7--10<br>
**Due:** Sunday, September 13, 11:59 p.m. ET<br>
**Legacy material retained:** damped-oscillator uncertainty propagation from
old HW3.

#### Problem 1 -- Manual mathematics: inverse sampling and Monte Carlo error (25 points)

Let \(U\sim\mathrm{Uniform}(0,1)\) and \(Y=U^2\). Students derive the CDF and
quantile function of \(Y\), \(E[Y]\), \(\operatorname{Var}(Y)\), and the
standard error of a Monte Carlo estimate of \(E[Y]\). They then determine the
sample size required for a stated 95% normal-approximation half-width. The
variance convention is explicitly \(N^{-1}\sum_i(Y_i-\bar Y)^2\), matching the
lecture.

#### Problem 2 -- Colab study: oscillator uncertainty (75 points)

Use a supplied `solve_ivp` damped-oscillator solver for a reference trajectory
and a tested, vectorized closed-form evaluator for the Monte Carlo loop, with
independent uncertain stiffness and damping. Students:

1. generate inputs using a local seeded NumPy generator;
2. propagate \(N=100,500,2000\) samples in `FAST_MODE` or use a supplied
   vectorized/parallel wrapper;
3. estimate the mean and standard error of a specified displacement-based
   quantity of interest;
4. estimate an exceedance probability and one output quantile;
5. use 30 independent repeated runs at each sample size to demonstrate the expected
   \(N^{-1/2}\) scaling of estimator variability rather than claiming that one
   realized error must decrease monotonically;
6. compare against a supplied high-accuracy reference and explain whether the
   reported Monte Carlo interval measures input uncertainty or estimator
   uncertainty.

No download or nonstandard package is required. The complete vectorized path,
including all repeated runs, must be benchmarked below five minutes on a free
Colab CPU before release.

---

### HW4 -- Prior information and Bayesian earthquake rates

**Coverage:** Lectures 11--12<br>
**Due:** Sunday, September 20, 11:59 p.m. ET<br>
**Legacy material retained:** the Southern California earthquake-rate problem
from old HW1/HW3, corrected and updated.

#### Problem 1 -- Manual mathematics: Gamma--Poisson updating (25 points)

The notebook explicitly supplies the shape--rate Gamma density, the Poisson
exposure likelihood, and the relevant Gamma integral. For \(n\) Poisson counts
observed over equal exposure intervals and a shape--rate Gamma prior on the event
rate, students use Bayes' rule to derive the posterior
distribution, posterior mean, posterior mode (with its existence condition),
and the posterior-predictive probability of zero events in the next interval.
They must identify where the exposure duration enters the update.

#### Problem 2 -- Colab study: major-earthquake risk (75 points)

Use an instructor-frozen CSV from the official USGS catalog query for Southern
California earthquakes above a stated magnitude threshold. Students:

1. load the snapshot and reproduce annual or decadal counts;
2. justify the count/exposure representation and note one limitation of a
   stationary Poisson process;
3. compare a weak prior and a supplied domain-informed prior;
4. plot prior, posterior, and posterior-predictive distributions;
5. calculate the probability of at least one qualifying earthquake over 10 and
   20 years, carrying parameter uncertainty through the predictive calculation;
6. perform a small prior-sensitivity analysis and make a risk-communication
   statement that distinguishes expected count from event probability.

The released data are a frozen snapshot, not a live USGS request, because
catalog records may be revised. The data README records query, threshold,
retrieval date, and checksum.

---

### HW5 -- Least squares and Bayesian elastic-modulus inference

**Coverage:** Lectures 13--15<br>
**Due:** Sunday, September 27, 11:59 p.m. ET<br>
**Legacy material retained:** the stress--strain study from old HW4.

#### Problem 1 -- Manual mathematics: zero-intercept linear regression (25 points)

For known \(s^2\) and \(\sigma_i=E\epsilon_i+e_i\),
\(e_i\stackrel{iid}{\sim}N(0,s^2)\),
students derive the least-squares estimator of \(E\). With
\(E\sim N(m_0,s_0^2)\), they then derive the Gaussian posterior mean and
variance and show the limiting behavior as \(s_0^2\to\infty\) and as the
measurement noise tends to zero, assuming \(\sum_i\epsilon_i^2>0\).

#### Problem 2 -- Colab study: where is Hooke's law defensible? (75 points)

Use the legacy stress--strain data. Students:

1. visualize the complete loading curve and identify candidate linear ranges;
2. fit classical and Bayesian zero-intercept models on a supplied initial
   range;
3. show residuals against strain and check whether the linear/noise assumptions
   remain plausible as the range expands;
4. compute posterior and posterior-predictive intervals;
5. select among prespecified strain cutoffs using the next five higher-strain
   observations as validation data: require at least four of five observations
   inside the 95% posterior-predictive intervals and a mean signed residual no
   larger than one supplied measurement-noise standard deviation; choose the
   largest cutoff that passes both checks;
6. report the elastic modulus with units and uncertainty, distinguishing
   parameter uncertainty from prediction uncertainty.

**Dataset decision D5:**

- **D5-A (legacy/default): stress--strain.** Strongest physical interpretation
  and direct continuity with the old assignment.
- **D5-B (modern/open): UCI Energy Efficiency.** CC BY 4.0,
  DOI 10.24432/C51307. Use one load response and three or four design variables.
  This supports multivariable Bayesian regression but gives up the clean
  modulus interpretation.

---

### HW6 -- Classification and clustering of manufacturing faults

**Coverage:** Lectures 16--17<br>
**Due:** Sunday, October 11, 11:59 p.m. ET<br>
**Legacy ideas retained:** logistic classification from the Challenger study
and clustering from old HW5, combined into one coherent application rather than
two unrelated datasets.

#### Problem 1 -- Manual mathematics: cost-sensitive classification (25 points)

Students derive the Bernoulli logistic log likelihood for one observation and
its gradient with respect to the linear predictor. Given false-negative cost
\(C_{FN}\) and false-positive cost \(C_{FP}\), they derive the probability
threshold that minimizes conditional expected loss and evaluate one small
confusion-matrix example.

#### Problem 2 -- Colab study: steel-plate fault discovery (75 points)

Use a frozen subset of the UCI Steel Plates Faults dataset (CC BY 4.0,
DOI 10.24432/C5J88N). Define one specified fault class versus all others and
use \(k=2\) for the unsupervised comparison. Students:

1. inspect class balance and define one-vs-rest target before splitting;
2. create train/validation/test partitions and fit scaling only on training
   data;
3. fit logistic regression and compare the 0.5 threshold with the threshold
   implied by supplied costs;
4. report confusion matrices and one proper probabilistic score;
5. fit `k`-means on training features without labels, assign validation/test
   clusters using the fitted centroids, and compare the binary clusters with
   the same held-out binary target using adjusted Rand index;
6. inspect cases on which the supervised and unsupervised views disagree and
   state what clustering can and cannot establish about fault types.

**Dataset decision D6:**

- **D6-A (modern/default): steel-plate faults.** One dataset naturally connects
  classification and clustering and avoids the Challenger extrapolation issue.
- **D6-B (legacy): Challenger logistic regression plus a small synthetic
  clustering companion.** More historically familiar, but less coherent and
  requires very careful treatment of the 31-degree extrapolation.

---

### HW7 -- Principal components and low-rank reconstruction

**Coverage:** Lecture 18<br>
**Due:** Sunday, October 18, 11:59 p.m. ET<br>
**Legacy idea retained:** dimensionality reduction, with the old full covariance
calculation replaced by SVD/low-rank methods.

#### Problem 1 -- Manual mathematics: a complete two-dimensional PCA (25 points)

For a supplied centered four-point dataset and the convention
\(C=n^{-1}X_c^T X_c\), students calculate the covariance matrix, its two
eigenpairs, principal-component scores, explained-variance fractions, and the
rank-one reconstructions. They verify that the **mean per-observation** squared
reconstruction error equals the discarded eigenvalue and explain the sign
indeterminacy of an eigenvector.

#### Problem 2 -- Colab study: low-rank reconstruction (75 points)

The recommended application is a public brain-MRI volume. Treat the ten slices
as observations and the image pixels as features, center each feature across
slices, and compute PCA through the economy SVD of the centered
slice-by-pixel matrix. Students:

1. load a small fixed volume or slice and inspect dimensions/intensity scale;
2. center the chosen image/stack and compute an economy SVD;
3. reconstruct at supplied ranks and plot error and compression ratio versus
   rank;
4. compare a visually convincing reconstruction with a quantitative criterion;
5. add a seeded noise perturbation and determine whether simple truncation
   improves reconstruction;
6. explain which image features are lost first and why good appearance is not a
   complete validation.

**Dataset decision D7 (required):**

- **D7-A (recommended): public brain MRI.** Vendor the pinned small brain TIFF
  used by `skimage.data.brain()` rather than relying on its dynamic downloader.
  Call this **low-rank MRI reconstruction**, not SMURF.
- **D7-B: legacy B--H functional PCA.** Strong engineering continuity and
  reuses HW2 data; use SVD of the centered ensemble rather than a full field
  covariance eigendecomposition.
- **D7-C: UCI Robot Execution Failures.** CC BY 4.0,
  DOI 10.24432/C5M89N; use force/torque time traces. This is the clearest
  engineering modernization but less visually immediate.

---

### HW8 -- State-space models and Kalman filtering

**Coverage:** Lectures 19--20<br>
**Due:** Sunday, October 25, 11:59 p.m. ET<br>
**Legacy material retained:** the Kalman oscillator from old HW5, connected to
the HW3 forward model.

#### Problem 1 -- Manual mathematics: one Kalman step (25 points)

Students convert a damped oscillator to first-order state-space form, use a
specified discrete transition/observation model, and carry out one numerical
prediction and update: predicted mean/covariance, innovation, innovation
variance, gain, and updated mean/covariance. They check covariance symmetry and
interpret the limiting behavior as measurement noise tends to zero.

#### Problem 2 -- Colab study: filtering the uncertain oscillator (75 points)

Reuse the HW3 oscillator geometry with fixed nominal stiffness and damping and
a supplied linear discretization. Parameter uncertainty from HW3 is not carried
into the ordinary Kalman filter; unmodeled disturbances are represented by the
stated process covariance \(Q\). Students:

1. generate one hidden trajectory and noisy position measurements with distinct
   fixed random streams;
2. complete a supplied Kalman-filter loop;
3. plot truth, observations, filtered state, and uncertainty bands;
4. report state RMSE and the fraction of time points for which the single hidden
   trajectory lies inside the displayed intervals, explicitly noting that this
   is not a repeated-sampling coverage study;
5. repeat with process noise under- and over-specified by a fixed factor;
6. use innovations to diagnose the misspecification and explain why the smoothest
   trajectory is not automatically the best estimate.

No external data or nonstandard dependency is required. A real fan-vibration
dataset can be offered as an ungraded extension, but it should not replace the
synthetic truth needed for validation.

---

### HW9 -- Gaussian-process prediction for ultrasonic calibration

**Coverage:** Lectures 21--22<br>
**Due:** Sunday, November 1, 11:59 p.m. ET<br>
**Selected modern dataset:** NIST Chwirut1 ultrasonic calibration data.

#### Problem 1 -- Manual mathematics: GP conditioning (25 points)

For two noisy training observations, one test location, a specified
squared-exponential kernel, and specified mean/noise parameters, students write
the joint Gaussian distribution and calculate the posterior predictive mean and
both (i) latent-function variance and (ii) future noisy-observation variance.
They check units, symmetry, nonnegative variance, and the zero-observation-noise
interpolation limit for the latent function at a training location.

#### Problem 2 -- Colab study: interpolation and extrapolation (75 points)

Use NIST's 214-observation Chwirut1 study of ultrasonic response versus metal
distance. Students:

1. inspect the 22 heavily replicated distance settings and plot empirical
   mean and sample variability by distance;
2. hold out every replicate at distances 2.25, 2.50, and 2.75 for interpolation,
   and every row with distance at least 5.0 for extrapolation;
3. use supplied Cholesky-based GP helpers, training-only response
   standardization, and fixed jitter to compare squared-exponential and
   Matern-3/2 kernels;
4. fit amplitude, length scale, and constant observation noise by marginal
   likelihood with one bounded optimization per kernel;
5. report RMSE, Gaussian negative log predictive density, and 95% noisy-
   observation interval fraction separately for the two holdouts;
6. use the replicated measurements to critique the stationary,
   homoscedastic-noise model.

The notebook downloads the official NIST ASCII file at runtime and verifies a
fixed SHA-256 checksum. It does not redistribute the source data because the
dataset page does not state an explicit redistribution license. NIST does not
state physical units, so the notebook labels both variables as NIST-reported
units rather than inventing them.

---

### HW10 -- Bayesian optimization for model calibration

**Coverage:** Lecture 23 plus assigned model-calibration material<br>
**Due:** Sunday, November 15, 11:59 p.m. ET<br>
**Legacy material retained:** catalytic-reaction data/solver and Forrester
Bayesian optimization from old HW4/HW6.

#### Problem 1 -- Manual mathematics: expected improvement (25 points)

For a noiseless Gaussian predictive distribution of a scalar loss and incumbent
\(f_{min}\), defined as the smallest observed loss, students derive expected
improvement for minimization and evaluate it at two candidate points. They show
that its \(\sigma\to0\) limit is \(\max(f_{min}-\mu,0)\), including both cases,
and explain exploitation and exploration in the two terms.

#### Problem 2 -- Colab study: calibrating a catalytic-reaction model (75 points)

Use the small legacy catalysis data and a supplied, tested `solve_ivp` forward
model. Students:

1. define a weighted data-misfit objective for two calibration parameters;
2. inspect a coarse supplied reference surface without using it in the
   optimization loop;
3. begin from a fixed small design, fit a GP surrogate, and carry out a bounded
   number of expected-improvement steps;
4. log every expensive model evaluation and compare the selected parameter with
   a dense reference optimum supplied only after the run;
5. visualize surrogate uncertainty and the acquisition function at selected
   iterations;
6. check residuals at the calibrated parameter and explain why minimizing data
   misfit is not the same as proving parameter identifiability.

**Design decision D10 (required):**

- **D10-A (recommended if the calibration background is ready): catalysis
  calibration plus Bayesian optimization.** Best scientific integration.
- **D10-B (safe fallback): the one-dimensional Forrester function.** Easier and
  fully covered by Lecture 23, but it is an optimization demonstration rather
  than a calibration study.

Because the current syllabus labels model-calibration videos as material still
to be recorded, D10-A must include a self-contained two-page background section
and complete forward-model scaffold if those videos are not available.

---

### HW11 -- Deep neural-network regression

**Coverage:** Lectures 24--25<br>
**Due:** Sunday, November 22, 11:59 p.m. ET<br>
**Legacy material retained:** airfoil self-noise neural regression from old HW7,
with leakage and test-set reuse corrected.

#### Problem 1 -- Manual mathematics: one neural-network update (25 points)

For a one-input, one-hidden-unit `tanh` network and squared loss, students carry
out a numerical forward pass, calculate the parameter count, and derive the
loss derivative with respect to the network output. The problem then supplies
the parameter-gradient vector and asks students to perform and check one
specified SGD update. Full backpropagation is not required because it is not in
the assigned lecture material.

#### Problem 2 -- Colab study: airfoil-noise prediction (75 points)

Use a frozen UCI Airfoil Self-Noise dataset (CC BY 4.0,
DOI 10.24432/C5VW2C). Students:

1. create train/validation/test splits before fitting scalers;
2. fit a supplied linear baseline and a compact dense network;
3. use validation data for early stopping/hyperparameter choice and touch the
   test set once at the end;
4. compare RMSE and residual structure, not training loss alone;
5. show one learning curve and one prediction diagnostic;
6. identify a region of input space with sparse training support and discuss
   whether the neural network's output there is trustworthy.

Use one compact CPU-only model in a deep-learning stack already present in
Colab; do not install a second framework. Seed the data split and initialization
where supported, and grade with tolerances rather than exact final weights.

**Dataset decision D11:**

- **D11-A (legacy/default): UCI Airfoil.** Small, engineering-centered, and
  suitable for a CPU runtime.
- **D11-B (visual alternative): Fashion-MNIST.** Compare a dense network with a
  small CNN. This covers image structure but is a more conventional assignment
  and requires a larger download.
- **D11-C (research-inspired alternative): coordinate MLP on public brain MRI.**
  Interesting connection to neural fields, but it does not naturally exercise
  CNN material.

---

### HW12 -- Physics-informed flow reconstruction

**Coverage:** Lecture 26 plus assigned PIV/application material<br>
**Due:** Sunday, November 29, 11:59 p.m. ET<br>
**Legacy idea retained:** physics-informed modeling, redesigned as a small,
strongly scaffolded study suitable for Thanksgiving week.

The following detailed problem design assumes the recommended D12-A option. If
D12-B or D12-C is selected, both the mathematics and metrics must be rewritten
for that branch rather than mixing incompatible flow models.

#### Problem 1 -- Manual mathematics: Poiseuille data and physics residuals (25 points)

All variables are nondimensionalized in the prompt. For axial velocity
\(w(x,y)\) in a circular cross-section, students derive the nondimensional
Poisson residual \(r_{pde}=-\nabla^2w-g\), the no-slip boundary residual, and
the composite objective

\[
L(\theta)=L_{data}(\theta)+\lambda_{phys}L_{phys}(\theta)
             +\lambda_{bc}L_{bc}(\theta).
\]

The data term is defined as
\(L_{data}=\|H[w_\theta]-y\|^2/n\), where the supplied linear operator \(H\)
applies the same blur/sampling process used to generate the observations.
Students evaluate each residual for the analytical Poiseuille field, verify
that every term is dimensionless, and identify one field that fits sparse data
but violates the governing equation.

#### Problem 2 -- Colab study: sparse flow-field reconstruction (75 points)

Students receive a complete compact coordinate-network trainer and modify only
the residual/loss and a small set of experiment controls. The field is
32-by-32, the collocation set and epoch cap are fixed, and the supplied
data-only baseline predictions are loaded rather than retrained. Students:

1. inspect sparse/noisy observations and the hidden reference grid;
2. fit one physics-informed model and compare it with the supplied data-only
   baseline;
3. report velocity error, Poisson-equation residual, and no-slip error;
4. compare both models on locations withheld in space, not only the training
   points;
5. run one short, lower-epoch sensitivity calculation at a second physics weight
   and explain the data--physics tradeoff;
6. state what this toy result does and does not imply for experimental PIV or
   4-D-flow MRI.

**Design decision D12 (required):**

- **D12-A (recommended research connection): synthetic SMURF-inspired
  Poiseuille flow MRI.** Generate a small 32-by-32 circular flow field, blur and
  corrupt seeded measurements, and reconstruct the axial velocity with a compact
  coordinate MLP. Use the fully developed-flow Poisson equation and no-slip
  condition as the physics/boundary residuals. It has exact ground truth and no
  data-license problem. It must be labeled **SMURF-inspired**, not a reproduction
  of SMURF: the connection is the coordinate-field/measurement-model idea, while
  the added physics loss belongs to this course exercise rather than the
  published SMURF objective.
- **D12-B (closest to listed application): PIV Challenge Case B1.** Use the two
  small CC0 images from `skimage.data.vortex()` and provide either precomputed
  coarse vectors or the correlation solver; students should not spend the week
  installing/debugging OpenPIV.
- **D12-C (lowest-risk): manufactured Taylor--Green vortex.** Synthetic
  particles/measurements, exact field, and the cleanest PDE validation, but less
  direct connection to the instructor's current research.

An actual SMURF clinical-data assignment is not proposed: no openly licensed
public course dataset or public implementation was located, and the full model
described in the paper is not an appropriate dependency/runtime assumption for
all free Colab users.

---

### HW13 -- Sampling and variational approximation

**Coverage:** Lectures 27--28<br>
**Due:** Sunday, December 6, 11:59 p.m. ET<br>
**Legacy material retained:** Challenger O-ring data from old HW4/Lecture 27 and
the variational-diagnostics style of old HW8, substantially reduced in size.

#### Problem 1 -- Manual mathematics: two approximations to one posterior (25 points)

For a specified correlated two-dimensional Gaussian target
\(p=N(\mu,\Sigma)\) and a symmetric Gaussian random-walk proposal, students
derive the Metropolis--Hastings acceptance ratio and
\(D_{KL}(q\|p)\) for a diagonal Gaussian \(q\). They find the reverse-KL
mean-field optimum
\(m=\mu\), \(d_i=1/(\Sigma^{-1})_{ii}\), and explain which posterior
dependence it cannot represent. These are two parts of one mathematical
comparison, not separate problems.

#### Problem 2 -- Colab study: Challenger logistic-posterior inference (75 points)

Use the small frozen Challenger O-ring dataset and a Bayesian logistic model for
intercept and temperature slope. The notebook supplies a normalized dense-grid
reference, a pure NumPy/SciPy random-walk Metropolis framework, and a
deterministic quadrature objective for diagonal-Gaussian variational inference.
Students:

1. inspect the data and write the Bernoulli-logistic posterior up to a
   normalizing constant;
2. complete and tune one bounded component of the supplied Metropolis sampler;
3. optimize the supplied mean-field VI objective from fixed initializations;
4. compare MCMC and VI posterior means, marginal intervals, covariance, and
   contour plots against the hidden-until-evaluation grid reference;
5. use trace, acceptance-rate, and effective-sample diagnostics for MCMC and
   objective/convergence plus posterior predictive checks for VI;
6. explain the lost dependence and any underdispersion, then discuss why a
   prediction at 31 degrees Fahrenheit is a hazardous extrapolation rather than
   treating it as established fact.

This default uses only NumPy/SciPy/Matplotlib and avoids a discrete variational
factor or a brittle probabilistic-programming install. The coal changepoint can
remain an optional lecture extension, but is not the required comparison.

## Decisions needed before student notebooks are written

Only three decisions materially change the structure and should be made first:

1. **D7:** public brain-MRI SVD/PCA, legacy B--H functional PCA, or robot
   force/torque PCA?
2. **D10:** catalytic-model calibration plus Bayesian optimization, or the
   simpler Forrester study?
3. **D12:** synthetic SMURF-inspired flow MRI, PIV Challenge, or manufactured
   Taylor--Green flow?

The other defaults are deliberately conservative and can be changed later:
D2-A (B--H), D5-A (stress--strain), D6-A (steel faults), D11-A (airfoil), and
the Challenger posterior for HW13.

## Data artifacts to prepare after the decisions

Create a small `lecturebook/data/homework/` directory containing only frozen
course artifacts. For every artifact add a row to `SOURCES.md` with source URL,
DOI when applicable, license/provenance, retrieval date, preprocessing script,
and SHA-256. Student notebooks should fetch raw files from the stable GitHub
Pages/raw-GitHub course location and verify the checksum before analysis. Use an
immutable release tag or commit in the download URL rather than the moving
default branch. Package a multi-file source, such as the two PIV images plus
coarse vectors, as one small archive.

Before release, explicitly clear the provenance/redistribution status of the
legacy B--H, stress--strain, catalysis, Challenger, and coal files. If a legacy
file cannot be documented, replace it with the listed open dataset or a frozen
synthetic fixture. For UCI derivatives, retain CC BY 4.0 attribution and state
the preprocessing; also retain the requested NOAA, USGS, Stanford-MRI, and PIV
acknowledgements.

All notebooks will be executed locally from a locked `uv` environment. The
neural-network and autodiff notebooks must additionally be run once in a fresh
Colab CPU runtime because a local environment cannot certify Colab's
preinstalled framework versions.

The actual student notebooks should be generated only after D7, D10, and D12
are selected. This prevents three rounds of mutually incompatible starter code
and makes it possible to test all 13 notebooks end-to-end in fresh Colab-like
environments before release.

## Candidate source links for the instructor review

- USGS earthquake catalog API:
  <https://earthquake.usgs.gov/fdsnws/event/1/>
- UCI Gas Turbine CO and NOx Emission Data Set:
  <https://archive.ics.uci.edu/dataset/551/gas+turbine+co+and+nox+emission+data+set>
- UCI Energy Efficiency:
  <https://archive.ics.uci.edu/dataset/242/energy+efficiency>
- UCI Steel Plates Faults:
  <https://archive.ics.uci.edu/dataset/198/steel+plates+faults>
- UCI Robot Execution Failures:
  <https://archive.ics.uci.edu/dataset/138/robot+execution+failures>
- UCI Airfoil Self-Noise:
  <https://archive.ics.uci.edu/dataset/291/airfoil+self+noise>
- NIST Chwirut1 ultrasonic calibration data:
  <https://www.itl.nist.gov/div898/strd/nls/data/chwirut1.shtml>
- Public MR head volume used by the scikit-image brain dataset:
  <https://graphics.stanford.edu/data/voldata/>
- PIV Challenge:
  <https://www.pivchallenge.org/>
- SMURF preprint:
  <https://arxiv.org/abs/2505.12494>
- Published SMURF article and code-availability statement:
  <https://www.sciencedirect.com/science/article/pii/S1361841526002999>
- Predictive Science Laboratory SMURF project page:
  <https://predictivesciencelab.org/project/smurf-unsupervised-flow-reconstruction-from-4d-flow-mri/>
