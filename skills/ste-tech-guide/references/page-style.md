# Page style

`assets/template.html` is the **recommended style**: a clean, wiki-style documentation page.
Use it when the user does not ask for a different look. If the user gives their own styling, use
theirs (see "Use the user's own style" below). The content rules and the print rules stay the same
in both cases.

## Contents
1. The recommended style
2. Components and when to use them
3. Use the user's own style
4. Rules for every style

---

## 1. The recommended style

A wiki-style page has no decoration. The reader sees only the content.

- **Layout:** one centered column, maximum 760 px wide, with 16 px side margins on small screens.
- **Font:** the system font stack (`-apple-system, "Segoe UI", Roboto, …`) at 14 px, line height
  about 1.7. Code uses the system monospace font at 12 px.
- **Colors:** dark navy text on a white background, grey borders, one blue for links and step
  numbers. All the colors are CSS variables in `:root`, so you can change them in one place.
- **Headings:** a large, light page title. Section headings (`h2`) have a thin line below them and
  a number ("3. How it works").
- **Header:** the title and "Created By <name>" with a small round initials avatar. Nothing else.

## 2. Components and when to use them

For the panels, `callouts-and-caveats.md` has the full decision guide and good/bad wording. The
template has a commented "panel gallery" with the error panel, the info panel and the "To be
confirmed" lozenge.

| Component | Class | Use it for |
|---|---|---|
| Table of contents | `.toc` | Pages with 4 or more sections. Links go to the sections on the same page. |
| Warning panel (yellow, `!`) | `.panel.warn` | The most likely mistake and its result. Start with a bold "Do not…". |
| Note panel (purple, `?`) | `.panel.note` | Necessary information that is not an instruction, for example a version requirement. |
| Summary panel (green, `✓`) | `.panel.ok` | The one rule to remember, at the end of the "how it works" section. |
| Info panel (blue, `i`) | `.panel.info` | Rarely. Do not use it for "About this page". |
| Error panel (red, `×`) | `.panel.error` | Only for something that causes data loss or a security problem. |
| Code block | `.code-block` + `.code-title` | Real config or code. The title is the file name or the config path. Put each line in `<span class="ln">`. |
| New or changed line | `.ln.add` | Lines that the reader adds (green). |
| Context line | `.ln.dim` | Lines that show where the change goes, but do not change (grey). |
| Numbered steps | `ol.steps` | The procedure. One action per step. |
| Table | `table` | Terms, before/after comparisons. |
| Lozenge | `.lozenge.green/.grey/.red` | Short status labels in a table cell, for example "No change". The red lozenge also marks an unverified fact: "To be confirmed". Not in the header. |
| Flow diagram | `.flow`, `.flow-row`, `.flow-node`, `.flow-note`, `.flow-arrow` | The order of steps. See SKILL.md, step 3. |
| Chips | `.chip`, `.chip.id`, `.chip.gone`, `.chip.url` | The data inside a flow step: the item to follow, a removed item, a resolved value. |
| Footer | `.footer` | References to source docs. |

## 3. Use the user's own style

The user can ask for a different look. For example, they can give company colors, a font, a logo, or
an existing HTML or CSS template. Then:

1. **Change the CSS variables in `:root` first.** Most color requests need only this change.
2. **Change the font stack** in `body` and `code`, if the user gives a font. If the font must load
   from the web, tell the user that the PDF needs network access when it is made.
3. **Keep the class names and the HTML structure.** Then the components and the flow diagram
   still work.
4. **Add header items only when the user asks for them**, for example their own logo. Use a local
   image or an inline SVG, not a link to an external site.
5. **If the user gives a full template of their own**, put the content into their template. Keep
   the rules in section 4 below.

If the user's request is not clear, use the recommended style. Then ask about the changes after
they see the preview.

## 4. Rules for every style

These rules make the page easy to read and make the PDF correct. Keep them in every style:

- No scripts, no animations, no hover-only content. The page is made for print.
- Long code lines wrap (`white-space: pre-wrap; overflow-wrap: anywhere`). Nothing scrolls sideways.
- Panels, code blocks, tables, steps and the flow diagram do not split across pages
  (`break-inside: avoid`).
- Headings stay with the text after them (`break-after: avoid`).
- `@page { size: A4; }` with margins, and `print-color-adjust: exact`, so that the colors print.
- By default, each section starts on a new page (`main > h2 ~ h2 { break-before: page; }`).
- The page works at phone width: the flow diagram changes to one column.
