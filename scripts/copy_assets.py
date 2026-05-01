"""
Copy usable assets from assets-raw/ into site/assets/ with clean filenames.
Skips all Squarespace CSS/JS bundles and unconfirmed AdobeStock images.
Run from the project root: python scripts/copy_assets.py
"""

import shutil
from pathlib import Path

ROOT = Path(".")
HOME = ROOT / "assets-raw/Sparks Occupational Therapy_files"
TEAM = ROOT / "assets-raw/Team 1 — Sparks Occupational Therapy_files"

COPIES = [
    # Logo
    (HOME / "Sparks_OT_Logo_Horizontal_Invert-for-Dark-Bkgd.png", "site/assets/logo/logo.png"),
    # Photos — Korrie portrait
    (HOME / "Korrie+Picture.jpg",       "site/assets/photos/korrie-portrait.jpg"),
    # Photos — clinic interiors / nature
    (HOME / "Entrance.JPEG",            "site/assets/photos/clinic-entrance.jpg"),
    (HOME / "Nest.jpeg",                "site/assets/photos/clinic-nest-1.jpg"),
    (HOME / "Nest+2.JPEG",              "site/assets/photos/clinic-nest-2.jpg"),
    (HOME / "Star.JPEG",                "site/assets/photos/clinic-star.jpg"),
    (HOME / "River.JPEG",               "site/assets/photos/nature-river.jpg"),
    (HOME / "Forest.JPEG",              "site/assets/photos/nature-1.jpg"),
    (HOME / "Forest+2.JPEG",            "site/assets/photos/nature-2.jpg"),
    (HOME / "Forest+3.jpg",             "site/assets/photos/nature-3.jpg"),
    # Mystery PNG — inspect before publishing
    (HOME / "C5D0A5B5-4BC2-418D-BAB7-F550E4C87FEA.PNG", "site/assets/photos/unknown-1.png"),
    # Team headshots (assignments tentative — verify against actual persons)
    (HOME / "Korrie+Picture.jpg",                                   "site/assets/team/korrie.jpg"),
    (TEAM / "Profesh-1-glasses.png",                                "site/assets/team/korrie-alt.png"),
    (TEAM / "E9733F73-0644-4F86-9178-2295AC1EDA52_1_102_a.jpeg",   "site/assets/team/julia.jpg"),
    (TEAM / "8F70BF9F-A954-4D72-A37C-5420E585AF4E.jpg",            "site/assets/team/anna.jpg"),
    (TEAM / "backpacking.jpg",                                      "site/assets/team/devin.jpg"),
    (TEAM / "Koko1.jpeg",                                           "site/assets/team/darcy.jpg"),
]

ADOBE_STOCK_SKIPPED = [
    "AdobeStock_166321257.jpeg",
    "AdobeStock_213790983.jpeg",
    "AdobeStock_267587702.jpeg",
]


def main():
    ok, missing = 0, 0
    for src, dst in COPIES:
        src, dst = Path(src), Path(dst)
        if not src.exists():
            print(f"  MISSING  {src}")
            missing += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  copied   {src.name} -> {dst}")
        ok += 1

    print(f"\n{ok} files copied, {missing} missing.")
    print("\n⚠️  AdobeStock images SKIPPED — license not confirmed for self-hosting:")
    for f in ADOBE_STOCK_SKIPPED:
        print(f"     ✗ {f}")
    print("   Confirm with client before adding these to the site.")


if __name__ == "__main__":
    main()
