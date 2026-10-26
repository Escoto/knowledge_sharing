---
name: ste-tech-guide
description: Write a how-to guide, explainer or runbook for engineers about a feature, setting, config option or code change, in simple English (ASD-STE100), as a clean HTML page that you preview and then export to PDF. Use it whenever the user asks for a guide, how-to, manual, training doc, technical instructions, onboarding or wiki page, or a doc for junior engineers or the team, in any project, even if they do not say STE or PDF. Also use it to rewrite a technical doc in simpler English.
license: MIT. See LICENSE at the repository root.
---

# STE tech guide

Make a short, correct, easy-to-read guide that explains **one feature** and **one concrete
change** to a reader who is new to the code. The output is a single self-contained HTML page. By
default, it uses the recommended clean, wiki-style look in `assets/template.html`. If the user asks
for their own styling, use it instead. The user reviews the page in a preview, and then you export
it to PDF.

Do not use this skill for README files or reference docs that stay as Markdown inside a codebase,
unless the user asks for this style.

The value of this skill is three things together:

1. **Facts from the source.** Every claim comes from the code, the docs or the tests, not from memory.
2. **Simple language.** ASD-STE100 rules make the guide easy for junior and non-native readers.
3. **A clean page.** There is nothing on it except the content: no fake branding, breadcrumbs, dates
   or decorations. It prints well.

## Workflow

### 1. Find the facts

Before you write, read the implementation of the feature, its config model, its docs and its tests.
Find the answers to these questions:

- What does the feature do, and in which order relative to the other steps? The order is often
  the main thing a junior engineer gets wrong.
- Where does the setting go (the exact path in the config), what type does it take, and what is
  the default?
- What error occurs when someone uses it incorrectly? Copy the real error message from the code.
- Which version of the library or service first has the feature? Compare it with the version that
  the target project pins.
- If the user names a target file, read it. Use its real keys, indentation and neighbours in the
  procedure.

Keep a list of things that you could not verify, for example a version number that you inferred
from a branch name. Try to verify each one, or ask the user. If a fact is still not verified when
you show the page, mark it on the page with a red "To be confirmed" lozenge, and list it in your
reply. Do not present a guess as a fact. `references/callouts-and-caveats.md` (section 4) tells
you where each kind of caveat goes.

### 2. Plan the sections

Use this default structure. It worked well for a feature guide. Remove a section if it does not
apply. Do not add extra sections, such as "Troubleshooting", "FAQ" or "Errors", unless the user asks
for them. Extra sections make the page longer and readers skip them. Put the one or two important
errors inside a warning panel where they occur.

| # | Section | Contents |
|---|---|---|
| 1 | Purpose | What the page tells you, in 2–3 sentences. When to use the feature. A "Term / Meaning on this page" table for 4–6 terms. |
| 2 | The problem | The real situation that needs the feature, with the real config or code. One **warn** panel for the most likely mistake and its error message. |
| 3 | How it works | A vertical flow diagram (see below). End the section with a green **Summary** panel that gives the one rule to remember. |
| 4 | Rules | Short bullet list: where the setting goes, its type, its default, its limits, and how it interacts with other settings. Put a version requirement in a **note** panel. |
| 5 | Procedure | "Before you start" bullets, then numbered steps (`ol.steps`) with one action each. Show the change as a code block with the new lines in green (`.ln.add`). |
| 6 | Check the result | A before/after table and 2–3 "Make sure that…" bullets that the reader can do. |

Add a small footer with references to the source docs, if there are any.

Before you add a panel (warning, note, summary, info or error), read
`references/callouts-and-caveats.md`. It tells you which panel to use, or if the text belongs in a
Rules bullet or a step. It has good and bad wording for each panel. Use a maximum of two panels in
one section.

### 3. Draw the flow diagram

Use the diagram when the order of steps matters. It is usually the part of the page that readers
remember.

- Make it **vertical**, top to bottom. Use one box per step.
- To the right of each box, write **one sentence**. It tells what occurs in the step **and why the
  step is in this position**, for example "…so this step must occur before the field is removed."
- Inside the boxes, use chips to show how the data changes. Use `.chip.id` for the item the reader
  must follow, `.chip.gone` (struck through) for an item that a step removes, and `.chip.url` for a
  resolved value.
- Mark the step that the guide is about with `.flow-node.key`, and the last step with `.flow-node.final`.
- Below the diagram, add a small caption if the names or values in it are only examples.
- Use the user's own step names if they gave them, for example `read table → {current schema} → …`.

### 4. Write in STE

Read `references/ste-writing-rules.md` before you write the text. The short version:

- Use short sentences: 20 words or fewer in steps, 25 or fewer in descriptions. Put one topic in
  each sentence.
- Use the active voice. Write instructions in the imperative ("Open the file."), with one action
  per sentence.
- Use one term for each thing on the whole page. Keep the technical names in `code` format exactly
  as the reader must type them.
- Use simple words: "make sure" not "ensure", "use" not "utilize", "before" not "prior to".
- Always state the "why", especially for order and for "Do not" instructions.

### 5. Build the page

`assets/template.html` is the **recommended style**: a clean, wiki-style page. Use it unless the
user asks for a different look. Copy the template and replace the sample content. The template
contains all the components: title and byline, table of contents, panels, code blocks with a title
bar and green/dim lines, tables, numbered steps, the flow diagram, lozenges and the footer. Delete
the components that you do not use. Do not change the CSS when you use the recommended style.

If the user gives their own styling (colors, font, logo, or a full template), use it. Read
`references/page-style.md` first. It tells you how to change the style safely, which components to
use for what, and which print rules every style must keep.

**Keep the header clean.** This rule applies to every style, because users removed each of these
items by hand in the session that made this skill:

- The header is the **title** and **"Created By <name>"** only, with a small initials avatar.
  Get the name from `git config user.name`, or ask the user.
- Do not add a product or logo bar (for example "Wiki · Spaces · Team"), breadcrumbs, a "Last
  updated" date, audience or type lozenges, or an "About this page" panel. Do not add links that go
  nowhere. The table of contents links to sections on the same page, so it can stay.
- Add a header item only when the user asks for it, for example their own logo.
- Do not use scripts, animations, hover effects or external resources. The page is made for print.
- Code blocks wrap long lines (`pre-wrap`), so nothing is cut off in the PDF. If a long value is
  not the point of a snippet, shorten it with `…` and a `# shortened here` comment.

Save the page where the user can open it. Inside the project, a `docs/guides/<topic>-guide.html`
path is a good default. Tell the user that the file is not committed.

### 6. Preview, then iterate

Open the HTML page in a preview, for example the browser pane or a local browser. Check that:

- No element scrolls sideways: the page `scrollWidth` is not more than the window width, and no
  `pre` element has `scrollWidth > clientWidth`.
- The diagram reads top to bottom, and each note is next to its box.

Show it to the user and ask for changes before you make the PDF. Users often remove sections or
header items at this point. Make each change in the HTML, and keep the HTML as the source.

### 7. Export to PDF

When the user approves the page, run:

```bash
python scripts/html_to_pdf.py <page.html> [<out.pdf>]
```

The script finds Chrome, Edge or Chromium. It prints the page headless with no browser header or
footer, waits until the file is fully written, and prints the page count.

The print CSS starts **each section on a new page** (`main > h2 ~ h2 { break-before: page; }`).
Thus, a section never splits, and a heading is never left alone at the bottom of a page. For a very
short guide where all the sections fit on one or two pages, delete that rule.

Look at every page of the PDF before you send it. Look for empty pages, split tables or code
blocks, and a heading at the bottom of a page. If you cannot render the PDF pages to images, say so.

Before you make the final PDF, look for every "To be confirmed" mark. Remove the marks that the
user confirmed, and correct the text if the user gave a different value. Keep a mark only if the
user asks to keep it.

Send the PDF to the user. In your reply, list the facts that are still not verified.

## Bundled files

- `assets/template.html`: the recommended style, with every component and sample content.
- `references/page-style.md`: the recommended style, how to use each component, how to use the
  user's own style, and the print rules for every style.
- `references/callouts-and-caveats.md`: which panel to use, good and bad wording for all five
  panels, and where each kind of caveat goes.
- `references/ste-writing-rules.md`: the writing rules, word swaps and a self-check. Read it before
  you write.
- `scripts/html_to_pdf.py`: HTML to PDF with headless Chrome or Edge. It uses only the Python
  standard library.
- `scripts/ste_check.py`: a quick check of the page text. It reports long sentences, likely passive
  voice and words to replace. It is a helper, not a full STE checker: use your judgment on each item.
