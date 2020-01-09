---
title: "Optimizing Automated Classification of Variable Stars in New Synoptic Surveys"
date: 2012-03-01
publishDate: 2020-01-09T21:52:32.762517Z
authors: ["James P. Long", "Noureddine El Karoui", "John A. Rice", "Joseph W. Richards", "Joshua S. Bloom"]
publication_types: ["2"]
abstract: "Efficient and automated classification of periodic variable stars is becoming increasingly important as the scale of astronomical surveys grows. Several recent articles have used methods from machine learning and statistics to construct classifiers on databases of labeled, multi-epoch sources with the intention of using these classifiers to automatically infer the classes of unlabeled sources from new surveys. However, the same source observed with two different synoptic surveys will generally yield different derived metrics (features) from the light curve. Since such features are used in classifiers, this survey- dependent mismatch in feature space will typically lead to degraded classifier performance. In this article we show how and why feature distributions change using OGLE and Hipparcos light curves. To overcome survey systematics, we apply a noisification method, which attempts to empirically match distributions of features between the labeled sources used to construct the classifier and the unlabeled sources we wish to classify. Results from simulated and real-world light curves show that noisification can significantly improve classifier performance. In a three-class problem using light curves from Hipparcos and OGLE, noisification reduces the classifier error rate from 27.0% to 7.0%. We recommend that noisification be used for upcoming surveys such as Gaia and LSST, and we describe some of the promises and challenges of applying noisification to these surveys."
featured: false
publication: "*Publications of the Astronomical Society of the Pacific*"
tags: ["Astrophysics - Instrumentation and Methods for Astrophysics", "Statistics - Applications"]
doi: "10.1086/664960"
---

