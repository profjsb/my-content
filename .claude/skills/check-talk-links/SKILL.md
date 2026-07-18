---
name: check-talk-links
description: >-
  Check every outbound link on the Talks & Media page (/talk/) for link rot — dead
  videos, moved event pages, paywalled or permission-walled slides — and repair what's
  fixable, falling back to Wayback Machine snapshots. Use when the user asks to check,
  verify, audit, or fix talk/media links, or as periodic maintenance (worth running a
  couple of times a year).
---

# Check & repair Talks & Media links

Runs against the front matter of every `content/talk/*/index.md`
(`url_video`, `url_slides`, `url_audio`, `url_transcript`, `event_url`; audio is
checked with HEAD so MP3s aren't downloaded). The engine lives in the companion skill:

```bash
python3 .claude/skills/add-talk/scripts/talks.py linkcheck
```

## Interpreting results

- **`DEAD` (404/410/timeouts)** — real rot; needs repair.
- **`WALLED` (401/403)** — ambiguous: could be a paywall (O'Reilly), a permissioned
  file (Google Drive), or just bot-blocking of curl (some `*.berkeley.edu` sites).
  **Verify in a real browser before replacing** — a link that works for humans stays.
- YouTube is checked via **oEmbed**, because deleted/private videos still return
  HTTP 200 on the watch page. An oEmbed 4xx means the video is really gone.

## Repair procedure (per dead link)

1. **Look for the moved original first**: site search on the host (BIDS, venue,
   podcast platform), the speaker's other platforms, or an alternate store/region for
   podcast episodes. For podcast audio, resolve the show's current RSS via the iTunes
   API (`itunes.apple.com/lookup?id=<podcastId>` or `/search?term=<show>&entity=podcast`)
   and take the episode `<enclosure>` — but note feeds truncate, so old episodes may be
   gone from every directory. A live original beats an archive copy.
2. **Fall back to the Wayback Machine**: check
   `https://web.archive.org/web/<original-url>` and link a **dated snapshot**
   (`https://web.archive.org/web/<timestamp>/<original-url>`) that actually renders the
   content. Video/audio players usually do *not* survive archiving — for those, prefer
   dropping the link over linking a broken snapshot.
3. **If nothing works**, remove the link, keep the entry, and record what was lost in
   the ledger (`research/talks.json` `notes`) and in the "known but not linkable"
   section of `research/PROCESS.md`. When replacing a URL, also preserve the old one in
   `notes` (`"original <url> dead as of <date>"`).

## After repairs

1. `python3 .claude/skills/add-talk/scripts/talks.py validate` — must be clean.
2. Re-run `linkcheck`; confirm only understood `WALLED` entries remain.
3. Update the **"Link health"** table and its date stamp in `research/PROCESS.md`
   (that table is the historical record — note newly-dead and newly-repaired links).
4. Commit on a branch and open a PR (merging `master` deploys via Netlify; the deploy
   preview is the place to click through repaired links).
