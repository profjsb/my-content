---
title: "On Machine-learned Classification of Variable Stars with Sparse and Noisy Time-series Data"
date: 2011-05-01
publishDate: 2020-01-09T21:52:32.822329Z
authors: ["Joseph W. Richards", "Dan L. Starr", "Nathaniel R. Butler", "Joshua S. Bloom", "John M. Brewer", "Arien Crellin-Quick", "Justin Higgins", "Rachel Kennedy", "Maxime Rischard"]
publication_types: ["2"]
abstract: "With the coming data deluge from synoptic surveys, there is a need for frameworks that can quickly and automatically produce calibrated classification probabilities for newly observed variables based on small numbers of time-series measurements. In this paper, we introduce a methodology for variable-star classification, drawing from modern machine-learning techniques. We describe how to homogenize the information gleaned from light curves by selection and computation of real-numbered metrics (features), detail methods to robustly estimate periodic features, introduce tree-ensemble methods for accurate variable-star classification, and show how to rigorously evaluate a classifier using cross validation. On a 25-class data set of 1542 well-studied variable stars, we achieve a 22.8% error rate using the random forest (RF) classifier; this represents a 24% improvement over the best previous classifier on these data. This methodology is effective for identifying samples of specific science classes: for pulsational variables used in Milky Way tomography we obtain a discovery efficiency of 98.2% and for eclipsing systems we find an efficiency of 99.1%, both at 95% purity. The RF classifier is superior to other methods in terms of accuracy, speed, and relative immunity to irrelevant features; the RF can also be used to estimate the importance of each feature in classification. Additionally, we present the first astronomical use of hierarchical classification methods to incorporate a known class taxonomy in the classifier, which reduces the catastrophic error rate from 8% to 7.8%. Excluding low- amplitude sources, the overall error rate improves to 14%, with a catastrophic error rate of 3.5%."
featured: false
publication: "*Astrophysical Journal*"
tags: ["methods: data analysis", "methods: statistical", "stars: variables: general", "techniques: photometric", "Astrophysics - Instrumentation and Methods for Astrophysics", "Statistics - Applications"]
doi: "10.1088/0004-637X/733/1/10"
---

