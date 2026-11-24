"""Keep local test-account values (SITE/settings.local.md) out of files that git tracks.

settings.local.md is ignored by git and holds lines like:
    - TEST_USER_ID: 11112222
Tracked files use the placeholder {TEST_USER_ID} instead of the real value.

It also looks for card numbers (13 to 19 digits that pass the Luhn check) and for the values in settings.card.local.md
(CARD_NUMBER and CARD_EMAIL): they are replaced with {CARD_NUMBER} / {CARD_EMAIL}, and --check fails if any is found.

Usage:
    python3 scrub_secrets.py <SITE> [--check] [path ...]
Without paths it scrubs the tracked files of the site: settings.md, site-map.md,
testcases.xlsx, and README.md, results.xlsx and json/ of runs/Results/ and every runs/Results_*/ folder.
A path may be a file or a folder (.md, .json, .csv, .html, .txt and .xlsx files inside it).
--check only reports where a real value is found and exits with 1 if any is found.
"""
import re
import sys
from pathlib import Path

TEXT = {".md", ".json", ".csv", ".html", ".txt"}
CARD_RE = re.compile(r"(?<![\d.])(?:\d[ -]?){12,18}\d(?!\d)")


def luhn(digits):
    total, flip = 0, False
    for ch in reversed(digits):
        d = int(ch)
        if flip:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        total += d
        flip = not flip
    return total % 10 == 0


def scrub_cards(text):
    """Replace every card-number-looking text (Luhn-valid, 13 to 19 digits) with {CARD_NUMBER}. Returns (new text, hits)."""
    hits = 0

    def sub(m):
        nonlocal hits
        digits = re.sub(r"\D", "", m.group(0))
        if 13 <= len(digits) <= 19 and luhn(digits):
            hits += 1
            return "{CARD_NUMBER}"
        return m.group(0)
    return CARD_RE.sub(sub, text), hits


def load_secrets(site):
    out = {}
    for name, only in (("settings.local.md", None), ("settings.card.local.md", {"CARD_NUMBER", "CARD_EMAIL"})):
        f = site / name
        if not f.exists():
            continue
        pairs = re.findall(r"^[ \t]*-[ \t]*([A-Z][A-Z0-9_]*)[ \t]*:[ \t]*(\S.*?)[ \t]*$", f.read_text(encoding="utf-8"), re.M)
        out.update({k: v for k, v in pairs if len(v) >= 4 and (only is None or k in only)})
    return out


def files_in(paths):
    for p in paths:
        if p.is_dir():
            yield from (f for f in sorted(p.rglob("*")) if f.suffix.lower() in TEXT | {".xlsx"})
        elif p.exists():
            yield p


def scrub(f, secrets, check):
    hits = 0
    if f.suffix.lower() == ".xlsx":
        from openpyxl import load_workbook
        wb = load_workbook(f)
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str):
                        new = cell.value
                        for k, v in secrets.items():
                            hits += new.count(v)
                            new = new.replace(v, "{" + k + "}")
                        new, n_cards = scrub_cards(new)
                        hits += n_cards
                        if new != cell.value and not check:
                            cell.value = new
        if hits and not check:
            try:
                wb.save(f)
            except PermissionError:
                print(f"FILE_OPEN {f}: close it in Excel and run again")
                return 0
    else:
        text = f.read_text(encoding="utf-8", errors="replace")
        new = text
        for k, v in secrets.items():
            hits += new.count(v)
            new = new.replace(v, "{" + k + "}")
        new, n_cards = scrub_cards(new)
        hits += n_cards
        if hits and not check:
            f.write_text(new, encoding="utf-8")
    return hits


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    site = Path(args.pop(0))
    check = "--check" in args
    paths = [Path(a) for a in args if a != "--check"]
    if not paths:
        paths = [site / "settings.md", site / "site-map.md", site / "testcases.xlsx"]
        for res in sorted((site / "runs").glob("Results*")):
            if res.is_dir():
                paths += [res / "README.md", res / "results.xlsx", res / "json"]
    secrets = load_secrets(site)
    total = 0
    for f in files_in(paths):
        n = scrub(f, secrets, check)
        if n:
            print(f"{'found' if check else 'scrubbed'} {n}x in {f}")
            total += n
    print(f"{'found' if check else 'scrubbed'} {total} in total")
    if check and total:
        sys.exit(1)


if __name__ == "__main__":
    main()
