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
