#!/usr/bin/env python3
"""
Content linter for ndp-transition-research-2026.

Scans all content markdown files for:
  - Frontmatter schema violations
  - Sensitive content patterns (private contact info, internal keywords)
  - File hygiene issues (naming convention, non-.md files in content folders)

Exit 0 = clean. Exit 1 = violations found.
"""

import os
import re
import sys

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

CONTENT_DIRS = re.compile(
    r'^(march|april|may|june|july|august|september|october|november|december)-\d+$'
    r'|^(speeches|stephen-lewis|transcript-archive)$'
)

VALID_TYPES = {"article", "speech", "transcript", "statement"}
VALID_LANGUAGES = {"en", "fr", "en-fr"}

REQUIRED_FIELDS = {
    "article":    {"title", "date", "source", "outlet", "language", "type"},
    "statement":  {"title", "date", "outlet", "language", "type"},
    "speech":     {"title", "date", "language", "type"},
    "transcript": {"title", "date", "source", "outlet", "language", "type", "speakers"},
}

DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
URL_RE  = re.compile(r'^https?://')
FILENAME_DATE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2}) \u2014 .+\.md$')

# Sensitive content patterns — checked against body text only
SENSITIVE_PATTERNS = [
    (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'), "email address"),
    (re.compile(r'\b(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b'), "phone number"),
    # Require specific sensitive compound phrases, not bare "internal" or "confidential"
    (re.compile(
        r'\b(internal memo|internal document|internal communication|internal strategy'
        r'|internal polling|internal survey|off the record|not for distribution|donor list'
        r'|private communication|unpublished)\b',
        re.IGNORECASE
    ), "sensitive keyword"),
]

# Files to skip in content dirs (non-content files that legitimately live there)
SKIP_FILENAMES = {"README.md"}
SKIP_EXTENSIONS = {".html", ".htm"}

# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def parse_frontmatter(text):
    """Return (frontmatter_dict, body) or (None, text) if no frontmatter."""
    if not text.startswith('---'):
        return None, text
    end = text.find('\n---', 3)
    if end == -1:
        return None, text
    fm_text = text[3:end].strip()
    body = text[end + 4:].strip()
    fm = {}
    for line in fm_text.splitlines():
        if ':' in line:
            key, _, val = line.partition(':')
            fm[key.strip()] = val.strip()
    return fm, body


def parse_speakers(text):
    """Check if a 'speakers:' block exists as a YAML list."""
    return bool(re.search(r'^speakers\s*:\s*\n(\s+-\s+\S)', text, re.MULTILINE))

# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_file(path, filename, violations):
    with open(path, encoding='utf-8') as f:
        raw = f.read()

    fm, body = parse_frontmatter(raw)

    # --- Filename convention ---
    if not FILENAME_DATE_RE.match(filename):
        violations.append(f"{path}: filename doesn't match YYYY-MM-DD \u2014 slug.md convention")

    if fm is None:
        violations.append(f"{path}: missing or malformed frontmatter")
        return

    # --- type ---
    ftype = fm.get('type', '').strip('"\'')
    if ftype not in VALID_TYPES:
        violations.append(f"{path}: invalid type '{ftype}' (must be one of {sorted(VALID_TYPES)})")
        return  # can't check required fields without a valid type

    # --- required fields ---
    for field in REQUIRED_FIELDS.get(ftype, set()):
        if field == 'speakers':
            if not parse_speakers(raw):
                violations.append(f"{path}: transcript missing 'speakers' list")
        elif field not in fm or not fm[field]:
            violations.append(f"{path}: missing required field '{field}'")

    # --- language ---
    lang = fm.get('language', '').strip('"\'')
    if lang and lang not in VALID_LANGUAGES:
        violations.append(f"{path}: invalid language '{lang}' (must be one of {sorted(VALID_LANGUAGES)})")

    # --- date format ---
    date_val = fm.get('date', '').strip('"\'')
    if date_val and not DATE_RE.match(date_val):
        violations.append(f"{path}: date '{date_val}' is not YYYY-MM-DD")

    # --- date matches filename ---
    m = FILENAME_DATE_RE.match(filename)
    if m and date_val and m.group(1) != date_val:
        violations.append(f"{path}: filename date {m.group(1)} doesn't match frontmatter date {date_val}")

    # --- source URL ---
    source = fm.get('source', '').strip('"\'')
    if source and not URL_RE.match(source):
        violations.append(f"{path}: source '{source}' is not a valid https:// URL")

    # --- stub field ---
    stub_raw = fm.get('stub', None)
    if stub_raw is not None:
        stub_val = stub_raw.strip('"\'').lower()
        if stub_val != 'true':
            violations.append(f"{path}: stub must be 'true' or omitted, got '{stub_raw}'")

    # --- sensitive content in body ---
    for pattern, label in SENSITIVE_PATTERNS:
        match = pattern.search(body)
        if match:
            snippet = match.group(0)[:60]
            violations.append(f"{path}: possible {label} in body — '{snippet}'")


def check_dir_for_non_md(dirpath, violations):
    for fname in os.listdir(dirpath):
        fpath = os.path.join(dirpath, fname)
        _, ext = os.path.splitext(fname)
        if os.path.isfile(fpath) and not fname.startswith('.') \
                and ext not in {'.md'} | SKIP_EXTENSIONS \
                and fname not in SKIP_FILENAMES:
            violations.append(f"{fpath}: unexpected file type '{ext}' in content folder")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    violations = []
    files_checked = 0

    for entry in os.listdir(repo_root):
        if not CONTENT_DIRS.match(entry):
            continue
        dirpath = os.path.join(repo_root, entry)
        if not os.path.isdir(dirpath):
            continue

        check_dir_for_non_md(dirpath, violations)

        for fname in os.listdir(dirpath):
            if not fname.endswith('.md'):
                continue
            if fname in SKIP_FILENAMES:
                continue
            fpath = os.path.join(dirpath, fname)
            check_file(fpath, fname, violations)
            files_checked += 1

    if violations:
        print(f"FAIL — {len(violations)} violation(s) across {files_checked} files:\n")
        for v in violations:
            print(f"  {v}")
        sys.exit(1)
    else:
        print(f"OK — {files_checked} files checked, no violations found.")
        sys.exit(0)


if __name__ == '__main__':
    main()
