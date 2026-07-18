#!/usr/bin/env python3
"""Maintenance engine for the Talks & Media section (content/talk/ + research/talks.json).

Subcommands:
  validate    check pages <-> talks.json consistency, numbering, dates, transcripts
  sync-slugs  backfill/refresh the "slug" field in talks.json by matching pages
  renumber    recompute talk_number = chronological rank across all pages
  scaffold    create a new talk page bundle + talks.json entry (auto-numbering)
  linkcheck   verify all outbound links (YouTube via oEmbed); reports rot

Stdlib-only. Run from the repo (or worktree) root:  python3 .claude/skills/add-talk/scripts/talks.py <cmd>
"""
import argparse
import calendar
import glob
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

CONTENT = "content/talk"
TALKS_JSON = "research/talks.json"

REQUIRED_FIELDS = ["title", "date", "event", "summary", "talk_type", "talk_number", "display_date"]
FIELD_ORDER = ["title", "date", "publishDate", "draft", "event", "event_url", "location",
               "summary", "talk_type", "talk_number", "display_date", "url_video",
               "url_slides", "url_audio", "url_transcript", "has_transcript"]


# ---------- front matter ----------

def parse_page(path):
    lines = open(path).read().split("\n")
    if lines[0] != "---":
        raise SystemExit(f"{path}: no front matter")
    end = lines[1:].index("---") + 1
    fm = {}
    for ln in lines[1:end]:
        m = re.match(r'^(\w+):\s*(.*)$', ln)
        if m:
            k, v = m.group(1), m.group(2).strip()
            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1]
            fm[k] = v
    body = "\n".join(lines[end + 1:])
    return fm, body


def pages():
    out = {}
    for p in sorted(glob.glob(f"{CONTENT}/*/index.md")):
        slug = p.split("/")[-2]
        fm, body = parse_page(p)
        out[slug] = (p, fm, body)
    return out


def load_json():
    return json.load(open(TALKS_JSON))


def save_json(data):
    with open(TALKS_JSON, "w") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# ---------- date conventions ----------

def normalize_date(d):
    """YYYY -> YYYY-07-01, YYYY-MM -> YYYY-MM-15, YYYY-MM-DD -> unchanged.
    Returns (full_date, display_date)."""
    if re.fullmatch(r"\d{4}", d):
        return f"{d}-07-01", d
    if re.fullmatch(r"\d{4}-\d{2}", d):
        y, m = d.split("-")
        return f"{d}-15", f"{calendar.month_abbr[int(m)]} {y}"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        y, m, _ = d.split("-")
        return d, f"{calendar.month_abbr[int(m)]} {y}"
    raise SystemExit(f"bad date {d!r} (want YYYY, YYYY-MM, or YYYY-MM-DD)")


# ---------- validate ----------

def rank_key(fm, slug, is_new=False):
    return (fm["date"], 1 if is_new else 0, int(fm.get("talk_number", 10 ** 6)), slug)


def cmd_validate(_args):
    errs, warns = [], []
    pg = pages()
    for slug, (p, fm, body) in pg.items():
        for f in REQUIRED_FIELDS:
            if f not in fm:
                errs.append(f"{p}: missing {f}")
        if "date" in fm and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fm["date"]):
            errs.append(f"{p}: date {fm['date']!r} not YYYY-MM-DD")
        dd = fm.get("display_date", "")
        if dd and not re.fullmatch(r"([A-Z][a-z]{2} )?\d{4}", dd):
            warns.append(f"{p}: display_date {dd!r} not 'Mon YYYY' or 'YYYY'")
        if fm.get("has_transcript") == "true" and "## Transcript" not in body:
            errs.append(f"{p}: has_transcript true but no '## Transcript' section")
        if fm.get("has_transcript") != "true" and "## Transcript" in body:
            errs.append(f"{p}: transcript present but has_transcript is not true")
        if not any(fm.get(k) for k in ("url_video", "url_slides", "event_url")):
            warns.append(f"{p}: no links at all (known-unreachable item?)")
    # numbering = chronological rank
    order = sorted(pg.items(), key=lambda kv: rank_key(kv[1][1], kv[0]))
    for want, (slug, (p, fm, _)) in enumerate(order, 1):
        got = int(fm.get("talk_number", -1))
        if got != want:
            errs.append(f"{p}: talk_number {got}, chronological rank is {want} (run renumber)")
    # ledger
    data = load_json()
    if len(data) != len(pg):
        errs.append(f"talks.json has {len(data)} entries, {len(pg)} pages exist")
    slugs = [t.get("slug") for t in data]
    for t in data:
        if not t.get("slug"):
            errs.append(f"talks.json n={t['n']}: no slug (run sync-slugs)")
        elif t["slug"] not in pg:
            errs.append(f"talks.json n={t['n']}: slug {t['slug']!r} has no page")
    dupes = {s for s in slugs if s and slugs.count(s) > 1}
    if dupes:
        errs.append(f"talks.json duplicate slugs: {dupes}")
    for e in errs:
        print(f"ERROR: {e}")
    for w in warns:
        print(f"warn:  {w}")
    print(f"\n{len(pg)} pages, {len(data)} ledger entries — {len(errs)} errors, {len(warns)} warnings")
    return 1 if errs else 0


# ---------- sync-slugs ----------

def norm_title(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def json_ym(d):
    return f"{d}-07"[:7] if re.fullmatch(r"\d{4}", d) else d[:7]


def cmd_sync_slugs(_args):
    pg = pages()
    by_key = {}
    for slug, (p, fm, _) in pg.items():
        by_key.setdefault((norm_title(fm["title"]), fm["date"][:7]), []).append(slug)
    by_title = {}
    for slug, (p, fm, _) in pg.items():
        by_title.setdefault(norm_title(fm["title"]), []).append(slug)
    data = load_json()
    unmatched = []
    for t in data:
        key = (norm_title(t["title"]), json_ym(t["date"]))
        cands = by_key.get(key) or (by_title.get(norm_title(t["title"]))
                                    if len(by_title.get(norm_title(t["title"]), [])) == 1 else None)
        if not cands or len(cands) != 1:
            unmatched.append((t["n"], t["title"], cands))
            continue
        t2 = {"n": t["n"], "slug": cands[0]}
        t2.update({k: v for k, v in t.items() if k not in ("n", "slug")})
        t.clear()
        t.update(t2)
    if unmatched:
        for n, title, c in unmatched:
            print(f"UNMATCHED n={n}: {title!r} candidates={c}")
        raise SystemExit("aborted — fix matches by hand (add slug to those entries), then rerun")
    save_json(data)
    print(f"slugs written for all {len(data)} entries")
    return 0


# ---------- renumber ----------

def apply_renumber(pg, quiet=False):
    order = sorted(pg.items(), key=lambda kv: rank_key(kv[1][1], kv[0]))
    changed = 0
    for want, (slug, (p, fm, _)) in enumerate(order, 1):
        if int(fm.get("talk_number", -1)) != want:
            src = open(p).read()
            src = re.sub(r"^talk_number: .*$", f"talk_number: {want}", src, count=1, flags=re.M)
            open(p, "w").write(src)
            if not quiet:
                print(f"{slug}: {fm.get('talk_number')} -> {want}")
            changed += 1
    return changed


def cmd_renumber(_args):
    n = apply_renumber(pages())
    print(f"{n} pages renumbered" if n else "numbering already correct")
    return 0


# ---------- scaffold ----------

def yq(s):
    return '"' + s.replace('"', '\\"') + '"'


def cmd_scaffold(args):
    slug = args.slug
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        raise SystemExit("slug must be kebab-case (lowercase alphanumerics and dashes)")
    path = f"{CONTENT}/{slug}/index.md"
    if os.path.exists(path):
        raise SystemExit(f"{path} already exists")
    date, display = normalize_date(args.date)
    fm = {
        "title": yq(args.title), "date": date, "publishDate": date, "draft": "false",
        "event": yq(args.event),
        "event_url": yq(args.event_url) if args.event_url else None,
        "location": yq(args.location) if args.location else None,
        "summary": yq(args.summary or ""), "talk_type": yq(args.type),
        "talk_number": "0", "display_date": yq(display),
        "url_video": yq(args.video) if args.video else None,
        "url_slides": yq(args.slides) if args.slides else None,
        "url_audio": yq(args.audio) if args.audio else None,
        "url_transcript": yq(args.transcript_url) if args.transcript_url else None,
        "has_transcript": "false",
    }
    os.makedirs(f"{CONTENT}/{slug}", exist_ok=True)
    lines = ["---"] + [f"{k}: {fm[k]}" for k in FIELD_ORDER if fm.get(k) is not None] + ["---", ""]
    body = (args.summary or "") + "\n"
    open(path, "w").write("\n".join(lines) + "\n" + body)

    data = load_json()
    entry = {"n": max(t["n"] for t in data) + 1, "slug": slug, "title": args.title,
             "event": args.event, "type": args.type, "date": args.date,
             "location": args.location or None, "video_url": args.video or None,
             "slides_url": args.slides or None, "event_url": args.event_url or None,
             "audio_url": args.audio or None, "transcript_url": args.transcript_url or None,
             "summary": args.summary or "", "notes": args.notes or ""}
    data.append(entry)
    save_json(data)

    apply_renumber(pages(), quiet=True)
    _, newfm, _ = pages()[slug]
    print(f"created {path} (talk #{newfm['talk_number']}) and talks.json entry n={entry['n']}")
    print("next: add transcript ('## Transcript' + auto-caption disclaimer, set "
          f"has_transcript: true) and research/{slug}.summary.txt if a recording exists; "
          "then run validate + linkcheck")
    return 0


# ---------- linkcheck ----------

def check_url(url, is_audio=False):
    m = re.search(r"youtube\.com/(?:live|embed|shorts)/([A-Za-z0-9_-]+)", url)
    if m:  # normalize /live/, /embed/, /shorts/ forms so oEmbed accepts them
        url = "https://www.youtube.com/watch?v=" + m.group(1)
    if "youtube.com/watch" in url or "youtu.be/" in url:
        import urllib.parse
        o = "https://www.youtube.com/oembed?url=" + urllib.parse.quote(url, safe="")
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                            "--max-time", "15", o], capture_output=True, text=True)
        return r.stdout.strip() or "000", "yt-oembed"
    if is_audio or url.split("?")[0].endswith((".mp3", ".m4a", ".ogg")):
        # HEAD so we don't download the media; take the final status after redirects
        r = subprocess.run(["curl", "-sIL", "-o", "/dev/null", "-w", "%{http_code}",
                            "--max-time", "20", "-A",
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", url],
                           capture_output=True, text=True)
        return r.stdout.strip() or "000", "head"
    r = subprocess.run(["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}",
                        "--max-time", "20", "-A",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", url],
                       capture_output=True, text=True)
    return r.stdout.strip() or "000", "get"


def cmd_linkcheck(_args):
    jobs = []
    for slug, (p, fm, _) in pages().items():
        for key in ("url_video", "url_slides", "url_audio", "url_transcript", "event_url"):
            if fm.get(key):
                jobs.append((slug, key, fm[key]))
    def run(j):
        slug, key, url = j
        code, how = check_url(url, is_audio=(key == "url_audio"))
        return slug, key, url, code, how
    dead, walled, ok = [], [], 0
    with ThreadPoolExecutor(max_workers=12) as ex:
        for slug, key, url, code, how in ex.map(run, jobs):
            c = int(code) if code.isdigit() else 0
            if c in (401, 403):
                walled.append((slug, key, url, code))
            elif c >= 400 or c == 0:
                dead.append((slug, key, url, code))
            else:
                ok += 1
    for slug, key, url, code in dead:
        print(f"DEAD   {code} {slug} {key} {url}")
    for slug, key, url, code in walled:
        print(f"WALLED {code} {slug} {key} {url}  (paywall or bot-block — verify in browser)")
    print(f"\n{ok} ok, {len(walled)} walled, {len(dead)} dead of {len(jobs)} links")
    return 1 if dead else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    sub.add_parser("sync-slugs")
    sub.add_parser("renumber")
    sub.add_parser("linkcheck")
    sc = sub.add_parser("scaffold")
    sc.add_argument("--slug", required=True)
    sc.add_argument("--title", required=True)
    sc.add_argument("--date", required=True, help="YYYY, YYYY-MM, or YYYY-MM-DD")
    sc.add_argument("--type", required=True,
                    help="Talk/Invited Talk/Keynote/Colloquium/Seminar/Lecture/Tutorial/"
                         "Panel/Plenary/Podcast/Radio/Interview")
    sc.add_argument("--event", required=True)
    sc.add_argument("--location")
    sc.add_argument("--event-url", dest="event_url")
    sc.add_argument("--video")
    sc.add_argument("--slides")
    sc.add_argument("--audio", help="direct audio URL (mp3) — rendered as a Listen button")
    sc.add_argument("--transcript-url", dest="transcript_url",
                    help="external transcript page (e.g. npr.org/transcripts/<id>); "
                         "shown only when there is no embedded transcript")
    sc.add_argument("--summary")
    sc.add_argument("--notes")
    args = ap.parse_args()
    fn = {"validate": cmd_validate, "sync-slugs": cmd_sync_slugs, "renumber": cmd_renumber,
          "scaffold": cmd_scaffold, "linkcheck": cmd_linkcheck}[args.cmd]
    sys.exit(fn(args))


if __name__ == "__main__":
    main()
