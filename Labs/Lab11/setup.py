"""
Lab 11: Streamlit UI — Setup
=============================
Run this script from your CISC395 workspace root AFTER completing Lab 10.

Usage (from CISC395/ root):
    python Labs/Lab11/setup.py

OR download and run in one line:

    Bash / Git Bash:
        mkdir -p Labs/Lab11 && curl -o Labs/Lab11/setup.py https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab11/setup.py && python Labs/Lab11/setup.py

    Windows PowerShell:
        New-Item -ItemType Directory -Force -Path Labs\\Lab11; Invoke-WebRequest -Uri https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab11/setup.py -OutFile Labs\\Lab11\\setup.py; python Labs\\Lab11\\setup.py
"""

import os
import sys
import urllib.request

BASE_URL   = "https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab11/"
SHARED_URL = "https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/shared/"
ZIP_URL    = "https://github.com/tisage/CISC395/archive/refs/heads/main.zip"


def download_file(url, dest):
    """Download a file and verify it is not empty or an HTML error page."""
    try:
        urllib.request.urlretrieve(url, dest)
    except Exception as e:
        return False, str(e)

    if os.path.getsize(dest) == 0:
        os.remove(dest)
        return False, "empty file (server returned nothing)"

    try:
        with open(dest, "r", errors="ignore") as f:
            first = f.read(80).lstrip()
        if first.startswith("<"):
            os.remove(dest)
            return False, "blocked by network (received HTML instead of file)"
    except Exception:
        pass

    return True, None


DOWNLOADS = [
    ("prompts/Lab11_Ex01_shell.md",  "prompts/Lab11_Ex01_shell.md"),
    ("prompts/Lab11_Ex02_chat.md",   "prompts/Lab11_Ex02_chat.md"),
    ("prompts/Lab11_Ex03_search.md", "prompts/Lab11_Ex03_search.md"),
    ("prompts/Lab11_Ex04_agent.md",  "prompts/Lab11_Ex04_agent.md"),
]

SHARED_DOWNLOADS = [
    ("check_progress.py", "tests/check_progress.py"),
]


def check_location():
    cwd = os.getcwd()
    if os.path.basename(cwd) in ("Lab11", "Labs"):
        print("WARNING: Run this from your CISC395 workspace root, not from inside Labs/.")
        print(f"  Current directory: {cwd}")
        print("  Try: cd ../.." if os.path.basename(cwd) == "Lab11" else "  Try: cd ..")
        print("  Then: python Labs/Lab11/setup.py")
        sys.exit(1)


def setup():
    check_location()

    root = "trip_notes"
    if not os.path.exists(root):
        print("ERROR: trip_notes/ not found.")
        print("Complete Lab 07 first to create the project, then run this setup.")
        sys.exit(1)

    if not os.path.exists(os.path.join(root, "src", "tools.py")):
        print("WARNING: src/tools.py not found — Lab 10 may not be complete.")
        print("You can continue but complete Lab 10 exercises first.")
        print()

    print("Setting up Lab 11 in trip_notes/...")
    print()

    for d in ["prompts", "tests"]:
        os.makedirs(os.path.join(root, d), exist_ok=True)

    print("Downloading...")
    failed = []
    all_downloads = [(BASE_URL + r, l) for r, l in DOWNLOADS] + \
                    [(SHARED_URL + r, l) for r, l in SHARED_DOWNLOADS]

    for url, local in all_downloads:
        dest = os.path.join(root, local)
        ok, reason = download_file(url, dest)
        if ok:
            print(f"  \u2713  trip_notes/{local}")
        else:
            print(f"  \u2717  trip_notes/{local}  ({reason})")
            failed.append(local)

    print()
    if failed:
        print(f"  {len(failed)} file(s) failed to download:")
        for f in failed:
            print(f"    - trip_notes/{f}")
        print()
        print("  Fix: Download the ZIP and copy the missing files manually:")
        print(f"    {ZIP_URL}")
        print()

    print("Done! Lab 11 files ready in trip_notes/.")
    print()
    print("Next steps:")
    print("  1. pip install streamlit")
    print("  2. python tests/check_progress.py --lab 11")
    print("  3. Follow Lab 11 exercises in order")
    print("  4. Run: streamlit run src/app.py")


def refresh():
    root = "trip_notes"
    if not os.path.exists(root):
        print("trip_notes/ not found. Run without --refresh first.")
        sys.exit(1)
    print("Refreshing Lab 11 files...")
    all_downloads = [(BASE_URL + r, l) for r, l in DOWNLOADS] + \
                    [(SHARED_URL + r, l) for r, l in SHARED_DOWNLOADS]
    for url, local in all_downloads:
        dest = os.path.join(root, local)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        ok, reason = download_file(url, dest)
        if ok:
            print(f"  \u2713  trip_notes/{local}")
        else:
            print(f"  \u2717  {local}  ({reason})")


if __name__ == "__main__":
    if "--refresh" in sys.argv:
        check_location()
        refresh()
    else:
        setup()
