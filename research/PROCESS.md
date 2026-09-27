# Talks & Media page — build retrospective

*Written 2026-07-18, after PR #3 was opened. For future reference when adding talks or
building similar sections. The page itself lives at `/talk/`; see the bottom of this doc
for how to update it (there are now skills for that).*

## What was built

A **Talks & Media** section styled after
[wesmckinney.com/presentations](https://wesmckinney.com/presentations): reverse-chronological
numbered cards, one page bundle per item, with an AI-written summary and (where
recoverable) a full transcript.

Final counts: **45 entries (2005–2025)** across 11 types (13 Talk, 7 Invited Talk,
5 Podcast, 4 Lecture, 4 Radio, 3 Keynote, 3 Colloquium, 2 Plenary, 2 Tutorial, 1 Seminar,
1 Panel) — **23 with video, 20 with slides, 39 with an event page, 18 with full
transcripts** (auto-generated captions, marked as such on each page).

## How it was done (process)

1. **Research sweep (cloud session, Jul 17–18 2026).** Multi-angle web research:
   YouTube/Vimeo; conference sites (SciPy, PyData, Strata/O'Reilly, KDD); institute
   archives (Simons Institute & Simons Foundation, IPAM, IAIFI/MIT, BIDS, LBNL);
   SlideShare and Speaker Deck for orphaned decks; NPR archives; the Wayback Machine to
   confirm events whose original pages had died. The Wayback Machine ended up used for
   *confirmation* only — no published link points at an archive.org snapshot.
2. **Structured dataset first.** Everything went into `research/talks.json` (title,
   event, type, date, location, video/slides/event URLs, one-line summary, and a `notes`
   field recording provenance and uncertainty). The page was generated *from* the
   dataset, so every claim on the page is auditable here.
3. **Transcript recovery.** For the 18 items with usable video/audio, auto-generated
   captions were pulled and lightly cleaned into `## Transcript` sections embedded in
   each page bundle; one-line AI summaries were distilled into `research/*.summary.txt`
   and the front-matter `summary`.
4. **Page build.** Site-level Hugo layouts only — `layouts/section/talk.html`,
   `layouts/talk/single.html`, and two partials (`talk_badge.html`,
   `talk_assets.html` with self-contained inline CSS/JS) — **no theme edits**, compatible
   with the pinned Hugo 0.60, dark-mode aware. Nav entry added at weight 25
   (between Publications and Projects).
5. **Transfer and PR.** The cloud sandbox could not push to GitHub, so the work traveled
   as artifacts: a site snapshot zip went *up* so the session could build against the
   real theme; the results came *down* as a zip and finally as a **git bundle**
   (`talks-media-page.bundle`), which was fetched into a local worktree
   (`wt-talks-media/`), pushed as `talks-media-page`, and opened as PR #3. Netlify's
   deploy preview built it green with Hugo 0.60.

## Key schema decisions (needed when updating)

- **Front matter is the published source of truth**; `research/talks.json` is the
  research ledger. They are linked by `slug`.
- `talk_number` is the "#N" chip and equals the **chronological rank** (1 = oldest,
  45 = newest). The list itself is ordered by `date` (`.Pages.ByDate.Reverse`), so a
  wrong `talk_number` won't reorder the page — it will just display a wrong number.
  **Inserting an older talk requires renumbering every later talk.** Note the trap:
  `talks.json`'s `n` is *discovery order* (the four radio items are n=42–45 but ranks
  #1, #4, #5, #9), so `n` ≠ `talk_number` by design.
- **Date precision conventions:** exact date when known; month-only → day 15
  (e.g. SciPy 2008 → `2008-08-15`); year-only → `YYYY-07-01`. `display_date` hides the
  false precision: `"Mon YYYY"` normally, bare `"YYYY"` when only the year is known.
  Approximations are recorded in `talks.json` `notes`.
- `talk_type` drives the badge color via substring match in `talk_badge.html`
  (keynote/panel/podcast/radio/interview/tutorial map to their own classes;
  colloquium/seminar/lecture share an "academic" class; everything else — including
  "Invited Talk" and "Plenary" — falls through to the default Talk style).
- **`topics`** (added with the filter bar, Jul 18): required list field powering the
  list-page Topic filter and the per-card topic chips — vocabulary `astronomy` /
  `industry` / `ai-ml` / `education` (`talks.py validate` enforces it). Assignments
  were derived from transcript content where transcripts exist (venue/title/summary
  metadata otherwise); the derivation rules live in the `add-talk` skill. The Type filter folds `talk_type` into six buckets
  via `layouts/partials/talk_filter_type.html` (Invited Talk/Plenary/Colloquium/Seminar
  → Talk; Lecture+Tutorial share a bucket; Interview → Radio).
- **Optional media fields** (added in the same-day restyle, see addendum):
  `url_audio` (direct MP3 → Listen button), `url_transcript` (external transcript
  page → Transcript button, shown only when `has_transcript` is false). A YouTube or
  Vimeo `url_video` auto-embeds a player on the talk's own page.

## What went well

- **Dataset-first workflow.** Building `talks.json` before any pages made the page
  generation mechanical and left an auditable provenance trail (the `notes` field paid
  for itself — it is why this retrospective can say precisely what is uncertain).
- **Link quality held up:** 76 of 82 outbound links were verified live on 2026-07-18,
  including **all 23 video links** (YouTube checked via oEmbed, which catches deleted
  videos that still return HTTP 200). Two "verify YouTube ID at build time" flags from
  the research phase (SciPy 2012, Simons "Visions" 2013) check out as live.
- **Transcript recovery exceeded expectations:** 18 of 23 recorded items yielded full
  transcripts from auto-captions, including 2012-era talks.
- **No theme edits.** The whole feature is site-level overrides, so it survives theme
  updates and the Hugo 0.60 pin. Netlify deploy preview validated it without local
  build gymnastics (local Hugo is too new to build this theme).
- **Design target matched:** the wesmckinney.com card style (badges, numbering,
  link buttons) translated cleanly to Hugo 0.60 templates with inline assets.

## What didn't go well

- **Cloud → local transfer was the major friction.** No direct push from the cloud
  sandbox meant zip/bundle sneakernet: three zero-byte failed zip exports
  (`_claude_build_kit.zip`, `_claude_build_kit2.zip`, `_claude_site_snapshot.zip`) and
  two randomly-named partial zips (`zi5Qxy3D`, `zi5qAkT3`) littered the repo root before
  a working kit zip, a results zip, and the final git bundle got through. The git bundle
  was the right mechanism — **next time, start with the bundle** (or do the work in a
  local session/worktree from the start).
- **Duplicate working copies left on master.** Unpacking the results zip into the main
  checkout left ~60 untracked dirs (`content/talk/`, `research/`, `layouts/`,
  `static/{css,js}/vendor/`) plus dirty `config/_default/menus.toml` and
  `content/talk/_index.md` in the master working tree — identical to the branch content
  but easy to accidentally commit. **Cleanup needed after merge** (the zips are already
  parked in `_to_delete_zips/`; the `static/*/vendor/` files are kit residue, not part
  of the feature).
- **Two numbering schemes diverged** (`n` vs `talk_number`, see above) and `talks.json`
  originally had no `slug` key linking ledger entries to page bundles — both fixed/
  mitigated in the follow-up commit that added this doc (slugs backfilled, skills encode
  the renumber rule).
- **Date archaeology was the slowest research task.** Several talks are dated only to a
  month or year (LSST AHM day-within-week, Astro Hack Week lecture day, Haas lecture
  year, podcast release months), and one deck's venue was never pinned down at all.
- **Link rot is already visible** — see the next two sections.

## Talks known but not linkable/reachable

The explicit goal was "link everything"; these are the items where that failed, so
future sessions don't re-litigate them (and can retry the *recoverable* ones).

### No public artifact at all

- **#4 BBC Newshour (June 2011) — "Black Hole Swallows a Star" (Swift J1644+57).**
  The interview aired and was once linked as an MP3 from the old Berkeley homepage;
  that file is offline and no BBC archive page was found. The page has **zero links** —
  it is on the site purely as a record. *Recoverable if a personal copy of the MP3
  exists; it could be self-hosted in the page bundle.*
- **#33 Masters of Data podcast (Mar 2019) — episode audio.** Confirmed unrecoverable
  2026-07-18: the episode is delisted from Apple (GB and US), absent from the iTunes
  episode index, has rolled off the show's current (Wistia) RSS feed, and has no
  Wayback capture. The entry now links only to the show's live page. *Recoverable if
  Sumo Logic re-publishes the archive or a personal copy exists.*

### Talk media never found (event/context link only)

- **#2 SciPy 2008** — only the proceedings paper survives; SciPy didn't post talk video
  in 2008.
- **#3 Hot-wiring the Transient Universe II (2009)** — only the IVOA TWiki agenda page.
- **#18 CIERA Northwestern colloquium (May 2014)** — announcement page only.
- **#19 DataEDGE panel (May 2014)** — speaker page only.
- ~~**#34 BIDS "Astrophysical Machine Learning" lecture (Apr 2019)** — event listing only,
  and that listing is now 404 (see link health), leaving the item effectively unreachable.~~
  **Resolved 2026-09-26:** a Wayback capture of the dead listing embeds the lecture video,
  which is still live on the BIDS YouTube channel; both are now linked (see link health).

### Slides survive, but no recording was ever found

\#6 Synoptic-survey ML (2011, SlideShare), #7 Royal Society (2012, Speaker Deck — the
meeting page once linked an MP3 of the talk, but its host `downloads.royalsociety.org` is
gone and the file was never archived; confirmed 2026-09-26),
\#10 LSST All-Hands (2012, Speaker Deck), ~~#16 NAS Big Data (2014 — slide match marked
*probable*)~~ (**resolved 2026-09-26:** the recording is on the National Academies' Vimeo
and the match is confirmed — see the last addendum), #20 Astro Hack Week tutorial (2014 — and the slides link is a
permission-walled Google Drive URL, so even that is effectively dead), #22 Data Science
Education (2015, SlideShare), #29 KDD (2017), #30 Autoencoding RNNs (2017),
\#35 DESI plenary (2019 — internal collaboration meeting, no public event page either),
\#36 DOE AI for Science town hall (2019), #40 ML Club (2021).

### Provenance uncertain (on the page with caveats in `talks.json` notes)

- ~~**#6 "Machine Learning and Classification in the Synoptic Survey Era" (2011)** —
  51-slide deck exists; exact venue/date estimated from related 2011–2012 work.~~
  **Resolved 2026-09-26:** the deck's own title slide reads "Berkeley Streaming Workshop;
  7 May 2012", so it is now `berkeley-streaming-2012` (see the old-format Keynote addendum).
- **#22 "Data Science Education: Needs & Opportunities in Astronomy" (2015)** — deck
  exists; venue unknown.
- **#30 "Autoencoding RNNs" (2017)** — deck only; venue unknown, dated from the paper
  posting.
- **#27 Haas Industrial ML lecture** — year approximate (2017).

### Paywalled

- **#15 Strata Santa Clara 2014 video** — behind the O'Reilly learning-platform
  subscription wall (returns 403). Kept as the link anyway since subscribers can reach it.

## Link health (last checked 2026-09-26)

### At PR time (2026-07-18)

All 82 outbound links were checked (GET with redirects; YouTube via oEmbed).
**76 live.** The 6 failures:

| # | Item | Link | Status | Diagnosis |
|---|------|------|--------|-----------|
| 12 | Berkeley Data Science Lecture 2013 | `url_video` (bids.berkeley.edu/resources/videos/…) | 404 | BIDS site restructured; webcast page gone. Wayback candidate. **Repaired 2026-09-26** (video found on YouTube — see the re-check below). |
| 12 | Berkeley Data Science Lecture 2013 | `event_url` (vcresearch.berkeley.edu/…) | 403 | Possibly bot-blocking — verify in a browser before replacing. **Repaired 2026-09-26** (not bot-blocking: the page is unpublished — see below). |
| 15 | Strata Santa Clara 2014 | `url_video` (oreilly.com/library/…) | 403 | Subscription wall (expected; not rot). |
| 20 | Astro Hack Week 2014 | `url_slides` (drive.google.com/…) | 401 | Permissioned Drive file — dead for visitors. Wayback/re-host candidate. |
| 33 | Masters of Data podcast 2019 | `event_url` (podcasts.apple.com/gb/…) | 404 | **Repaired 2026-07-18:** episode delisted everywhere (Apple GB+US 404, absent from the iTunes episode index, rolled off the show's Wistia feed, no Wayback capture); `event_url` now points at the live show page (sumologic.com/podcast). The audio itself is unrecoverable — see the unreachable list. |
| 34 | BIDS 2019 lecture | `event_url` (bids.berkeley.edu/events/…) | 404 | BIDS site restructured. Wayback candidate. **Repaired 2026-09-26** (Wayback, plus the lecture video — see below). |

### Re-check (2026-09-26)

`linkcheck` over 153 links: **137 ok, 9 walled, 7 dead** — the three July BIDS/vcresearch
failures plus four event pages that rotted after July. Each dead link was opened in a real
browser before repair. `#` is the current `talk_number`.

| # | Item | Link | Status | Diagnosis | Repair |
|---|------|------|--------|-----------|--------|
| 63 | `berkeley-data-science-lecture-2013` | `url_video` (bids.berkeley.edu/resources/videos/…) | 404 | BIDS site restructured (July row 12). | **Moved original:** the CITRIS YouTube upload the BIDS page embedded (`4mBUX47YtSE`); its captions introduce Bloom as the series' first speaker. |
| 63 | `berkeley-data-science-lecture-2013` | `event_url` (vcresearch.berkeley.edu/2013-14-data-science-lectures) | 504 (July: 403) | Not bot-blocking: a browser gets Pantheon's 504 or Drupal "Access denied" — the page is unpublished; the site root is live. | Wayback snapshot (2021-06-20). |
| 99 | `bids-2019` | `event_url` (bids.berkeley.edu/events/…) | 404 | BIDS site restructured (July row 34). | Wayback snapshot (2023-03-29). It embeds the lecture video, still live on the BIDS YouTube channel (`kf8a-NnjVQY`) — **added as `url_video`**. |
| 40 | `cospar-2010` | `event_url` (ui.adsabs.harvard.edu/abs/…) | 405 | AWS WAF bot challenge (`x-amzn-waf-action: captcha`); a fresh browser gets a "confirm you are human" CAPTCHA. The record exists (site publication `2010-cosp-38-2351-b`). | **No change** — not rot. `linkcheck` now reports WAF challenges as WALLED. |
| 68 | `hipacc-exascale-2014` | `event_url` (hipacc.ucsc.edu/…) | 000 | TLS certificate expired 2026-07-23 (browsers warn); `http://` redirects to a 404. The page itself is still on UCSC's legacy server. | Wayback snapshot (2024-11-06; talk under the Program tab). Talk video found in the workshop's YouTube playlist (`jkj8U5rxRMw`) — **added as `url_video`**. The slides PDF is behind the same certificate and was never archived. |
| 53 | `royal-society-2012` | `event_url` (royalsociety.org/…/2012/transients-universe/) | 404 | Page gone, though the Royal Society's own site search still lists it. | Wayback snapshot (2021-10-20) — later captures are the 2022 redesign without the programme; the talk is under Session 4. The programme's MP3 is unrecoverable (host gone, never archived). |
| 59 | `yale-colloquium-2012` | `event_url` (physics.yale.edu/events/physics-club/archive) | 404 | Yale Physics site relaunch; the pre-Fall-2016 Physics Club archive was not migrated. | Wayback snapshot (2026-03-12). |

After repairs: **145 ok, 10 walled, 0 dead of 155 links** (149 ok of 159 once master's AAS additions were merged in). All 10 walled links are
understood: ADS (above); the O'Reilly paywall and the permissioned Drive deck (July rows 15
and 20); and bot-blocking by aas.org (3 links), Columbia DSI, CfA ITC, archive.siam.org and
the JHU Gazette, each noted in its ledger entry as live in a browser.

After the old-format Keynote sweep (see its addendum), with the a16z pair merged: **171 ok,
10 walled, 0 dead of 181 links**; the walled ten are unchanged.

## Addendum — same-day restyle & audio pass (2026-07-18)

A second pass the same day, modeled on wesmckinney.com's transcript pages
(e.g. `/transcripts/2025-10-08-test-set-julia-silge-part1`):

- **Fonts copied from that site** (its `styles.css`): Inter (headings/UI), Lora
  (prose), IBM Plex Mono (the #N chip), loaded via Google Fonts, with its warm-cream
  palette (`#FDF8F0` page background, light mode only) — scoped to `/talk/` pages via
  the self-contained `talk_assets.html` partial.
- **Single pages redesigned**: large title above a metadata card (uppercase
  EVENT/LOCATION/DATE labels, type chip top-right, link buttons), auto-embedded
  YouTube/Vimeo player (`talk_video_embed.html`), the AI disclaimer as a left-bordered
  callout (template-rendered — the old per-page italic line under `## Transcript` was
  removed from all 18 transcript pages), a template-provided `Summary` heading, and a
  sticky "Contents" rail with scrollspy (transcript pages only, ≥1100px viewports).
- **Listen buttons** (`url_audio`): direct audio recovered for 7 items — the three NPR
  segments (direct `ondemand.npr.org` MP3s extracted from the story-page HTML), both
  TWiML episodes and Software Engineering Daily (megaphone.fm enclosures), and Gradient
  Dissent (captivate.fm enclosure via the show's RSS, found through the iTunes API).
- **External transcript links** (`url_transcript`): the three NPR items link
  `npr.org/transcripts/<storyId>` (shown for the two without embedded transcripts).
- **Link repair**: Masters of Data `event_url` moved from the dead Apple GB page to the
  live show page; the episode audio itself proved unrecoverable (see the unreachable
  list). Post-pass link health: **87 ok, 3 walled, 2 dead of 92 links** (the two BIDS
  404s remain the only rot).
- **Transcript cleanup** (parallel editing agents, same day): all 18 transcripts
  de-filler-ed (um/uh/"you know"/"kind of"), stutters collapsed, punctuation and
  capitalization fixed, reflowed into paragraphs at speaker turns/topic shifts, and
  obvious proper-name mis-transcriptions corrected (Charrington, Filippenko, RR Lyrae,
  Palomar Transient Factory, U-Net, Kaggle, …). 170k → 160k words (93.8% retained —
  filler only, no content cut; per-file floor 87.5%). The page callout now says
  "auto-generated and lightly edited for readability". List-page typography was also
  matched to wesmckinney.com/presentations' exact card CSS (tighter cards, serif
  section label, smaller normal-weight italic titles, Wes's #N chip styling).

## Addendum — CV merge (2026-07-18, PR #6)

Merged the talks list from the CV (TeX), including entries commented out there for
space. **45 → 94 entries; range now 1995–2025.** Process: parsed the CV, deduped
against existing entries, fanned out research agents (ADS/arXiv for proceedings-era
talks, Wayback for dead workshop sites, venue archives) — links were found for many,
and per the explicit decision, **talks with no surviving links/media still get entries**
(16 of 94 are link-less records).

Corrections that came out of the research (CV vs web, web wins where verifiable):
- Hot-wiring the Transient Universe: the classification-engine talk was at **HTU-I,
  Tucson, June 5 2007** (renamed `hotwired-2009` → `hotwired-2007`); a separate
  **HTU-II (Santa Cruz, Apr 27 2009)** talk "The Synoptic Infrared Imaging Survey"
  was added.
- `autoencoding-rnn-2017` → `autoencoding-rnn-2018`: venue found (AI Workflows in
  Astronomy & Microscopy, San Jose, Sep 2018); an NCSA Oct 2018 delivery added.
- IPDPS 2014 keynote was **Phoenix** (CV said Flagstaff), official title "…at Scale
  and Under Duress"; Gehrels memorial was at **NASA Goddard** (CV said NAS); AAS 191
  was **Jan 1998** (CV said Jan 1997); 4th Huntsville was **Sept 1997** (CV said Oct);
  AAAS talk was **Feb 15 2015** (CV said Jan); STScI colloquium **Nov 9 2011** (CV said
  Nov 11); IPAM date confirmed Sep 23 2019 (CV's Nov 2019 wrong); `stanford-c4du-2025`
  retitled to the CV's "Eurekaizing Anomalies"; `harvard-iacs-2020` dated Oct 2020 per CV.
- Media recovered for old talks: KIPAC@10 2013 and MMDS 2014 videos (YouTube),
  VOEvent 2005 slides PDF + QuickTime movie (live on the IVOA wiki), Barcelona 2001
  slides (Wayback capture of his old Caltech pages).
- Pre-2010 colloquia/seminars generally have no surviving media — they are on the page
  as records with `notes` documenting the search.

Link health after merge: **119 ok, 7 walled, 4→2 dead of 130** (the two remaining dead
are the known BIDS 404s; a dead SLAC index was swapped to a Wayback snapshot and a
never-archived KIPAC event link dropped).

## Addendum — local slide-archive sweep (2026-07-18, PR #7)

Scanned ~/Talks, ~/OldLaptop/Talks, and ~/OldLaptop/MoreOldTalk (~250 Keynote/PDF/PPT
files; note `~/OldLaptop/*` are symlinks — `find` needs `-L`). Pipeline: filter
non-talks (courses, backups, personal) → extract first-page text (pypdf) or the
preview image embedded in each .key zip → vision agents read titles/venues/dates off
the title slides → dedupe against the ledger → web-verify events. **100 → 124
entries.**

- **24 new talks** (1998–2024), highlights: Swift@5 2009 (archived program lists the
  talk), COSPAR 2010 Bremen, SACNAS 2010, the Royal Society Kavli satellite meeting
  2012 (archived page lists him as speaker), a second SIAM CSE13 talk (MS158), the
  UC-HiPACC exascale workshop 2014, BASCD 2019 keynote, MLSE 2020, the CPAR/DREAM 2023
  first delivery of the "Real AI Revolution" talk, AIRA splinter at AAS 241, and
  C²OA²SE 2024 (Michigan Tech, Ann Arbor).
- **Slide-derived corrections**: autoencoding-rnn-2018 pinned to Sep 11, 2018, Santa
  Clara with the full workshop name; ncsa-2018 pinned to Oct 17, 2018 with the real
  workshop title; simons-visions-2013 moved to May 30 per the deck. A slide dated
  "AAS Austin Jan 2011" was corrected to AAS 219 (Jan 2012 — SN 2011fe postdates
  Jan 2011); "IAU Oxford Sept 2011" matches no IAU meeting and is recorded as an
  Oxford seminar with a caveat note (*wrong: it was IAU Symposium 285 — corrected in the
  old-format Keynote addendum*).
- **Privacy rule applied** (industry decks without venues are private): excluded
  a16z academic roundtable (since published at JB's request, deck in the slide viewer:
  see the 2026-09-26 a16z addendum), D. E. Shaw, Thomson Reuters, Vodafone, Fujitsu forum,
  TCV CIO/CTO, WeWork, Arkadium, Orange Institute, and all wise.io product/client
  decks (several marked "Confidential / Not for distribution"), plus Valency investor
  decks. Also excluded: courses/guest lectures (INFO 296A), lab-internal decks (BAIR
  retreat, Moore check-ins, group intros), student-authored decks, posters, and decks
  whose first page carried no identifying metadata (amnh, davis, como, keck, cefalù —
  the last could not be matched to any real Cefalù 2012 meeting). (*Their slide text
  later identified four of them, cefalù being a 2008 meeting; como was a colleague's
  talk — see the old-format Keynote addendum.*)
- 15 old-format Keynote bundles had no extractable preview (incl. citris2010,
  i4science, gw) — unreadable without opening Keynote; left for a manual pass.
  (*Done 2026-09-26 without Keynote, by reading the bundles' XML — see the old-format
  Keynote addendum.*)

## Addendum — AAS/HEAD meeting abstracts (2026-09-26)

JB supplied six ADS abstracts; the meeting programs sorted them:

- **Four oral talks, now with abstracts on their pages.** New: AAS 199 (Jan 2002).
  Enriched: AAS 191 (Jan 1998; title set to the official abstract title), HEAD 9 (Oct
  2006), and the 2010 Pierce Prize lecture, which gained the AAS's own video, now
  embedded (direct `.mp4` files embed like YouTube).
- **Two posters, deliberately left off** (posters are out of scope for this page):
  AAS 213 469.07 "Rapid and Automated Classification of Events from the Palomar
  Transient Factory" (poster session 469 "PTF", Jan 7 2009) and AAS 214 602.03
  "EXIST-observed GRBs As A Gateway to the z > 7 Universe" (late-abstract poster, Jun 2009).

Where the sources live now: AAS moved its pre-2010 meeting programs and BAAS abstracts to
`aasarchives.blob.core.windows.net` (linked from aas.org/meetings/past-meetings) and meeting
videos to `aasfiles.blob.core.windows.net`. aas.org itself returns 403 to curl (so
`linkcheck` reports it WALLED), and ADS abstract pages demand human verification, so ADS
links appear only in page bodies, never in link fields.

## Addendum — transcripts for the recovered recordings (2026-09-26, PR #13)

The link-rot repair (see "Re-check (2026-09-26)" under link health) turned up three
YouTube recordings, and all three now have embedded transcripts, Key Quotes and
`research/<slug>.summary.txt` files. **Transcript pages: 20 → 23.**

| Talk | Recording | Words (raw → clean) | Notes |
|------|-----------|---------------------|-------|
| `berkeley-data-science-lecture-2013` | CITRIS, 1:03 | 12,210 → 11,258 (92%) | Pérez intro, lecture, panel, audience Q&A; speaker labels; 5 quotes |
| `bids-2019` | BIDS, 48 min | 8,502 → 8,195 (96%) | single speaker; 3 `[inaudible audience question]` markers; 4 quotes |
| `hipacc-exascale-2014` | UC-HiPACC, 18 min | 3,049 → 2,839 (93%) | single speaker; 4 quotes |

- **Pipeline:** `yt-dlp --write-auto-subs` VTT → keep only the lines carrying inline
  `<c>` timing tags (the new words; the untagged lines are rolling repeats) → six
  3–4.6k-word chunks → parallel Opus editing agents with one shared rule sheet (remove
  filler, collapse stutters, fix punctuation and mis-heard names, keep content) → a
  checker for leftover fillers, stutters and word retention → spot checks against the raw
  captions. Overall 93.8% of words retained, the same as the July pass.
- **Speaker labels (2013 panel):** PÉREZ, BLOOM, STARK, SILVER, ALLEN, AUDIENCE, taken
  from introductions and field-specific content. Two turns were settled by idiolect:
  "wind up" appears 9 times in Bloom's ~4.5k words and never in the other speakers' ~6k.
  Seven turns that stayed ambiguous are labeled `PANELIST`.
- **Verified name fixes:** Manik Varma (a Visiting Miller Professor in spring 2019;
  caption "Matic pharma"), Aaron Culich (Stark's Stat 157 co-instructor, fall 2013;
  "Aaron Coolidge"), Ruth Angus of AMNH ("with Angus from the aah"), NERSC ("nurse"),
  Haviland Hall's seismometer ("basement of heaven"), the Ørsted satellite ("urstead"),
  "time-domain data" ("China main data"), Cesium, bigmacc.info, SAMSI. **Kept as
  captioned** (unverified): "Gyro" (BIDS 2019; possibly Uroš Seljak), the Stanford visitor
  "Shannon Neulon", and the VCRO organizer "Kaya".
- **Topics:** `berkeley-data-science-lecture-2013` gained `education`, since about a fifth
  of the event (mostly the Q&A) is about training students, the Python boot camp and new
  courses. The other two stay `astronomy`/`ai-ml`. The HiPACC card summary, previously a
  placeholder, was rewritten from the transcript.

## Addendum — NRC big-data workshop recording (2026-09-26)

JB supplied the National Academies' Vimeo recording of `nas-big-data-2014`, "Computational
Training and Data Literacy for Domain Scientists", until then a slides-only entry whose
venue was marked *probable*. It now has the video, a transcript, Key Quotes and a
`research/nas-big-data-2014.summary.txt`. **Transcript pages: 23 → 24.**

- **Venue confirmed three ways:** the Vimeo description (a Committee on Applied and Theoretical Statistics workshop, April 11, 2014);
  the deck's title slide and speaker notes (local archive,
  `~/OldLaptop/MoreOldTalk/nas_bloom_teaching_big_data.key`, an old-format Keynote bundle
  whose `index.apxl` XML yields the slide text); and the workshop proceedings (NAP 2015,
  doi:10.17226/18981), whose Chapter 4 summarizes the talk under this exact title. The
  page body links that chapter. The event is now credited to the National Research
  Council, which convened the workshop. `event_url` is the Academies' current project page;
  the old `/our-work/` URL now 301s there.
- **First Vimeo video on the page.** `url_video` is the canonical `vimeo.com/94389370`,
  because `talk_video_embed.html` only embeds `vimeo.com/<id>` URLs, not the showcase URL
  (`vimeo.com/showcase/2861203?video=…`). The video's embed permission is public.
- **Pipeline (Vimeo has no captions):** yt-dlp's Vimeo extractor now fails (its OAuth
  token fetch returns 401), so the 240p MP4 came straight from the player config
  (`player.vimeo.com/video/<id>/config` → `request.files.progressive`). It was transcribed
  locally with faster-whisper `distil-large-v3` (CPU int8, VAD; ~13 min for the 33.6-min
  talk on an M2, plus a one-time 1.5 GB model download). Then **every doubtful passage and
  every Key Quote was re-transcribed with `medium.en`** as an independent check (28 clips),
  and the result was cleaned by hand, with names and terms checked against the deck.
  5,569 → 5,468 words (98% kept; Whisper already drops most fillers).
- **The second model settled:** "after-hours hackathons" (distil: "after our"), "muck in on
  the command line" ("mock in"), "robotic telescope resources" ("research. sources"), "IBM
  Watson is using" ("is used. using"), and a phantom "We are with…" that was really
  "…arriving in just a few years from now with a huge amount of data". **Kept as spoken**
  because both models agreed: "four or five people take this course for credit" (he later
  says renaming it raised for-credit enrollment to about 40), "say, in MATLAB",
  "U.S. national involvement" (LOFAR/SKA) and "mentor-mentoree".
- **Speakers:** FREW (session chair James Frew, per the proceedings), whose introductions are
  cut mid-sentence at the start of the video, then BLOOM. The excerpt ends before any Q&A.
- **Topics:** `education` + `astronomy`. About 15% of the talk is the astronomy data-deluge
  motivation (LSST, LOFAR/SKA, the PTF transient pipeline, a PNAS Kepler result), and it
  carries the argument. Machine learning comes up only in passing, so no `ai-ml`.

## Addendum — a16z Academic Roundtable talk and interview (2026-09-26)

JB asked for a16z's "Supernovas and Novel Insight: Where Machine Learning is Headed Next"
(a16z.com, Jan 2015), then supplied the deck of the talk he gave at the same event, a16z's
second annual Academic Roundtable (Sep 25–27, 2014, at the firm's Menlo Park offices). Both
entries are dated 27 Sep 2014.

- **#76 `a16z-roundtable-2014`: "Practicable Machine Intelligence in Science & Industry"
  (Invited Talk).** a16z's invitation asked for 15 minutes on his ML research, and the
  archived agenda (Wayback's 2014-10-21 capture of academic.a16z.com, now the `event_url`)
  lists it at 11:10am on the last morning as the "Artificial Intelligence" session. No
  recording was posted. The 24-slide deck is in the embedded viewer (`talks.py slides`,
  2.1 MB of WebP); the PDF stays out of the repo. At JB's request this lifts the
  slide-archive privacy exclusion (above) for this one deck.
- **#77 `a16z-interview-2014`: the a16z video (Podcast).** It is an interview a16z filmed
  at the roundtable after the talk (he refers back to "my talk"), not a talk recording.
  **Typed `Podcast` per JB**; the first pass used `Interview`, which the Type filter files
  under Radio. The a16z page's Vimeo embed is dead (the page prints the raw `[vimeo]`
  shortcode), so the page embeds a16z's own YouTube re-upload (`6hQqpQ3IZlY`).
  **Transcript pages: 24 → 25.**
- **Transcript from local Whisper, per JB, not auto-captions.** The installed yt-dlp
  (2026.07) gets HTTP 403 from YouTube's media servers, so the audio came from the latest
  yt-dlp run in isolation (`uvx --from "yt-dlp[default]@latest" yt-dlp --js-runtimes node
  -f 140`). faster-whisper `distil-large-v3` (int8, CPU) transcribed the 14.5 minutes in
  15, and an AI pass removed fillers, false starts and stutters: 2,794 → 2,657 words
  (95%). Doubtful phrases and every Key Quote were re-heard with `medium.en` on isolated
  clips. Whisper fixed several auto-caption errors: "in the penthouse" was "couldn't have
  done in the past", "apply non-data" was "opine on data", and "no extra mning data" was
  "noisy streaming data". It also reversed one guess from the caption-based draft: "the
  total amount of data" is really "the toy amount of data" (a single 0.14-second word in
  both Whisper models).
- **Same-day order:** `rank_key` breaks date ties on the existing `talk_number`, so the
  talk stays #76 and the interview #77 through later renumbers.

## Addendum — old-format Keynote sweep (2026-09-26)

The July slide-archive sweep read each deck only through its embedded preview image and
left "15 old-format Keynote bundles" for a manual pass. Old-format decks (Keynote '08/'09,
before the 2013 IWA format) turn out to be machine-readable: the `.key` is a zip, or a
directory package, whose `index.apxl` (sometimes `index.apxl.gz`) is XML. Splitting it on
`<key:slide ` and stripping the tags from each `<sf:p>…</sf:p>` gives every slide's text,
and each slide's `<key:notes>` element holds its speaker notes. So this pass re-read
**every** old-format deck in the three folders as text, not just the 15, and deduped the
title slides, venue lines and notes against the ledger. **18 new entries: 130 → 148**
(counting the a16z pair that merged just before).

```python
import html, re, zipfile
def paras(frag):   # text of each <sf:p> paragraph in an XML fragment
    return [html.unescape(re.sub(r"<[^>]+>", "", p)).strip()
            for p in re.findall(r"<sf:p\b[^>]*>(.*?)</sf:p>", frag, re.S)]
xml = zipfile.ZipFile(path).read("index.apxl").decode()   # or gunzip index.apxl.gz
for seg in re.split(r"<key:slide\s", xml)[1:]:              # master slides don't match
    seg = seg.split("</key:slide>")[0]
    body, _, notes = seg.partition("<key:notes")
    slide_text, speaker_notes = paras(body), paras(notes)
```

**Inventory.** `find -L ~/Talks ~/OldLaptop/Talks ~/OldLaptop/MoreOldTalk -iname '*.key'
-prune` finds 208 items: **99 old-format decks** (98 zips and 1 directory package), 95
new-format decks, 12 zero-byte files and 2 zipped new-format packages. All 99 old-format
decks parsed, giving 4,598 slides, 1,970 of them with speaker notes. Title slides usually
name the venue and date. When they didn't, other sources filled the gap:
- the notes ("as you'll see tonight…", "Perley, this meeting");
- the file's last-saved time;
- JB's email (organizer confirmations, via msgvault);
- his merit-review CVs (`~/Admin/Merit/*/jsbcv_*.tex`).

Every addition was then checked on the web: live pages where they still exist, Wayback
captures otherwise.

**What the "15 with no preview" were:**
- **12 zero-byte files** in `~/OldLaptop/Talks`: `citris2010`, `citris2010_nobackup` (plus an
  empty `.zip`), `gw`, `i4science`, `i4science_2011`, `jc20111`, `RRL_midIR`, `sacnas`,
  `siam_2011`, `siam_2011_long`, `stsci_2011`, `tvs_tucson_lsst`. Each is 0 bytes in 0 blocks
  with only a Finder-info xattr, so the content was lost when the laptop was copied; neither
  Keynote nor a parser can read them.
  - Readable copies of 7 survive (`Backup of …`, the `MoreOldTalk` duplicates,
    `SASIR/sacnas_bloom_oct1.key`).
  - Of the other five: `citris2010` (and its `_nobackup` twin) is now `citris-2010`, found
    through its recording; `stsci_2011` is already `stsci-2011`; `siam_2011_long` was a
    longer cut of `siam-cse-2011`; `RRL_midIR` (RR Lyrae in the mid-IR?) is simply gone.
- **1 directory package**, `GRBs/invited_swift_penn_state_nov_2009_08.key`, readable after
  gunzipping `index.apxl.gz`; it is Swift@5, already `swift5-2009`.
- **2 zipped new-format packages** in `~/Talks`, `jul2019talk.key` and `invnet.key` (their IWA
  text came out through a small raw-snappy decoder). Both are student-authored decks by
  Keming Zhang (deepCR, 2019; cyclic-permutation-invariant networks, 2020), so they are out
  of scope.

**Added (18).** Each ledger `notes` field records the deck, email and web evidence.

| Slug | Date | Talk | Found through |
|------|------|------|---------------|
| `cefalu-2008` | 2008-09-19 | GRBs as Cosmological Probes | deck; July's "Cefalù 2012" guess was wrong (SOC listing on the archived conference page; programs never archived, so the day is the slide's) |
| `eventful-universe-2010` | 2010-03-18 | Scratching Decadal Itches with GRBs (invited) | deck; archived NOAO schedule |
| `citris-2010` | 2010-03-31 | Automating Discovery and Classification of the Dynamic Universe | 0-byte deck → organizer email → CITRIS's 54-min YouTube recording. **Title is descriptive** (the announced one wasn't preserved) |
| `keck-2010` | 2010-04-13 | Cosmic Forensics: Tracking Stellar Deaths | deck; Keck's invitation (by-invitation "Evenings with Astronomers" series; no web listing of this lecture) |
| `scidac-2010` | 2010-05-20 | Exploiting the Transient IR Sky | deck; organizer email; the SciDAC consortium meeting's schedule (unlinked by request, see notes) |
| `learning-in-retirement-2010` | 2010-09-14 | Gamma-Ray Bursts: Birth Cries of Black Holes | deck; UC Berkeley Retirement Center newsletter |
| `dean-lecture-2010` | 2010-10-04 | Making Sense of the Dynamic Universe in the Synoptic Survey Era | **no deck**: the merit CVs' outreach paragraph → organizer email → archived Academy listing + iTunes U audio |
| `compass-2010` | 2010-10-07 | What Are Gamma-Ray Bursts? | deck; archived Compass Project post |
| `llnl-2010` | 2010-11-19 | SASIR: A Wide-Field Synoptic Survey for this Decade | deck; organizer email (no web listing survives) |
| `gwpaw-2011` | 2011-01-28 | EM Followup: Past, Present, Future (invited) | backup deck (`gw.key` is 0 bytes); archived GWPAW program and slides PDF |
| `berkeley-roundtable-2011` | 2011-04-29 | Making Sense of the Dynamic Universe in the Synoptic Survey Era | deck; email (internal donor event, like the 2022/2025 roundtables) |
| `iaus285-2011` | 2011-09-23 | Technical and Observational Challenges for Future Time-Domain Surveys (invited) | deck; IAU S285 proceedings (Cambridge Core) |
| `ucdavis-2011` | 2011-10-08 | Challenges to Automating the Scientific Workflow in Streaming Astronomical Data (invited) | deck; archived workshop schedule |
| `columbia-2011` | 2011-11-08 | The Transient Universe | deck (no title slide); Columbia's pizza-lunch listing |
| `amnh-2011` | 2011-11-08 | Time-Domain Challenges in the Synoptic Survey Era | deck; organizer email; AMNH's public calendar |
| `dean-lecture-2012` | 2012-09-10 | The Supernova of a Generation: SN 2011fe | deck (its title slide says Sept 9; the Academy's page and email say Monday Sept 10); iTunes U audio |
| `hotwired-2013` | 2013-11-14 | The Modern Automated Astrophysics Stack | deck; archived HTU-III speakers page; SLAC eConf proceedings |
| `berkeley-roundtable-2014` | 2014-05-05 | Inference in Time Domain Astrophysics | deck; email (the invitation's title was "Big Data Science in Time Domain Astronomy") |

**Corrected (3).** Two slugs changed; Hugo `aliases` keep the old URLs working.
- **`citris-2013` → `citris-2011`.** The CITRIS video (YouTube upload 2011-05-19) is the
  **April 5, 2011 i4Science lecture**, not a 2013 Research Exchange talk: the i4Science deck
  has the same title, and the organizer's program has the 2:00pm slot. The Research Exchange
  series link moved to `citris-2010`, his actual Research Exchange talk.
- **`oxford-2011`**, the SN 2011fe talk (`sn2011fe_iau`, title slide "IAU Oxford- 20 Sept
  2011"): the July sweep said "IAU Oxford Sept 2011" matched no IAU meeting, but **IAU
  Symposium 285** (New Horizons in Time-Domain Astronomy) ran in Oxford on Sept 19–23,
  2011. It is now credited to the symposium (Tuesday, "Explosive or Irreversible
  Changes") and linked to the proceedings. His invited review on the closing day is the
  new `iaus285-2011`.
- **`synoptic-survey-ml-2011` → `berkeley-streaming-2012`.** Found while deduping; not an
  old-format deck. The SlideShare deck's title slide (slide 2) reads "Classification of
  Astronomical Time-Series Data in the Synoptic Survey Era … Berkeley Streaming Workshop;
  7 May 2012", i.e. the workshop "From Data to Knowledge: Machine Learning with Real-time and
  Streaming Applications". That resolves item #6 of "Provenance uncertain" above.
- Ledger-only notes: `samsi-2012` (the deck says Sept 20, but its save times match the
  program's Sept 21) and `ciera-northwestern-2014` (the CV and the roundtable deck give
  "Inference in Time Domain Astrophysics"; the CIERA announcement's title is kept).

**Excluded (same rules as July).** Every other old-format deck either matches an entry
already on the page or falls under one of these groups:
- **Not his talk:** `como` was prepared for the "GRBs as Probes" meeting (Como, May 2011),
  but he did not attend and Nial Tanvir presented it for the group.
- **Home-department internal:** `sasir_berkeley` was the Berkeley astronomy Theory Lunch
  (Sept 29, 2010). The rule applied: a visiting talk at another department's lunch
  (`columbia-2011`) counts, a lunch talk in his own department does not.
- **Unverified collaboration meeting:** `sasir_bigboss_nov2009` (a SASIR pitch to BigBOSS;
  no trace in email or on the web).
- **Not a talk:**
  - `Backup of tvs_tucson_lsst` is five welcome slides as co-chair of the LSST TVS workshop
    (NOAO, March 2011).
  - `lsst_aas` (+ backup) is image-only LSST status slides with notes, for the Nov 2010
    town hall that `sasir-townhall-2010` already covers.
  - `aas2010_poster` is a poster.
- **Courses and guest lectures:** `ay290-2011` (+ backup), `ay290-2013`, `ay250-2013`,
  `intro` (Python for Data Science), `ischool` and `ischool copy` (INFO 296A, 2013 and
  2014).
- **Lab-internal:** `lars` (+ backup; a group meeting, July 2011), `jc20111` (+ copies; a
  journal club), `nch-bloomlab`, `dark` (a retreat dinner talk, "DARK Out in Portugal
  2012"), `astronomy` (a department map), `moore_sloan_bids_bloom` (an internal BIDS
  announcement, Nov 2013).
- **Industry, client or funder (private):** `thomson-reuters-wiseio-k09`, `arkadium`,
  `deshaw_bloom`, `wiseio_joshlecture_slides`, `machine_intelligence engine` and
  `machine_intelligence engine_jsb`,
  `ml tech`, `claudia1`/`claudia2`, `haas`/`haas_life` (a wise.io "Life as an
  Entrepreneur" talk at Haas, Nov 2013, whose deck also carries the title slide of an
  Oct 2013 "Citrix Data Camp" pitch; no public listing for either), and
  `bloom_mooresloan_draft`/`bloom_datascience` (the Moore/Sloan "Supporting Data Science"
  workshop, March 2013).
- **Fragments:** `bloom_1min_2013`, `maxwise_mira_slide`, `josh-scipy`, and the IAU S285
  side slides `iau_gw_slides` and `grb_questions_iau`.
- **Already on the page, no change:** `petrosian-fest`, `lobster_bloom`, `exist_cospar`
  (+ `exist_cospar_no_backup`), `invited_swift_penn_state_nov_2009`, `pierce_aas_2010`,
  `aas_townhall`, `sacnas_bloom_oct1`, `siam_2011`, `mit_colloqium`,
  `sn2011fe_bloom_aas_2012` and `sn2011fe_bloom_iau` (AAS 219; the latter is its Jan 2012
  copy), `royal society 2012`, `b3` (the Royal Society satellite meeting), `neutrino`
  (IceCube), `bloom_SAMSI` (+ `bloom_SAMSI_16`), `yale_colloqium`, `scipy2012_bloom`/`siam2013_bloom`/`visions_of_cs_bloom`/
  `ciera` (SIAM CSE 2013, Visions 2013 and CIERA reuses), `siam_2013_bloom_catalogs`,
  `bloom_kipac`, `data_science_bloom`, `strata_josh_henrik_key09`, `hipacc`,
  `nas_bloom_teaching_big_data`, `mmds2014_bloom`, `aaas_bloom_16x9`, `pydata_bloom_16x9`.

**Recordings and link health.** Three additions have recordings:
- `citris-2010` is on CITRIS's YouTube channel.
- Both Benjamin Dean lectures have the Academy's audio from its former iTunes U collection.
  Those MP3s survive only on Apple's legacy CDN (`a*.phobos.apple.com`), over **http only**,
  and are **not in the Wayback Machine**. They are the most fragile links on the page, so
  save copies.

No recordings were found for the other additions. Two live pages (SLAC's eConf proceedings
and Columbia's astronomy wiki) fail certificate verification in the Miniforge `curl` that
`linkcheck` finds first on this machine, though they load fine in browsers and in
`/usr/bin/curl`. So `hotwired-2013` links the archived workshop page and `columbia-2011`
the archived wiki page, with the live URLs in the notes. `linkcheck` itself now checks
Wayback snapshots one at a time after its parallel pass. This sweep adds 11 Wayback links
(26 in all), and in parallel the Wayback Machine refuses connections (curl reports
`000`), which had made working snapshots look dead.

**Leads for a later pass:**
- `~/OldLaptop/TalksOld` has 21 more `.key` files from about 2007–08 (`SSLColloquium`,
  `neyman`, `sfaa`, `santa-fe07`, `princeton1`, `microsoft`, `report_ucla`, …). Neither
  sweep covered it.
- The merit-review CVs list talks, including commented-out lines ("% Barcelona SASIR",
  "% USF talk") that were never chased.
- The UC Berkeley Retirement Center lists a second Learning in Retirement talk, "Transforming
  Astrophysics with AI" (Nov 5, 2024), with a YouTube recording (`tniRyPP1aGg`). It is not on
  the page yet.
- Transcripts for `citris-2010` (54 min video) and the two Dean lectures (1 h 38 min and
  1 h 24 min of audio), via the local-Whisper pipeline.

## Addendum — Learning in Retirement 2024 lecture (2026-09-27)

JB asked for a missing talk: "Transforming Astrophysics with AI" (Tue Nov 5, 2024), Part II of
the UC Berkeley Retirement Center's Learning in Retirement series "Berkeley in Space", organized by
Donald Mastronarde. It is now `learning-in-retirement-2024` (#137), a Lecture whose event name
follows `learning-in-retirement-2010` (from the old-format Keynote sweep). **Transcript pages: +1.**

- **Sources:** the LIR "Past LIR Events and Recordings" page (retirement.berkeley.edu/lir, under
  "2024 Past Events"; in Wayback from 2025-02-07) gives the title, date, series and speaker. Its
  "View recording" link is the Retirement Center's YouTube upload (`tniRyPP1aGg`, 1:05:51). The deck's
  title slide agrees. The deck survives as `~/Talks/bloom_coase_2024.key`, last saved two days later
  for `c2oa2se-2024`. The LIR's Drive "resource library" stops at 2017, so there is no slides link.
- **Zoom, no Q&A:** the video shows Bloom's webcam over his slides, so the location is "Berkeley, CA
  (virtual)", as for `harvard-iacs-2020`. The recording stops at his closing thank-you, before the
  Q&A. Speakers are MASTRONARDE (introduction) and BLOOM.
- **Transcript (local Whisper):** `distil-large-v3` took 2 h 26 min for the 66 minutes, because the
  M2 was shared with another session's Whisper jobs (load average 100–200). Four parallel Opus
  agents cleaned it using one rule sheet and a list of terms read off the slides. The slide list
  came from 73 distinct frames sampled with PyAV (no ffmpeg needed) and from the deck's text, pulled
  with a pure-Python IWA/Snappy decoder. 10,935 → 10,755 words (98%). `medium.en` re-heard every
  Key Quote and the doubtful passages. Three disputed words then went to a narrow-window run of
  both models with word probabilities. It settled "none of which **is**" (not "are"). "Data sets
  that/there are out there" stayed split (0.88 vs 0.60), so the quote starts after it. The host's
  "decartered" was "garnered". Both models agree on, so the text keeps as spoken: "on the
  right-hand side is supervised" (the slide says unsupervised), "far away from their host galaxy"
  (star), "would tell us it shouldn't" and "this action space isn't as complex as even
  self-driving cars" (p = 1.00 in both; he means more complex). Four of these audio-checked
  fixes missed the PR #18 merge and followed in a small PR.
- **Topics:** `astronomy` + `ai-ml`. Valency never appears (Wise.io only in the bio), so there is no
  `industry`, and a primer on ML types for a lay audience doesn't make it `education`.
- **Numbering:** it landed after PRs #15–#17, so its ledger entry is `n = 149`, and `renumber`
  puts it at #137, just ahead of `c2oa2se-2024` two days later.

## Maintenance

Two skills were added with this branch:

- **`add-talk`** (`.claude/skills/add-talk/`) — add a new talk/podcast/media item:
  scaffolds the page bundle, appends to `talks.json`, handles numbering (including
  inserts), transcripts, and verification. Engine: `scripts/talks.py`
  (`validate` / `scaffold` / `renumber` / `linkcheck`, stdlib-only).
- **`check-talk-links`** (`.claude/skills/check-talk-links/`) — periodic link-rot check
  with Wayback-replacement guidance; re-date-stamp the table above when run.
