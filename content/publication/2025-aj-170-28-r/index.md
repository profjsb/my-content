---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: 'AstroM<SUP>3</SUP>: A Self-supervised Multimodal Model for Astronomy'
subtitle: ''
summary: ''
authors:
- M. Rizhko
- Joshua S. Bloom
tags: []
categories: []
date: '2025-07-01'
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
abstract: Abstract While machine-learned models are now routinely employed to facilitate astronomical
  inquiry, model inputs tend to be limited to a primary data source (namely images or time
  series) and, in the more advanced approaches, some metadata. Yet with the growing use of
  wide-field, multiplexed observational resources, individual sources of interest often have
  a broad range of observational modes available. Here we construct an astronomical multimodal
  dataset and propose AstroM3, a self-supervised pretraining approach that enables a model
  to learn from multiple modalities simultaneously. We extend the Contrastive Language-Image
  Pretraining (CLIP) model to a trimodal setting, allowing the integration of time-series
  photometry data, spectra, and astrophysical metadata. In a fine-tuning supervised setting,
  CLIP pretraining improves classification accuracy, particularly when labeled data is limited,
  with increases of up to 14.29% in spectra classification, 2.27% in metadata, and 10.20%
  in photometry. Furthermore, we show that combining photometry, spectra, and metadata improves
  classification accuracy over single-modality models. In addition to fine-tuned classification,
  we can use the trained model in other downstream tasks that are not explicitly contemplated
  during the construction of the self-supervised model. In particular we show the efficacy
  of using the learned embeddings to identify misclassifications, for similarity search, and
  for anomaly detection. One surprising highlight is the “rediscovery” of Mira subtypes and
  two rotational variable subclasses using manifold learning and dimensionality reduction
  algorithms. To our knowledge this is the first construction of an n > 2 mode model in astronomy.
  Extensions to n > 3 modes are naturally anticipated with this approach.
publication: '*The Astronomical Journal*'
doi: 10.3847/1538-3881/adcbad
---
