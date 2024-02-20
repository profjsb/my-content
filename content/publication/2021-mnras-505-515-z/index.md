---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: Classification of periodic variable stars with novel cyclic-permutation invariant
  neural networks
subtitle: ''
summary: ''
authors:
- Keming Zhang
- Joshua S. Bloom
tags:
- 'methods: data analysis'
- surveys
- 'stars: variables: general'
- Astrophysics - Instrumentation and Methods for Astrophysics
- Astrophysics - Solar and Stellar Astrophysics
- Computer Science - Machine Learning
- Physics - Data Analysis
- Statistics and Probability
categories: []
date: '2021-07-01'
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
publishDate: '2021-12-06T01:24:20.267097Z'
publication_types:
- '2'
abstract: We present Cyclic-Permutation Invariant Neural Networks, a novel class of
  neural networks (NNs) designed to be invariant to phase shifts of period-folded
  periodic sequences by means of 'symmetry padding'. In the context of periodic variable
  star light curves, initial phases are exogenous to the physical origin of the variability
  and should thus be immaterial to the downstream inference application. Although
  previous work utilizing NNs commonly operated on period-folded light curves, no
  approach to date has taken advantage of such a symmetry. Across three different
  data sets of variable star light curves, we show that two implementations of Cyclic-Permutation
  Invariant Networks- iTCN and iResNet-consistently outperform state-of-the-art non-
  invariant baselines and reduce overall error rates by between 4 to 22 per cent.
  Over a 10-class OGLE-III sample, the iTCN/iResNet achieves an average per-class
  accuracy of 93.4 per cent/93.3 per cent, compared to recurrent NN/random forest
  accuracies of 70.5 per cent/89.5 per cent in a recent study using the same data.
  Finding improvement on a non-astronomy benchmark, we suggest that the methodology
  introduced here should also be applicable to a wide range of science domains where
  periodic data abounds.
publication: '*Monthly Notices of the Royal Astronomical Society*'
doi: 10.1093/mnras/stab1248
links:
- name: arXiv
  url: https://arxiv.org/abs/2011.01243
---
