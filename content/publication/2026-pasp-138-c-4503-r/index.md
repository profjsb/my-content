---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: Pre-training Vision Models for the Classification of Alerts from Wide-field Time-domain
  Surveys
subtitle: ''
summary: ''
authors:
- Nabeel Rehemtulla
- Adam A. Miller
- Mike Walmsley
- Ved G. Shah
- Theophile Jegou du Laz
- Michael W. Coughlin
- Argyro Sasli
- Joshua S. Bloom
- Christoffer Fremling
- Matthew J. Graham
- Steven L. Groom
- David Hale
- Ashish A. Mahabal
- Daniel A. Perley
- Josiah Purdum
- Ben Rusholme
- Jesper Sollerman
- Mansi M. Kasliwal
tags: []
categories: []
date: '2026-03-01'
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
abstract: Abstract Modern wide-field time-domain surveys facilitate the study of transient,
  variable and moving phenomena by conducting image differencing and relaying alerts to their
  communities. Machine learning tools have been used on data from these surveys and their
  precursors for more than a decade, and convolutional neural networks (CNNs), which make
  predictions directly from input images, saw particularly broad adoption through the 2010s.
  Since then, continually rapid advances in computer vision have transformed the standard
  practices around using such models. It is now commonplace to use standardized architectures
  pre-trained on large corpora of everyday images (e.g., ImageNet). In contrast, time-domain
  astronomy studies still typically design custom CNN architectures and train them from scratch.
  Here, we explore the effects of adopting various pre-training regimens and standardized
  model architectures on the performance of alert classification. We find that the resulting
  models match or outperform a custom, specialized CNN like what is typically used for filtering
  alerts. Moreover, our results show that pre-training on galaxy images from Galaxy Zoo tends
  to yield better performance than pre-training on ImageNet or training from scratch. We observe
  that the design of standardized architectures are much better optimized than the custom
  CNN baseline, requiring significantly less time and memory for inference despite having
  more trainable parameters. On the eve of the Legacy Survey of Space and Time and other image-differencing
  surveys, these findings advocate for a paradigm shift in the creation of vision models for
  alerts, demonstrating that greater performance and efficiency, in time and in data, can
  be achieved by adopting the latest practices from the computer vision field.
publication: '*Publications of the Astronomical Society of the Pacific*'
doi: 10.1088/1538-3873/ae50bc
---
