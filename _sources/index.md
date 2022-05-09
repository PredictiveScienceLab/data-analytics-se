(intro)=
# Preface

These are the lecture notes for ME 539 Introduction to Scientific Machine Learning.
Please note that these notes are a companion to the class lectures.
They are definitely not a self-contained, textbook-like, exposition of the topic of scientific machine learning.
They are supposed to be complementary to the course lectures.

(course-description)=
## Course description

This course provides an introduction to data science for individuals with no prior knowledge of data science or machine learning. The course starts with an extensive review of probability theory as the language of uncertainty, discusses Monte Carlo sampling for uncertainty propagation, covers the basics of supervised (Bayesian generalized linear regression, logistic regression, Gaussian processes, deep neural networks, convolutional neural networks), unsupervised learning (k-means clustering, principal component analysis, Gaussian mixtures) and state space models (Kalman filters). The course also reviews the state-of-the-art in physics-informed deep learning and ends with a discussion of automated Bayesian inference using probabilistic programming (Markov chain Monte Carlo, sequential Monte Carlo, and variational inference). Throughout the course, the instructor follows a probabilistic perspective that highlights the first principles behind the presented methods with the ultimate goal of teaching the student how to create and fit their own models. 

(course-learning-outcomes)=
## Course learning outcomes
After completing this course, you will be able to: 
+ Represent uncertainty in parameters in engineering or scientific models using probability theory.
+ Propagate uncertainty through physical models to quantify the induced uncertainty in quantities of interest.
+ Solve basic supervised learning tasks, such as: regression, classification, and filtering.
+ Solve basic unsupervised learning tasks, such as: clustering, dimensionality reduction, and density estimation.
+ Create new models that encode physical information and other causal assumptions.
+ Calibrate arbitrary models using data.
+ Apply various Python coding skills.
+ Load and visualize data sets in Jupyter notebooks.
+ Visualize uncertainty in Jupyter notebooks.
+ Recognize basic Python software (e.g., Pandas, numpy, scipy, scikit-learn) and advanced Python software (e.g., pytorch, pyro, Tensorflow, pymc3) commonly used in modern data science.

(prerequisites)=
## Prerequisites
+ Working knowledge of multivariate calculus and basic linear algebra.
+ Basic Python knowledge.
+ Knowledge of probability and numerical methods for engineers would be helpful, but not required.

(gaps)=
## What if I am not familiar with Python?
If you have no prior experience with Python, you have two options:
 + The fastest option is to go through the [Basic Python Tutorials](python-basics) that I have prepared.
 This set of tutorials is a bit terse, but it covers pretty much everything we are going to need in this course. You can probably go through them in a couple of days.
 + The longer option is to go over Lectures 1 to 7 of my undergraduate course on [data science for mechanical engineers](https://purduemechanicalengineering.github.io/me-297-intro-to-data-science/index.html).
 This is a much gentler introduction to the same basic Python concepts.
 It should take you about a week to cover these seven lectures.
