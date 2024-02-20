---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: 'HEALPix Alchemy: Fast All-Sky Geometry and Image Arithmetic in a Relational
  Database for Multimessenger Astronomy Brokers'
subtitle: ''
summary: ''
authors:
- Leo P. Singer
- B. Parazin
- Michael W. Coughlin
- Joshua S. Bloom
- Arien Crellin-Quick
- Daniel A. Goldstein
- Stéfan van der Walt
tags:
- Gravitational wave astronomy
- Time domain astronomy
- Virtual observatories
- Cloud computing
- Astronomy databases
- '675'
- '2109'
- '1774'
- '1970'
- '83'
- Astrophysics - Instrumentation and Methods for Astrophysics
- Astrophysics - High Energy Astrophysical Phenomena
- General Relativity and Quantum Cosmology
categories: []
date: '2022-05-01'
lastmod: 2024-02-20T11:10:08-08:00
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
publishDate: '2024-02-20T19:10:08.321324Z'
publication_types:
- '2'
abstract: Efficient searches for electromagnetic counterparts to gravitational wave,
  high-energy neutrino, and gamma-ray burst events demand rapid processing of image
  arithmetic and geometry set operations in a database to cross-match galaxy catalogs,
  observation footprints, and all-sky images. Here we introduce HEALPix Alchemy, an
  open-source, pure Python implementation of a set of methods that enables rapid all-sky
  geometry calculations. HEALPix Alchemy is built upon HEALPix, a spatial indexing
  strategy that is widely used in astronomical databases as well as the native format
  of LIGO-Virgo-KAGRA gravitational-wave sky localization maps. Our approach leverages
  new multirange types built into the PostgreSQL 14 database engine. This enables
  fast all-sky queries against probabilistic multimessenger event localizations and
  telescope survey footprints. Questions such as ``What are the galaxies contained
  within the 90% credible region of an event?'' and ``What is the rank-ordered list
  of the fields within an observing footprint with the highest probability of containing
  the event?'' can be performed in less than a few seconds on commodity hardware using
  off-the-shelf cloud-managed database implementations without server-side database
  extensions. Common queries scale roughly linearly with the number of telescope pointings.
  As the number of fields grows into the hundreds or thousands, HEALPix Alchemy is
  orders of magnitude faster than other implementations. HEALPix Alchemy is now used
  as the spatial geometry engine within SkyPortal, which forms the basis of the Zwicky
  Transient Facility transient marshal, called Fritz.
publication: '*Astronomical Journal*'
doi: 10.3847/1538-3881/ac5ab8
links:
- name: arXiv
  url: https://arxiv.org/abs/2112.06947
---
