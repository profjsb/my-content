---
title: "Active Learning to Overcome Sample Selection Bias: Application to Photometric Variable Star Classification"
date: 2012-01-01
publishDate: 2020-01-09T21:52:32.782977Z
authors: ["Joseph W. Richards", "Dan L. Starr", "Henrik Brink", "Adam A. Miller", "Joshua S. Bloom", "Nathaniel R. Butler", "J. Berian James", "James P. Long", "John Rice"]
publication_types: ["2"]
abstract: "Despite the great promise of machine-learning algorithms to classify and predict astrophysical parameters for the vast numbers of astrophysical sources and transients observed in large-scale surveys, the peculiarities of the training data often manifest as strongly biased predictions on the data of interest. Typically, training sets are derived from historical surveys of brighter, more nearby objects than those from more extensive, deeper surveys (testing data). This sample selection bias can cause catastrophic errors in predictions on the testing data because (1) standard assumptions for machine-learned model selection procedures break down and (2) dense regions of testing space might be completely devoid of training data. We explore possible remedies to sample selection bias, including importance weighting, co-training, and active learning (AL). We argue that AL—where the data whose inclusion in the training set would most improve predictions on the testing set are queried for manual follow-up—is an effective approach and is appropriate for many astronomical applications. For a variable star classification problem on a well-studied set of stars from Hipparcos and Optical Gravitational Lensing Experiment, AL is the optimal method in terms of error rate on the testing data, beating the off-the-shelf classifier by 3.4% and the other proposed methods by at least 3.0%. To aid with manual labeling of variable stars, we developed a Web interface which allows for easy light curve visualization and querying of external databases. Finally, we apply AL to classify variable stars in the All Sky Automated Survey, finding dramatic improvement in our agreement with the ASAS Catalog of Variable Stars, from 65.5% to 79.5%, and a significant increase in the classifier's average confidence for the testing set, from 14.6% to 42.9%, after a few AL iterations."
featured: false
publication: "*Astrophysical Journal*"
tags: ["methods: data analysis", "methods: statistical", "stars: variables: general", "techniques: photometric", "Astrophysics - Instrumentation and Methods for Astrophysics", "Statistics - Applications"]
doi: "10.1088/0004-637X/744/2/192"
---

