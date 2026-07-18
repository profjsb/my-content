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
  list-page Topic filter — vocabulary `astronomy` / `industry` / `ai-ml` / `education`
  (`talks.py validate` enforces it). The Type filter folds `talk_type` into six buckets
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
- **#34 BIDS "Astrophysical Machine Learning" lecture (Apr 2019)** — event listing only,
  and that listing is now 404 (see link health), leaving the item effectively unreachable.

### Slides survive, but no recording was ever found

\#6 Synoptic-survey ML (2011, SlideShare), #7 Royal Society (2012, Speaker Deck),
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

## Link health at PR time (checked 2026-07-18)

All 82 outbound links were checked (GET with redirects; YouTube via oEmbed).
**76 live.** The 6 failures:

| # | Item | Link | Status | Diagnosis |
|---|------|------|--------|-----------|
| 12 | Berkeley Data Science Lecture 2013 | `url_video` (bids.berkeley.edu/resources/videos/…) | 404 | BIDS site restructured; webcast page gone. Wayback candidate. |
| 12 | Berkeley Data Science Lecture 2013 | `event_url` (vcresearch.berkeley.edu/…) | 403 | Possibly bot-blocking — verify in a browser before replacing. |
| 15 | Strata Santa Clara 2014 | `url_video` (oreilly.com/library/…) | 403 | Subscription wall (expected; not rot). |
| 20 | Astro Hack Week 2014 | `url_slides` (drive.google.com/…) | 401 | Permissioned Drive file — dead for visitors. Wayback/re-host candidate. |
| 33 | Masters of Data podcast 2019 | `event_url` (podcasts.apple.com/gb/…) | 404 | **Repaired 2026-07-18:** episode delisted everywhere (Apple GB+US 404, absent from the iTunes episode index, rolled off the show's Wistia feed, no Wayback capture); `event_url` now points at the live show page (sumologic.com/podcast). The audio itself is unrecoverable — see the unreachable list. |
| 34 | BIDS 2019 lecture | `event_url` (bids.berkeley.edu/events/…) | 404 | BIDS site restructured. Wayback candidate. |

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

## Maintenance

Two skills were added with this branch:

- **`add-talk`** (`.claude/skills/add-talk/`) — add a new talk/podcast/media item:
  scaffolds the page bundle, appends to `talks.json`, handles numbering (including
  inserts), transcripts, and verification. Engine: `scripts/talks.py`
  (`validate` / `scaffold` / `renumber` / `linkcheck`, stdlib-only).
- **`check-talk-links`** (`.claude/skills/check-talk-links/`) — periodic link-rot check
  with Wayback-replacement guidance; re-date-stamp the table above when run.
