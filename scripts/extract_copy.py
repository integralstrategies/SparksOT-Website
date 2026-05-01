"""
Extract page copy from Squarespace-exported HTML files into clean JSON.
Run from the project root:  python scripts/extract_copy.py
Output: scripts/copy.json
"""

import json
import re
from pathlib import Path
from html.parser import HTMLParser


ASSETS_RAW = Path("assets-raw")

PAGES = {
    "home": ASSETS_RAW / "Sparks Occupational Therapy.html",
    "team": ASSETS_RAW / "Team 1 — Sparks Occupational Therapy.html",
    "contact": ASSETS_RAW / "Contact — Sparks Occupational Therapy.html",
}


class TextExtractor(HTMLParser):
    """Walk the DOM and collect visible text, skipping script/style tags."""

    SKIP_TAGS = {"script", "style", "noscript", "head"}

    def __init__(self):
        super().__init__()
        self._skip_depth = 0
        self._current_tag = None
        self.chunks: list[dict] = []
        self._buf = ""
        self._tag_stack: list[str] = []

    def handle_starttag(self, tag, attrs):
        self._tag_stack.append(tag)
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        self._flush()
        if self._tag_stack and self._tag_stack[-1] == tag:
            self._tag_stack.pop()
        if tag in self.SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data):
        if self._skip_depth:
            return
        text = data.strip()
        if text:
            self._buf += (" " if self._buf else "") + text

    def _flush(self):
        text = self._buf.strip()
        if text:
            self.chunks.append({
                "tag": self._tag_stack[-1] if self._tag_stack else "?",
                "text": re.sub(r"\s+", " ", text),
            })
        self._buf = ""


def extract_page(path: Path) -> list[dict]:
    html = path.read_text(encoding="utf-8", errors="replace")
    parser = TextExtractor()
    parser.feed(html)
    # Deduplicate adjacent identical chunks
    seen: list[dict] = []
    for chunk in parser.chunks:
        if not seen or seen[-1]["text"] != chunk["text"]:
            seen.append(chunk)
    return seen


def main():
    output: dict[str, list[dict]] = {}
    for page, path in PAGES.items():
        if not path.exists():
            print(f"WARN: {path} not found, skipping")
            continue
        chunks = extract_page(path)
        output[page] = chunks
        print(f"{page}: {len(chunks)} text chunks extracted")

    out_path = Path("scripts/copy.json")
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
