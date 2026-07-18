---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: 'A Morphological Model to Separate Resolved -- Unresolved Sources in the DESI Legacy
  Surveys: Application in the LS4 Alert Stream'
subtitle: ''
summary: ''
authors:
- Chang 畅 Liu 刘
- Adam A. Miller
- Joshua S. Bloom
- Robert A. Knop
- Peter E. Nugent
tags: []
categories: []
date: '2025-08-01'
lastmod: '2026-07-17T00:00:00Z'
featured: false
draft: false
image:
  caption: ''
  focal_point: ''
  preview_only: false
projects: []
publishDate: '2026-07-17T00:00:00Z'
publication_types:
- '2'
abstract: Abstract Separating resolved and unresolved sources in large imaging surveys is
  a fundamental step to enable downstream science, such as searching for extragalactic transients
  in wide-field time-domain surveys. Here we present our method to effectively separate point
  sources from the resolved, extended sources in the Dark Energy Spectroscopic Instrument
  (DESI) Legacy Surveys (LS). We develop a supervised machine learning model based on the
  Gradient Boosting algorithm XGBoost. The features input to the model are purely morphological
  and are derived from the tabulated LS data products. We train the model using ∼2 × 105 LS
  sources in the COSMOS field with HST morphological labels and evaluate the model performance
  on LS sources with spectroscopic classification from the DESI Data Release 1 (∼2 × 107 objects)
  and the Sloan Digital Sky Survey Data Release 17 (∼3 × 106 objects), as well as on ∼2 ×
  108 Gaia stars. A significant fraction of LS sources are not observed in every LS filter,
  and we therefore build a “Hybrid” model as a linear combination of two XGBoost models, each
  containing features combining aperture flux measurements from the “blue” (gr) and “red”
  (iz) filters. The Hybrid model shows a reasonable balance between sensitivity and robustness,
  and achieves higher accuracy and flexibility compared to the LS morphological typing. With
  the Hybrid model, we provide classification scores for ∼3 × 109 LS sources, making this
  the largest ever machine learning catalog separating resolved and unresolved sources. The
  catalog has been incorporated into the real-time pipeline of the La Silla Schmidt Southern
  Survey (LS4), enabling the identification of extragalactic transients within the LS4 alert
  stream.
publication: '*Publications of the Astronomical Society of the Pacific*'
doi: 10.1088/1538-3873/adf7db
---
