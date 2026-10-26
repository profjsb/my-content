# AGENTS.md
## Overview
Personal academic website for Joshua Bloom ([https://joshbloom.org](https://joshbloom.org)), built with Hugo and the Academic theme v4.7.0 (git submodule at `themes/academic`). Deployed on Netlify per `netlify.toml`; pushing to `master` publishes the site.
## Critical: Hugo version
This theme predates modern Hugo and **does not build with current Hugo releases** (fails with template errors such as `can't evaluate field GoogleAnalytics`). Netlify builds with Hugo **0.60.0**, pinned in `netlify.toml`. For local builds/preview, use a similarly old Hugo binary — do not attempt to patch the theme to satisfy a newer Hugo, and do not bump `HUGO_VERSION` (only `update_academic.sh` should, when the theme itself is updated).
## Conventions
- Real config lives in `config/_default/`. The root `config.toml` is only a Blogdown/Forestry compatibility stub — don't edit it.
  
- To hide a homepage section (`content/home/*.md`), set `active = false` rather than deleting the file.
  
- Posts drafted as Jupyter notebooks are converted with `jupyter nbconvert index.ipynb --to markdown --NbConvertApp.output_files_dir=.` (Hugo ignores `.ipynb` files via `ignoreFiles`).
  
- Publications: use the `update-publications` skill. The older academic-admin import workflow and its journal-macro `sed` cleanups are recorded in the root-level `help` file.
## Design system
The whole site uses the warm-cream look first built for Talks & Media (Inter for UI and headings, Lora for prose, IBM Plex Mono for code and chips).
- Styles live in `assets/scss/bloom/`, imported from `assets/scss/custom.scss` (appended to the theme's SCSS bundle; libsass, so `@import` only). `_tokens.scss` holds every color and font as CSS custom properties, with the dark palette under `body.dark` (how Academic toggles dark mode). Use tokens rather than hex values.
- Reusable components are `.ui-*` classes in `_components.scss`: wrapper, page title, section label, card (head/meta/title), stream card, button and button row, pills and filter rows, chips, badges, search box, info card, note, prose, contents rail. New pages should compose these instead of adding page-specific CSS or inline `<style>`.
- Shared list items: `talk_card.html`, `pub_card.html` (with `pub_authors.html`), and `li_compact.html`, which renders talks and publications with those cards and everything else as a stream card.
- Site overrides of theme templates (they no longer track theme updates; re-check them if the theme is bumped): `_default/list.html`, `404.html`, `authors/list.html`, `section/post.html`, `section/publication.html` (+ `.json`), `publication/single.html`, `partials/li_compact.html`, `partials/custom_head.html`. Everything else (homepage widgets, article pages, navbar, footer, search overlay) is restyled with CSS only.
- `data/themes/bloom.toml` and `data/fonts/bloom.toml` feed the theme's own SCSS variables and Google Fonts link; the root font size is pinned to 16px in `_base.scss` (keep `font_size = "L"` in params).
