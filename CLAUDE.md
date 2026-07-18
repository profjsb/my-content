# CLAUDE.md
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
## Overview
Personal academic website for Joshua Bloom ([https://joshbloom.org](https://joshbloom.org)), built with Hugo and the Academic theme v4.7.0, vendored as a git submodule at `themes/academic` (run `git submodule update --init` after a fresh clone). Deployed on Netlify per `netlify.toml`; pushing to `master` publishes the site.
## Critical: Hugo version
This theme predates modern Hugo and **does not build with current Hugo releases** (fails with template errors such as `can't evaluate field GoogleAnalytics`). Netlify builds with Hugo **0.60.0**, pinned in `netlify.toml`. For local builds/preview, use a similarly old Hugo binary — do not attempt to patch the theme to satisfy a newer Hugo, and do not bump `HUGO_VERSION` (only `update_academic.sh` should, when the theme itself is updated).
## Commands
- `./view.sh` — local dev server (`hugo --i18n-warnings server`, serves at localhost:1313)
  
- `hugo --gc --minify` — production build (what Netlify runs); output goes to `public/` (gitignored)
  
- `bash ./update_academic.sh` — check for/apply theme submodule updates and re-pin `HUGO_VERSION` in `netlify.toml`
  
## Architecture
- **Config** lives in `config/_default/` (`config.toml` = site basics, `params.toml` = theme options, `menus.toml` = nav). The root `config.toml` is only a Blogdown/Forestry compatibility stub — don't edit it.
  
- **Homepage** is assembled from widget sections in `content/home/*.md`. Each file declares `widget`, `active`, and `weight` (display order). To hide a section, set `active = false` rather than deleting the file.
  
- **Posts** in `content/post/`: newer posts are page bundles (`<slug>/index.md` plus images in the same folder); older ones are single `.md` files. Posts drafted as Jupyter notebooks are converted with `jupyter nbconvert index.ipynb --to markdown --NbConvertApp.output_files_dir=.` (Hugo ignores `.ipynb` files via `ignoreFiles`).
  
- **Publications** in `content/publication/<slug>/`: ~450 entries, one folder per paper containing `index.md` (front matter: `authors`, `date`, `publication_types`, `publication` = journal name) and `cite.bib`. Slugs derive from ADS bibcodes.
  
- **Author profile** in `content/authors/josh/_index.md` (bio shown by the about widget).
  
## Publications import workflow
The `help` file at the repo root records the established workflow (the root-level `*.bib` files are its inputs/outputs):

1. Export BibTeX from ADS, filtering with a query like `author:("Bloom, Joshua Simon") AND -bibstem:(...)` to exclude circulars/abstracts.
  
2. Import with the [academic-admin](https://github.com/sourcethemes/academic-admin) CLI: `academic import --overwrite --bibtex <file>.bib`
  
3. Clean up the generated markdown with the `sed` one-liners in `help`: expand journal macros (`*apj*` → `*Astrophysical Journal*`, `*mnras*` → `*Monthly Notices of the Royal Astronomical Society*`, etc.), strip `~` and `ensuremath`.
