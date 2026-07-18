#!/usr/bin/env python3
"""
pubgen.py — import/update Hugo Academic publications from an ADS LaTeX
"list of works" export (the kind produced from an ADS BibTeX export and
hand-maintained as a numbered \\item list, e.g. bloom_list_of_works/main.tex).

Pipeline: parse ADS bibcodes from the refereed section -> diff against existing
content/publication/ folders -> (optionally) enrich metadata from Crossref and
the arXiv API -> write standard page bundles (index.md + cite.bib).

Correctness safeguards baked in (learned the hard way):
  * The directory slug is reproduced with the EXACT academic-admin / python-slugify
    convention. `verify` round-trips it against every existing entry and refuses
    to proceed on any mismatch — a wrong slug silently creates DUPLICATE pages.
  * Only entries between \\begin{document} and \\end{document} are imported;
    items after \\end{document} are decommissioned and skipped.
  * Every Crossref match is validated by title-overlap + year + journal
    consistency, so a fuzzy search can't attach the wrong paper's DOI/authors.
  * Existing folders are never overwritten.

Usage:
  pubgen.py verify   --content content/publication
  pubgen.py plan     --tex main.tex --content content/publication
  pubgen.py generate --tex main.tex --content content/publication --out <dir> [--enrich] [--mailto you@example.com]

Dependencies: python-slugify, pyyaml  (pip install python-slugify pyyaml)
"""
import argparse, glob, html, json, os, re, sys, time, urllib.parse, urllib.request

try:
    from slugify import slugify as _pyslug
except ImportError:
    sys.exit("pip install python-slugify")
try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml")

FM_HEADER = "# Documentation: https://sourcethemes.com/academic/docs/managing-content/"

# ---------------------------------------------------------------------------
# Slug: reproduce the academic-admin (python-slugify) folder-naming convention.
# Verified to round-trip against all existing entries via `verify`. Do not
# "simplify" this without re-running verify — the ampersand and camelCase rules
# are load-bearing (A&A->aa, ARA&A->araa, NCimC->n-cim-c, arXiv->ar-xiv).
# ---------------------------------------------------------------------------
def ads_slug(bibcode):
    s = bibcode
    s = re.sub(r'(.)([A-Z][a-z]+)', r'\1-\2', s)   # camel: boundary before Xxx
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', s)   # camel: lower/digit -> Upper
    s = re.sub(r'([A-Za-z])([0-9])', r'\1-\2', s)   # letter -> digit
    s = re.sub(r'([0-9])([A-Za-z])', r'\1-\2', s)   # digit -> letter
    s = s.replace('&', '')                          # importer deletes '&' (joins sides)
    return _pyslug(s)

# ---------------------------------------------------------------------------
# Parsing the LaTeX list of works
# ---------------------------------------------------------------------------
LATEX_GREEK = {r'\delta':'δ',r'\Delta':'Δ',r'\alpha':'α',r'\beta':'β',r'\gamma':'γ',
    r'\Gamma':'Γ',r'\mu':'μ',r'\pi':'π',r'\sigma':'σ',r'\Sigma':'Σ',r'\lambda':'λ',
    r'\Lambda':'Λ',r'\nu':'ν',r'\tau':'τ',r'\theta':'θ',r'\rho':'ρ',r'\phi':'φ',
    r'\chi':'χ',r'\omega':'ω',r'\Omega':'Ω',r'\epsilon':'ε',r'\eta':'η',r'\kappa':'κ',
    r'\zeta':'ζ',r'\odot':'⊙'}
SUFFIX = {'III','II','IV','V','Jr','Jr.','Sr','Sr.'}

def _clean(t):
    t = t.replace('\\\\', '').replace('~', ' ')
    t = re.sub(r'\{\\(bf|em|it)\s*', '', t)
    t = re.sub(r'\\textcolor\{black\}\{', '', t)
    return re.sub(r'\s+', ' ', t.replace('{', '').replace('}', '')).strip()

def clean_title(t):
    for k, v in LATEX_GREEK.items():
        t = t.replace(k + ' ', v).replace(k, v)
    t = t.replace('$', '').replace('\\&', '&').replace('~', ' ')
    t = re.sub(r'\\[a-zA-Z]+', '', t).replace('{', '').replace('}', '')
    return re.sub(r'\s+', ' ', t).strip()

def _brace_match(s, i):
    depth = 0
    for j in range(i, len(s)):
        if s[j] == '{': depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0: return j
    return -1

def parse_tex(tex_path):
    """Return list of dicts: code, slug, title, authors_raw, journal, vol, page, year."""
    raw = open(tex_path, encoding='utf-8', errors='replace').read()
    if r'\end{document}' in raw:
        raw = raw[:raw.index(r'\end{document}')]        # respect document boundary
    m = re.search(r'\\section\s*\{?[^}]*Refereed', raw)
    body = raw[m.start():] if m else raw
    recs = []
    for it in re.split(r'\n\s*\\item\s', body):
        mm = re.search(r'adsabs\.harvard\.edu/abs/([^}]+)\}', it)
        if not mm:
            continue
        code = mm.group(1).strip()
        if code == '%R':
            continue
        tm = re.search(r'\{\\em', it)
        if not tm:
            continue
        ti = tm.start(); tclose = _brace_match(it, ti)
        title = _clean(it[ti + 4:tclose])
        authors_raw = _clean(it[:ti])
        rest = it[tclose + 1:]
        jm = re.search(r'\{\\bf', rest)
        journal = vol = page = year = ''
        if jm:
            ji = jm.start(); jclose = _brace_match(rest, ji)
            journal = _clean(rest[ji + 4:jclose])
            after = rest[jclose + 1:]
            vpy = re.search(r'([0-9A-Za-z]+)\s*,\s*([A-Za-z0-9.]+)\s*\((\d{4})\)', after)
            if vpy:
                vol, page, year = vpy.groups()
            else:
                ym = re.search(r'\((\d{4})\)', after)
                year = ym.group(1) if ym else ''
        recs.append(dict(code=code, slug=ads_slug(code), title=title,
                         authors_raw=authors_raw, journal=journal,
                         vol=vol, page=page, year=year, enriched=False))
    return recs

def existing_dirs(content_dir):
    return {os.path.basename(os.path.dirname(p))
            for p in glob.glob(os.path.join(content_dir, '*', 'cite.bib'))} | \
           {d for d in os.listdir(content_dir) if os.path.isdir(os.path.join(content_dir, d))}

# ---------------------------------------------------------------------------
# verify: prove the slug convention still matches this repo before trusting it
# ---------------------------------------------------------------------------
def cmd_verify(content_dir):
    miss = []
    n = 0
    for bib in glob.glob(os.path.join(content_dir, '*', 'cite.bib')):
        d = os.path.basename(os.path.dirname(bib))
        m = re.search(r'@\w+\{([^,]+),', open(bib, encoding='utf-8', errors='replace').read())
        if not m:
            continue
        n += 1
        if ads_slug(m.group(1)) != d:
            miss.append((m.group(1), d, ads_slug(m.group(1))))
    print(f"slug round-trip: checked {n} entries, {len(miss)} mismatches")
    for k, d, g in miss[:30]:
        print(f"  MISMATCH bibcode={k} dir={d} got={g}")
    if miss:
        print("\nRefusing to trust ads_slug(): the folder-naming convention in this "
              "repo differs from the built-in one. Fix ads_slug() until this is clean.")
        return 1
    print("OK — ads_slug() reproduces every existing folder name. Safe to generate.")
    return 0

# ---------------------------------------------------------------------------
# Enrichment (Crossref + arXiv) with match validation
# ---------------------------------------------------------------------------
def _http(url, mailto, tries=4, timeout=45):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': f'pubgen/1.0 (mailto:{mailto})'})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            last = e; time.sleep(2)
    raise last

def _strip_jats(a):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', a or ''))).strip()

def _toks(s):
    return set(re.findall(r'[a-z0-9]+', (s or '').lower()))

def _stem(code):
    m = re.match(r'^\d{4}([A-Za-z&]+?)[.\d]', code)
    return m.group(1) if m else '?'

def _container_ok(code, cont, doi=''):
    s = _stem(code); c = (cont or '').lower(); doi = doi or ''
    if s == 'SPIE':  return ('spie' in c) or doi.startswith('10.1117') or 'space telescopes' in c or 'instrumentation' in c or 'ground-based' in c
    if s == 'NatAs': return 'nature astronomy' in c
    if s == 'Natur': return c.strip() == 'nature'
    if s == 'ApJS':  return 'astrophysical journal' in c and 'suppl' in c
    if s == 'ApJ':   return 'astrophysical journal' in c and 'suppl' not in c
    if s == 'A&A':   return 'astronomy' in c and 'astrophysics' in c
    if s == 'MNRAS': return 'monthly notices' in c
    if s == 'PASP':  return 'astronomical society of the pacific' in c
    if s == 'PASJ':  return 'astronomical society of japan' in c
    if s == 'AJ':    return c in ('the astronomical journal', 'astronomical journal')
    return None  # unknown journal -> no container gate

def _arxiv_id(code):
    m = re.match(r'\d{4}arXiv(\d{3,4}\.?\d+)[A-Z]?$', code)
    if not m:
        return None
    s = m.group(1)
    if '.' not in s and len(s) >= 9:
        s = s[:4] + '.' + s[4:]
    return s

def _take_crossref(rec, item):
    names = [((a.get('given', '') + ' ' + a.get('family', '')).strip() or a.get('name', '').strip())
             for a in item.get('author', [])]
    if names:
        rec['authors'] = names
    rec['doi'] = item.get('DOI', '')
    rec['container'] = (item.get('container-title') or [''])[0]
    for k in ('published-print', 'published-online', 'issued', 'published'):
        dp = item.get(k, {}).get('date-parts', [[None]])[0]
        if len(dp) >= 2 and dp[1]:
            rec['month'] = f"{dp[1]:02d}"; break
    rec['abstract'] = _strip_jats(item.get('abstract', ''))
    rec['enriched'] = 'crossref'

def enrich(rec, mailto):
    aid = _arxiv_id(rec['code'])
    try:
        if aid:
            x = _http(f"http://export.arxiv.org/api/query?id_list={aid}&max_results=1", mailto)
            au = re.findall(r'<author>\s*<name>([^<]+)</name>', x)
            ab = re.search(r'<entry>.*?<summary>(.*?)</summary>', x, re.S)
            pub = re.search(r'<published>(\d{4})-(\d{2})', x)
            doi = re.search(r'<arxiv:doi[^>]*>([^<]+)</arxiv:doi>', x)
            if au:
                rec['authors'] = [a.strip() for a in au]; rec['enriched'] = 'arxiv'; rec['arxiv'] = aid
            if ab: rec['abstract'] = _strip_jats(ab.group(1))
            if pub: rec['month'] = pub.group(2)
            if doi: rec['doi'] = doi.group(1).strip()
            return
        q = urllib.parse.urlencode({'query.bibliographic': rec['title'], 'rows': '10', 'mailto': mailto})
        items = json.loads(_http(f"https://api.crossref.org/works?{q}", mailto))['message']['items']
        want = _toks(rec['title']); best = None; bs = -1
        for it in items:
            yr = None
            for k in ('published-print', 'published-online', 'issued', 'published'):
                dp = it.get(k, {}).get('date-parts', [[None]])[0]
                if dp and dp[0]: yr = dp[0]; break
            if not (yr and rec['year'] and abs(int(yr) - int(rec['year'])) <= 1):
                continue
            ct = (it.get('container-title') or [''])[0]
            if _container_ok(rec['code'], ct, it.get('DOI', '')) is False:
                continue
            sc = len(want & _toks(' '.join(it.get('title') or [])))
            if sc > bs:
                best, bs = it, sc
        if best and bs >= 4:
            _take_crossref(rec, best)
    except Exception as e:
        rec['err'] = str(e)[:120]

# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------
def _norm_bloom(name):
    # normalise the site owner's name; adjust the surname/target for other repos
    if re.search(r'\bBloom\b', name) and re.search(r'\bJ', name):
        return 'Joshua S. Bloom'
    return name

def _parse_tex_authors(raw):
    s = raw.replace(' and ', ', ')
    s = re.sub(r"\\['\"`^~]", '', s)
    s = re.sub(r'[{}]', '', s)
    toks = [t.strip() for t in re.split(r',\s*', s) if t.strip()]
    bare = {x.rstrip('.') for x in SUFFIX}
    toks = [t for t in toks if t not in SUFFIX and t not in bare]
    out, i = [], 0
    while i < len(toks):
        given = toks[i + 1] if i + 1 < len(toks) else ''
        out.append(_norm_bloom((given + ' ' + toks[i]).strip()))
        i += 2
    return [a for a in out if a]

def _pub_type(code):
    if re.match(r'^\d{4}SPIE', code): return '6'   # book section
    if 'pese' in code: return '1'                   # conference series
    return '2'                                       # journal article

def _pub_display(rec):
    if re.match(r'^\d{4}arXiv', rec['code']):
        return 'arXiv e-prints'
    return rec['journal'].replace('ArXiv e-prints', 'arXiv e-prints').strip()

def _spie_vol(code):
    m = re.search(r'SPIE\.?(\d+)', code)
    return m.group(1) if m else ''

def _bibtex(rec, authors, title, journal, ptype):
    entry = '@inbook' if ptype == '6' else '@article'
    lines = [f'{entry}{{{rec["code"]},',
             '    author = {' + ' and '.join(authors) + '},',
             '    title = {{' + title + '}},']
    lines.append(('    booktitle = {' if ptype == '6' else '    journal = {') + journal + '},')
    lines.append(f"    year = {{{rec['year']}}},")
    vol = rec.get('vol') or (_spie_vol(rec['code']) if ptype == '6' else '')
    if vol: lines.append(f'    volume = {{{vol}}},')
    if rec.get('page'): lines.append(f"    pages = {{{rec['page']}}},")
    if rec.get('doi'): lines.append(f"    doi = {{{rec['doi']}}},")
    if rec.get('arxiv'):
        lines.append(f"    eprint = {{{rec['arxiv']}}},")
        lines.append('    archivePrefix = {arXiv},')
    return '\n'.join(lines) + '\n}\n'

def write_bundle(rec, out_dir, stamp, force_tex_authors=()):
    title = clean_title(rec['title'])
    if rec['enriched'] and rec['code'] not in force_tex_authors:
        authors = [_norm_bloom(a) for a in rec.get('authors', [])]
    else:
        authors = _parse_tex_authors(rec['authors_raw'])
    authors = [a for a in authors if a]
    ptype = _pub_type(rec['code'])
    journal = _pub_display(rec)
    date = f"{rec['year']}-{(rec.get('month') or '01')}-01"

    fm = {'title': title, 'subtitle': '', 'summary': '', 'authors': authors,
          'tags': [], 'categories': [], 'date': date, 'lastmod': stamp,
          'featured': False, 'draft': False,
          'image': {'caption': '', 'focal_point': '', 'preview_only': False},
          'projects': [], 'publishDate': stamp, 'publication_types': [ptype],
          'abstract': rec.get('abstract', '') or '', 'publication': f'*{journal}*'}
    if rec.get('doi') and not re.match(r'^\d{4}arXiv', rec['code']):
        fm['doi'] = rec['doi']
    if rec.get('arxiv'):
        fm['links'] = [{'name': 'arXiv', 'url': f"https://arxiv.org/abs/{rec['arxiv']}"}]

    body = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=88, default_flow_style=False)
    d = os.path.join(out_dir, rec['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.md'), 'w', encoding='utf-8').write("---\n" + FM_HEADER + "\n\n" + body + "---\n")
    open(os.path.join(d, 'cite.bib'), 'w', encoding='utf-8').write(_bibtex(rec, authors, title, journal, ptype))

def cmd_plan(tex, content_dir):
    recs = parse_tex(tex)
    have = existing_dirs(content_dir)
    missing = [r for r in recs if r['slug'] not in have]
    print(f"{len(recs)} refereed entries in {os.path.basename(tex)}; "
          f"{len(recs) - len(missing)} already present; {len(missing)} missing:")
    for r in missing:
        print(f"  {r['code']:22} -> {r['slug']:30} {r['year']}  {r['title'][:48]}")
    return missing

def cmd_generate(tex, content_dir, out_dir, do_enrich, mailto, stamp):
    if cmd_verify(content_dir) != 0:
        return 1
    missing = cmd_plan(tex, content_dir)
    have = existing_dirs(content_dir)
    # guard: never target a slug that already exists
    missing = [r for r in missing if r['slug'] not in have]
    if not missing:
        print("nothing to generate.")
        return 0
    if do_enrich:
        print(f"\nenriching {len(missing)} entries via Crossref/arXiv ...")
        for i, r in enumerate(missing, 1):
            enrich(r, mailto)
            print(f"  [{i}/{len(missing)}] {r['code']:22} {r['enriched'] or 'TEX-FALLBACK'}")
            time.sleep(0.34)
    print(f"\nwriting bundles to {out_dir}/ ...")
    for r in missing:
        write_bundle(r, out_dir, stamp)
    ok = sum(1 for r in missing if r['enriched'])
    print(f"wrote {len(missing)} bundles ({ok} enriched, {len(missing) - ok} tex-fallback).")
    print("\nNext: run `hugo list all` to confirm every new front matter parses, "
          "then review author lists before committing.")
    return 0

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('verify', help='prove ads_slug() matches every existing folder')
    v.add_argument('--content', default='content/publication')
    p = sub.add_parser('plan', help='list bibcodes present in the .tex but missing from the site')
    p.add_argument('--tex', required=True); p.add_argument('--content', default='content/publication')
    g = sub.add_parser('generate', help='write index.md + cite.bib bundles for missing entries')
    g.add_argument('--tex', required=True)
    g.add_argument('--content', default='content/publication')
    g.add_argument('--out', default='content/publication')
    g.add_argument('--enrich', action='store_true', help='fetch authors/DOI/abstract from Crossref & arXiv')
    g.add_argument('--mailto', default='anonymous@example.com', help='contact email for the Crossref polite pool')
    g.add_argument('--stamp', default='1970-01-01T00:00:00Z', help='ISO timestamp for publishDate/lastmod')
    a = ap.parse_args()
    if a.cmd == 'verify':
        sys.exit(cmd_verify(a.content))
    if a.cmd == 'plan':
        cmd_plan(a.tex, a.content); sys.exit(0)
    if a.cmd == 'generate':
        sys.exit(cmd_generate(a.tex, a.content, a.out, a.enrich, a.mailto, a.stamp))

if __name__ == '__main__':
    main()
