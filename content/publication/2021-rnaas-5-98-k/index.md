---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: 'DEEPCR on ACS/WFC: Cosmic-Ray Rejection for HST ACS/WFC Photometry'
subtitle: ''
summary: ''
authors:
- K. J. Kwon
- Keming Zhang
- Joshua S. Bloom
tags:
- Astronomy data reduction
- Convolutional neural networks
- Classification
- Neural networks
- Cosmic rays
- Hubble Space Telescope
- Astronomical detectors
- '1861'
- '1938'
- '1907'
- '1933'
- '329'
- '761'
- '84'
categories: []
date: '2021-04-01'
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
publishDate: '2021-12-06T01:24:20.707604Z'
publication_types:
- '2'
abstract: DEEPCR is a deep-learning-based cosmic-ray rejection algorithm previously
  demonstrated to be superior to state-of-the-art LACosmic on Hubble Space Telescope
  (HST) Advanced Camera for Surveys (ACS)/WFC F606W imaging data. In this research
  note, we present a new DEEPCR model for use on all filters of HST ACS/WFC. We train
  and test the model with ACS/WFC F435W, F606W, and F814W images, covering the entire
  spectral range of the ACS optical channel. The global model demonstrates near 100%
  detection rates of CRs in extragalactic fields and globular clusters and 91% in
  resolved galaxy fields. We further confirm the global applicability of the model
  by comparing its performance against single-filter models that were trained simultaneously
  and by testing the global model on data from another filter which was not previously
  used for training.
publication: '*Research Notes of the American Astronomical Society*'
doi: 10.3847/2515-5172/abf6c8
---
