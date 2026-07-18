---
title: "Machine Learning for Time-Domain Astrophysics"
date: 2018-02-26
publishDate: 2018-02-26
draft: false
event: "Real-Time Decision Making program, Simons Institute"
event_url: "https://simons.berkeley.edu/talks/machine-learning-time-domain-astrophysics"
location: "Berkeley, CA"
summary: "How statistical ML applies to astronomy in batch and streaming contexts: feature-engineered supernova identification and variable-star characterization, and autoencoder/RNN architectures that learn without hand-built features."
topics: ["astronomy", "ai-ml"]
talk_type: "Talk"
talk_number: 91
display_date: "Feb 2018"
url_video: "https://www.youtube.com/watch?v=iLBNeWnqnkQ"
has_transcript: true
---

How statistical ML applies to astronomy in batch and streaming contexts: feature-engineered supernova identification and variable-star characterization, and autoencoder/RNN architectures that learn without hand-built features.

*He also co-organized this semester-long program.*

## Transcript

[PETER] --CS math side of things. He is touching upon the second of our talks today in astrophysics here, machine learning for time-domain astrophysics, and the interesting part about this is it's really gonna answer one of the questions — it's an approach to answer one of the questions that Eric brought up in the previous talk, which is: what do you do when you have sparse, incomplete data from a survey like LSST when you're trying to sort through these millions of objects every single day? So, Josh? Thank you.

[JOSH BLOOM] Thank you, Peter, and thanks to the Simons Institute, and to the Moore and the Sloan Foundations for their support in the past and currently. I think it's worth saying at the outset that the fundamental reason why we do the work we do to innovate on the algorithmic side and computationally is to do novel science. In this case, it'll be in astrophysics, but what you're gonna hear throughout the week is a broad interest in using these tools and building new tools to do some novel work in the physical domains. We also use this because of the fire hose that you just heard about in the previous talk, just to be able to handle that onslaught and be able to make the best use of the data that's coming at us. And I think increasingly what we're seeing is that because this is a very powerful set of tools, i.e., machine learning in astronomy, it's also becoming a competitive advantage for the groups that know how to use it.

Let me start off with what is probably the most exciting discovery of the last decade, if not longer, in astrophysics, which brings together the physics community and the astrophysics community around the so-called merging neutron star events. You're gonna hear a lot about this from Alessandra and Mansi later today, so I don't want to harp on it, but use it really as a launching-off point and point of departure for saying that there are some very big prizes in understanding the universe and the connection of, say, the gravitational wave universe with the electromagnetic universe. And we're just starting to see this era start up. And so the discovery last summer

and the announcements that you heard about just over the last couple of months have really emphasized to many of us the importance of being able to do real-time inference and discovery — not just because if you don't find it, you don't get to do good science afterwards, but because there are many other groups working on this. And in fact, that's perhaps best shown with this paper here, which has 3,677 authors. There are a lot of people involved in this work, all taking different facets around what is fundamentally just a single event. You'll hear a lot more about that event and its importance and its implications later on.

But I think this event really is a great reason for us to recognize that we need to do discovery on images, as you heard about in the previous talk, and for those of you that were at the boot camp before. On the left-hand side: are these real or spurious images? That's an important question. And then we need to do inference. If you look at the graph on the right-hand side, this is what we call a light curve in astronomy parlance. It's brightness on the Y axis and time on the X axis, and the question is, when you look at this, is it worth spending time on this object, not just with the instrument that's doing the discovery but with other follow-up facilities that are potentially more sensitive or can look at it in a

different wavelength or take a spectrum to understand perhaps the chemical composition of this object? That's the question that we ask. And if it wasn't clear from Eric's talk, it's probably worth saying that if you have sufficient sensitivity, every single thing in the sky changes. It changes its color, it changes its brightness, it changes its position on the sky if you look hard enough. And so while oftentimes we focus on the things that are most fantastic — the biggest explosions that just become so obvious they're as bright as their whole host galaxy — there are lots more subtle objects that are only changing at the few percent level or less that have some very interesting facets to them that many groups wanna follow up.

What you see on the right-hand side is also a light curve that's pretty rich. You see it's irregularly sampled. You can't really see the fact that some of these data points are noisy, but oftentimes some of the most exciting science comes out when you only have one or two data points on a new object as it's being born or as it's just starting to evolve. And so a really important question that we have to wind up asking, again, in the real-time context is: if we only have a few data points, do we observe that object and continue to observe that object and keep burning resources?

The agenda in my talk today, really geared for non-astronomers to get somewhat up to speed on the state of

machine learning in the time-domain astronomy world, is to introduce to you the different ways in which we view the time domain and real-time types of inference, with the lens not just as astronomers but as people who are applying and potentially even innovating on some of the tools to get better science out. And I hope at the end to present some interesting challenges and maybe even some right places to start for the non-astronomers in the room from a collaborative perspective.

I'll start with just some of the constraints and some of the things that we think about when we're building some of these computational systems and working on some of our algorithms. I'll talk about discovery, and this has been discussed both in the previous talk and was also done in the boot camp, so I'll go over that part pretty quickly and focus a lot on inference — the real-time part of the inference: what is this object, I only have a few data points, what do I do next? And then the retrospective: not just looking at a single object, but looking at large catalogs of objects in the time domain to try to figure out how I get good science out. And then I'll end with some of those challenges and open questions.

Just to level set what I'll present here, something that doesn't look at all like the scientific method but is actually the way in which astronomers work: you do lots of planning and acquisition

of data. What you heard about in LSST, what you'll see about ZTF, is trying to figure out the ways in which you wind up observing the sky. This is what's often called the cadence: how often do you repeat a certain observation of the same part of the sky? And there's obviously a trade-off. If you don't go back to the same part of the sky, then you're gonna miss objects that are changing rapidly, but it means then you have the opportunity to survey a larger part of the sky. So there are always some biases, in a positive way, of what type of science people are trying to get at from that perspective. It's allocating telescope resources, it's deciding how to move the data around, et cetera.

The next part, which I won't spend much time on either, is in the cataloging and characterization. You heard from Eric's talk how LSST is going to be cataloging potentially interesting places on the sky and maybe even telling you a little bit about the properties of those objects on the sky. How do you extract from an image of the sky metadata like the brightness? That's a non-trivial exercise, and it needs to be done right and well, certainly at scale. Associating that data with other catalogs is important, and again, storage and retrieval of that and making that efficient and useful for communities is quite important.

Instead, what I'll focus

on is really the next part, the discovery, which is the question: is this source in my catalog real or not? And is the source even potentially interesting for me to spend time on? And what's the appropriate science that I could potentially get out of this if I decided to keep going and start asking more questions of this data? I make the distinction, by the way, between cataloging and discovery because if you put something into your database, it doesn't mean you recognize that it's interesting.

And for me, the best exemplar of this comes from a catalog from about 400 years ago from Galileo, who was observing and discovering the Galilean moons, and you can see the actual photograph of part of that journal. There's Jupiter there, there are three of the Galilean moons, and we now know on that day that Neptune was actually at the position that's listed as a fixed star. And about two weeks later, Galileo came back and noticed that that fixed star had kinda moved, but didn't really recognize that that was actually another planet. So it was about 150 years later that Neptune was actually discovered. I find this fascinating, and potentially the best well-known example in science of cataloging something really important but not recognizing its importance. So I try to make that distinction. I argue that if Galileo had found Neptune, he would've been very

famous. Okay, we've got some laughter, which is good.

What comes after discovery is inference. I now know this object is interesting, I now know it's real. What is the source? Is this like something we've seen before? Is it not? If we're right about the classification, what is it gonna look like the next time I observe? And then the last part of that is: what's the next action? This is the federation that came up in some of the discussion after the last talk. Is this source important enough to spend more resources on it? And what is it that I actually want to do with it? And more importantly perhaps, given the sociology of the astronomy community: can I convince my friends, and collaborators, and enemies to actually stop observing what they're looking at because my object is more important than your object? We still very much focus, from a real-time perspective, on individual objects, and I'll try to emphasize for you in just a little bit why that's so. And then the last part of that, of course, is if you then have that hypothesis about what you should be doing next, you go, and you plan, and you get more data. And so this cycle continues on and on.

All right, let me give you four different facets of the things that we're trying to optimize over, because in the end, if we're talking about machine learning, we're talking about

some sort of optimization. And unfortunately, this is not a loss function that I can trivially write down and then just throw whatever mechanics I have at it to get the right answer. Some of this stuff is a little bit softer, but I wanted to tell you a little bit about the ways that we think about this and are motivated by it.

Number one is something I think you all know, which is that experts don't scale. Haven't quite figured that out yet. This picture from the 1890s is of a bunch of so-called computers looking at lots of images: when astronomy had a big data problem, lots of images coming off of telescopes, it was hire and train people to just look at data. This is what I call the "just hire more grad students" syndrome, which is what many of us have been told for years, even in the time domain: that if you have more data, you just need to get more grad students to look at that data. That obviously doesn't scale in the sheer numbers, but if we're also interested in some of these real-time applications, where an image is taken and then 60 seconds later you need to take another action based on those images, people aren't that fast. And from another perspective, which is probably even the most damning, people are pretty subjective. And so if we want to do this in an objective way — doesn't mean that there won't be biases —

you want to be able to do what it is that these people are doing on the right programmatically, and do it systematically, at least where you can codify and you can version what it is that they're doing.

Another facet, which I think has been danced around a little bit when we talk about the LSST fire hose, is that we're now entering this age of what I'll call cheap discovery, where we're gonna be getting literally 10 million transient alerts per night from LSST, and maybe an order of magnitude less from ZTF starting next week. But we have a very, very expensive follow-up. To get the best and most novel science out of the changing sky, we have to use these facilities like the Hubble Space Telescope, like the James Webb Space Telescope. These are all billion-dollar-plus level facilities, and those resources, as you can imagine, are very precious, and they're massively oversubscribed. Everybody wants to be using these facilities, and it's extremely expensive for them to do that. So there's an opportunity cost, because when you do your science, it means somebody else isn't doing their science, and that's interesting from a systemic perspective. There's also the people opportunity cost as well. It costs energy and people to spend time getting these observations prepared. And then there are these interesting questions around the false positives. If I'm trying to do extremely novel science, how often should

I be using one of these billion-dollar facilities and just observing a place in the sky where good science doesn't actually come out? And oftentimes, you wind up being more conservative and requiring a guaranteed scientific payout before you actually do any speculative work on these big facilities. Another facet--

[NANCY] Discovery is getting expensive.

[JOSH BLOOM] Sorry, what's that?

[NANCY] Discovery is getting expensive, right, with LSST?

[JOSH BLOOM] Well, discovery per-- or dollars per discovery would be an interesting number to look at. I'd argue that it's actually getting cheaper, if each one of those is equally interesting, you could argue. And again, because LSST wasn't designed to do time domain — it was designed to do other science in the static sky — I'd argue that's a very, very cheap use of resources, to piggyback off of the static sky science.

And then there's the kind of Rumsfeldian challenge, which is trying to optimize over the known knowns — so there's some bread-and-butter science that you could get out of doing time domain — the unknown unknowns, and then stuff in the middle, things that you have theoretical models for but you haven't yet seen, like the known unknowns. And what's interesting is that this plot is, I don't know, 10 years old or so. The curve that you see for the neutron star-neutron star mergers is approximately correct just from the theoretical perspective of what we expected to see following a neutron star-neutron star merger.

Now I'd call this more of a known known, but before, I used to herald that one as a known unknown. But there's stuff that are unknown unknowns, and by definition I can't put them on this plot. So you see the timescales over which big explosive events wind up proceeding. There are some other really interesting things that wind up happening even on shorter timescales than are shown here, and I'll emphasize those a little bit later on.

Another aspect of this Rumsfeldian challenge is the small number of labels. In a huge amount of the machine learning literature, there is this implicit assumption that I have lots and lots of data, at least from a supervised perspective, to be able to build these models. If you want to build a good image classifier, just get more images and get a whole bunch of people to label them, like at the Flickr level, or do it implicitly through Google searches and things like that. In astronomy, we don't have that many labels. For things that we're really interested in, we only have one exemplar of a real object that is a neutron star-neutron star merger. One. We've got theoretical models of a whole bunch of those with different inputs, but for some of these we really only have dozens or maybe hundreds at best, or maybe thousands as we're entering into this LSST era. So we're really,

even though it's a big data fire hose, from a labeling perspective it's still very much a small data problem.

And the last is that it's all well and good to have some plots that show how you have a better false positive versus false negative curve than somebody else in retrospect. These systems that involve machine learning that are gonna be put into place for astronomy have to be done with robust systems that actually work in real time. And oftentimes one of the biggest challenges we have is not on the algorithmic side; it's not on being able to produce those plots in retrospect. It's being able to stand up robust systems that work at scale that can ingest this fire hose and produce results that people can wind up accepting and using and then moving on into that value chain of inference. And for those that haven't read this yet, this is one of my favorite papers in machine learning. It has no equations in it. It just highlights all the different bugaboos of what it means to build a real, robust, functioning system that involves machine learning, and how different that is even from just best software engineering practices. So forget about the fact that astronomers are not trained as software engineers — we're certainly not trained in general as being able to build and stand up and maintain and innovate these very large-scale systems.

So that's some of the constraints and some

of the concerns that we have as we start thinking about bringing machine learning into our world.

I want to now touch a little bit on discovery — that facet of, "I've got something in my database, is this interesting? Is it real? And what should I do next with it?" You've already seen real-bogus mentioned in the previous talk. You see the bad subtractions on the top as we're trying to find new objects, and the real, good subtractions on the bottom. It's a little bit like Anna Karenina, where all the bogus detections are all different than each other, and all the real ones are all similar to each other. But unfortunately, state of the art puts us at about a thousand to one, or maybe we're getting down to a few hundred to one, of this needle in a haystack. That is, for every real object in a real image that we wind up taking of the sky, there are hundreds of bogus detections. So we have to find these real ones in the face of quite a large number of bogus detections.

And what's nice is that if we can build a real-time framework to identify what's real and what's not, we get some really nice things out of that. It will be fast, because it's just algorithmic implementation. Embarrassingly parallel, because every single object we can ask that question. Transparent, in the sense that we can know why we got the answer we got. So if

you're doing it in a random forest context, you can literally follow down the different trees and figure out why you got that answer. It's deterministic, so given the same data, you get the same answer, unlike with people. And it's versionable, so I can keep on upgrading, and if I need to go back and reproduce what I had before, I at least have a fighting chance at that.

What we found in some of the early work on building a real-bogus detector for real systems was that it was a very hard problem. It was based on features that we derived out of the images and the subtraction images — we got of order 75 of those. First of all, that's a bit of a computational challenge, 'cause some of those features are expensive to construct. But then we also wound up realizing that there are only really a few algorithms that actually did well on the same input feature space. And in particular, we found that random forest was doing extremely well relative to all the others given the same feature set. And so we wound up implementing this and sticking this into a real pipeline that was run up at LBL as part of PTF, and what happened is every time a new transient or a new object was cataloged, it would wind up getting scored in a real-bogus sense from zero to one, and then, depending upon where you make your cut of what you call real and what you call not real, you wind up

pushing this into downstream systems to be followed up and potentially even looked at by people.

One of the things that those who were at the boot camp saw, and the astronomers already know about this, is this great discovery that was done by Peter, which I'll call ML-assisted in the sense that a real-bogus classifier was applied to this incoming data stream on new images that were coming off of PTF. About 11 hours after explosion, PTF wound up observing and cataloging, and then Peter wound up noting that one of the highest-ranked real-bogus objects from the catalog was actually a very young supernova that turned out to be the nearest Type Ia supernova in more than three decades. So only a few people in the history of mankind have observed supernovae this close by and this early and have been the discoverer, so I was very happy to see that Peter changed his business card just so everyone knew how important that was. But the thumb--

[PETER] Is covering a student to be determined. Yeah.

[JOSH BLOOM] Exactly. There's a student under that fingernail there. But what's more important — and this supernova, by the way, would wind up rising in brightness to the point where if you had binoculars you could have observed it through those binoculars, which is just absolutely stunning. So it was eventually found and could have been seen by astronomers worldwide, but because it was found so

early, we were able to do, as a community, a lot of really interesting science that we hadn't been able to do in the decades before that: get spectra, get more observations of it. And a paper that I worked on with Peter and a few others in the room was ruling out possible progenitors, the things that make those supernovae. So everything in green and all the other colors were excluded because of the lack of detections of certain characteristic signatures that we could have seen, and that left behind essentially only compact objects as the only viable candidates. It doesn't matter that you know all the different plots and what they all mean up here — just to point out, though, that because we were able to get on so early to this object and recognize its importance, we were able to do some novel science with that.

This idea of building real-bogus has really flourished, and as Danny talked about — and this is one of his slides from his boot camp discussion — this was used in the Dark Energy Camera survey, particularly around finding supernovae. And so there, they wind up building another real-bogus detector, and they set a different threshold between zero and one, and depending upon whether you're above or below that threshold, you wound up getting what is essentially world-class false positive, false negative rates. So getting down to MDR — means misdetection rate — meaning that

if you set your threshold criteria at 0.5, around 4% of the new candidates that you wind up having in your catalog you wind up not identifying as real. But that means that your false positive rate is also extremely low. So you see where this trade-off is. Only about 2% you would say are real when they're actually not. Now, the nice thing is if you keep on coming back to the same part of the sky, you wind up seeing the evolution of this real-bogus score, and objects that are getting brighter in the sky generally will wind up getting a more favorable real-bogus score over time.

So this has now become a cottage industry, and essentially every time-domain survey that is looking at images has their own flavor and their own approach and their own training data for being able to identify and do discovery effectively in real time. I'd say while there's probably still a little bit of blood to squeeze out of the stone, if you look at this plot on the right-hand side, we can't get much better than this. So maybe we get down a factor of two or something like that in misdetection rate. But just to emphasize that this isn't just a theoretical exercise on existing old data: these are being put into practice in real-time systems.

Let me talk a little bit more about real-time inference. And by the way,

please stop me if you have any questions. I'm happy to take them in real time. Yeah? I was only joking — I am not taking any questions.

[AUDIENCE MEMBER] If it's a 2% false positive rate, that still means like 30% of the things that you're saying are real are in fact bogus? 'Cause you said there were 100 times more bogus elements?

[JOSH BLOOM] Yeah. If you do the math, you're actually saying that — and this is why you need to pull this number way, way down — oftentimes most people won't start observing and doing follow-up until there are multiple real detections in the same place of the sky. Or you're willing, if it's a nearby galaxy, to ask from a query perspective: is there something which is really new, which has just only got one detection, it looks like it's real, and it's near one of those galaxies? In that case, you might be willing to put your neck out and actually start observing with other telescope facilities. The other thing you can do is — that's just where the threshold is, and in principle, that's where the gray area is. If you want to be extremely confident in what you actually call real, even with a single detection, you can just require your tau in this case to be very, very close to one. And so that's really a measure of probability. I don't know how well calibrated that is for the DES survey —

if it's at 0.5, whether it's really 50/50 real or not. But that's one way you can gain confidence and cut down the number of follow-ups after that. Yeah.

[AUDIENCE MEMBER] This is just photometrically based? Or--

[JOSH BLOOM] This is just photometrically based as in-- sorry, what do you mean by that?

[AUDIENCE MEMBER] There's no spectra. There's no spectra.

[JOSH BLOOM] No spectra yet, right. Correct. This would be the launching-off point to get spectra. These are just based on the images and the preceding images for that part of the sky.

[AUDIENCE MEMBER] Gotcha. Yeah. Quick background: spectroscopic information is expensive.

[JOSH BLOOM] Thank you for saying that. Spectroscopic information is extremely expensive. Typically, that's only done on one object or only a handful of objects, and you typically need large telescopes to do it, and it has to be a pointed observation.

[AUDIENCE MEMBER] Yes. I guess it's a more general question, so we can take it at the end if it's too much of a generic thing. I'm curious, in general for astrophysics, what is the real cost of discarding the data? If you are sticking in some — I'm not saying black box, but something where you might not completely understand how the process works — and you throw out some real signals, how bad is this for discovery?

[JOSH BLOOM] No, it's a fine thing to talk about. It's a great question. For those that didn't hear it: how

bad is it to throw out real signals that you just misclassified, effectively? Unlike in particle physics, where we really can't save all the data as it's coming off of an accelerator, and you have to make choices essentially in very real time about whether I save this event or I don't save this event, astronomers at least are in a mode, even in the LSST era, where every photon is sacred, and we save everything. Now, it goes into a database, but in principle, if that part of the sky becomes interesting eventually, we then have certainly a fossil record from our databases of what we had said before and what was there before. So we're not really throwing that out. There are interesting questions about accessibility to those databases, and whether that's really kind of a dev null in all practical terms, or whether that's something that people can actually mine. I would generally argue that most people are not mining previous surveys and their data effectively. But when you do, you often get lots and lots of prizes about what was happening in that part of the sky before you observed there.

[AUDIENCE MEMBER] So when you have something like this, you're not discarding the events?

[JOSH BLOOM] You're not discarding them, but again, it's sort of a decision process of: I've got this huge fire hose, I've gotta somehow make that into a little nice stream of things that

I can handle, and I'm not gonna throw out all the water that's in the fire hose that I'm not dealing with. I'm only gonna deal with the things that I really like. But because we're often interested in the changing sky on rapid timescales, and the most interesting observations that we can take are ones that come immediately after discovery, it doesn't help me much if I go back into my catalog a year later and say, "Oh, there was a really cool thing that was happening." Too bad, because most of the objects — if you go back to my light curve plot of the known unknowns and the known knowns — most of those things eventually disappear. And so if you miss it, it's pretty much gone.

[AUDIENCE MEMBER] Yeah, thanks.

[JOSH BLOOM] From a real-time inference perspective, just quickly, what we were able to do is put a very rudimentary classifier in the next step, which is: this is an interesting source — what is that potential source? We had three high-level types. Is it a variable star of some sort? Is it a transient, i.e., something that's changing explosively? Or is it a rock in our own solar system, i.e., an asteroid or so? And then there are subclasses beyond that. We didn't do a great job of this — and this is a confusion matrix, for those that know about that. You'd like to see all your power up to one on the diagonal, and all the off-diagonal power is

misclassifications. We didn't do a great job with this, but we did show that you could use external databases effectively in real time to get some notion of what this object was, which gave a little bit of indication for those working on that survey that this would be worth looking at. And again, a big part of what we try to do is not just do this on paper, but do it in practice, and so we got to the point where this classifier was acting as a person and having conversations in the same effective chatroom with other people. This is what we called the PTF Robot, and in this case it was saying, "I think this is a supernova or a nova or some explosive transient of some sort." And this turned out to be a very interesting object which led to a paper in Nature, where actually we had missed it, but there was some burbling before this actual explosive event, which was a really important find for a supernova — to be able to see some pre-supernova activity. So again, we got to the point, I wouldn't say where we had great results or it was very accurate, but we at least spent some time in trying to make sure that this got into production.

This isn't just in the optical domain. We've done similar things of being able to do real-time inference in the gamma-ray sky on objects that I've spent a

bunch of time on, these things called gamma-ray bursts. These are short-lived blasts of high-energy light, gamma rays and X-rays, that come from a random place in the sky. What you see on the left-hand side is a depiction of the static gamma-ray sky. Essentially this is the entire sky if you looked out with gamma-ray eyes, and then you see a burst that lasts for five seconds or so, and it briefly swamps the entire universe in gamma rays. So these are very, very bright events, difficult to localize on the sky, but they don't just produce gamma rays. They also wind up producing optical light after that, and these are the brightest optical sources in the universe. Much brighter than quasars. Much brighter than pretty much any type of supernova you could ever imagine. You see the relative brightness on the Y axis here in a log scale in power, so some of the brightest gamma-ray bursts — afterglows, as they're called — just swamp everything else as well in the optical sky.

And what's great about that is we can see these events to the edge of the observable universe, and if we can recognize that we have an object that can be observed at the edge of the observable universe with large telescopes, we can get spectra, for instance, of these afterglows, and they act as sort of lighthouses, and we can learn a lot about the very early universe using those events as probes, if only

we observe them in the first few hours after they've happened.

[AUDIENCE MEMBER] Mechanism?

[JOSH BLOOM] The mechanism — the progenitors that lead to these things, the ones that are very bright, are basically very large massive stars that wind up collapsing, probably into a black hole. Think of these as beyond supernovae, which wind up collapsing into other types of objects. And then the actual physics of what produces this light is basically relativistic shocks that are emitted, that are moving very, very close to the speed of light and have a tremendous amount of energy, and that energy — the kinetic energy — is released as these shocks wind up happening.

So what you'd like to do is be able to take the information not from ground-based observatories, which have a hard time observing gamma-ray light, but from the satellites that wind up discovering these things, and infer whether the objects you have are at high redshifts — so very, very high distance, very far away objects. This is also a hard problem, and what we wound up looking at is whether we could take — and you can probably see right here, there are only a few objects in red that are these very high-redshift objects that we'd like to follow up with our big facilities. And the ones in black are the ones whose redshifts we know are not very high, and the ones in gray are ones we don't know the answers to. And there are just not

that many of those, so the question is: could we take the immediately available data and make a prediction of whether something is high redshift or not? And the answer is really no. As you can probably see — it might be a little bit difficult — there's almost no way to pick the red points out of the other points, but now we have multiple features that we can try to use to try to improve it. And what we did is we said, "Well, if we can't say yes or no, this thing is definitely at a high redshift or not, can we rank a new object to say, if I have an X amount of observing time to follow up, is it worth doing or not?" — which is a slightly harder question to ask. But we wound up finding that if we only follow up 20% of the ones that we rank-order and say are the highest redshift, then 60% of those will wind up being at high redshift. So this is a big impurity, big precision-recall problem, but the area under that curve relative to random is actually non-zero. So this is actually a very useful tool that we were able to build and deploy, and we did it with only 600 events — and talk about small numbers of labels, we only had 17 objects that we could train on. So getting guarantees, or at least trying to convince ourselves that we weren't overfitting

on the data was where we spent most of our time.

Okay, let me transition now to large-scale aggregate inference — not on individual objects necessarily in real time, but in the time domain over large catalogs of sources. Yeah?

[AUDIENCE MEMBER] Was that validated with real follow-up or with synthetic retrospective?

[JOSH BLOOM] We, for a year or two, were publishing whether we think something is high redshift or not. We had a hard time actually just determining whether we were right with this calibrated curve, but certainly there were a few that we thought were high redshift which weren't, and it was the other way around. But this wasn't actually a very well-used tool in the community, to be honest, and we wound up shutting it down. So this is an example of something that worked really well on paper but potentially not very well in practice.

[NANCY] Let me ask the same question on what data's going into the--

[JOSH BLOOM] This is data that's just available, for those that know about it, from the Swift satellite. When one of these satellites winds up discovering a gamma-ray burst, they send down a whole telemetry of stuff like where it is in the sky, how bright it was, how long it lasted, and some other information about the rudimentary spectrum. I think there are eight or 10 features that went into this.

[NANCY] The host properties?

[JOSH BLOOM] No. No, no. This is literally just the first packet that

comes down from Swift — what can we say about it without knowing anything about what's detected in UVOT or even XRT?

[AUDIENCE MEMBER] Okay.

[JOSH BLOOM] This is a picture of the variable sky as viewed by the Southern Hemisphere, at least, and you notice the big hole up in the top left there. Each one of these points looks a lot like that light curve in the top left, which is basically time on the X axis and brightness on the Y axis. And the question, again, is: is this object, which looks kind of nasty and looks sort of random, worth spending time on from a follow-up perspective? There was a survey that was published a number of years ago that had 50,000 variable stars of the sky, and there were only about 800 of those that had bona fide classifications across about 25, 26 different classes of variable stars, and we asked the question: could we use that data to get good classifications that were probabilistically determined from that survey?

So we did what we generally will do when we do a machine learning approach, the old-school thing: we make this into a supervised problem. We take that very ratty time series data, turn it into a supervised classification problem where we just do features, and so we produced about 75 features from that, using unordered statistics like variability metrics, ordered statistics and doing periodograms, et cetera, and then even context metrics:

where is this on the sky, what color is it, et cetera. And with that, we were able to produce what is and was the best in class, where we wound up being able to very reliably, and with calibrated probabilities, determine over these many classes what a source was. So if you gave us a source that wasn't part of our training data and you asked us to label it, we were able to show what its class was, and then we were able to do some follow-up observations of that source to actually prove, for a minority subset of those, that the classifications were actually correct.

And we produced what I think is one of the first probabilistic catalogs of variable stars, which we made accessible to the world, where we let people traverse through the taxonomy of variable stars, click on things, and then order them by the different probabilities of whether they belong to that class or not. You can see that blue curve there is the probability, and then on the right-hand side, you wind up seeing essentially the probability that these belong to different classes. So having probabilistic-- oh, then we made it social so Facebook would buy us. That didn't work either. And so what we were able to do is produce this catalog.

And what we've done since then is work on a system which we call Cesium, which allows not just us but many other people

to build their own survey classifiers over large amounts of time series data. And we did this around astronomy, but we try to make this in a domain-agnostic way so that you could actually use this on any sort of domain that had time series data. This is still a work in progress, but we're now actually starting to be able to use this for new surveys as they come online. And rather than building one-off purpose-built infrastructure, we're getting to build a whole bunch and make use of a whole bunch of subsystems in these architectures that use some of the modern software practices.

Now again, one of the things I wanna emphasize is that building probabilistic catalogs and making websites and stuff is cool, but our main focus of doing this is to be able to do novel science. And so what we try to do in my group was take that probabilistic catalog and then ask interesting questions of that and then do follow-ups. For instance, what we were able to do is look for very strange types of objects called R Cor Bor or DY Per stars, and cutting to the chase, with follow-up observations with spectra of only about 20 of our candidates, eight of them wound up being new discoveries of these very, very rare stars in a catalog that had been around for 10 years. One of the stars was almost as bright as you could see with the naked eye

and was probably known by the Babylonians. And here we were able to do this using machine learning to help us hone in on the probable objects. Very, very low purity of the sample, but very high efficiency of discovery. Yeah?

[AUDIENCE MEMBER] Going back to the catalogs and surveys, are there any sources of bias, aside from Southern Hemispheric bias?

[JOSH BLOOM] That's a great question, and something we try to grapple with. There is a bias in the sense that it was taken by a single telescope in a certain filter. And it was taken with a certain cadence, so we're certainly biased in that survey against finding objects that change very rapidly and go away. That's one bias, so you don't see any of those in the sample. They spent a lot of time in the galactic plane, and there's certainly a distribution of variable star types that is different in the galactic plane than off the galactic plane, and we're trying to figure out how you could disentangle almost a prior of what you would expect that distribution over those 26 classes to be, so that instead you could wind up producing some sort of posterior where people could then dial in whatever their biases were and get different probabilities out. Yeah.

[AUDIENCE MEMBER] I think I saw the Magellanic Clouds there too.

[JOSH BLOOM] Yeah, the Magellanic Clouds are there, and we don't have those in the Northern

Hemisphere, et cetera. So yes, certainly there are biases in that, which is why there is some difficulty, which I'll highlight at the end, of taking that entire classification machinery in that model exactly and then applying it to another survey. Another survey taken of the same part of the sky would discover, and would have in its catalog, a different distribution of variable stars.

The other thing we did is find highly eccentric detached eclipsing binaries, which allowed us, with, again, follow-up observations with high-resolution spectroscopy of the stars that we found, to put them on the mass-radius relation of stars, which is a pretty fundamental thing that you like to know. It's actually hard to find stars where you can actually do this, but we were able to find a number of those. And again, we used that catalog as a launching-off point to do novel science. So those became science papers in and of themselves.

And the last thing that we've done in this field is something that's, I think, still pretty bizarre and I'm still coming to terms with: this is the idea of looking at a light curve like the ones I've shown you and trying to infer the fundamental properties of those objects that you would only get traditionally from spectra. What is the temperature of that object? What's its surface gravity? What's its metallicity? And what we were able to show is that by just looking at the variability in time over a couple of different

colors of variable stars in a certain part of the sky, we were able to infer the three properties I just mentioned with as much accuracy as you would get from a low-resolution spectrum. So it turns the time-domain surveys like ZTF and LSST into these sort of low-resolution spectrographs. The way I think about that is: if you heard an opera singer on the other side of the door, you could guess their gender — that one's pretty easy, that's like temperature — you could guess their weight, and you could guess their age, and be accurate to about as well as you could do if you were actually able to then go and measure them directly. So this is very interesting. Like the gamma-ray burst project, this is only something that's worked so far in retrospect. We've yet to then apply this to new surveys, but this is one of the things that we're hoping to do as some of these new surveys come online.

Everything that I've mentioned so far has been using what I'll call handcrafted features. But there are some real challenges with that. Feature engineering, for those that know about that, is very expensive, and oftentimes requires a lot of domain knowledge. If you are trying to separate two very similar types of classes of variable stars, oftentimes you'll bring in the expert in that domain or subdomain or sub-subdomain, and try to build some math that encodes what their brain is telling them of

why these two things are different. That's an expensive and iterative process. It's also a small data problem where we don't have a lot to train on, and oftentimes the traditional machine learning techniques don't account for feature uncertainty, and it's often very difficult to apply one model to another survey.

One of the things that I'm excited to talk about today is where we threw out traditional feature engineering and we used an autoencoding recurrent neural net to create those features for us in an unsupervised way. That is where we don't need a whole bunch of labels. And for those that don't know about autoencoders, the idea is actually pretty simple. You create an encoding function, which is demonstrated with this E here, of that light curve, essentially that raw data — and then, it's actually probably pretty hard to see on the screen, you compress that down to a bottleneck, which is a small number of floating point numbers, like 64 numbers, and then you take that encoded small number of data points and you decode it so that you try to reproduce your original light curve. So without knowing what this object is, if I get the architecture right, I can build this encoder-bottleneck-decoder thing, and then use the bottleneck as features in a traditional classifier.

And this encoding process actually works pretty well. These are some examples. The raw data is up at the top for two different sources, and

for now just focus on the red curve. What you can see, if we fold it on the correct period of this source, you wind up seeing that the red points very well match the blue data. So the encoding and the decoding, even though it's a very lossy process, wind up producing some pretty nice-looking light curves. And what's cool about that is something we were able to demonstrate in the paper, where if we just had sinusoids — very noisy, irregularly sampled sinusoids — and we actually looked at those encoding features — essentially it's like a small N-dimensional embedding — we're able to show that those features correlate very closely with the things that we put in. So we get period out, we get phase out, we get amplitude out of these things.

And so what does that mean? It means that this network is learning, in this case here, what it means to be a periodic source, and it learns what it means to have a period of a certain sort, because we're taking what is hundreds of data points and compressing it effectively down to four. And in the context of astronomy, what we're doing there is we're not saying we know this is gonna have this period, and it's gotta have this amplitude, it's gotta have this skewness and kurtosis. It's saying: just learn the features that get me back to my original source. So cutting to the chase here, we were able to show that we rivaled the best-in-

class results from all the handcrafted feature engineering. In two of the three surveys we looked at, we beat all the other best-in-class sources and models. So we're very excited about this, and what it means for us is that instead of having to build new features for every new survey we look at, we can actually just throw it into this machinery and use that bottleneck layer as a way for us to build features.

For those ML folks in the room and online, here's the architecture we used. I think one of the important things to point out is that unlike other recurrent neural net architectures, we're able to make explicit use of the delta times between the observations. And we're also, in our loss function, accounting for the inherent uncertainties in the observations. So if you have one observation which is kinda ratty and doesn't have a very good measurement — actually has a very large error — it won't adversely affect your reconstruction. And what's also nice about this is we're able to augment our data not by, as people do in the image domain, moving images around and shifting them and changing pixels here and there. We're able to take the original light curve data itself and essentially bootstrap, resample that light curve, and that actually wound up helping the learning quite a lot. And I think the thing I'm most excited about: it means that we can do unsupervised feature learning. So instead of having to learn features and

build features by hand, we can leverage large corpuses of unlabeled light curves to build up these features. And because that bottleneck just becomes these abstract features, we can then use those and augment them with other sorts of metadata like colors, et cetera. I'll skip that for now.

Let me just, in the last few minutes, highlight some of the challenges and open questions that we have. One of the things I'd love to spend time on with the folks in the room is trying to understand how we can find new phenomena — look at a retrospective catalog and say, "Are there any clusters in some space that are different than the types of objects we already know about?" And I'd also like to, in a real-time mode as a new object is just starting to develop, not just identify this is worth following up, but identify: is this worth following up, and it's actually different than anything we've ever seen before, or different enough that it's worth spending even more resources on to learn more?

Another thing that I think is interesting is this whole small data, or at least small label corpus, problem. And the question there is how we can leverage one model built on one survey and apply it to another survey — that's transfer learning. Can we even do better than this sort of 4% misdetection rate? And there, teams like at Harvard — Pavlos

Protopapas and his group — are looking at some unsupervised and semi-supervised techniques.

What's interesting is that if you think about the architecture that we created for the classification problem, this is a very non-linear, non-parametric model that can produce realistic light curves of real objects without me having to put the physics in. So can I use this going the other way, and try to infer back the physics for some of these objects whose physics we actually know? Can I use these as surrogates or emulators? For instance, let's say in the gravitational wave world, it's extremely expensive to generate a gravitational wave signature with a few input parameters computationally, so you have these coarse grids. Can you fill in those coarse grids with similar types of networks to produce these emulators? And can we use these neural net models to be able to help the LSST, for instance, figure out what their cadences should be? If I can now produce a fake universe of transients of all different sorts, you can then actually create a cadence and optimize on a cadence to be able to find those sources.

And then systematic or systemic optimization is probably beyond the reach of this group or anyone, which is: optimize over all global resources. I'd love to be able to maximize the scientific output, but again, we're in this competing mode where different groups are all trying to get access to similar telescopes. And last, does this all

have to be fully automated, or is there still a role for people in the real-time loop of the real-time discovery? Certainly people eventually will be the ones that write the papers, at least for now, and if that doesn't happen, that'll be pretty exciting as well. But is there a role for people to be asked questions from the model and say, "I think it's one of these two, can you do a little bit of exploratory work? Give me the answer," and then the model could wind up updating itself? I'm generally curious about that.

Let me end with a pretty exciting discovery that was announced just a couple of days ago, where an astronomer in Argentina was just turning his telescope on for the first time — and the first thing you do is you look at a beautiful galaxy — and he happened to catch a supernova that was going off right in the earliest stages, the earliest stages pretty much we've ever seen. These are the observations from that amateur astronomer. And then eventually observations were taken later, as in like a day later, and it took a while for the amateur astronomer to figure out that there was this new source, but this was heralded as like winning the cosmic lottery. You turn on your facility, you look at something, you find something that shows up in Nature a year

later, and people are very excited about this, rightfully so. This is the earliest parts of the evolution of a supernova that we very, very rarely get access to. But what I hope you've seen in the talk today is that we shouldn't want to win the lottery as astronomers. We want to guarantee a nightly annuity of essentially guaranteed payoff, and have that be optimized not only over our facility but globally. And so I think that's an important point: we're trying to systematize discovery and inference, and it's very clear that machine learning is becoming a very, very critical part of that whole process. So I'll stop there, and I think we've got time for just a few questions. (applause)

[PETER] So was that the GE in you in the last slide there? Oh no, that's the one before, about the annuity end.

[JOSH BLOOM] Oh, the annuity. Yeah, well, guaranteed payoff is much nicer than every now and then if you're lucky.

[PETER] I wanted to kick off with a question for you. Did you learn anything interesting with the things that you misclassified? Was it something missing in your model, or was the actual object that you were looking at not exactly — like, the label on it wasn't exactly right?

[JOSH BLOOM] Yeah, that's a good question. In the construction of a model, or even more broadly, a system of software that involves applying a model to data and building that model, you often wind up holding

out some of the sources that you think you know the answer to, and you apply the model to that, and then you measure how well you think you're doing. Oftentimes you're extremely confident in the model that this source is, let's say, of type RR Lyrae or a supernova, but the label says something else. That's either your model's wrong, which is often the case, or sometimes it's a cause to go back and say, "Was my label actually right?" And so it actually can be a bit of an iterative process for the missed labels during this model construction process, where you go and you say, "Did I actually label that right or not?" And if you labeled it right, then your model was wrong, and the question is: what can you do in your model so that you don't get that wrong again? And what you do there is potentially go back to the drawing board and say, "What are the other features that I'm missing?"

One of the negatives of the recurrent neural net autoencoder that I presented is that it becomes much more of a black box. You don't know what those features are, so do you add more features, do you make less? One of the benefits of the handcoded features: if you get something wrong, you can say, "Oh, I got it wrong because I forgot to take into account that some of these types of objects look like this at the beginning, even though most of

the ones in my training set looked like something else. So I'll just build an extra feature that fits for that sort of thing." I think that's a long answer to your short question. It's an iterative process. You either learn something about how you're doing modeling ineffectively, or you could learn something fundamental about your data.

Now, the real challenge is if you're doing all this in an offline mode, because you've iteratively rebuilt your model even on held-out testing data, you haven't really held out your testing data as much as you need to to gain a real good confidence of what your ultimate uncertainties and errors are gonna wind up being once you put this into a live mode. What I generally say is that the only real testing data is data that hasn't been created yet — i.e., the universe hasn't evolved in the next second to produce those objects. So it's all very well and nice to have "here's my false positive, false negative curve" on paper. The only real machine learning system in astronomy that you can trust is one that's actually been put into production — is my contention.

[AUDIENCE MEMBER] You mentioned optimization, global optimization, of follow-up. We just, as the community, just witnessed the largest follow-up campaign ever conducted for a source. Is there any evidence, in your opinion, that it was suboptimal in some form?

[JOSH BLOOM] I think that's a great question. We just saw, for those that

didn't hear it, essentially the entire world of astronomers going after one place in the sky. It was massively suboptimal. People were observing the same part of the sky with the same sort of filter at the same time. Now, the nice part about that is that we're really, really sure that the observations at that point in time and that filter were right, because it wasn't one person saying it, it was 10 persons saying it. So there is something nice about that, but there was very little coordination, I'd say, and the next time there should be more.

Now what happens is, because these precious follow-up resources like large telescopes are indeed precious, what you wind up seeing is that the people that lord over those, like the directors of them, wind up playing a bit of referee and saying, "Well, you guys shouldn't do it," or oftentimes more of a matchmaker and saying, "You're all asking me for the same observation; you are now part of the same group." And so it's a very ad hoc, very real-time process of how these collaborations wind up evolving. It's hard to see how we break out of that model. Individual telescopes and telescope consortia are doing a pretty good job of that, recognizing they need to optimize, but globally I think this is largely an intractable problem — not technologically, but more sociologically and politically. Nancy, do you have a question?

[NANCY] Yeah. I just wanna say I really enjoyed your talk, Josh.

The question I had was about your encoder. You showed a slide about different variable stars. I was trying to read it quickly, but the three examples I think were all periodic. Not this one — I think the one after, where you have a table where you compare more traditional methods to this fancier method--

[JOSH BLOOM] Oh, yeah. Yeah, this one.

[NANCY] So is this-- I mean, I was curious how well this works for variable stars that are not periodic, and where, even if the final answer's not 90-something percent, the traditional classifiers really do a bad job, so there could be more dramatic improvement — whether there's a--

[JOSH BLOOM] It's

a great question. We focused on periodic variables 'cause there was the largest corpus of label data that we could find on those. We are asking that exact question on not just variable stars, but explosive sources. There's a new challenge coming out called the PLASTIC challenge, which I'm sure you know about, which is for supernovae and transients so n-- particularly non-variable stars of being able to classify those. So there's a group that's gonna be producing fake versions of all these different types of objects, and they're asking the rest of the community, "Can you build a good classifier on that?" I think the sort of network that we built can be very applicable to those, but I, we haven't done the work yet to see how good

those are relative to the other classifiers. [NANCY] 'Cause that's where you don't know a priori what the features should be, right?

[JOSH BLOOM] That's right. Unfortunately, a lot of the very aperiodic stars are ones that just have stochastic variations, and so other than fitting power spectrum density distributions of what the variability is, there's not a whole lot of other features that you can build. Certainly a periodogram doesn't really make sense in that context. But in the context of burbling quasars, we have built specific purpose-built features knowing that quasar light curves behave like damped random walks, and so you can get parameter fits out of those.

[PETER] We have one question

from the Twitter universe.

[JOSH BLOOM] Twitter universe.

[PETER] Eric Bellm, of all people, has a question for you. Is it practical or useful to apply a fine-tuning layer atop your pretrained autoencoding neural net to apply it to new surveys, à la applications using ImageNet?

[JOSH BLOOM] It's a great question. That's our supposition. I think we mentioned that a bit in the paper, but we haven't done the exercise to take a pretrained network on a large survey and just say, "This network has figured out something fundamental about how variable stars work, but it doesn't know a lot about the way in which this particular data was taken in this other survey. Let's apply it." We have taken the network we built on one

survey, applied it directly to the other, and it worked really well, just like when you apply ImageNet or VGG-Net to images that aren't from that original corpus, you get very good answers. But you're right, what you'd like to be able to do is freeze some of the layers of the model and then retrain some of the other layers so that it learns some of the peculiarities of that survey. That was a good question.

[PETER] All right.

[AUDIENCE MEMBER] Go ahead.

[JOSH BLOOM] He's had his hand up for a while. Yeah.

[AUDIENCE MEMBER] So my question follows up from this one about the follow-up for use of telescopes' resources. That sounds an awful lot like

explore versus exploit in behavioral ecology, which game theorists talk about quite a bit. Have you looked there for inspiration?

[JOSH BLOOM] Certainly the notion of explore/exploit is top of mind in the groups that I've worked in, where you say, "I can either go after, let's say, Type Ia supernovae, which if I get enough of those, it's a guaranteed payout on some timescale." Exploit as in, "I have a little moment in my telescope follow-up resources where I don't have anything scheduled. Why don't I go after something where I'm not sure what the answer is?" What hasn't been done is where there's an explicit discussion and identification of what the explore/exploit metrics are, let alone the adherence to those metrics, because oftentimes when you're on a

telescope and somebody hands you a basket of a hundred objects that you could look at, you go, "Yeah, I don't like that one. That one's in that part of the sky. I don't like that part of the sky right now," or, "There's a cloud over there." So we haven't done a really good job as a community, and I don't know any groups that are being extremely explicit about, "We are going to explore this amount," as in potentially waste a whole lot of resources, "and exploit this amount." Maybe take the rest offline?

[PETER] Yeah. Okay, so let's take our lunch break now, and then we'll come back at 1:30. (applause)
