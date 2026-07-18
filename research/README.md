# Talks & Media research data (July 2026)
- `talks.json` — canonical structured list of 45 talks/media appearances gathered from
  YouTube, Vimeo, conference sites (Strata, KDD, SciPy, PyData), institute archives
  (Simons Institute/Foundation, IPAM, IAIFI/MIT, LBNL), SlideShare, Speaker Deck,
  NPR, and the Wayback Machine. Each entry carries a `slug` linking it to its
  `content/talk/<slug>/` page bundle (`n` is append order, not the site's number).
- `*.summary.txt` — AI-generated per-talk summaries derived from talk transcripts.
- `PROCESS.md` — build retrospective: how this page was made, what went well/badly,
  which talks are known but not linkable, and link-health history.
- Full transcripts are embedded in each `content/talk/<slug>/index.md` page.
- This folder is not published by Hugo (only content/, static/, assets/ are).
- To add or maintain entries, use the `add-talk` and `check-talk-links` skills
  (`.claude/skills/`).
