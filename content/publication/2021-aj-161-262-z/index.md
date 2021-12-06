---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: Real-time Likelihood-free Inference of Roman Binary Microlensing Events with
  Amortized Neural Posterior Estimation
subtitle: ''
summary: ''
authors:
- Keming Zhang
- Joshua S. Bloom
- B. Scott Gaudi
- François Lanusse
- Casey Lam
- Jessica R. Lu
tags:
- Binary lens microlensing
- Gravitational microlensing exoplanet detection
- '2136'
- '2147'
- Astrophysics - Instrumentation and Methods for Astrophysics
- Astrophysics - Earth and Planetary Astrophysics
- Computer Science - Machine Learning
- Physics - Data Analysis
- Statistics and Probability
categories: []
date: '2021-06-01'
lastmod: 2021-12-05T17:24:20-08:00
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ''
  focal_point: ''
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
publishDate: '2021-12-06T01:24:20.547592Z'
publication_types:
- '2'
abstract: 'Fast and automated inference of binary-lens, single-source (2L1S) microlensing
  events with sampling-based Bayesian algorithms (e.g., Markov Chain Monte Carlo,
  MCMC) is challenged on two fronts: the high computational cost of likelihood evaluations
  with microlensing simulation codes, and a pathological parameter space where the
  negative-log-likelihood surface can contain a multitude of local minima that are
  narrow and deep. Analysis of 2L1S events usually involves grid searches over some
  parameters to locate approximate solutions as a prerequisite to posterior sampling,
  an expensive process that often requires human-in-the- loop domain expertise. As
  the next-generation, space-based microlensing survey with the Roman Space Telescope
  is expected to yield thousands of binary microlensing events, a new fast and automated
  method is desirable. Here, we present a likelihood- free inference approach named
  amortized neural posterior estimation, where a neural density estimator (NDE) learns
  a surrogate posterior $hatp(boldsymbolþeta | boldsymbolx)$ as an observation-parameterized
  conditional probability distribution, from pre-computed simulations over the full
  prior space. Trained on 291,012 simulated Roman-like 2L1S simulations, the NDE produces
  accurate and precise posteriors within seconds for any observation within the prior
  support without requiring a domain expert in the loop, thus allowing for real-time
  and automated inference. We show that the NDE also captures expected posterior degeneracies.
  The NDE posterior could then be refined into the exact posterior with a downstream
  MCMC sampler with minimal burn-in steps.'
publication: '*aj*'
doi: 10.3847/1538-3881/abf42e
links:
- name: arXiv
  url: https://arxiv.org/abs/2102.05673
---
