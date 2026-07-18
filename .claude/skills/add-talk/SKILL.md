---
name: add-talk
description: >-
  Add a new talk, keynote, podcast, panel, or radio/media appearance to the Talks &
  Media page (/talk/) of this Hugo site. Use when the user asks to add a talk or
  presentation, record a new speaking engagement or interview, or update the talks
  page. Handles link research (video/slides/event page), page-bundle scaffolding with
  correct chronological numbering, optional transcript embedding, and the
  research/talks.json ledger.
---

# Add a talk to the Talks & Media page

The section lives in `content/talk/` — one page bundle per item
(`content/talk/<slug>/index.md`), listed reverse-chronologically by `date` with a
"#N" chip (`talk_number` = chronological rank, 1 = oldest). `research/talks.json` is
the research **ledger** (keyed by `slug`; its `n` is append order, *not* the site
number). `research/<slug>.summary.txt` holds a one-line AI summary when a transcript
exists. Layouts are site-level (`layouts/section/talk.html`, `layouts/talk/single.html`,
partials) — you should not need to touch them to add content.

Background and past decisions (including which talks are known but unreachable):
`research/PROCESS.md`.

## Engine

```bash
T=".claude/skills/add-talk/scripts/talks.py"   # stdlib-only; run from repo root
python3 $T validate     # pages <-> ledger consistency, numbering, transcript flags
python3 $T scaffold ... # create bundle + ledger entry, auto-number, renumber others
python3 $T renumber     # recompute talk_number after any date edits
python3 $T linkcheck    # verify all outbound links (YouTube via oEmbed)
```

## Workflow

1. **Gather facts.** Title, event, type, date (whatever precision is known), location,
   and any links the user already has. Valid types (drive badge colors):
   `Talk`, `Invited Talk`, `Keynote`, `Colloquium`, `Seminar`, `Lecture`, `Tutorial`,
   `Panel`, `Plenary`, `Podcast`, `Radio`, `Interview`. Also pick one or more **topics**
   for the list-page filter — vocabulary: `astronomy`, `industry`, `ai-ml`, `education`
   (most talks get 2; e.g. an astro-ML colloquium is `astronomy,ai-ml`). For the filter's
   Type row, types fold into six buckets in `talk_filter_type.html`: Invited Talk /
   Plenary / Colloquium / Seminar count as Talk; Lecture and Tutorial share one bucket;
   Interview counts as Radio.

2. **Research the links.** Look for (a) video — YouTube/venue archive/institute site;
   (b) slides — Speaker Deck, SlideShare, venue page; (c) an event page; (d) for radio
   and podcasts, **direct audio** (`url_audio` → the Listen button) and an **external
   transcript** (`url_transcript`). Verify each link actually resolves; for YouTube use
   oEmbed (`https://www.youtube.com/oembed?url=<video-url>` — the watch page returns
   200 even for deleted videos). If media is known to exist but can't be found or is
   paywalled, still add the talk with whatever links exist and record the situation in
   the ledger `notes` — and append it to the "known but not linkable" list in
   `research/PROCESS.md` so nobody re-hunts it later.

   Audio-source recipes that worked:
   - **NPR:** the story page HTML contains the direct MP3 — `curl -sL <story-url> |
     grep -oE 'https://ondemand\.npr\.org[^"&?]*\.mp3'`; the transcript lives at
     `https://www.npr.org/transcripts/<storyId>` (the number in the story URL).
   - **Podcasts:** grep the episode page for `.mp3` (many embed the enclosure URL);
     otherwise resolve the show's RSS via the iTunes API
     (`https://itunes.apple.com/lookup?id=<podcastId>` → `feedUrl`, or
     `.../search?term=<show>&entity=podcast`) and take the episode's `<enclosure>`.
     Beware: feeds often truncate to recent episodes — old episodes may be gone from
     every directory (that's how the 2019 Masters of Data episode was lost).

3. **Scaffold** (from the repo root, on a branch — see step 6):

   ```bash
   python3 $T scaffold --slug pydata-global-2026 \
     --title "The Talk Title" --date 2026-03-14 --type "Invited Talk" \
     --event "PyData Global 2026" --location "Online" \
     --topics "industry,ai-ml" \
     --video "https://www.youtube.com/watch?v=..." \
     --slides "https://speakerdeck.com/..." --event-url "https://..." \
     --audio "https://.../episode.mp3" --transcript-url "https://.../transcripts/..." \
     --summary "One-to-two sentence summary for the card." \
     --notes "provenance/uncertainty notes for the ledger"
   ```

   Link rendering rules: a YouTube or Vimeo `url_video` **auto-embeds a player** on the
   talk's page (other hosts just get the Video button); `url_audio` renders a Listen
   button; `url_transcript` renders an external Transcript button only when the page has
   no embedded transcript (`has_transcript: false`).

   - Slug: short memorable kebab-case, usually `<venue>-<year>` (`iaifi-2025`,
     `npr-science-friday-2011`).
   - Date conventions are automatic: pass `YYYY-MM-DD`, `YYYY-MM` (stored as day 15),
     or `YYYY` (stored as `YYYY-07-01`); `display_date` hides the false precision.
   - Numbering is automatic, **including inserting an older talk** — every later page
     gets renumbered. Never hand-edit `talk_number`; if you change a `date` later, run
     `renumber`.

4. **Transcript (when a recording exists).** Pull auto-captions (e.g.
   `yt-dlp --write-auto-subs --skip-download`), clean them into readable prose
   paragraphs with speaker labels where clear, then append to the page body:

   ```markdown
   ## Transcript

   *Auto-generated captions; may contain transcription errors.*

   <the transcript>
   ```

   Set `has_transcript: true` in the front matter (validate enforces the pairing) and
   write a one-line distilled summary to `research/<slug>.summary.txt`.

5. **Verify.** `python3 $T validate && python3 $T linkcheck`. Both must be clean
   (linkcheck "WALLED" entries are acceptable if noted in the ledger).

6. **Preview + ship.** Local Hugo is too new for this theme (pinned 0.60 — see
   CLAUDE.md), so don't fight local builds: commit on a branch, push, open a PR, and
   check the **Netlify deploy preview**. Merging to `master` deploys the live site.
