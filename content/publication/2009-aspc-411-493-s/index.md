---
title: "The Berkeley Transient Classification Pipeline: Deriving Real-time Knowledge from Time-domain Surveys"
date: 2009-01-01
publishDate: 2020-01-09T21:52:32.935370Z
authors: ["D. L. Starr", "J. S. Bloom", "J. M. Brewer", "N. R. Butler", "D. Poznanski", "M. Rischard", "C. Klein"]
publication_types: ["6"]
abstract: "The Berkeley Transients Classification Pipeline (TCP) is a parallelized source identification, classification, and broadcast pipeline which ingests several real-time data torrents and emits science events of pre-articulated interest. The TCP's classification machine-learning algorithms are trained using a comprehensive science class hierarchy of light-curves which are resampled to emulate the cadence and quality of incoming observatory data streams. The referenced classified light-curves are contained within our growing public data warehouse, DotAstro.org (http://dotastro.org/). To effectively distinguish a source's classification from neighboring classes or hierarchical parents, dozens of real-number metrics (``features'') are derived from its light-curve, color information, spatial context, and historical data. Upon science class identification (or reclassification), a VOEvent XML containing all available information is broadcast to subscribed telescopes and science groups for followup. Subsequently acquired data for that source can then be fed back to DotAstro.org which the TCP will use to reinforce its internal model of the source's science class. <P />"
featured: false
publication: "*Astronomical Data Analysis Software and Systems XVIII ASP Conference Series, Vol. 411, proceedings of the conference held 2-5 November 2008 at Hotel Loews Le Concorde, Québec City, QC, Canada. Edited by David A. Bohlender, Daniel Durand, and Patrick Dowler.  San Francisco: Astronomical Society of the Pacific, 2009., p.493*"
---

