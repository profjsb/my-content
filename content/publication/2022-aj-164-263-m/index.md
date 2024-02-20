---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: Deep Generative Modeling of Periodic Variable Stars Using Physical Parameters
subtitle: ''
summary: ''
authors:
- Jorge Martı́nez-Palomera
- Joshua S. Bloom
- Ellianna S. Abrahams
tags:
- Time domain astronomy
- Time series analysis
- Convolutional neural networks
- Periodic variable stars
- '2109'
- '1916'
- '1938'
- '1213'
categories: []
date: '2022-12-01'
lastmod: 2024-02-20T11:10:07-08:00
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
publishDate: '2024-02-20T19:10:07.591889Z'
publication_types:
- '2'
abstract: The ability to generate physically plausible ensembles of variable sources
  is critical to the optimization of time domain survey cadences and the training
  of classification models on data sets with few to no labels. Traditional data augmentation
  techniques expand training sets by reenvisioning observed exemplars, seeking to
  simulate observations of specific training sources under different (exogenous) conditions.
  Unlike fully theory- driven models, these approaches do not typically allow principled
  interpolation nor extrapolation. Moreover, the principal drawback of theory-driven
  models lies in the prohibitive computational cost of simulating source observables
  from ab initio parameters. In this work, we propose a computationally tractable
  machine learning approach to generate realistic light curves of periodic variables
  capable of integrating physical parameters and variability classes as inputs. Our
  deep generative model, inspired by the transparent latent space generative adversarial
  networks, uses a variational autoencoder (VAE) architecture with temporal convolutional
  network layers, trained using the OGLE-III optical light curves and physical characteristics
  (e.g., effective temperature and absolute magnitude) from Gaia DR2. A test using
  the temperature- shape relationship of RR Lyrae demonstrates the efficacy of our
  generative ``physics-enhanced latent space VAE'' (PELS-VAE) model. Such deep generative
  models, serving as nonlinear nonparametric emulators, present a novel tool for astronomers
  to create synthetic time series over arbitrary cadences.
publication: '*Astronomical Journal*'
doi: 10.3847/1538-3881/ac9b3f
---
