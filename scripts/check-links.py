#!/usr/bin/env python3
"""
Link rot checker for ndp-transition-research-2026.

Extracts all source: URLs from content file frontmatter and checks
whether they resolve. Distinguishes dead links (404, timeout) from
paywalled/blocked links (403, 401) which are expected and non-fatal.

Exit 0 = all links live (or expected paywalls).
Exit 1 = dead links found.
"""

import os
import re
import sys
import time
import urllib.request
import urllib.error

CONTENT_DIRS = re.compile(
    r'^(march|april|may|june|july|august|september|october|november|december)-\d+$'
    r'|^(speeches|stephen-lewis)$'
)

SOURCE_RE = re.compile(r'^source\s*:\s*["\']?(https?://[^\s"\']+)', re.MULTILINE)

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (compatible; ndp-research-linkchecker/1.0; '
        '+https://github.com/barrettsoron/ndp-transition-research-2026)'
    )
}

REQUEST_DELAY = 0.5  # seconds between requests


def check_url(url):
    """
    Returns (status, category) where category is:
      'ok'       — 2xx/3xx, link is live
      'paywall'  — 401/403/429, expected block, non-fatal
      'dead'     — 404/410, link is gone
      'error'    — timeout or connection failure
    """
    for method in ('HEAD', 'GET'):
        try:
            req = urllib.request.Request(url, headers=HEADERS, method=method)
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status, 'ok'
        except urllib.error.HTTPError as e:
            if e.code in (405,) and method == 'HEAD':
                continue  # retry with GET
            if e.code in (401, 403, 429):
                return e.code, 'paywall'
            if e.code in (404, 410):
                return e.code, 'dead'
            return e.code, 'error'
        except urllib.error.URLError:
            return 0, 'error'
        except Exception:
            return 0, 'error'
    return 0, 'error'


def collect_sources(repo_root):
    """Return list of (filepath, url) for all source: fields in content files."""
    sources = []
    for entry in os.listdir(repo_root):
        if not CONTENT_DIRS.match(entry):
            continue
        dirpath = os.path.join(repo_root, entry)
        if not os.path.isdir(dirpath):
            continue
        for fname in os.listdir(dirpath):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(dirpath, fname)
            with open(fpath, encoding='utf-8') as f:
                text = f.read()
            # Only scan frontmatter (between first --- markers)
            if text.startswith('---'):
                end = text.find('\n---', 3)
                fm = text[:end] if end != -1 else text
            else:
                continue
            for m in SOURCE_RE.finditer(fm):
                sources.append((fpath, m.group(1)))
    return sources


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sources = collect_sources(repo_root)

    dead = []
    paywalls = []
    ok_count = 0

    print(f"Checking {len(sources)} source URLs...\n")

    for fpath, url in sources:
        time.sleep(REQUEST_DELAY)
        status, category = check_url(url)
        rel = os.path.relpath(fpath, repo_root)

        if category == 'ok':
            ok_count += 1
        elif category == 'paywall':
            paywalls.append((rel, url, status))
            print(f"  PAYWALL [{status}] {rel}\n           {url}")
        elif category == 'dead':
            dead.append((rel, url, status))
            print(f"  DEAD    [{status}] {rel}\n           {url}")
        else:
            dead.append((rel, url, status))
            print(f"  ERROR   [{status}] {rel}\n           {url}")

    print(f"\n{ok_count} ok  |  {len(paywalls)} paywalled (non-fatal)  |  {len(dead)} dead/error")

    if dead:
        print(f"\nFAIL — {len(dead)} dead link(s) found.")
        sys.exit(1)
    else:
        print("\nOK — no dead links.")
        sys.exit(0)


if __name__ == '__main__':
    main()
