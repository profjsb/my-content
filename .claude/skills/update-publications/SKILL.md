---
name: update-publications
description: >-
  Import or update the Hugo Academic publication list from an ADS "list of works"
  export (a LaTeX file of numbered \item entries, or an ADS BibTeX export). Use when
  the user asks to update/refresh/sync their publications, add papers from an ADS or
  BibTeX/LaTeX file, or reconcile content/publication/ against a citation list. Handles
  slug generation, Crossref/arXiv metadata enrichment, and page-bundle creation for this
  Hugo Academic site.
---

# Update publications from an ADS list of works

This repo's publications live in `content/publication/<slug>/` — one folder per paper,
each with `index.md` (front matter) and `cite.bib`. New papers are typically supplied as
an ADS **"list of works"** LaTeX file (numbered `\item` entries with ADS `\href` links) or
a BibTeX export. This skill adds the entries that are missing from the site.

## The one rule that matters most

**The folder slug must exactly match the `academic-admin` / python-slugify convention.**
A wrong slug does not error — it silently creates a **duplicate** page for a paper that is
already on the site. The bundled script's `ads_slug()` is verified to round-trip against
every existing folder; always run `verify` before generating, and never hand-edit slugs.

The convention has non-obvious rules (all load-bearing):
`A&A`→`aa`, `ARA&A`→`araa`, `Ap&SS`→`apss` (the `&` is deleted, not turned into a separator),
`NCimC`→`n-cim-c`, `arXiv`→`ar-xiv`, plus camelCase and letter/digit boundary splits.

## Workflow

The engine is `scripts/pubgen.py` (deps: `python-slugify`, `pyyaml`). Run each step and
**read the output before the next** — don't let it run unattended.

```bash
PY=python3   # or a venv that has python-slugify + pyyaml
SK=.claude/skills/update-publications/scripts/pubgen.py

# 1. VERIFY the slug convention still matches this repo (445+ entries). Must be clean.
$PY $SK verify --content content/publication

# 2. PLAN — show which bibcodes in the source are missing from the site (dry run).
$PY $SK plan --tex /path/to/list_of_works/main.tex --content content/publication

# 3. Work on a branch/worktree (this repo's convention; keep CLAUDE.md guidance in mind).
git worktree add ../my-content-pubs -b update-publications
#    Point --out at the WORKTREE's content dir, but --content at a full checkout so the
#    slug verify + "already present" diff see all existing folders (worktrees omit
#    untracked dirs).
$PY $SK generate --tex /path/to/main.tex \
     --content content/publication \
     --out ../my-content-pubs/content/publication \
     --enrich --mailto you@example.com \
     --stamp "$(date -u +%Y-%m-%dT00:00:00Z)"

# 4. VALIDATE: content only parses under the pinned Hugo (see CLAUDE.md). Use list-all,
#    which parses all front matter without hitting the theme's render-time error:
( cd ../my-content-pubs && hugo list all >/dev/null && echo "all front matter parsed" )

# 5. Review author lists, then commit the new bundles and open a PR.
```

## What the generator does (and its known limits)

- **Scope**: only `\item` entries between `\begin{document}` and `\end{document}` in the
  refereed section. Entries after `\end{document}` are decommissioned and skipped on purpose.
- **Enrichment** (`--enrich`): journal articles → Crossref, preprints → arXiv API. Every
  Crossref hit is validated by title-overlap **and** year **and** journal-name consistency,
  so a fuzzy search cannot attach the wrong paper's DOI/authors. Entries with no confident
  match fall back to the author list parsed from the `.tex` (an info line reports which).
- **`publication_types`**: journals → `2`, SPIE proceedings → `6` (emitted as `@inbook`),
  conference series (e.g. PESE) → `1`. Matches the existing entries' mapping.
- **Front matter**: the current block-YAML format (title, authors, date, publishDate,
  publication_types, abstract, publication, doi, optional arXiv `links`).
- **Never overwrites** an existing folder.

### Manual checks that caught real problems here

- **Crossref author quality is weak for old proceedings.** One SPIE entry came back with
  mangled names ("Al. Soderberg", a mis-attached "III" suffix). Audit the generated
  `authors:` lists for suffix tokens / odd initials; for a bad one, prefer the curated
  `.tex` authors (the generator's `force_tex_authors` set in `write_bundle`).
- **Look-alike slugs already on disk.** Some bibcodes slugify to a folder that already
  exists (e.g. `NCimC`, `Ap&SS`, `RMxAC`). `verify` + the "already present" diff handle
  this — but it's why you must run `verify` first and diff against a **full** checkout.
- **Owner name normalization.** `_norm_bloom()` collapses `J. S. Bloom` / `Josh S. Bloom`
  → `Joshua S. Bloom` for consistency. Change the surname/target if reusing elsewhere.

## Adapting to another Academic site

`ads_slug()` is generic. If `verify` reports mismatches on a different repo, the theme
version used a different importer — reconcile `ads_slug()` until `verify` is clean before
trusting any generated slug. Update `_norm_bloom()` for a different site owner, and confirm
the `publication_types` mapping against that repo's existing entries.
