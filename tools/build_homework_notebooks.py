#!/usr/bin/env python3
"""Build the ten Fall 2026 student-facing homework notebook drafts.

Complete drafts contain one manual-mathematics problem and one scaffolded
Colab study.  Homework 5, 8, and 10 intentionally remain review placeholders
until their rolled-forward material is consolidated.  The notebooks contain
prompts and infrastructure, not solutions.
"""

from __future__ import annotations

import hashlib
from copy import deepcopy
from pathlib import Path
import re
from textwrap import dedent

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
HOMEWORK = ROOT / "lecturebook" / "homework"


def markdown(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(dedent(text).strip() + "\n")


def code(text: str = "# YOUR CODE HERE") -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(dedent(text).strip() + "\n")


def response(prompt: str = "Replace this text with your work.") -> nbf.NotebookNode:
    cell = markdown(f"> **Response:** {prompt}")
    cell.metadata["tags"] = ["student-work"]
    return cell


def work_cell() -> nbf.NotebookNode:
    return work_code("# YOUR CODE HERE")


def work_code(text: str) -> nbf.NotebookNode:
    cell = code(text)
    cell.metadata["tags"] = ["student-work"]
    return cell


def opening(number: int, title: str, coverage: str, due: str) -> list[nbf.NotebookNode]:
    return [
        markdown(
            f"""
            # Homework {number} — {title}

            **Coverage:** {coverage}<br>
            **Due:** {due}, 11:59 p.m. ET<br>
            **Total:** 100 points

            ## Instructions

            - Complete this notebook in Google Colab.
            - Problem 1 is a manual mathematics problem. Show every important
              step in Markdown/LaTeX, or insert one clearly legible image of
              your handwritten derivation. Code may check arithmetic only
              after the derivation is complete.
            - Problem 2 is a scaffolded scientific-computing study. Use the
              supplied random seeds and do not delete setup, helper, or check
              cells.
            - Your submitted notebook must run from beginning to end in a
              fresh Colab runtime without Google Drive, absolute paths, or
              additional package installation.
            - Label plots and include documented units. If a legacy dataset
              has no documented units, label the quantity as normalized or
              unit-unspecified rather than inventing units. Unless stated
              otherwise, report numerical answers to at least four
              significant digits.

            ## Student details

            - **First name:**
            - **Last name:**
            - **Purdue email:**
            """
        )
    ]


def data_setup(number: int, extra_imports: str = "") -> nbf.NotebookNode:
    return code(
        f"""
        from pathlib import Path

        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        {extra_imports}

        SEED = 539{number:02d}
        rng = np.random.default_rng(SEED)
        sns.set_theme(style="ticks", context="notebook")
        plt.rcParams["figure.dpi"] = 120
        np.set_printoptions(precision=6, suppress=True)

        # During drafting this points to master. Before release, the instructor
        # will replace DATA_REVISION with the immutable course release tag.
        DATA_REVISION = "master"
        DATA_BASE = (
            "https://raw.githubusercontent.com/PredictiveScienceLab/"
            f"data-analytics-se/{{DATA_REVISION}}/lecturebook/data/homework"
        )

        def course_data(name):
            local_candidates = [
                Path("../data/homework") / name,
                Path("lecturebook/data/homework") / name,
            ]
            for local in local_candidates:
                if local.exists():
                    return local
            return f"{{DATA_BASE}}/{{name}}"
        """
    )


def make_notebook(number: int, cells: list[nbf.NotebookNode]) -> nbf.NotebookNode:
    notebook = nbf.v4.new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.11"},
        },
    )
    for index, cell in enumerate(notebook.cells):
        token = f"homework-{number:02d}-{index}-{cell.cell_type}".encode()
        cell.id = hashlib.sha1(token).hexdigest()[:8]
    nbf.validate(notebook)
    return notebook


def homework_01() -> nbf.NotebookNode:
    cells = opening(
        1, "Probability and Mechanical Reliability", "Lectures 1–4",
        "Sunday, August 30, 2026",
    )
    cells += [
        code(
            """
            import numpy as np
            import matplotlib.pyplot as plt
            from scipy import integrate, stats

            SEED = 53901
            rng = np.random.default_rng(SEED)
            plt.style.use("seaborn-v0_8-whitegrid")
            np.set_printoptions(precision=6, suppress=True)
            """
        ),
        markdown(
            r"""
            ## Problem 1 — Bayes' rule and test design (25 points)

            A disease has prevalence \(P(D)=0.004\). A diagnostic test has
            sensitivity \(P(+\mid D)=0.80\) and specificity
            \(P(-\mid D^c)=0.90\).

            1. **Probability tree (5 points).** Draw the complete two-stage
               probability tree. Label every branch and calculate the four
               joint probabilities at its leaves.
            2. **Reverse conditionals (8 points).** Starting from Bayes' rule,
               derive and calculate \(P(D\mid +)\) and \(P(D\mid -)\). Show
               the numerator and denominator in both calculations.
            3. **Interpretation (4 points).** Explain numerically why the
               positive predictive value remains small even though a positive
               result is evidence in favor of disease.
            4. **Test design (8 points).** Keep the prevalence fixed and raise
               sensitivity to \(0.99\). Let \(q=P(+\mid D^c)\). Derive the
               largest \(q\) for which \(P(D\mid+)\ge0.90\), and report the
               corresponding minimum specificity.
            """
        ),
        response(),
        markdown(
            r"""
            ## Problem 2 — Weibull gear reliability (75 points)

            Eight nominally identical gears were tested to failure. Their
            lifetimes are given below in years. Model lifetime \(T\) with the
            two-parameter Weibull distribution

            \[
            f(t)=\frac{k}{\lambda}\left(\frac{t}{\lambda}\right)^{k-1}
            \exp\!\left[-\left(\frac{t}{\lambda}\right)^k\right],\qquad
            S(t)=\exp\!\left[-\left(\frac{t}{\lambda}\right)^k\right].
            \]

            The fitting call is supplied; maximum-likelihood theory is not
            assessed this week.
            """
        ),
        code(
            """
            failure_times_years = np.array(
                [10.5, 7.5, 8.1, 8.4, 11.2, 9.3, 8.9, 12.4], dtype=float
            )
            shape_hat, location_hat, scale_hat = stats.weibull_min.fit(
                failure_times_years, floc=0.0
            )
            gear_model = stats.weibull_min(shape_hat, loc=0.0, scale=scale_hat)
            print("The two-parameter Weibull fit is ready for analysis.")
            """
        ),
        markdown(
            """
            ### 2.1 Empirical and fitted survival (15 points)

            Make one figure containing the no-censoring empirical survival
            curve, the fitted Weibull survival curve, and a rug or marker for
            every observed lifetime. Describe where agreement is weakest.
            """
        ),
        work_cell(),
        response("Describe the most visible agreement or disagreement."),
        markdown(
            r"""
            ### 2.2 Parameters and reliability quantities (20 points)

            Report \(k\) and \(\lambda\), including units. Then calculate the
            mean, median, \(P(8<T<10)\), and the first-percentile lifetime
            \(t_{0.01}\). Explain operationally what \(t_{0.01}\) means.
            """
        ),
        work_cell(),
        response(),
        markdown(
            r"""
            ### 2.3 Probability-model checks (15 points)

            Implement the Weibull PDF, CDF, and survival formulas yourself
            (do not call the corresponding SciPy methods). Verify numerically
            that the density integrates to one, that \(F(t)+S(t)=1\) at
            \(t=6,9,12\), and that all three functions agree with `gear_model`
            at those times. Report the largest discrepancy.
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.4 Replacement decision (15 points)

            A proposal replaces each gear at age 8 years. The fitted
            probability of failure before replacement must not exceed 0.10.
            Calculate the risk, decide whether the proposal passes, and—if it
            fails—calculate the latest replacement age satisfying the target.
            """
        ),
        work_cell(),
        response("State the decision and the numerical evidence."),
        markdown(
            """
            ### 2.5 Limitation (10 points)

            State one specific reason why eight run-to-failure observations
            are insufficient for a high-consequence maintenance decision and
            identify additional data or experimental information that would
            address it. Use no more than four sentences.
            """
        ),
        response(),
    ]
    return make_notebook(1, cells)


def homework_02() -> nbf.NotebookNode:
    cells = opening(
        2, "Dependence and Random Vectors in Engineering Data", "Lectures 5–6",
        "Sunday, September 6, 2026",
    )
    cells += [
        data_setup(2),
        markdown(
            r"""
            ## Problem 1 — A joint PMF and a linear combination (25 points)

            Let \(X\in\{-1,0,2\}\) and \(Y\in\{0,1\}\) have joint PMF

            \[
            \begin{array}{c|cc}
             &Y=0&Y=1\\ \hline
            X=-1&0.10&0.15\\
            X=0 &0.20&0.10\\
            X=2 &0.15&0.30
            \end{array}.
            \]

            1. Verify normalization and find both marginal PMFs. **(4)**
            2. Find the complete conditional PMF \(p_{X\mid Y=1}\). **(3)**
            3. Calculate \(E[X]\) and \(E[Y]\). **(3)**
            4. Calculate \(E[X^2]\), \(E[Y^2]\), \(E[XY]\), the covariance
               matrix of \((X,Y)^T\), and their correlation. **(7)**
            5. Decide whether \(X\) and \(Y\) are independent using an explicit
               joint-versus-product comparison. **(3)**
            6. For \(W=2X-Y\), calculate \(E[W]\) and \(\operatorname{Var}(W)\)
               both by enumerating outcomes and by using the mean vector and
               covariance matrix. **(5)**
            """
        ),
        response(),
        markdown(
            """
            ## Problem 2 — A B–H curve ensemble as a random vector (75 points)

            Each row of the supplied course dataset is one course-supplied
            curve realization. Columns are common acquisition-grid locations.
            The historical file does
            not preserve the physical applied-field values, so we use a
            dimensionless normalized coordinate \(u\in[0,1]\) and do not
            invent physical units for that axis.

            **Data note:** this is a legacy course asset whose original
            provenance and redistribution status are still being documented;
            do not redistribute it outside this course.
            """
        ),
        code(
            """
            curves_frame = pd.read_csv(course_data("hw02_bh_curves.csv"))
            sample_id = curves_frame.pop("sample_id").to_numpy()
            B = curves_frame.to_numpy(dtype=float)
            u = np.linspace(0.0, 1.0, B.shape[1])
            assert B.shape == (200, 150)
            print("Ensemble shape:", B.shape)
            """
        ),
        markdown(
            """
            ### 2.1 Inspect the ensemble (10 points)

            Select 12 distinct rows with `rng.choice(..., replace=False)` and
            plot them against \(u\). Describe the variation shared by the
            ensemble and one feature that varies noticeably.
            """
        ),
        work_cell(),
        response(),
        markdown(
            r"""
            ### 2.2 Pointwise statistics (15 points)

            Calculate the pointwise sample mean and standard deviation using
            `ddof=1`. Plot the mean and a mean-plus-or-minus-one-standard-
            deviation band. Explain why this band describes curve-to-curve
            variability rather than uncertainty in the estimated mean.
            """
        ),
        work_cell(),
        response(),
        markdown(
            r"""
            ### 2.3 A 25-dimensional random vector (20 points)

            Use `grid_indices = np.linspace(5, 145, 25, dtype=int)` and define
            \(Z\) as the response at those 25 coordinates. Calculate its mean
            vector, sample covariance matrix, and correlation matrix. Display
            covariance and correlation as labeled heat maps. Verify covariance
            symmetry and positive semidefiniteness numerically.
            """
        ),
        code(
            """
            grid_indices = np.linspace(5, 145, 25, dtype=int)
            s25 = np.linspace(0.0, 1.0, 25)  # reparameterized retained range
            Z = B[:, grid_indices]
            assert Z.shape == (200, 25)
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.4 Nearby and separated coordinates (10 points)

            Compare covariance and correlation for retained coordinates
            `(12, 13)` and `(0, 24)`. Explain why correlation is the more direct
            comparison when marginal standard deviations differ.
            """
        ),
        work_cell(),
        response(),
        markdown(
            r"""
            ### 2.5 Linear engineering summaries (15 points)

            Reparameterize the retained coordinates by \(s\in[0,1]\). Define
            \(Q_1=25^{-1}\sum_j Z_j\) and
            \(Q_2=\int_0^1 sB(s)\,ds\), using trapezoidal weights on the 25
            retained coordinates. Write \(Q=AZ\). Predict \(E[Q]\) and
            \(\operatorname{Cov}(Q)\) using matrix formulas, then calculate
            both directly for all 200 curves. Require agreement to `1e-10` and
            interpret the two summaries and their correlation.
            """
        ),
        code(
            """
            average_weights = np.ones(25) / 25.0
            step = s25[1] - s25[0]
            integral_weights = step * s25.copy()
            integral_weights[[0, -1]] *= 0.5
            A = np.vstack([average_weights, integral_weights])
            assert A.shape == (2, 25)
            """
        ),
        work_cell(),
        response(),
        markdown(
            """
            ### 2.6 Scientific limitation (5 points)

            State one specific limitation of treating these 200 curves as the
            complete uncertainty model for future production. Address the
            sampling or physical process, not merely “measurement error.”
            """
        ),
        response(),
    ]
    return make_notebook(2, cells)


def homework_03() -> nbf.NotebookNode:
    cells = opening(
        3, "Monte Carlo Uncertainty Propagation", "Lectures 7–10",
        "Sunday, September 13, 2026",
    )
    cells += [
        code(
            """
            import numpy as np
            import matplotlib.pyplot as plt
            from scipy.integrate import solve_ivp

            SEED = 53903
            seed_sequence = np.random.SeedSequence(SEED)
            main_seed, repeated_seed = seed_sequence.spawn(2)
            rng_main = np.random.default_rng(main_seed)
            rng_repeated = np.random.default_rng(repeated_seed)
            plt.style.use("seaborn-v0_8-whitegrid")
            """
        ),
        markdown(
            r"""
            ## Problem 1 — Inverse sampling and Monte Carlo error (25 points)

            Let \(U\sim\operatorname{Uniform}(0,1)\) and \(Y=U^2\).

            1. Derive the complete piecewise CDF \(F_Y(y)\). **(6)**
            2. Derive \(F_Y^{-1}(p)\) and explain inverse-transform sampling. **(4)**
            3. Calculate \(E[Y]\), \(E[Y^2]\), and \(\operatorname{Var}(Y)\). **(7)**
            4. For \(\widehat\mu_N=N^{-1}\sum_iY_i\), derive its exact
               standard error and the plug-in estimate using
               \(\widehat v_N=N^{-1}\sum_i(Y_i-\widehat\mu_N)^2\). Find the
               smallest \(N\) giving a 95% normal-approximation half-width no
               greater than 0.01. **(8)**
            """
        ),
        response(),
        markdown(
            r"""
            ## Problem 2 — Monte Carlo propagation through a damped oscillator (75 points)

            Consider the one-kilogram oscillator

            \[
            \ddot y+C\dot y+Ky=0,\qquad y(0)=1\text{ m},\quad
            \dot y(0)=0\text{ m/s},
            \]

            with independent \(K\sim U(35,45)\) N/m and
            \(C\sim U(0.4,0.8)\) N s/m. The quantity of interest is
            \(Q=y(5\text{ s})\), measured in meters. A high-accuracy ODE solver and vectorized
            closed-form evaluator are supplied; deriving the closed form is
            not assessed.
            """
        ),
        code(
            """
            FINAL_TIME = 5.0

            def qoi_solve_ivp(k, c):
                def rhs(t, state):
                    y, velocity = state
                    return [velocity, -c * velocity - k * y]
                solution = solve_ivp(
                    rhs, (0.0, FINAL_TIME), [1.0, 0.0],
                    t_eval=[FINAL_TIME], rtol=1e-10, atol=1e-12,
                )
                return solution.y[0, -1]

            def qoi_closed_form(k, c):
                k = np.asarray(k, dtype=float)
                c = np.asarray(c, dtype=float)
                alpha = 0.5 * c
                omega_d = np.sqrt(k - alpha**2)
                return np.exp(-alpha * FINAL_TIME) * (
                    np.cos(omega_d * FINAL_TIME)
                    + alpha / omega_d * np.sin(omega_d * FINAL_TIME)
                )

            HIGH_ACCURACY_MEAN_REFERENCE = 0.10664762742989539

            def sample_inputs(local_rng, size):
                '''Complete this function to draw independent K and C.'''
                raise NotImplementedError("Draw the two specified uniforms.")
            """
        ),
        markdown(
            """
            ### 2.1 Validate the fast evaluator (10 points)

            At `(k,c) = (35,0.4), (40,0.6), (45,0.8)`, compare the two
            evaluators. Verify a maximum absolute discrepancy below `1e-8`
            and explain why this check must precede large Monte Carlo runs.
            """
        ),
        work_cell(),
        response(),
        markdown(
            r"""
            ### 2.2 Nested Monte Carlo estimates (20 points)

            Draw one sample of size 2,000. Use its first 100, first 500, and
            all 2,000 outputs for nested estimates. For each \(N\), report the
            mean, variance with denominator \(N\), estimated standard error,
            and 95% normal-approximation Monte Carlo interval for \(E[Q]\).
            Explain why realized errors need not decrease monotonically.
            """
        ),
        work_cell(),
        response(),
        markdown(
            r"""
            ### 2.3 Propagated output variability (15 points)

            With all 2,000 outputs, plot a normalized histogram and estimate
            \(P(Q>0.25)\), the 0.95 quantile, and the central empirical 95%
            interval. Explain why this interval is not a confidence interval
            for the mean.
            """
        ),
        work_cell(),
        response(),
        markdown(
            r"""
            ### 2.4 Demonstrate \(N^{-1/2}\) scaling (20 points)

            At each \(N\in\{100,500,2000\}\), perform 30 independent runs.
            Calculate the empirical standard deviation of the 30 mean
            estimates (denominator 30), make a log-log plot, add an anchored
            \(N^{-1/2}\) reference line, and fit the log-log slope. Check
            whether the supplied high-accuracy mean lies inside the single
            nested-sample \(N=2000\) interval from Section 2.2.
            """
        ),
        work_cell(),
        response(),
        markdown(
            """
            ### 2.5 Interpretation and limitation (10 points)

            In at most six sentences, distinguish Monte Carlo estimator
            uncertainty from input-propagated output variability and state one
            limitation of either the independent uniform inputs or the linear
            oscillator model.
            """
        ),
        response(),
    ]
    return make_notebook(3, cells)


def homework_04() -> nbf.NotebookNode:
    cells = opening(
        4, "Prior Information and Bayesian Earthquake Rates", "Lectures 11–12",
        "Sunday, September 20, 2026",
    )
    cells += [
        data_setup(4, "from scipy import stats"),
        markdown(
            r"""
            ## Problem 1 — Gamma–Poisson updating (25 points)

            Use the Gamma **shape-rate** density
            \[
            p(\lambda)=\frac{\beta^\alpha}{\Gamma(\alpha)}
            \lambda^{\alpha-1}e^{-\beta\lambda}
            \]
            and independent counts
            \(Y_i\mid\lambda\sim\operatorname{Poisson}(\lambda\Delta_i)\).

            1. Write the likelihood as a function of \(\lambda\) and state the
               units of \(\lambda\) and \(\beta\). **(5)**
            2. Derive the posterior and identify its updated shape and rate. **(8)**
            3. Derive the posterior mean and mode, including the condition for
               an interior mode. **(4)**
            4. For a future exposure \(\Delta_*\), derive
               \(P(Y_*=0\mid y)=[\beta_N/(\beta_N+\Delta_*)]^{\alpha_N}\),
               obtain \(P(Y_*\ge1\mid y)\), and verify its limiting behavior
               as \(\Delta_*\to0\) and \(\infty\). **(8)**
            """
        ),
        response(),
        markdown(
            r"""
            ## Problem 2 — Major-earthquake rate and risk (75 points)

            The frozen USGS ComCat extract contains earthquakes of magnitude
            at least 6.5 from 1900 through 2025 in the rectangular region
            \(32\le\mathrm{latitude}\le37\) N and
            \(-122\le\mathrm{longitude}\le-114\) degrees. It was retrieved on
            August 17, 2026 through the
            [USGS event API](https://earthquake.usgs.gov/fdsnws/event/1/).
            It is a teaching dataset, not an official forecast.
            """
        ),
        code(
            """
            events = pd.read_csv(
                course_data("hw04_southern_california_earthquakes.csv"),
                parse_dates=["time"],
            ).sort_values("time").reset_index(drop=True)
            YEARS = np.arange(1900, 2026)
            annual_counts = (
                events["time"].dt.year.value_counts()
                .reindex(YEARS, fill_value=0).sort_index().to_numpy()
            )
            assert annual_counts.shape == (126,)
            events.head()
            """
        ),
        code(
            """
            PRIORS = {
                "weak": {"alpha": 0.5, "beta": 0.5},
                "reference": {"alpha": 4.0, "beta": 32.0},
                "lower_rate": {"alpha": 2.0, "beta": 40.0},
            }

            def gamma_poisson_update(alpha, beta, counts, exposure_years):
                '''Return posterior shape and rate after students complete it.'''
                raise NotImplementedError

            def sample_future_counts(alpha_post, beta_post, horizon_years,
                                     n_samples=100_000, seed=SEED):
                '''Return posterior-predictive Poisson counts.'''
                raise NotImplementedError
            """
        ),
        markdown(
            """
            ### 2.1 Audit and represent the observations (10 points)

            Verify uniqueness, magnitude threshold, missingness, and total
            count. Plot annual or decadal counts and explain why all zero-event
            years must remain in the likelihood.
            """
        ),
        work_cell(),
        response(),
        markdown(
            r"""
            ### 2.2 Prior and posterior comparison (20 points)

            Compare these shape-rate priors for events per year:

            - weak: \(\Gamma(0.5,0.5)\);
            - reference: \(\Gamma(4,32)\), a hypothetical prior with mean
              0.125 events/year and 32 prior exposure-years;
            - lower-rate sensitivity: \(\Gamma(2,40)\).

            Implement the conjugate update, report each prior/posterior mean in
            events per decade, and plot all prior and posterior densities.
            """
        ),
        work_cell(),
        markdown(
            r"""
            ### 2.3 Posterior-predictive counts (20 points)

            For each prior, simulate 100,000 posterior-predictive counts over
            the next decade using a local seeded generator. Plot the PMF,
            report the mean and central 95% interval, and verify the simulated
            zero-count probability against your formula from Problem 1.
            """
        ),
        work_cell(),
        markdown(
            r"""
            ### 2.4 Ten- and twenty-year risk (15 points)

            For all three priors, calculate \(P(Y_*\ge1\mid y)\) over 10 and
            20 years. Compare with the plug-in calculation
            \(1-\exp[-E(\lambda\mid y)T]\) and explain the difference. Present
            a compact sensitivity table.
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.5 Risk communication (10 points)

            Write 150–200 words that distinguish expected count from the
            probability of one or more events, report the sensitivity range,
            and identify two concrete model limitations (at least one specific
            to this catalog, threshold, or bounding box). Do not present the
            calculation as an official earthquake forecast.
            """
        ),
        response(),
    ]
    return make_notebook(4, cells)


def homework_05() -> nbf.NotebookNode:
    cells = opening(
        5, "Least Squares and Bayesian Elastic-Modulus Inference", "Lectures 13–15",
        "Sunday, September 27, 2026",
    )
    cells += [
        data_setup(5, "from scipy import stats"),
        markdown(
            r"""
            ## Problem 1 — Zero-intercept regression (25 points)

            Assume
            \[
            \sigma_i=E\epsilon_i+e_i,\quad e_i\overset{iid}{\sim}N(0,s^2),
            \qquad E\sim N(m_0,s_0^2),
            \]
            with known \(s^2\) and \(\sum_i\epsilon_i^2>0\).

            1. Derive the least-squares estimate of \(E\). **(6)**
            2. Complete the square to derive the Gaussian posterior mean and
               variance. **(10)**
            3. Show the diffuse-prior limit and describe the zero-noise limit.
               **(5)**
            4. State all units and explain why \(\sum_i\epsilon_i^2>0\) is
               necessary. **(4)**
            """
        ),
        response(),
        markdown(
            """
            ## Problem 2 — Where is Hooke's law defensible? (75 points)

            The supplied molecular-dynamics data are attributed in the legacy
            course assignment to Professor Alejandro Strachan's group. Strain
            is dimensionless (multiply by 100 only when plotting percent
            strain); stress is in MPa.
            """
        ),
        code(
            """
            data = pd.read_csv(course_data("hw05_stress_strain.csv"))
            strain = data["strain"].to_numpy(float)
            stress = data["stress_mpa"].to_numpy(float)

            NOISE_SD = 30.0       # MPa, treated as independently calibrated
            PRIOR_MEAN = 7000.0   # MPa
            PRIOR_SD = 3000.0     # MPa
            INITIAL_CUTOFF = 0.025
            CANDIDATE_CUTOFFS = np.arange(0.010, 0.061, 0.005)

            assert data.shape == (1001, 2)
            assert np.all(np.diff(strain) > 0)
            data.head()
            """
        ),
        code(
            """
            def fit_zero_intercept_bayes(epsilon, sigma,
                                         noise_sd=NOISE_SD,
                                         prior_mean=PRIOR_MEAN,
                                         prior_sd=PRIOR_SD):
                '''Return LS estimate and Gaussian posterior mean/variance.'''
                raise NotImplementedError

            def predictive_summary(epsilon_new, fit, noise_sd=NOISE_SD):
                '''Return latent mean, epistemic SD, and predictive SD.'''
                raise NotImplementedError
            """
        ),
        markdown(
            """
            ### 2.1 Inspect the loading curve (10 points)

            Plot stress against percent strain. Describe the initial,
            nonlinear, and softening/failure regimes without selecting a
            cutoff by eye.
            """
        ),
        work_cell(),
        response(),
        markdown(
            r"""
            ### 2.2 Initial Bayesian fit (20 points)

            Implement the zero-intercept least-squares and Gaussian posterior
            formulas for points with \(\epsilon\le0.025\). Report the LS
            estimate, posterior mean, posterior SD, and 95% credible interval
            for \(E\), in MPa and GPa.
            """
        ),
        work_cell(),
        markdown(
            r"""
            ### 2.3 Residual and predictive diagnostics (20 points)

            Plot residual versus strain. Derive and plot both the 95% interval
            for the latent line and the wider posterior-predictive interval,
            using variance \(\epsilon_*^2s_N^2+s^2\) for a new observation.
            Explain why the intervals differ.
            """
        ),
        work_cell(),
        response(),
        markdown(
            """
            ### 2.4 Select the largest defensible cutoff (15 points)

            For every supplied cutoff, train on all observations at or below
            it and validate on the next five observations. A cutoff passes
            only if at least four of five validation stresses fall in their
            95% posterior-predictive intervals and the absolute mean signed
            residual is at most 30 MPa. Tabulate results, select the largest
            passing cutoff, and visualize both decision criteria.
            """
        ),
        work_cell(),
        markdown(
            r"""
            ### 2.5 Final modulus and limitations (10 points)

            Refit at the selected cutoff. Report the cutoff as fraction and
            percent strain, \(E\)'s posterior mean and 95% credible interval in
            GPa, and a posterior-predictive stress interval at strain 0.02.
            Then discuss two concrete limitations of the model or validation
            rule in 100–150 words.
            """
        ),
        work_cell(),
        response(),
    ]
    return make_notebook(5, cells)


def homework_06() -> nbf.NotebookNode:
    cells = opening(
        6, "Classification and Clustering of Manufacturing Faults", "Lectures 16–17",
        "Sunday, October 11, 2026",
    )
    cells += [
        data_setup(
            6,
            """from sklearn.cluster import KMeans
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import adjusted_rand_score, confusion_matrix
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler""",
        ),
        markdown(
            r"""
            ## Problem 1 — Cost-sensitive classification (25 points)

            For \(p=\operatorname{sigm}(\eta)\),
            \(\eta=w^T\phi(x)\), and \(y\in\{0,1\}\):

            1. Write the Bernoulli likelihood and log likelihood. **(5)**
            2. Using \(dp/d\eta=p(1-p)\), derive \(d\ell/d\eta=y-p\). **(6)**
            3. If a false negative costs \(C_{FN}\) and a false positive costs
               \(C_{FP}\), derive the Bayes decision threshold and evaluate it
               for \(C_{FN}=5,C_{FP}=1\). **(8)**
            4. For
               `y=[1,0,1,0,1,0,0,1]` and
               `p=[.80,.55,.40,.30,.20,.15,.10,.05]`, calculate confusion
               matrices `[[TN,FP],[FN,TP]]` and total cost at thresholds 0.5
               and \(1/6\). **(6)**
            """
        ),
        response(),
        markdown(
            """
            ## Problem 2 — Steel-plate fault discovery (75 points)

            The UCI Steel Plates Faults dataset (DOI 10.24432/C5J88N, CC BY
            4.0) contains 27 numerical predictors and seven recorded fault
            classes. The supervised target is K-scratch versus all other
            faults; clustering receives no target labels.
            """
        ),
        code(
            """
            faults = pd.read_csv(course_data("hw06_steel_plate_faults.csv"))
            TARGET_CLASS = "K_Scatch"
            FEATURE_COLUMNS = [c for c in faults.columns if c != "fault_type"]
            X = faults[FEATURE_COLUMNS].to_numpy(float)
            y = (faults["fault_type"] == TARGET_CLASS).astype(int).to_numpy()
            assert faults.shape == (1941, 28)
            faults.head()
            """
        ),
        code(
            """
            indices = np.arange(len(y))
            idx_development, idx_test = train_test_split(
                indices, test_size=0.20, random_state=SEED, stratify=y
            )
            idx_train, idx_valid = train_test_split(
                idx_development, test_size=0.25, random_state=SEED,
                stratify=y[idx_development],
            )
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X[idx_train])
            X_valid = scaler.transform(X[idx_valid])
            X_test = scaler.transform(X[idx_test])
            y_train, y_valid, y_test = y[idx_train], y[idx_valid], y[idx_test]
            C_FN, C_FP = 5.0, 1.0
            assert (len(idx_train), len(idx_valid), len(idx_test)) == (1164, 388, 389)
            """
        ),
        markdown(
            """
            ### 2.1 Target, prevalence, and split (10 points)

            Report all class counts and the binary prevalence. Explain why
            accuracy alone can mislead. Verify the supplied stratified
            60/20/20 split, index disjointness, class proportions, and that the
            scaler learned from training predictors only.
            """
        ),
        work_cell(),
        response(),
        markdown(
            r"""
            ### 2.2 Logistic probabilities and decision costs (20 points)

            Fit `LogisticRegression(C=1, solver="lbfgs", max_iter=2000)` to
            training data. On validation data, compare thresholds 0.5 and
            \(1/6\) using \(C_{FN}=5,C_{FP}=1\): confusion matrices, false
            positives, false negatives, and mean decision cost. Report the
            probability-based Brier score
            \(N^{-1}\sum_i(p_i-y_i)^2\) once; it does not depend on a
            classification threshold. Explain the tradeoff.
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.3 Final supervised evaluation (15 points)

            Freeze the model and thresholds, then evaluate the test set once.
            Report both confusion matrices, Brier score, and mean cost. Explain
            why the test result must not initiate another tuning round.
            """
        ),
        work_cell(),
        response(),
        markdown(
            """
            ### 2.4 Unsupervised comparison (15 points)

            Fit two-cluster K-means (`n_init=20`, seed `SEED`) using standardized
            training predictors only. Use the supplied `adjusted_rand_score`:
            it equals 1 for identical partitions and is approximately 0 for
            chance-level agreement, while remaining invariant to cluster-label
            permutations. Report validation/test adjusted Rand index against
            the binary target, identify the five features with
            largest absolute standardized-centroid difference, and make a
            two-feature plot whose marker shape shows the recorded label.
            Explain why cluster numbers themselves are arbitrary.
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.5 Disagreements and interpretation (15 points)

            Map clusters to their majority training labels for interpretation
            only. Display at least five test cases where this mapping and the
            cost-sensitive classifier disagree. In 150–200 words, distinguish
            what supervised probabilities and clusters answer, explain why
            cluster agreement does not establish physical fault types, and
            give one plausible source of disagreement.
            """
        ),
        work_cell(),
        response(),
    ]
    return make_notebook(6, cells)


def homework_08() -> nbf.NotebookNode:
    cells = opening(
        8, "State-Space Models and Kalman Filtering", "Lectures 19–20",
        "Sunday, October 25, 2026",
    )
    cells += [
        data_setup(8, "from scipy.linalg import expm"),
        markdown(
            r"""
            ## Problem 1 — One Kalman-filter step (25 points)

            For \(\ddot q+2\zeta\omega_0\dot q+\omega_0^2q=u(t)\), let
            \(x=(q,\dot q)^T\), \(\omega_0=2\), \(\zeta=0.1\), and
            \(\Delta t=0.1\). Use forward Euler and

            \[
            m_0=(0.5,-0.2)^T,\quad
            P_0=\begin{bmatrix}.04&.01\\.01&.09\end{bmatrix},\quad u_0=.3,
            \]
            \[
            Q=\operatorname{diag}(.001,.004),\quad H=[1\;0],\quad
            R=.01,\quad y_1=.42.
            \]

            1. Derive the continuous matrix, \(F=I+\Delta tA_c\), and \(B\). **(5)**
            2. Calculate the predicted mean and covariance. **(6)**
            3. Calculate innovation, innovation variance, and gain. **(6)**
            4. Calculate the updated mean and Joseph-form covariance
               \(P_1=(I-KH)P_1^-(I-KH)^T+KRK^T\); verify symmetry. **(6)**
            5. Describe the \(R\to0\) limit and why exact position does not
               necessarily imply zero velocity variance. **(2)**
            """
        ),
        response(),
        markdown(
            """
            ## Problem 2 — Filtering a hidden forced oscillator (75 points)

            The cell below creates a reproducible trajectory and noisy position
            observations with separate process and measurement random streams.
            """
        ),
        code(
            """
            omega0, zeta = 2.0, 0.15
            dt, final_time = 0.05, 20.0
            force_amplitude, force_frequency = 0.6, 1.2
            Ac = np.array([[0.0, 1.0], [-omega0**2, -2*zeta*omega0]])
            b = np.array([[0.0], [1.0]])
            aug = np.zeros((3, 3)); aug[:2, :2] = Ac; aug[:2, 2:] = b
            disc = expm(aug * dt)
            F, B = disc[:2, :2], disc[:2, 2]
            Q_TRUE = np.diag([2e-5, 5e-4])
            H = np.array([[1.0, 0.0]])
            R = np.array([[0.04**2]])
            FILTER_M0 = np.array([0.0, 0.0])
            FILTER_P0 = np.diag([0.25, 0.25])
            t = np.arange(0.0, final_time + dt/2, dt)
            u = force_amplitude * np.cos(force_frequency * t[:-1])
            process_rng = np.random.default_rng(5390801)
            measurement_rng = np.random.default_rng(5390802)
            x_true = np.empty((len(t), 2)); x_true[0] = [0.35, -0.20]
            for k in range(len(t) - 1):
                x_true[k+1] = (
                    F @ x_true[k]
                    + B*u[k]
                    + process_rng.multivariate_normal(np.zeros(2), Q_TRUE)
                )
            y = (H @ x_true.T).ravel() + measurement_rng.normal(
                0.0, np.sqrt(R[0, 0]), len(t)
            )
            print("Steps:", len(t), "F[0,:] =", F[0])
            """
        ),
        code(
            """
            def kalman_filter(y, u, F, B, H, Q, R, m0, P0):
                '''Filter y with a fixed update/predict convention.

                First assimilate y[0] into the prior (m0, P0) at t[0] and
                store that posterior at index 0. For k=0,...,len(u)-1,
                predict with u[k] to t[k+1], assimilate y[k+1], and store the
                posterior at index k+1.

                Return means (n,2), covariances (n,2,2), innovations (n,),
                and innovation variances (n,). Use a linear solve for the gain
                and the Joseph update
                P = (I-KH) @ P_minus @ (I-KH).T + K @ R @ K.T.
                '''
                # YOUR IMPLEMENTATION HERE
                raise NotImplementedError

            def validate_filter_outputs(means, covariances, innovations,
                                        innovation_variances, n_steps):
                '''Run deterministic structural checks on a filter result.'''
                means = np.asarray(means, float)
                covariances = np.asarray(covariances, float)
                innovations = np.asarray(innovations, float)
                innovation_variances = np.asarray(innovation_variances, float)
                assert means.shape == (n_steps, 2)
                assert covariances.shape == (n_steps, 2, 2)
                assert innovations.shape == (n_steps,)
                assert innovation_variances.shape == (n_steps,)
                assert all(np.all(np.isfinite(a)) for a in (
                    means, covariances, innovations, innovation_variances
                ))
                assert np.allclose(
                    covariances, np.swapaxes(covariances, -1, -2), atol=1e-10
                )
                assert np.linalg.eigvalsh(covariances).min() >= -1e-10
                assert np.all(innovation_variances > 0)
                return True
            """
        ),
        markdown(
            """
            ### 2.1 Inspect and implement (25 points)

            Plot truth and measurements and explain the separate random
            streams. Complete the supplied Kalman-filter function using
            `FILTER_M0`, `FILTER_P0`, and its stated update/predict ordering.
            Run `validate_filter_outputs` on the returned arrays before
            interpreting any result.
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.2 Numerical validation (15 points)

            Verify output shapes and finiteness, covariance symmetry to
            `1e-10`, and positive semidefiniteness to numerical tolerance.
            Check the first entries of the supplied discretization against
            `F[0,0] = 0.99505374` and `F[0,1] = 0.04917539`.
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.3 Nominal filtering performance (15 points)

            With the correct process covariance, plot truth, observations,
            filtered position/velocity, and 95% marginal bands. Report both
            state RMSEs and the fraction of time points within each band.
            """
        ),
        work_cell(),
        markdown(
            r"""
            ### 2.4 Process-noise misspecification (10 points)

            Repeat with \(Q=0.05Q_{true}\) and \(Q=20Q_{true}\). Compare state
            RMSE, average posterior SD, and standardized-innovation mean and
            SD across all three cases.
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.5 Interpretation (10 points)

            Explain why the smoothest estimate need not be best, what the
            innovation diagnostics reveal, and why the interval fraction from
            one realized trajectory is not repeated-sampling coverage.
            """
        ),
        response(),
    ]
    return make_notebook(8, cells)


def homework_09() -> nbf.NotebookNode:
    cells = opening(
        9, "Gaussian-Process Prediction for NIST Ultrasonic Calibration", "Lectures 21–22",
        "Sunday, November 1, 2026",
    )
    cells += [
        code(
            r"""
            import hashlib
            import io
            import urllib.request

            import numpy as np
            import pandas as pd
            import matplotlib.pyplot as plt
            import seaborn as sns
            from scipy.linalg import cho_factor, cho_solve, solve_triangular
            from scipy.optimize import minimize

            sns.set_theme(style="ticks", context="notebook")
            plt.rcParams["figure.dpi"] = 120
            np.set_printoptions(precision=6, suppress=True)

            NIST_DATA_URL = (
                "https://www.itl.nist.gov/div898/strd/nls/data/"
                "LINKS/DATA/Chwirut1.dat"
            )
            NIST_DATA_SHA256 = (
                "d9a055dfe5af71a8754c00f073ef00f8"
                "fed2e3fd1c6fd20cea8fd62d7cc3ed84"
            )

            request = urllib.request.Request(
                NIST_DATA_URL,
                headers={"User-Agent": "Purdue-ME539-course-materials/1.0"},
            )
            with urllib.request.urlopen(request, timeout=60) as response:
                nist_payload = response.read()

            actual_sha256 = hashlib.sha256(nist_payload).hexdigest()
            assert actual_sha256 == NIST_DATA_SHA256, (
                "The NIST file has changed. Stop and contact the instructor."
            )

            nist_array = np.loadtxt(io.BytesIO(nist_payload), skiprows=60)
            chwirut = pd.DataFrame(
                {
                    "ultrasonic_response": nist_array[:, 0],
                    "metal_distance": nist_array[:, 1],
                }
            )

            x = chwirut["metal_distance"].to_numpy(float)
            y = chwirut["ultrasonic_response"].to_numpy(float)

            interpolation = np.isin(x, [2.25, 2.50, 2.75])
            extrapolation = x >= 5.0
            training = ~(interpolation | extrapolation)

            y_mean = y[training].mean()
            y_sd = y[training].std(ddof=0)
            y_standard = (y - y_mean) / y_sd

            assert chwirut.shape == (214, 2)
            assert np.isfinite(chwirut.to_numpy()).all()
            assert np.unique(x).size == 22
            assert (training.sum(), interpolation.sum(), extrapolation.sum()) == (
                159, 26, 29
            )
            assert set(np.unique(x[interpolation])) == {2.25, 2.50, 2.75}
            assert x[extrapolation].min() == 5.0

            print("NIST Chwirut1 data loaded; fixed split masks are ready.")
            """
        ),
        markdown(
            r"""
            ## Problem 1 — Gaussian-process conditioning (25 points)

            Let observations be \(x=(0,2)\) days and \(y=(1,-0.5)^T\), where
            response is measured in an arbitrary response unit. Use a zero
            prior mean, signal standard deviation of one response unit,
            length scale of one day, and kernel
            \(k(x,x')=\exp[-(x-x')^2/2]\) when the numerical values of
            \(x,x'\) are expressed in days. The observation-noise variance is
            \(\sigma_n^2=0.04\) response-unit squared. Predict the latent
            response at \(x_*=1\) day.

            1. Write the joint Gaussian distribution of \((y_1,y_2,f_*)\). **(5)**
            2. Construct \(K_y,k_*\) and solve \(K_y\alpha=y\). **(6)**
            3. Calculate posterior mean, latent variance, and future noisy-
               observation variance. **(6)**
            4. Show that the zero-noise limit interpolates at a training point
               and has zero latent variance. **(5)**
            5. State units and verify symmetry/nonnegative variance. **(3)**
            """
        ),
        response(),
        markdown(
            r"""
            ## Problem 2 — NIST ultrasonic calibration (75 points)

            The [NIST Chwirut1 dataset](https://www.itl.nist.gov/div898/strd/nls/data/chwirut1.shtml)
            contains 214 observed ultrasonic responses at 22 metal-distance
            settings. Many distance settings were measured repeatedly. NIST
            does not state units for either quantity on the dataset page, so
            label them as **NIST-reported units** rather than inventing units.

            The setup cell downloads the official NIST ASCII file at runtime
            and verifies its SHA-256 checksum; the course repository does not
            redistribute the data. We will compare GP interpolation across an
            interior gap with extrapolation beyond the largest training
            distance. Every replicate at a withheld distance is withheld, so
            an identical input cannot leak into both training and test sets.
            """
        ),
        code(
            """
            JITTER = 1e-8

            def pairwise_distance(x_left, x_right):
                x_left = np.asarray(x_left, float).reshape(-1)
                x_right = np.asarray(x_right, float).reshape(-1)
                return np.abs(x_left[:, None] - x_right[None, :])

            def gp_negative_log_marginal_likelihood(log_parameters, kernel,
                                                    x_train, y_train):
                amplitude, length_scale, noise_sd = np.exp(log_parameters)
                K = kernel(x_train, x_train, amplitude, length_scale)
                K = K + (noise_sd**2 + JITTER) * np.eye(len(x_train))
                factor = cho_factor(K, lower=True, check_finite=True)
                alpha = cho_solve(factor, y_train)
                return (
                    0.5 * y_train @ alpha
                    + np.log(np.diag(factor[0])).sum()
                    + 0.5 * len(x_train) * np.log(2*np.pi)
                )

            def fit_gp(kernel, x_train, y_train):
                initial = np.log([1.0, 1.0, 0.15])
                bounds = np.log([[0.1, 5.0], [0.05, 15.0], [0.01, 2.0]])
                result = minimize(
                    gp_negative_log_marginal_likelihood,
                    initial,
                    args=(kernel, x_train, y_train),
                    method="L-BFGS-B",
                    bounds=bounds,
                )
                if not result.success:
                    raise RuntimeError(result.message)
                return result

            def gp_posterior(kernel, fitted_log_parameters,
                             x_train, y_train, x_test):
                amplitude, length_scale, noise_sd = np.exp(fitted_log_parameters)
                K = kernel(x_train, x_train, amplitude, length_scale)
                K = K + (noise_sd**2 + JITTER) * np.eye(len(x_train))
                factor = cho_factor(K, lower=True, check_finite=True)
                K_cross = kernel(x_train, x_test, amplitude, length_scale)
                alpha = cho_solve(factor, y_train)
                mean = K_cross.T @ alpha
                projected = solve_triangular(factor[0], K_cross, lower=True)
                prior_variance = np.diag(
                    kernel(x_test, x_test, amplitude, length_scale)
                )
                raw_latent_variance = (
                    prior_variance - np.sum(projected**2, axis=0)
                )
                if raw_latent_variance.min(initial=0.0) < -1e-8:
                    raise FloatingPointError(
                        "A materially negative GP variance was computed."
                    )
                # Clip roundoff only after rejecting a substantive violation.
                latent_variance = np.maximum(raw_latent_variance, 0.0)
                noisy_variance = latent_variance + noise_sd**2
                return mean, latent_variance, noisy_variance
            """
        ),
        markdown(
            r"""
            ### 2.1 Audit the replicated data and split (12 points)

            Verify the row count, number and range of distinct distances,
            missingness, response range, and replicate count at every distance.
            Make one figure showing all observations, the per-distance mean,
            and a mean-plus-or-minus-one-sample-SD band or error bars. Mark the
            interpolation and extrapolation holdouts. Confirm that response
            standardization used the training rows only, and explain why a
            random row split would leak information through replicated inputs.
            """
        ),
        work_code(
            """
            replicate_summary = (
                chwirut.groupby("metal_distance")["ultrasonic_response"]
                .agg(["count", "mean", "std"])
                .reset_index()
            )

            # YOUR CODE HERE: audit the data and construct the requested plot.
            """
        ),
        response("Report the audit and explain why the split is by distance."),
        markdown(
            r"""
            ### 2.2 Kernels and exact GP fitting (23 points)

            Implement
            \[
            k_{RBF}(r)=a^2e^{-r^2/(2\ell^2)},\qquad
            k_{M32}(r)=a^2(1+\sqrt3r/\ell)e^{-\sqrt3r/\ell}.
            \]
            where $r=|x-x'|$. Implement both kernels, then use the supplied
            Cholesky posterior and negative log marginal likelihood. Optimize
            once per kernel in log coordinates from
            `(a, ell, noise)=(1,1,0.15)`. The supplied bounds are in standardized
            response units and NIST-reported distance units. Report the fitted
            parameters and objective. Check kernel symmetry, the diagonal
            value $a^2$, positive semidefiniteness to numerical tolerance,
            and nonnegative predictive variances.
            """
        ),
        work_code(
            r"""
            def rbf_kernel(x_left, x_right, amplitude, length_scale):
                r = pairwise_distance(x_left, x_right)
                # YOUR CODE HERE
                raise NotImplementedError


            def matern32_kernel(x_left, x_right, amplitude, length_scale):
                r = pairwise_distance(x_left, x_right)
                # YOUR CODE HERE
                raise NotImplementedError


            def validate_kernel(kernel):
                check_x = np.array([0.5, 1.25, 3.0, 4.75])
                amplitude = 1.7
                K = kernel(check_x, check_x, amplitude, 0.8)
                assert K.shape == (4, 4)
                assert np.allclose(K, K.T, atol=1e-12)
                assert np.allclose(np.diag(K), amplitude**2, atol=1e-12)
                assert np.linalg.eigvalsh(K).min() >= -1e-10


            # Required contract after you complete this cell:
            # fit_results[name] = {
            #     "kernel": callable,
            #     "optimization": scipy OptimizeResult,
            #     "parameters": np.array([amplitude, length_scale, noise_sd]),
            # }
            fit_results = {}

            def validate_fit_results(results):
                assert set(results) == {"RBF", "Matern-3/2"}
                for result in results.values():
                    assert callable(result["kernel"])
                    assert result["optimization"].success
                    parameters = np.asarray(result["parameters"], float)
                    assert parameters.shape == (3,)
                    assert np.isfinite(parameters).all()
                    assert np.all(parameters > 0)

            # YOUR CODE HERE: validate both kernels, populate fit_results on
            # the training split, report parameters/objectives, and call
            # validate_fit_results(fit_results).
            """
        ),
        markdown(
            r"""
            ### 2.3 Posterior prediction (15 points)

            For both kernels, predict on a dense distance grid and at every
            held-out observation. Convert standardized-response predictions
            back using
            \[
            \mu_y=y_{mean}+y_{sd}\mu_{std},\qquad
            v_y=y_{sd}^2v_{std}.
            \]
            Make aligned kernel panels showing training observations, both
            holdouts, posterior mean, and the 95% **noisy-observation** interval.
            Use common axis limits so the panels are visually comparable.
            """
        ),
        work_code(
            """
            prediction_grid = np.linspace(x.min(), x.max(), 500)
            prediction_inputs = {
                "grid": prediction_grid,
                "interpolation": x[interpolation],
                "extrapolation": x[extrapolation],
            }

            # Required contract after you complete this cell:
            # predictions[kernel_name][split_name] = {
            #     "mean": one-dimensional array,
            #     "latent_variance": one-dimensional array,
            #     "noisy_variance": one-dimensional array,
            # }
            predictions = {}

            def validate_predictions(results):
                assert set(results) == {"RBF", "Matern-3/2"}
                for kernel_result in results.values():
                    assert set(kernel_result) == set(prediction_inputs)
                    for split_name, values in kernel_result.items():
                        expected_shape = prediction_inputs[split_name].shape
                        assert set(values) == {
                            "mean", "latent_variance", "noisy_variance"
                        }
                        for quantity in values.values():
                            quantity = np.asarray(quantity, float)
                            assert quantity.shape == expected_shape
                            assert np.isfinite(quantity).all()
                        assert np.all(values["latent_variance"] >= 0)
                        assert np.all(
                            values["noisy_variance"]
                            >= values["latent_variance"]
                        )

            # YOUR CODE HERE: populate predictions in original response units,
            # call validate_predictions(predictions), and make the two panels.
            """
        ),
        markdown(
            r"""
            ### 2.4 Held-out evaluation (15 points)

            For each kernel and holdout separately, report RMSE for the
            NIST ultrasonic response and mean negative log predictive density
            from the noisy predictive Gaussian,
            \[
            \frac1N\sum_i\frac12\left[\log(2\pi v_i)
            +\frac{(y_i-\mu_i)^2}{v_i}\right].
            \]
            Also report the fraction inside the 95% noisy-observation interval.
            Do not combine interpolation and extrapolation into one score.
            """
        ),
        work_code(
            """
            def held_out_metrics(y_true, mean, noisy_variance):
                y_true = np.asarray(y_true, float)
                mean = np.asarray(mean, float)
                noisy_variance = np.asarray(noisy_variance, float)
                assert y_true.shape == mean.shape == noisy_variance.shape
                assert np.all(noisy_variance > 0)
                # YOUR CODE HERE
                raise NotImplementedError


            # Required final schema and ordering:
            METRIC_COLUMNS = [
                "kernel", "holdout", "rmse", "mean_nlpd", "coverage_95"
            ]
            metrics = pd.DataFrame(columns=METRIC_COLUMNS)

            def validate_metrics(table):
                assert list(table.columns) == METRIC_COLUMNS
                assert table.shape == (4, 5)
                assert set(table["kernel"]) == {"RBF", "Matern-3/2"}
                assert set(table["holdout"]) == {
                    "interpolation", "extrapolation"
                }
                numeric = table[["rmse", "mean_nlpd", "coverage_95"]]
                assert np.isfinite(numeric.to_numpy(float)).all()
                assert table["coverage_95"].between(0, 1).all()

            # YOUR CODE HERE: calculate the four rows in the required order
            # (RBF interpolation, RBF extrapolation, Matern-3/2 interpolation,
            # Matern-3/2 extrapolation), then call validate_metrics(metrics).
            """
        ),
        markdown(
            r"""
            ### 2.5 Scientific interpretation (10 points)

            Use your replicate summary to assess the constant-noise assumption.
            Compare the two kernels separately for interpolation and
            extrapolation, and explain why extrapolation uncertainty should not
            be read as a guarantee. Then state one concrete limitation of a
            stationary, homoscedastic GP for this calibration dataset and one
            model or experiment change that would address it. Support your
            conclusions with numerical or graphical evidence from this study.
            """
        ),
        response(),
    ]
    return make_notebook(9, cells)


def deep_neural_network_source() -> nbf.NotebookNode:
    cells = opening(
        11, "Deep Neural-Network Regression", "Lectures 24–25",
        "Sunday, November 22, 2026",
    )
    cells += [
        data_setup(
            11,
            """import copy
        import random
        import torch
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import mean_absolute_error, mean_squared_error
        from sklearn.model_selection import train_test_split
        from sklearn.neighbors import NearestNeighbors
        from sklearn.preprocessing import StandardScaler""",
        ),
        markdown(
            r"""
            ## Problem 1 — One neural-network update (25 points)

            For \(h=\tanh(w_hx+b_h)\), \(\widehat y=w_oh+b_o\), and
            \(L=\tfrac12(\widehat y-y)^2\), use
            \(x=.5,y=1.2,w_h=.8,b_h=-.1,w_o=1.5,b_o=.2\).

            1. Calculate preactivation, activation, prediction, and loss. **(7)**
            2. Count trainable scalar parameters. **(3)**
            3. Derive/evaluate \(\partial L/\partial\widehat y\). **(4)**
            4. Given gradient `(-.386438,-.772876,-.164018,-.563031)` in
               parameter order \((w_h,b_h,w_o,b_o)\), take one SGD step with
               learning rate 0.05. **(7)**
            5. Recompute prediction/loss and decide whether it is a descent
               step. **(4)**
            """
        ),
        response(),
        markdown(
            """
            ## Problem 2 — Airfoil self-noise regression (75 points)

            The UCI Airfoil Self-Noise dataset (DOI 10.24432/C5VW2C, CC BY
            4.0) has 1,503 observations, five inputs, and sound-pressure level
            in dB. Use PyTorch already present in Colab; install no framework.
            """
        ),
        code(
            """
            random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
            torch.use_deterministic_algorithms(True, warn_only=True)
            airfoil = pd.read_csv(course_data("hw11_airfoil_self_noise.csv"))
            TARGET = "sound_pressure_db"
            FEATURES = [c for c in airfoil.columns if c != TARGET]
            X = airfoil[FEATURES].to_numpy(np.float32)
            y = airfoil[TARGET].to_numpy(np.float32)
            idx = np.arange(len(airfoil))
            train_idx, remainder_idx = train_test_split(
                idx, test_size=0.30, random_state=SEED, shuffle=True
            )
            valid_idx, test_idx = train_test_split(
                remainder_idx, test_size=0.50, random_state=SEED + 1, shuffle=True
            )
            assert (len(train_idx), len(valid_idx), len(test_idx)) == (1052, 225, 226)
            airfoil.head()
            """
        ),
        code(
            """
            def make_model():
                return torch.nn.Sequential(
                    torch.nn.Linear(5, 16),
                    torch.nn.Tanh(),
                    torch.nn.Linear(16, 16),
                    torch.nn.Tanh(),
                    torch.nn.Linear(16, 1),
                )

            def count_parameters(model):
                return sum(p.numel() for p in model.parameters() if p.requires_grad)

            def train_network(model, X_train_scaled, y_train_scaled,
                              X_valid_scaled, y_valid_scaled,
                              max_epochs=250, patience=25,
                              min_delta=1e-6, seed=SEED):
                '''Seeded mini-batch trainer with validation early stopping.'''
                Xtr = torch.as_tensor(X_train_scaled, dtype=torch.float32)
                ytr = torch.as_tensor(y_train_scaled, dtype=torch.float32).reshape(-1, 1)
                Xva = torch.as_tensor(X_valid_scaled, dtype=torch.float32)
                yva = torch.as_tensor(y_valid_scaled, dtype=torch.float32).reshape(-1, 1)
                dataset = torch.utils.data.TensorDataset(Xtr, ytr)
                generator = torch.Generator().manual_seed(seed)
                loader = torch.utils.data.DataLoader(
                    dataset, batch_size=64, shuffle=True, generator=generator
                )
                optimizer = torch.optim.Adam(
                    model.parameters(), lr=1e-3, weight_decay=1e-5
                )
                loss_fn = torch.nn.MSELoss()
                best_loss = np.inf
                best_state = copy.deepcopy(model.state_dict())
                epochs_without_improvement = 0
                history = {"train": [], "valid": []}

                for _ in range(max_epochs):
                    model.train()
                    batch_losses = []
                    for xb, yb in loader:
                        optimizer.zero_grad()
                        loss = loss_fn(model(xb), yb)
                        loss.backward()
                        optimizer.step()
                        batch_losses.append(float(loss.detach()))
                    model.eval()
                    with torch.no_grad():
                        valid_loss = float(loss_fn(model(Xva), yva))
                    history["train"].append(float(np.mean(batch_losses)))
                    history["valid"].append(valid_loss)
                    if valid_loss < best_loss - min_delta:
                        best_loss = valid_loss
                        best_state = copy.deepcopy(model.state_dict())
                        epochs_without_improvement = 0
                    else:
                        epochs_without_improvement += 1
                    if epochs_without_improvement >= patience:
                        break

                model.load_state_dict(best_state)
                return model, history, best_loss

            assert count_parameters(make_model()) == 385
            """
        ),
        markdown(
            """
            ### 2.1 Inspect, split, and transform (10 points)

            Describe all variables and units. Verify disjoint split indices.
            Fit separate standard scalers to training predictors and training
            target only; transform validation/test without refitting.
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.2 Linear baseline (15 points)

            Fit `LinearRegression` on standardized training data. Report
            validation RMSE/MAE on the original dB scale and plot residuals.
            Keep the test set untouched.
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.3 Neural model and training (20 points)

            Inspect the supplied `5 → 16 → 16 → 1` tanh network and verify 385
            trainable parameters. Use the supplied seeded trainer (Adam,
            learning rate `1e-3`, weight decay `1e-5`, batch size 64, MSE,
            250 epochs, patience 25, `min_delta=1e-6`). Confirm that it restores
            the best validation checkpoint. Plot training and validation loss
            and justify the stopping epoch.
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.4 One final test evaluation (15 points)

            Freeze every decision, then evaluate both models on test data once.
            Report RMSE/MAE in dB, plot observed versus predicted and residuals
            versus prediction, and state whether the neural model materially
            improves the baseline.
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.5 Sparse-support trust check (15 points)

            In standardized input space, compute each test point's distance to
            its nearest training point. Compare neural-network test RMSE in the
            upper distance quartile with all remaining points. Decide whether
            sparse-support predictions are trustworthy and name one limitation
            hidden by aggregate RMSE.
            """
        ),
        work_cell(),
        response("Give your scientific conclusion in 150 words or fewer."),
    ]
    return make_notebook(11, cells)


def sampling_variational_source() -> nbf.NotebookNode:
    cells = opening(
        13, "Sampling and Variational Approximation", "Lectures 27–28",
        "Sunday, December 6, 2026",
    )
    cells += [
        data_setup(
            13,
            """from numpy.polynomial.hermite import hermgauss
        from scipy.optimize import minimize
        from scipy.special import expit, logsumexp""",
        ),
        markdown(
            r"""
            ## Problem 1 — Two approximations to a correlated Gaussian (25 points)

            Let \(p(\theta)=N(0,\Sigma)\),
            \(\Sigma=\begin{bmatrix}1&.8\\.8&1\end{bmatrix}\). A Metropolis
            proposal is \(N(\theta,s^2I)\), and
            \(q=N(m,D)\) with diagonal \(D=\operatorname{diag}(d_1,d_2)\).

            1. Derive the Metropolis acceptance probability and identify the
               cancellations. **(5)**
            2. Evaluate it from \((0,0)^T\) to \((1,0)^T\). **(4)**
            3. Write \(D_{KL}(q\|p)\) in closed form. **(6)**
            4. Minimize over \(m,d_1,d_2\), deriving
               \(m=0,d_i=1/(\Sigma^{-1})_{ii}\), and evaluate. **(7)**
            5. Explain the lost dependence and marginal underdispersion. **(3)**
            """
        ),
        response(),
        markdown(
            r"""
            ## Problem 2 — Challenger logistic-posterior inference (75 points)

            The frozen teaching extract has 23 pre-accident shuttle launches
            with nonmissing damage indicators. Model
            \[
            x_i=(T_i-70)/10,\qquad
            y_i\sim\operatorname{Bernoulli}[\operatorname{logit}^{-1}
            (\alpha+\beta x_i)],
            \]
            with independent \(\alpha,\beta\sim N(0,2.5^2)\).
            """
        ),
        code(
            """
            challenger = pd.read_csv(course_data("hw13_challenger_prelaunch.csv"))
            temperature = challenger["temperature_f"].to_numpy(float)
            y = challenger["damage_incident"].to_numpy(int)
            x = (temperature - 70.0) / 10.0
            PRIOR_SD = 2.5
            assert len(challenger) == 23 and set(np.unique(y)) <= {0, 1}
            challenger.head()
            """
        ),
        code(
            """
            def log_posterior(theta):
                '''Stable, vectorized log posterior up to a constant.'''
                theta = np.asarray(theta, float)
                eta = theta[..., 0, None] + theta[..., 1, None] * x
                log_likelihood = np.sum(
                    y * eta - np.logaddexp(0.0, eta), axis=-1
                )
                log_prior = -0.5 * np.sum((theta / PRIOR_SD)**2, axis=-1)
                return log_likelihood + log_prior

            assert np.isclose(log_posterior([0.0, 0.0]), -15.9423851529)
            assert np.isclose(log_posterior([-1.0, -2.0]), -10.6419612123)

            def numerical_hessian(function, point, step=1e-4):
                '''Central-difference Hessian for this two-parameter problem.'''
                point = np.asarray(point, float)
                dimension = len(point)
                H = np.empty((dimension, dimension))
                for i in range(dimension):
                    ei = np.zeros(dimension); ei[i] = step
                    for j in range(dimension):
                        ej = np.zeros(dimension); ej[j] = step
                        H[i, j] = (
                            function(point + ei + ej)
                            - function(point + ei - ej)
                            - function(point - ei + ej)
                            + function(point - ei - ej)
                        ) / (4 * step**2)
                return 0.5 * (H + H.T)

            GRID_SIZE = 301

            def normalized_reference_grid(logp, center, covariance,
                                          grid_size=GRID_SIZE):
                '''Normalize a MAP ± 6 marginal-SD rectangular grid.

                Boundary mass is the sum of normalized discrete weights on
                the outermost rows and columns, counting corners once.
                '''
                sd = np.sqrt(np.diag(covariance))
                axes = [
                    np.linspace(center[j] - 6*sd[j], center[j] + 6*sd[j], grid_size)
                    for j in range(2)
                ]
                A, B = np.meshgrid(*axes, indexing="ij")
                points = np.column_stack([A.ravel(), B.ravel()])
                log_weights = logp(points).reshape(A.shape)
                weights = np.exp(log_weights - logsumexp(log_weights))
                edge = np.zeros_like(weights, dtype=bool)
                edge[[0, -1], :] = True; edge[:, [0, -1]] = True
                return axes, weights, float(weights[edge].sum())

            def component_ess(samples):
                '''Initial-positive-sequence ESS for every sample column.'''
                samples = np.asarray(samples, float)
                n = len(samples)
                result = []
                for values in samples.T:
                    centered = values - values.mean()
                    size = 1 << (2*n - 1).bit_length()
                    spectrum = np.fft.rfft(centered, n=size)
                    acov = np.fft.irfft(spectrum * spectrum.conjugate(), n=size)[:n]
                    if acov[0] <= 0:
                        result.append(float(n))
                        continue
                    acf = acov / acov[0]
                    pair_count = len(acf) // 2
                    paired = acf[:2*pair_count].reshape(-1, 2).sum(axis=1)
                    first_nonpositive = np.flatnonzero(paired <= 0)
                    keep = (
                        first_nonpositive[0]
                        if len(first_nonpositive)
                        else len(paired)
                    )
                    tau = max(1.0, -1.0 + 2.0 * paired[:keep].sum())
                    result.append(n / tau)
                return np.asarray(result)

            def random_walk_metropolis(logp, initial, proposal_chol,
                                       n_steps, local_rng):
                '''Complete only the marked log-scale acceptance decision.'''
                theta = np.asarray(initial, float).copy()
                current_lp = float(logp(theta))
                samples = np.empty((n_steps, len(theta)))
                accepted = 0
                for i in range(n_steps):
                    proposed = theta + proposal_chol @ local_rng.normal(size=len(theta))
                    proposed_lp = float(logp(proposed))
                    accept = False  # TODO: replace with the log-scale MH test
                    if accept:
                        theta, current_lp = proposed, proposed_lp
                        accepted += 1
                    samples[i] = theta
                return samples, accepted / n_steps

            gh_nodes, gh_weights = hermgauss(20)
            GH_Z = np.stack(
                np.meshgrid(gh_nodes, gh_nodes, indexing="ij"), axis=-1
            ).reshape(-1, 2)
            GH_W = np.outer(gh_weights, gh_weights).ravel() / np.pi

            def vi_objective(parameters):
                mean = parameters[:2]
                log_sd = parameters[2:]
                sd = np.exp(log_sd)
                theta = mean + np.sqrt(2.0) * sd * GH_Z
                expected_logp = GH_W @ log_posterior(theta)
                expected_logq = -1.0 * (1.0 + np.log(2*np.pi)) - log_sd.sum()
                return expected_logq - expected_logp
            """
        ),
        markdown(
            r"""
            ### 2.1 Posterior and deterministic reference (10 points)

            Verify the supplied stable log posterior and explain the temperature
            rescaling and prior. Find the MAP with BFGS and use the supplied
            Hessian helper for the Laplace covariance. Normalize the supplied
            301-by-301 grid spanning MAP plus/minus six Laplace marginal SDs.
            Report the helper's explicitly defined outer-edge mass and require
            it to be below \(10^{-4}\).
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.2 Random-walk Metropolis (20 points)

            Implement the acceptance decision on the log scale. Use the
            Laplace Cholesky as proposal preconditioner; start every chain at
            the MAP and compare scalar scales 0.8, 1.2, and 1.5 in 3,000-step
            pilots. Create four independent generators with
            `np.random.SeedSequence(53913).spawn(4)`, using the first three in
            scale order and the fourth for the final run. Among pilots with
            acceptance in `[0.20, 0.60]`, select the largest minimum-component
            ESS from the supplied helper. Run 25,000 iterations, discard 5,000,
            and report traces, acceptance, and component ESS.
            """
        ),
        work_cell(),
        markdown(
            r"""
            ### 2.3 Diagonal Gaussian variational inference (20 points)

            Parameterize \(q=N(m,\operatorname{diag}(e^{2\ell_1},e^{2\ell_2}))\).
            Use the supplied 20-by-20 Gauss–Hermite objective and minimize
            \(E_q[\log q-\log p]\) using L-BFGS-B, bounds
            \(-5\le\ell_i\le2\), initialized at the MAP and Laplace marginal
            SDs. Verify optimizer convergence and numerical stability.
            """
        ),
        work_cell(),
        markdown(
            """
            ### 2.4 Compare the approximations (15 points)

            Compare grid, MCMC, and VI means, marginal 95% intervals,
            covariance matrices, and two-dimensional contours. Explicitly
            identify which dependence the diagonal approximation cannot
            represent and where underdispersion appears.
            """
        ),
        work_cell(),
        markdown(
            r"""
            ### 2.5 Predictive risk and extrapolation (10 points)

            Using retained MCMC draws as the primary approximation, plot the
            pointwise median and 95% credible band for damage probability over
            the observed temperature range. At \(31^\circ\mathrm F\), report
            the median and central 95% interval under the grid reference,
            MCMC, and VI. Explain why this is hazardous
            extrapolation, not an established causal fact, and why discarding
            covariance can affect this derived probability differently from
            parameter marginal variances.
            """
        ),
        work_cell(),
        response(),
    ]
    return make_notebook(13, cells)


def retarget_notebook(
    notebook: nbf.NotebookNode,
    *,
    old_number: int,
    new_number: int,
    title: str,
    coverage: str,
    due: str,
) -> nbf.NotebookNode:
    """Retarget a completed source draft without changing its data links."""
    notebook = deepcopy(notebook)
    opening_cell = notebook.cells[0]
    opening_cell.source = re.sub(
        r"^# Homework \d+ — .*?$",
        f"# Homework {new_number} — {title}",
        opening_cell.source,
        count=1,
        flags=re.MULTILINE,
    )
    opening_cell.source = re.sub(
        r"^\*\*Coverage:\*\* .*?  $",
        f"**Coverage:** {coverage}  ",
        opening_cell.source,
        count=1,
        flags=re.MULTILINE,
    )
    opening_cell.source = re.sub(
        r"^\*\*Due:\*\* .*?, 11:59 p\.m\. ET  $",
        f"**Due:** {due}, 11:59 p.m. ET  ",
        opening_cell.source,
        count=1,
        flags=re.MULTILINE,
    )

    old_seed = f"539{old_number:02d}"
    new_seed = f"539{new_number:02d}"
    if old_seed != new_seed:
        for cell in notebook.cells:
            cell.source = cell.source.replace(old_seed, new_seed)

    for index, cell in enumerate(notebook.cells):
        token = f"homework-{new_number:02d}-{index}-{cell.cell_type}".encode()
        cell.id = hashlib.sha1(token).hexdigest()[:8]
    nbf.validate(notebook)
    return notebook


def placeholder_homework(
    number: int, title: str, coverage: str, due: str
) -> nbf.NotebookNode:
    cell = markdown(
        f"""
        # Homework {number} — {title}

        **Coverage:** {coverage}<br>
        **Due:** {due}, 11:59 p.m. ET
        """
    )
    return make_notebook(number, [cell])


def active_homework_02() -> nbf.NotebookNode:
    """Merge one 25-point math problem with one 75-point MC study."""
    random_vectors = homework_02()
    monte_carlo = homework_03()
    notebook = nbf.v4.new_notebook(
        cells=[
            deepcopy(monte_carlo.cells[0]),
            deepcopy(monte_carlo.cells[1]),
            *deepcopy(random_vectors.cells[2:4]),
            *deepcopy(monte_carlo.cells[4:]),
        ],
        metadata=deepcopy(monte_carlo.metadata),
    )
    return retarget_notebook(
        notebook,
        old_number=3,
        new_number=2,
        title="Random Vectors and Monte Carlo Uncertainty Propagation",
        coverage="Lectures 5–10",
        due="Sunday, September 13, 2026",
    )


ACTIVE_BUILDERS = {
    1: homework_01,
    2: active_homework_02,
    3: lambda: retarget_notebook(
        homework_04(), old_number=4, new_number=3,
        title="Prior Information and Bayesian Earthquake Rates",
        coverage="Lectures 11–12", due="Sunday, September 20, 2026",
    ),
    4: lambda: retarget_notebook(
        homework_05(), old_number=5, new_number=4,
        title="Least Squares and Bayesian Elastic-Modulus Inference",
        coverage="Lectures 13–15", due="Sunday, September 27, 2026",
    ),
    5: lambda: placeholder_homework(
        5, "Classification, Clustering, and Dimensionality Reduction",
        "Lectures 16–18", "Sunday, October 18, 2026",
    ),
    6: lambda: retarget_notebook(
        homework_08(), old_number=8, new_number=6,
        title="State-Space Models and Kalman Filtering",
        coverage="Lectures 19–20", due="Sunday, October 25, 2026",
    ),
    7: lambda: retarget_notebook(
        homework_09(), old_number=9, new_number=7,
        title="Gaussian-Process Prediction for NIST Ultrasonic Calibration",
        coverage="Lectures 21–22", due="Sunday, November 1, 2026",
    ),
    8: lambda: placeholder_homework(
        8, "Bayesian Optimization for Model Calibration",
        "Lecture 23 and assigned model-calibration material",
        "Sunday, November 15, 2026",
    ),
    9: lambda: retarget_notebook(
        deep_neural_network_source(), old_number=11, new_number=9,
        title="Deep Neural-Network Regression",
        coverage="Lectures 24–25", due="Sunday, November 22, 2026",
    ),
    10: lambda: placeholder_homework(
        10, "Physics-Informed Modeling and Posterior Characterization",
        "Lectures 26–28", "Sunday, December 6, 2026",
    ),
}


def main() -> None:
    assert set(ACTIVE_BUILDERS) == set(range(1, 11))
    for number, builder in ACTIVE_BUILDERS.items():
        notebook = builder()
        path = HOMEWORK / f"homework-{number:02d}.ipynb"
        nbf.write(notebook, path)
        print(f"Wrote {path.relative_to(ROOT)} ({len(notebook.cells)} cells)")


if __name__ == "__main__":
    main()
