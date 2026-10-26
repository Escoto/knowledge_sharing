#!/usr/bin/env python3
"""Quick STE (ASD-STE100) and length check of an HTML guide.

Usage:
    python ste_check.py page.html

Reports:
  - sentences that are too long (20 words in procedure steps, 25 in other text)
  - likely passive voice
  - words that have a simpler STE-style replacement
  - a length report per section (words, code block lines, diagram steps, procedure steps,
    panels), checked against the length budget in SKILL.md

Text in <code>, <pre>, <style> and <script> is not checked for STE, because technical names stay
as they are. HTML comments are ignored. This is a helper, not a full STE checker. Decide on each item.
"""

import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

PROCEDURE_LIMIT = 20
DESCRIPTIVE_LIMIT = 25

# Length budget (see "Length budget" in SKILL.md)
GUIDE_WORDS_MAX = 900
SECTION_WORDS_MAX = 250
CODE_LINES_MAX = 15
FLOW_STEPS_MAX = 5
PROCEDURE_STEPS_MAX = 8
PANELS_PER_SECTION_MAX = 2
WORDS_PER_MINUTE = 200

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
WORD = re.compile(r"[\w'’/-]+")


@dataclass
class Section:
    title: str
    words: int = 0
    code_blocks: list = field(default_factory=list)  # line count of each code block
    flow_steps: int = 0
    procedure_steps: int = 0
    panels: int = 0


class GuideParser(HTMLParser):
    """Collect text per block element, and size data per section (h2)."""

    BLOCKS = {"p", "li", "td", "th", "h1", "h2", "h3", "div"}
    SKIP = {"code", "pre", "style", "script"}

    def __init__(self) -> None:
        super().__init__()
        self.blocks: list[tuple[str, bool]] = []
        self.sections: list[Section] = [Section("(header)")]
        self.buf: list[str] = []
        self.skip_depth = 0
        self.ol_stack: list[bool] = []  # True for an <ol class="steps">
        self.in_h2 = False
        self.h2_buf: list[str] = []
        self.in_pre = False
        self.pre_spans = 0
        self.pre_text: list[str] = []

    @property
    def section(self) -> Section:
        return self.sections[-1]

    @property
    def in_steps(self) -> bool:
        return any(self.ol_stack)

    def _flush(self) -> None:
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if text:
            self.blocks.append((text, self.in_steps))
            self.section.words += len(WORD.findall(text))
        self.buf = []

    def handle_starttag(self, tag, attrs):
        classes = (dict(attrs).get("class") or "").split()
        if tag == "pre":
            self.in_pre, self.pre_spans, self.pre_text = True, 0, []
        if self.in_pre and tag == "span" and "ln" in classes:
            self.pre_spans += 1
        if tag in self.SKIP:
            self.skip_depth += 1
            if self.skip_depth == 1 and not self.in_h2:
                self.buf.append(" X ")  # inline code counts as one word in the sentence
            return
        if self.skip_depth:
            return
        if tag == "h2":
            self._flush()
            self.in_h2, self.h2_buf = True, []
        if tag == "ol":
            self.ol_stack.append("steps" in classes)
        if tag == "li" and self.ol_stack and self.ol_stack[-1]:
            self.section.procedure_steps += 1
        if tag == "div" and "flow-node" in classes:
            self.section.flow_steps += 1
        if tag == "div" and "panel" in classes:
            self.section.panels += 1
        if tag in self.BLOCKS and tag != "h2":
            self._flush()

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip_depth = max(0, self.skip_depth - 1)
            if tag == "pre" and self.in_pre:
                lines = self.pre_spans or len("".join(self.pre_text).strip("\n").splitlines())
                self.section.code_blocks.append(lines)
                self.in_pre = False
            return
        if self.skip_depth:
            return
        if tag == "h2" and self.in_h2:
            title = re.sub(r"\s+", " ", "".join(self.h2_buf)).strip()
            self.in_h2 = False
            self.sections.append(Section(title))
            self.buf = list(self.h2_buf)
            self._flush()
            return
        if tag in self.BLOCKS:
            self._flush()
        if tag == "ol" and self.ol_stack:
            self.ol_stack.pop()

    def handle_data(self, data):
        if self.in_pre:
            self.pre_text.append(data)
        if self.in_h2:
            self.h2_buf.append(data)  # keep inline code in the section title
        elif not self.skip_depth:
            self.buf.append(data)


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", text)
    return [p.strip() for p in parts if p.strip()]


def report(title, items):
    print(f"\n== {title}: {len(items)}")
    for item in items:
        print(f"  - {item}")


def length_report(sections: list[Section]) -> list[str]:
    print("\n== Length report")
    print(f"  {'Section':<44} {'Words':>5} {'Code lines':>12} {'Flow':>5} {'Steps':>5} {'Panels':>6}")
    over = []
    for s in sections:
        if not (s.words or s.code_blocks or s.flow_steps or s.procedure_steps or s.panels):
            continue
        code = ",".join(str(n) for n in s.code_blocks) or "-"
        print(f"  {s.title[:44]:<44} {s.words:>5} {code:>12} {s.flow_steps or '-':>5} {s.procedure_steps or '-':>5} {s.panels or '-':>6}")
        if s.title == "(header)":
            continue
        if s.words > SECTION_WORDS_MAX:
            over.append(f"'{s.title}': {s.words} words > {SECTION_WORDS_MAX}. Cut, or split the section.")
        for n in s.code_blocks:
            if n > CODE_LINES_MAX:
                over.append(f"'{s.title}': code block of {n} lines > {CODE_LINES_MAX}. Show only the changed lines and 2-3 context lines.")
        if s.flow_steps > FLOW_STEPS_MAX:
            over.append(f"'{s.title}': diagram with {s.flow_steps} steps > {FLOW_STEPS_MAX}. Merge small steps, leave out optional steps.")
        if s.procedure_steps > PROCEDURE_STEPS_MAX:
            over.append(f"'{s.title}': {s.procedure_steps} procedure steps > {PROCEDURE_STEPS_MAX}. Merge steps, or split the guide.")
        if s.panels > PANELS_PER_SECTION_MAX:
            over.append(f"'{s.title}': {s.panels} panels > {PANELS_PER_SECTION_MAX}. Move some to Rules bullets or steps.")

    total = sum(s.words for s in sections)
    minutes = total / WORDS_PER_MINUTE
    code_lines = sum(sum(s.code_blocks) for s in sections)
    print(f"\n  Total: {total} words (not counting code), about {minutes:.1f} min of reading, {code_lines} code lines.")
    print(f"  Budget: 600-{GUIDE_WORDS_MAX} words, about 5 min.")
    if total > GUIDE_WORDS_MAX:
        over.insert(0, f"Whole guide: {total} words > {GUIDE_WORDS_MAX}. Do a cut pass, or split into two guides.")
    report("Over the length budget", over)
    return over


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    parser = GuideParser()
    parser.feed(Path(sys.argv[1]).read_text(encoding="utf-8"))
    parser._flush()

    long_items, passive_items, word_items = [], [], []
    seen = set()
    for block, is_step in parser.blocks:
        for s in sentences(block):
            if s in seen:
                continue
            seen.add(s)
            words = len(WORD.findall(s))
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

    report("Long sentences", long_items)
    report("Possible passive voice", passive_items)
    report("Words to replace", word_items)
    over = length_report(parser.sections)
    total = len(long_items) + len(word_items) + len(over)
    print(f"\n{total} item(s) to fix, {len(passive_items)} passive item(s) to review.")


if __name__ == "__main__":
    main()
