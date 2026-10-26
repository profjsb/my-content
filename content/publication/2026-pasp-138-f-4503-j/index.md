---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: 'BOOM and Babamul: A Real-time, Multi-survey, Optical Alert Broker System Operating
  at Scale'
subtitle: ''
summary: ''
authors:
- Theophile Jegou du Laz
- Michael W. Coughlin
- Peter Bachant
- Jacob E. Simones
- Thomas Culino
- Antoine Le Calloch
- Sushant Sharma Chaudhary
- Xander J. Hall
- Tyler Barna
- Daniel Warshofsky
- Matthew Graham
- Mansi M. Kasliwal
- Ashish Mahabal
- Joshua S. Bloom
- Antonella Palmese
- Frank J. Masci
- Steven L. Groom
- Richard Dekany
- Reed L. Riddle
- George Helou
tags: []
categories: []
date: '2026-06-01'
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
abstract: Abstract With the arrival of ever higher throughput wide-field surveys and a multitude
  of multi-messenger and multi-wavelength instruments to complement them, software capable
  of harnessing these associated data streams is urgently required. To meet these needs, a
  number of community supported alert brokers have been built, currently focused on processing
  of Zwicky Transient Facility (ZTF; ∼10 5 –10 6 alerts per night) with an eye toward Vera
  C. Rubin Observatory’s Legacy Survey of Space and Time (LSST; ∼2 × 10 7 alerts per night).
  Building upon the system that successfully ran in production for ZTF’s first seven years
  of operation, we introduce Burst & Outburst Observations Monitor ( BOOM ), an analysis framework
  focused on real-time, joint brokering of these alert streams. BOOM harnesses the performance
  of a Rust -based software stack relying on a non-relational MongoDB database combined with
  a Valkey in-memory processing queue and a Kafka cluster for message sharing. With this system,
  we demonstrate feature parity with the existing ZTF system with a throughput ∼7× higher.
  We describe the workflow that enables the real-time processing as well as the results with
  custom filters we have built to demonstrate the system’s capabilities. In conclusion, we
  present the development roadmap for both BOOM and Babamul —the public-facing LSST alert
  broker built atop BOOM —as we begin the Rubin era.
publication: '*Publications of the Astronomical Society of the Pacific*'
doi: 10.1088/1538-3873/ae6fef
---
