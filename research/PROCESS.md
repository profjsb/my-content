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
\#10 LSST All-Hands (2012, Speaker Deck), #16 NAS Big Data (2014 — slide match marked
*probable*), #20 Astro Hack Week tutorial (2014 — and the slides link is a
permission-walled Google Drive URL, so even that is effectively dead), #22 Data Science
Education (2015, SlideShare), #29 KDD (2017), #30 Autoencoding RNNs (2017),
\#35 DESI plenary (2019 — internal collaboration meeting, no public event page either),
\#36 DOE AI for Science town hall (2019), #40 ML Club (2021).

### Provenance uncertain (on the page with caveats in `talks.json` notes)

- **#6 "Machine Learning and Classification in the Synoptic Survey Era" (2011)** —
  51-slide deck exists; exact venue/date estimated from related 2011–2012 work.
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
  Oxford seminar with a caveat note.
- **Privacy rule applied** (industry decks without venues are private): excluded
  a16z academic roundtable (deck only; a16z's public interview from it was added
  2026-09-26, see that addendum), D. E. Shaw, Thomson Reuters, Vodafone, Fujitsu forum,
  TCV CIO/CTO, WeWork, Arkadium, Orange Institute, and all wise.io product/client
  decks (several marked "Confidential / Not for distribution"), plus Valency investor
  decks. Also excluded: courses/guest lectures (INFO 296A), lab-internal decks (BAIR
  retreat, Moore check-ins, group intros), student-authored decks, posters, and decks
  whose first page carried no identifying metadata (amnh, davis, como, keck, cefalù —
  the last could not be matched to any real Cefalù 2012 meeting).
- 15 old-format Keynote bundles had no extractable preview (incl. citris2010,
  i4science, gw) — unreadable without opening Keynote; left for a manual pass.

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

## Addendum — a16z Academic Roundtable interview (2026-09-26)

JB asked for a16z's "Supernovas and Novel Insight: Where Machine Learning is Headed Next"
(a16z.com, Jan 2015) to be added (`a16z-roundtable-2014`). It is **an interview a16z filmed
at its second annual Academic Roundtable** (Sep 25–27, 2014, at the firm's Menlo Park
offices), not a recording of his roundtable talk, so it is typed `Interview` and dated to
the talk day (27 Sep 2014, from the deck's title slide; he refers back to "my talk"). The
a16z page's Vimeo embed is dead (the page prints the raw `[vimeo]` shortcode), but a16z's
own YouTube re-upload (`6hQqpQ3IZlY`) is live and now embedded, with a transcript cleaned
from its auto-captions (2,845 → 2,629 words, 92%). **Transcript pages: 23 → 24.**

The privacy rule above still covers the talk itself ("Practicable Machine Intelligence in
Science & Industry"): no public recording was found, and the deck stays private and off
the site.

## Maintenance

Two skills were added with this branch:

- **`add-talk`** (`.claude/skills/add-talk/`) — add a new talk/podcast/media item:
  scaffolds the page bundle, appends to `talks.json`, handles numbering (including
  inserts), transcripts, and verification. Engine: `scripts/talks.py`
  (`validate` / `scaffold` / `renumber` / `linkcheck`, stdlib-only).
- **`check-talk-links`** (`.claude/skills/check-talk-links/`) — periodic link-rot check
  with Wayback-replacement guidance; re-date-stamp the table above when run.
