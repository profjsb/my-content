---
title: "deepCR: Cosmic Ray Rejection with Deep Learning"
date: 2019-09-01
publishDate: 2020-01-09T21:52:32.549487Z
authors: ["Keming Zhang", "Joshua Bloom"]
publication_types: ["2"]
abstract: "Cosmic ray (CR) identification and replacement are critical components of imaging and spectroscopic reduction pipelines involving solid-state detectors. We present deepCR, a deep learning based framework for CR identification and subsequent image inpainting based on the predicted CR mask. To demonstrate the effectiveness of this framework, we train and evaluate models on Hubble Space Telescope ACS/WFC images of sparse extragalactic fields, globular clusters, and resolved galaxies. We demonstrate that at a false positive rate of 0.5%, deepCR achieves close to 100% detection rates in both extragalactic and globular cluster fields, and 91% in resolved galaxy fields, which is a significant improvement over the current state-of-the-art method LACosmic. Compared to a multicore CPU implementation of LACosmic, deepCR CR mask predictions run up to 6.5 times faster on CPU and 90 times faster on a single GPU. For image inpainting, the mean squared errors of deepCR predictions are 20 times lower in globular cluster fields, 5 times lower in resolved galaxy fields, and 2.5 times lower in extragalactic fields, compared to the best performing non-neural technique tested. We present our framework and the trained models as an open-source Python project, with a simple-to-use API. To facilitate reproducibility of the results we also provide a benchmarking codebase."
featured: false
publication: "*The Journal of Open Source Software*"
tags: ["Python", "deep learning", "Pytorch", "cosmic ray", "astronomy", "image processing", "Astrophysics - Instrumentation and Methods for Astrophysics", "Computer Science - Computer Vision and Pattern Recognition"]
doi: "10.21105/joss.01651"
---

