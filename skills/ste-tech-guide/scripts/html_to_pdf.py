#!/usr/bin/env python3
"""Print an HTML page to PDF with headless Chrome, Edge or Chromium.

Usage:
    python html_to_pdf.py page.html [out.pdf]

The page's own @page / @media print CSS controls the paper size and the page breaks.
The browser header and footer (date, URL, page numbers) are turned off.
Set BROWSER_PATH to use a specific browser binary.
"""

import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

MAX_PAGES = 5  # length budget for one guide, see SKILL.md


def find_browser() -> str:
    env = os.environ.get("BROWSER_PATH")
    if env and Path(env).exists():
        return env

    system = platform.system()
    candidates = []
    if system == "Windows":
        for base in (os.environ.get("PROGRAMFILES(X86)"), os.environ.get("PROGRAMFILES"), os.environ.get("LOCALAPPDATA")):
            if base:
                candidates += [
                    Path(base) / "Google/Chrome/Application/chrome.exe",
                    Path(base) / "Microsoft/Edge/Application/msedge.exe",
                ]
    elif system == "Darwin":
        candidates += [
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
            Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
        ]
    for path in candidates:
        if path.exists():
            return str(path)

    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "msedge", "chrome"):
        found = shutil.which(name)
        if found:
            return found

    sys.exit("No Chrome, Edge or Chromium found. Set BROWSER_PATH to the browser binary.")


def wait_for_file(path: Path, started: float, timeout: float = 60.0) -> None:
    """Wait until the PDF exists, is newer than the start time, and its size is stable.

    Some browsers (Edge on Windows) return before they finish writing the file.
    """
    deadline = time.time() + timeout
    last_size = -1
    while time.time() < deadline:
        if path.exists() and path.stat().st_mtime >= started - 1:
            size = path.stat().st_size
            if size > 0 and size == last_size:
                return
            last_size = size
        time.sleep(0.5)
    sys.exit(f"The browser did not write {path} within {timeout:.0f} seconds.")


def count_pages(pdf: Path) -> int:
    data = pdf.read_bytes()
    return len(re.findall(rb"/Type\s*/Page(?!s)", data))


def main() -> None:
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)

    html = Path(sys.argv[1]).resolve()
    if not html.exists():
        sys.exit(f"File not found: {html}")
    out = Path(sys.argv[2]).resolve() if len(sys.argv) == 3 else html.with_suffix(".pdf")

    browser = find_browser()
    started = time.time()
    # A separate profile makes the browser run as its own process, so it does not hand
    # the job to a browser window that is already open.
    profile = tempfile.mkdtemp(prefix="html_to_pdf_")
    try:
        subprocess.run(
            [
                browser,
                "--headless=new",
                "--disable-gpu",
                "--no-first-run",
                "--no-pdf-header-footer",
                f"--user-data-dir={profile}",
                f"--print-to-pdf={out}",
                html.as_uri(),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=120,
        )
        wait_for_file(out, started)
    finally:
        # The browser can keep log files open for a short time after it exits.
        shutil.rmtree(profile, ignore_errors=True)

    pages = count_pages(out)
    print(f"PDF: {out}")
    print(f"Pages: {pages}")
    print(f"Size: {out.stat().st_size // 1024} KB")
    if pages > MAX_PAGES:
        print(f"Warning: {pages} pages is more than the budget of about {MAX_PAGES}. "
              "Cut the text (see 'Length budget' in SKILL.md), or split the guide.")


if __name__ == "__main__":
    main()
