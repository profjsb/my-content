---
title: "A recurrent neural network for classification of unevenly sampled variable stars"
date: 2018-11-01
publishDate: 2020-01-09T21:52:32.565900Z
authors: ["Brett Naul", "Joshua S. Bloom", "Fernando Pérez", "Stéfan van der Walt"]
publication_types: ["2"]
abstract: "Astronomical surveys of celestial sources produce streams of noisy time series measuring flux versus time (`light curves'). Unlike in many other physical domains, however, large (and source- specific) temporal gaps in data arise naturally due to intranight cadence choices as well as diurnal and seasonal constraints$^1-5$. With nightly observations of millions of variable stars and transients from upcoming surveys$^4,6$, efficient and accurate discovery and classification techniques on noisy, irregularly sampled data must be employed with minimal human-in-the-loop involvement. Machine learning for inference tasks on such data traditionally requires the laborious hand- coding of domain-specific numerical summaries of raw data (`features')$^7$. Here, we present a novel unsupervised autoencoding recurrent neural network$^8$ that makes explicit use of sampling times and known heteroskedastic noise properties. When trained on optical variable star catalogues, this network produces supervised classification models that rival other best-in-class approaches. We find that autoencoded features learned in one time-domain survey perform nearly as well when applied to another survey. These networks can continue to learn from new unlabelled observations and may be used in other unsupervised tasks, such as forecasting and anomaly detection."
featured: false
publication: "*Nature Astronomy*"
tags: ["Astrophysics - Instrumentation and Methods for Astrophysics", "Astrophysics - Solar and Stellar Astrophysics", "Physics - Data Analysis", "Statistics and Probability"]
doi: "10.1038/s41550-017-0321-z"
---

