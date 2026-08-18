# ME 539 — Introduction to Scientific Machine Learning

This repository contains the lecture book, Jupyter notebooks, and supporting
materials for Purdue University's ME 539, *Introduction to Scientific Machine
Learning*. The current offering is taught by Prof. Ilias Bilionis in Fall 2026.

## Fall 2026 offering

- Campus students meet Tuesdays and Thursdays, 10:30–11:15 a.m. ET, in
  ME 2061.
- Online/EPE and asynchronous students have no required synchronous class
  meetings. They complete the same course modules and follow the published
  homework and exam deadlines.
- The course uses 28 numbered lecture modules, ten homework assignments, and
  three noncomprehensive unit exams.
- Registered Purdue students access lecture videos, announcements, assignment
  links, and the official course schedule through
  [Brightspace](https://purdue.brightspace.com/d2l/login). Homework is submitted
  through Gradescope.
- Google Colab is the recommended environment for course activities and
  homework. The repository can also be run locally using the locked `uv`
  environment described below.

Course policies, deadlines, examination logistics, and accommodations are
governed by the current syllabus and Brightspace site.

The material is distributed under the GNU General Public License v3. If you
reuse or modify it, follow the terms in [LICENSE](LICENSE) and cite this
repository. Prof. Bilionis welcomes a note at ibilion@purdue.edu when the
material is reused.

## Lecture Book

The published lecture book is available
[here](https://predictivesciencelab.github.io/data-analytics-se/index.html).
It contains the reading activities, hands-on notebooks, and homework pages used
by the course. Pre-recorded videos for the numbered lecture modules are linked
through the Purdue course site.

## Local development

All Python environments, dependencies, and command-line tools for this
repository are managed with [uv](https://docs.astral.sh/uv/):

```bash
uv sync --locked
```

The notebooks that draw directed graphs also require the Graphviz `dot` system
executable. On macOS it can be installed with `brew install graphviz`; this is a
system dependency rather than a Python package.

To audit notebook execution without changing their stored outputs, run:

```bash
uv run --locked python tools/execute_notebooks.py
```

Pass `--in-place` only when the refreshed outputs should be saved. Build the
classic Jupyter Book with `./make.sh`; maintainers can publish the validated
build with `./make.sh --publish`.

## Older Course Versions

+ [Fall 2020 version](https://github.com/PredictiveScienceLab/data-analytics-se/tree/fall2020)
+ [Fall 2021 version](https://github.com/PredictiveScienceLab/data-analytics-se/tree/fall2021)
+ [Summer 2022 version](https://github.com/PredictiveScienceLab/data-analytics-se/tree/summer2022)
+ [Fall 2023 version](https://github.com/PredictiveScienceLab/data-analytics-se/tree/fall2023)

This course evolved from the ME 597 "Data Analytics for Scientists and Engineers," taught two times by Prof. Bilionis, and the ME 597/MA 598 "Introduction to Uncertainty Quantification," taught three times by Prof. Bilionis (the first time, Spring 2016 it was co-taught with Prof. Guang Lin).
If you are interested in accessing the old versions of the course, they can be found [here](https://github.com/PredictiveScienceLab/uq-course).

Note that there is also a 1-credit undergraduate version of the course under ME 297, "Introduction to Data Science for Mechanical Engineers." This version can be found [here](https://github.com/PurdueMechanicalEngineering/me-297-intro-to-data-science).
