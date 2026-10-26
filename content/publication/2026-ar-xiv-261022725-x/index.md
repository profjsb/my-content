---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: Multi-modal transmission forecasting for the Vera C. Rubin Observatory
subtitle: ''
summary: ''
authors:
- Peter Xiangyuan Ma
- Joshua S. Bloom
tags: []
categories: []
date: '2026-10-01'
lastmod: '2026-10-26T00:00:00Z'
featured: false
draft: false
image:
  caption: ''
  focal_point: ''
  preview_only: false
projects: []
publishDate: '2026-10-26T00:00:00Z'
publication_types:
- '2'
abstract: In the age of large automated surveys conducted at facilities like the NSF-DOE Vera
  C. Rubin Observatory, delivering precision science goals demands highly efficient scheduling
  strategies that remain agile and dynamic to changing environments on the summit. On site,
  a variety of telemetry informs the scheduler of the best next pointing given the atmosphere's
  transmission. This live monitoring is provided by the Dutch Rubin Enhanced Atmospheric Monitor
  (DREAM) all-sky camera. Currently, dynamic scheduling uses short-term predictive algorithms,
  such as tracking cloud cross-correlations, to anticipate movement at short scheduling timescales.
  However, many of Rubin's core science objectives require survey strategies to commit to
  observations 20--40,min in advance (pair mode), which remains out of reach because clouds
  at those timescales can arrive from beyond the horizon. We developed a single monolithic
  multimodal strategy that folds asynchronous data from both the DREAM camera and weather
  satellite imagery to forecast multi-horizon sky transmission at 90,s, 5,min, 20,min, and
  30,min in advance. We demonstrate that at 20-minute timescales, our model reduces transmission
  error by 21% and false-clear misses by 22% versus Rubin's frozen-flow tracker, and reduces
  false-clear misses by 26% versus persistence. We also demonstrate empirically, through ablations,
  that the DREAM all-sky camera provides short-horizon predictive power while satellite imagery
  provides long-horizon predictive power. We estimate the optimistic order-of-magnitude gain
  for survey efficiency improvement to be between 0.1% to 1%.
publication: '*arXiv e-prints*'
links:
- name: arXiv
  url: https://arxiv.org/abs/2610.22725
---
