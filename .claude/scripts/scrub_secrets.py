"""Keep local test-account values (SITE/settings.local.md) out of files that git tracks.

settings.local.md is ignored by git and holds lines like:
    - TEST_USER_ID: 11112222
Tracked files use the placeholder {TEST_USER_ID} instead of the real value.

Usage:
    python3 scrub_secrets.py <SITE> [--check] [path ...]
Without paths it scrubs the tracked files of the site: settings.md, site-map.md,
testcases.xlsx, runs/Results/README.md, runs/Results/results.xlsx and runs/Results/json/.
A path may be a file or a folder (.md, .json, .csv, .html, .txt and .xlsx files inside it).
--check only reports where a real value is found and exits with 1 if any is found.
"""
import re
import sys
from pathlib import Path

TEXT = {".md", ".json", ".csv", ".html", ".txt"}


def load_secrets(site):
    f = site / "settings.local.md"
    if not f.exists():
        return {}
    pairs = re.findall(r"^[ \t]*-[ \t]*([A-Z][A-Z0-9_]*)[ \t]*:[ \t]*(\S.*?)[ \t]*$", f.read_text(encoding="utf-8"), re.M)
    return {k: v for k, v in pairs if len(v) >= 4}


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
        res = site / "runs" / "Results"
        paths = [site / "settings.md", site / "site-map.md", site / "testcases.xlsx",
                 res / "README.md", res / "results.xlsx", res / "json"]
    secrets = load_secrets(site)
    if not secrets:
        print(f"no values in {site / 'settings.local.md'}; nothing to do")
        return
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
