#!/usr/bin/env python3
"""Quick STE (ASD-STE100) check of the text in an HTML guide.

Usage:
    python ste_check.py page.html

Reports:
  - sentences that are too long (20 words in procedure steps, 25 in other text)
  - likely passive voice
  - words that have a simpler STE-style replacement

Text in <code>, <pre>, <style> and <script> is ignored, because technical names stay as they are.
This is a helper, not a full STE checker. Decide on each item.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PROCEDURE_LIMIT = 20
DESCRIPTIVE_LIMIT = 25

WORD_SWAPS = {
    r"\bensur(e|es|ed|ing)\b": "make sure",
    r"\butili[sz](e|es|ed|ing)\b": "use",
    r"\bleverag(e|es|ed|ing)\b": "use",
    r"\bperform(s|ed|ing)?\b": "do / run",
    r"\bobtain(s|ed|ing)?\b": "get",
    r"\bretriev(e|es|ed|ing)\b": "get",
    r"\bcommenc(e|es|ed|ing)\b": "start",
    r"\binitiat(e|es|ed|ing)\b": "start",
    r"\bterminat(e|es|ed|ing)\b": "stop",
    r"\bprior to\b": "before",
    r"\bsubsequent(ly)?\b": "next / after",
    r"\bin order to\b": "to",
    r"\bdue to\b": "because of",
    r"\bapproximately\b": "about",
    r"\bvia\b": "through / with",
    r"\ballow(s|ed|ing)?\b": "let / make it possible",
    r"\benabl(e|es|ed|ing)\b": "let / make it possible",
    r"\bshould\b": "imperative or 'must'",
    r"\be\.g\.": "for example",
    r"\bi\.e\.": "that is",
    r"\betc\.": "list the items",
    r"\b(simply|just|easily|obviously|basically)\b": "delete the word",
    r"\bin case of\b": "if",
    r"\bis able to\b": "can",
    r"\b(might|may|probably)\b": "'can', or state the condition (if X, then Y)",
    r"\ba number of\b": "some / many",
}

PASSIVE = re.compile(r"\b(is|are|was|were|be|been|being)\s+(\w+ly\s+)?(\w+ed|made|done|sent|set|kept|put|run|built|written|given|shown|taken|found)\b", re.I)


class TextBlocks(HTMLParser):
    """Collect text per block element, and note if the block is a procedure step."""

    BLOCKS = {"p", "li", "td", "th", "h1", "h2", "h3", "div"}
    SKIP = {"code", "pre", "style", "script"}

    def __init__(self) -> None:
        super().__init__()
        self.blocks: list[tuple[str, bool]] = []
        self.buf: list[str] = []
        self.skip_depth = 0
        self.in_steps = 0
        self.stack: list[str] = []

    def _flush(self) -> None:
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if text:
            self.blocks.append((text, self.in_steps > 0))
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1
            self.buf.append(" X ")  # keep the code as one word in the sentence
            return
        if tag == "ol" and "steps" in (dict(attrs).get("class") or ""):
            self.in_steps += 1
        if tag in self.BLOCKS:
            self._flush()
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if tag in self.BLOCKS:
            self._flush()
        if tag == "ol" and self.in_steps:
            self.in_steps -= 1

    def handle_data(self, data):
        if not self.skip_depth:
            self.buf.append(data)


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", text)
    return [p.strip() for p in parts if p.strip()]


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    parser = TextBlocks()
    parser.feed(Path(sys.argv[1]).read_text(encoding="utf-8"))
    parser._flush()

    long_items, passive_items, word_items = [], [], []
    seen = set()
    for block, is_step in parser.blocks:
        for s in sentences(block):
            if s in seen:
                continue
            seen.add(s)
            words = len(re.findall(r"[\w'’/-]+", s))
            limit = PROCEDURE_LIMIT if is_step else DESCRIPTIVE_LIMIT
            if words > limit:
                long_items.append(f"[{words} words > {limit}{', step' if is_step else ''}] {s}")
            m = PASSIVE.search(s)
            if m:
                passive_items.append(f"'{m.group(0)}' in: {s}")
            for pattern, swap in WORD_SWAPS.items():
                w = re.search(pattern, s, re.I)
                if w:
                    word_items.append(f"'{w.group(0)}' -> {swap}  in: {s}")

    def report(title, items):
        print(f"\n== {title}: {len(items)}")
        for item in items:
            print(f"  - {item}")

    report("Long sentences", long_items)
    report("Possible passive voice", passive_items)
    report("Words to replace", word_items)
    total = len(long_items) + len(word_items)
    print(f"\n{total} item(s) to fix, {len(passive_items)} passive item(s) to review.")


if __name__ == "__main__":
    main()
