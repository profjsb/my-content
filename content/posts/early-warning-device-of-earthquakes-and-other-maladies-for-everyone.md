---
title: 'An early warning device of earthquakes (and other maladies) for everyone'
date: 2014-09-04T00:54:00.002-07:00
draft: false
tags : [earthquake early warning, device, earthquake, invention, California, raspberry pi]
---

  

### Summary

In October 2013, I built a prototype earthquake early warning (EEW) device, for less than $110 in parts, for my house that taps into the California ShakeAlert system. In the recent 6.0 magnitude quake centered near Napa, we got about 5 seconds warning here at my home in Berkeley, CA before the shaking began. Such devices could (and _should_) be mass produced, sold as ubiquitously as fire alarms or carbon monoxide detectors at a similar price point and installed with as little friction. Much of the clever stuff happens upstream from the device - but I've got some ideas detailed here that could lead to the robustness and the ease of use/installation. This blog represents the disclosure of what I've been working on.

[![](http://icons.iconarchive.com/icons/position-relative/social-2/24/hackernews-icon.png)](http://news.ycombinator.com/submit)

### Background

An earthquake early warning (EEW) network has been in the place for years in some of the most volatile, quake-prone places in the world. EEW networks make use of the fact that sensors close to rupture points can push shake information much faster than the speed of wave propagation of quakes. Like the observed delay between a lightening flash and the associated thunder clap increases with distance, so too can the warning time for earthquakes to locations far from the rupture/sensor sites.  The [Japanese EEW network](http://www.jma.go.jp/jma/en/Activities/eew1.html) provided [seconds to minutes](http://en.wikipedia.org/wiki/2011_T%C5%8Dhoku_earthquake_and_tsunami#cite_note-46) warning across the country, saving [countless lives and properties](http://www.jma.go.jp/jma/en/Activities/eew2.html). Apple's iOS has the ability to [push EEW alerts to cell phones in Japan](http://support.apple.com/kb/ht5006). In contrast the EEW infrastructure in the US is far behind. This is something that numerous researchers at the [US Geological Society and other universities](http://www.cisn.org/eew/) have been working on to rectify since ~2007; they have built CISN [ShakeAlert](http://www.shakealert.org/faq/) as a prototype EEW system. Last year, Gov. Brown [signed into law Senate Bill 135](http://sd20.senate.ca.gov/news/2013-09-24-governor-jerry-brown-signs-sen-padilla-s-bill-create-california-earthquake-early-war) which mandates (but does not fund) the creation of a comprehensive EEW system for California. It is estimated that [another $80M will be needed to get a full-fledged system off the ground](http://www.shakealert.org/faq/).

  

As as professor at Berkeley working in (astronomical) time-domain data, I was extremely happy to be asked and to serve (alongside John Vidale, Steven Glaser, Tom Brocher, and Michael Manga) on the advisory board for the [Berkeley Seismology Lab](http://seismo.berkeley.edu/) (BSL), directed by Prof. Richard Allen. At our July 2013 meeting, I learned of the ShakeAlert system and was granted beta access to try the system out.  [The Bay Area Rapid Transit (BART), Google, and others are also beta users](http://www.eew.caltech.edu/research/). You can read the [publications](http://www.eew.caltech.edu/publications/index.html#shakealert) from the group and about the system and the software to connect [here](http://www.eew.caltech.edu/docs/UserDisplay_OperationsGuide_V2.3.pdf). I tried out the alert system on my laptop but realized that when my laptop was closed or when it wasn't close by then I wouldn't be alerted. This led to the idea of creating an always-on device that would remain listening to EEW (and other) alerts and could be installed just about anywhere, by anyone, for cheap.

### The Device

The basic idea is to create a device that is installed on the wall/ceiling, connected wirelessly to a local network (or networks), configured, and largely forgotten until a major shaking or event is on its way. In particular, the device:

*   can receive (either via push or push) alerts about earthquakes and/or other disasters/problems from remote server systems;
*   (optionally) can allow users to authenticate to alerting systems during an installation process (or reconfiguration process);
*   (optionally) will allow to device to either a) store (and optionally update) its geolocation so as the calculate the expected local severity (ELS) of problem and the time-lag between the expected local arrival of the impending event and/or b) receive ELS and time-lag data from the server(s) computed remotely for the known location of the device;
*   (optionally) filter out alerts based on event data (such as calculated magnitude), ELS and time-lag information;
*   (optionally) alert people near the device about the impending event using audible signals, visual events (e.g., flashes) and/or tactile events (e.g., vibration);
*   (optionally) act as a relay, broadcasting the event to other nearby devices (e.g., via bluetooth protocol) which in turn may be preconfigured to alert people nearby or to other devices;
*   allow the alert data to be received via wired network (e.g. ethernet), wireless network (e.g., wifi), and/or cellular phone based network (e.g., CDMA);
*   (optionally) allow network failover to occur such that if the preferred network connection should drop, the device will be capable of automatically using another network to receive data from the preferred servers;
*   (optionally) work off of battery backup such that if wired power is lost the device can remain on and ready to receive network events;

Screenshots of some of the drawings I prepared are below.  

#### A working prototype

Since I had beta access to the ShakeAlert system, I decided to try to build a prototype of the device outlined above, primarily to see if I could reliably get EEW events and keep my family safe at home. To create a low-power device that could run for hours or days off of a [USB battery](http://www.amazon.com/gp/product/B007WOKBRY/ref=ox_ya_os_product_refresh_T1), I bought a [raspberry pi](http://www.amazon.com/gp/product/B009SQQF9C/ref=oh_details_o00_s00_i07?ie=UTF8&psc=1), [SD card](http://www.amazon.com/gp/product/B00B7ID99I/ref=oh_details_o00_s00_i04?ie=UTF8&psc=1) (for the OS and associated data files), [wired power speaker](http://www.amazon.com/gp/product/B0082E9K7U/ref=oh_details_o00_s00_i05?ie=UTF8&psc=1), and a [mini wifi adapter](http://www.amazon.com/gp/product/B003MTTJOY/ref=oh_details_o00_s00_i03?ie=UTF8&psc=1). The total cost was $109.62 (including a USB charger). I installed the [raspian](http://www.raspbian.org/) flavor of OS and made sure that an SSH server woke at boot time. Since I needed to make sure that the external speaker would be on (and loud), I needed to add to my rc.local:

  

  

modprobe snd\_bcm2835

amixer cset numid=3 1

  

Most importantly, since the ShakeAlert software needs to run in an window manager and I wanted to have remote access to that manager, I needed to make sure that a VNC server started at boot time. I added a [script vncboot](https://drive.google.com/file/d/0BzkoULEX2bniWTVQNVJrU250eG8/edit?usp=sharing) to my init.d. I also made sure that the OpenDisplay booted upon restart and was configured to my location and preferred alert settings. Last, I configured the wireless network settings to use my home wifi (based on a dry loop DSL connection) as default and then failover to a wifi network created from my cellular-based mifi. This way, for aftershocks, I could still get alerted even if the power to the house was out (so long as the cell network remains up).

[![](http://4.bp.blogspot.com/-9lkbE_BqT_o/VAfyT9dfNQI/AAAAAAAAEO0/A5Aup-vmesA/s400/eew.png)](http://4.bp.blogspot.com/-9lkbE_BqT_o/VAfyT9dfNQI/AAAAAAAAEO0/A5Aup-vmesA/s1600/eew.png)

Basic setup of the working prototype. Here's it's running off of a USB battery.

Over the last 11 months, the prototype has been pretty stable, going down for about a month when I changed my wifi network but forgot to reconfigure the device. It produced alerts seldomly (since I don't want to be woken up except for potentially life-threatening events). The recent 6.0 magnitude event was a reminder that it can work and that it's widespread usage can save lives. This week I added a tweetbot component that listens for new events and pushes events with a high likelihood of shaking in Berkeley. If you're interested and live nearby you might want to follow [@eew\_bot](https://twitter.com/eew_bot).  
  

#### Not just quakes

### 

We're not expecting a big fallout problem anytime soon, but one can imagine having the device capable of receiving and broadcasting alerts about radiation leaks in nearby nuclear power plants, chemical spills at a nearby railroad, tsunamis, probable tornados touchdowns, or dirty bombs. EEW is just the start.

### Next Steps

First, I hope that everyone reading this blog does everything in their power to promote the funding and construction of a robust EEW system for California and other areas that are threatening by major quakes. The work of CISN is critical.  
  
If mass produced, I'm envisioning the device as a single package, the size and form factor of a fire alarm. It would need low power (3 or 5V or power-over-ethernet) connecting to an internal (backup) battery. Like other wireless based home devices, it would/could be configured almost entirely through the cloud or connected laptop. Updates could be done over the air and as new warning systems come on line they could be seamlessly added and configured to each device. People would be able to test their system by manually lowering thresholds. I'm not an earthquake expert nor consumer product guy but I got to think that installing these in every house, school, and office could save countless live. If anyone want to get rocking in getting this out into the world, please get in touch!  
  
Update (7 Sept 2014):  
I put all the components in a makeshift cardboard package, fastening each component with twist ties. I'm testing how long it will run off of the battery without being connected to power.  

[![](http://1.bp.blogspot.com/-gzif5dRMQvI/VA00SUd3QAI/AAAAAAAAEQ0/BOtqf8jCVho/s1600/IMG_1777.png)](http://1.bp.blogspot.com/-gzif5dRMQvI/VA00SUd3QAI/AAAAAAAAEQ0/BOtqf8jCVho/s1600/IMG_1777.png)

  
  

[![](http://4.bp.blogspot.com/-DXB02Qj06TU/VA00VN8MODI/AAAAAAAAEQ8/zAn2n3EcY9s/s1600/IMG_1778.png)](http://4.bp.blogspot.com/-DXB02Qj06TU/VA00VN8MODI/AAAAAAAAEQ8/zAn2n3EcY9s/s1600/IMG_1778.png)

### East Bay folks might recognize the container as one from [Gregoire](http://gregoirerestaurant.com/About).

###   

### \- Joshua Bloom, Berkeley, CA (all rights reserved)

### Acknowledgements

In the past few years of thinking about EEW systems, I've been extremely fortunate to have numerous conversations with Ryan Anderson, Joey Richards, Dan Starr, Chris Swanson, Henrik Brink and Richard Allen. We envisioned a different sort of device and local-mesh network and [proposed for some funding to build a prototype](https://drive.google.com/file/d/0BzkoULEX2bniWTVQNVJrU250eG8/edit?usp=sharing) (which was not funded). Discussion of this network and associated device might be a good new post! We also thought of using EEW devices to automatically short stocks within a few seconds of rupture then unwind the positions if there was a false alarm. We decided this was too evil (and require too much capital sitting around for potentially years) to pursue.

#### Device Invention drawings

[![](http://4.bp.blogspot.com/-CxhaseRnsQo/VAgZBu-Y4oI/AAAAAAAAEPE/-fjmGYAWsCM/s1600/eew-device-invention-sm.jpg)](http://4.bp.blogspot.com/-CxhaseRnsQo/VAgZBu-Y4oI/AAAAAAAAEPE/-fjmGYAWsCM/s1600/eew-device-invention-sm.jpg)

[![](http://1.bp.blogspot.com/-Tqj3VGcUr4w/VAgZhqCckDI/AAAAAAAAEPM/HybDLu3cs-I/s1600/eew-device-invention-sm2.jpg)](http://1.bp.blogspot.com/-Tqj3VGcUr4w/VAgZhqCckDI/AAAAAAAAEPM/HybDLu3cs-I/s1600/eew-device-invention-sm2.jpg)

  

[![](http://1.bp.blogspot.com/-1DPhAuk0CSg/VAgZiOoubpI/AAAAAAAAEPQ/JZYNoe1pxzI/s1600/eew-device-invention-sm3.jpg)](http://1.bp.blogspot.com/-1DPhAuk0CSg/VAgZiOoubpI/AAAAAAAAEPQ/JZYNoe1pxzI/s1600/eew-device-invention-sm3.jpg)

  

[![](http://3.bp.blogspot.com/-mR7CK_hc6Yo/VAgZidLTeCI/AAAAAAAAEPU/1YswY4TeoFs/s1600/eew-device-invention-sm4.jpg)](http://3.bp.blogspot.com/-mR7CK_hc6Yo/VAgZidLTeCI/AAAAAAAAEPU/1YswY4TeoFs/s1600/eew-device-invention-sm4.jpg)