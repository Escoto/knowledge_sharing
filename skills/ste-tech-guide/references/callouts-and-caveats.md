# Callouts and caveats

Use this file when you decide whether something goes in a panel, and when you write the panel text.
It also tells you where each kind of caveat goes.

## Contents
1. Choose the right place
2. How to write a panel
3. The five panels, with examples
4. Caveats

---

## 1. Choose the right place

Ask these questions in this order. Stop at the first "yes".

| # | Question | Put it in |
|---|---|---|
| 1 | Is it an instruction that the reader must do? | A procedure step, not a panel. (Exception: a "Do not…" that prevents a failure, see question 3.) |
| 2 | If the reader ignores it, can it cause data loss, a security problem, or damage that is hard to undo? | **Error** panel (red `×`) |
| 3 | If the reader ignores it, can it break the job, the build or the result? | **Warning** panel (yellow `!`) |
| 4 | Must the reader check or have something before they start, for example a version, a permission or another setting? | **Note** panel (purple `?`). If it is an action, use a "Before you start" bullet. |
| 5 | Is it the one rule to remember from a concept section? | **Summary** panel (green `✓`). Maximum one per section. |
| 6 | Is it a limit, a default or a type of the feature? | A bullet in the **Rules** section. |
| 7 | Is it useful background, but the reader can do the task without it? | Normal text. Use an **Info** panel (blue `i`) only if the text interrupts the flow. |

**Limit the panels.** Use a maximum of two panels in one section. When a page has many panels, the
reader stops reading them. If a section needs three, it is too long, or some panels are Rules bullets.

## 2. How to write a panel

- **Start with a bold lead sentence.** For an error or a warning, the lead is a command:
  "**Do not…**". For a note, a summary or an info panel, the lead is a short label: "**Library
  version.**", "**Summary.**".
- **Then write one or two sentences.** Tell the result of the mistake, or the exact condition.
- **Do not write "Warning:" or "Note:".** The color and the icon already tell the reader.
- **Be exact.** Give the real error message, the real version and the real setting name. "Can cause
  issues" tells the reader nothing.
- **Do not use "might", "may" or "probably".** Tell the condition: "If X, then Y."

## 3. The five panels, with examples

### Error (red `×`)

Use it only for data loss, a security problem, or damage that is hard to undo.

Good:

```html
<div class="panel error">
  <div class="icon">×</div>
  <div class="body"><p><b>Do not run this script on the production catalog.</b> The script deletes all the rows in the target table. You cannot get the rows back.</p></div>
</div>
```

Bad: "CAUTION!!! Be very careful when you run this in prod."
Why it is bad: it does not tell the reader what to do or what occurs. Capital letters and "!!!" do
not add information.

### Warning (yellow `!`)

Use it for the most likely mistake that breaks the job, the build or the result.

Good:

```html
<div class="panel warn">
  <div class="icon">!</div>
  <div class="body"><p><b>Do not add <code>record_id</code> to <code>drop_columns</code>.</b> If you do this, the job cannot make the URL. The job stops with the error <code>Placeholder 'record_id' not found in the row data</code>.</p></div>
</div>
```

Bad: "Be careful with drop_columns, as it might cause issues with the URL."
Why it is bad: "be careful" is not an action, "might" is not exact, and the reader cannot recognize
the error when it occurs.

### Note (purple `?`)

Use it for a condition that the reader must know before they start, but that is not a step.

Good:

```html
<div class="panel note">
  <div class="icon">?</div>
  <div class="body"><p><b>Library version.</b> This setting is in version 2.0 and later versions. Version 1.x does not accept the setting and stops with a validation error.</p></div>
</div>
```

Bad: "Note that you should probably make sure that you are on a recent version of the library."
Why it is bad: "probably" and "recent" are not exact. The reader does not know which version to use.

### Summary (green `✓`)

Use it once, at the end of the section that explains how the feature works. It gives the one rule
that the reader must remember.

Good:

```html
<div class="panel ok">
  <div class="icon">✓</div>
  <div class="body"><p><b>Summary.</b> Remove a field in the mapping when the API never needs it. Use <code>example_setting</code> when the URL needs the field, but the body does not need it.</p></div>
</div>
```

Bad: "In summary, there are several ways to handle fields, and the right one depends on your use case."
Why it is bad: it gives no rule. The reader cannot decide anything from it.

### Info (blue `i`)

Use it rarely, for background that helps but that the reader does not need to do the task.

Good:

```html
<div class="panel info">
  <div class="icon">i</div>
  <div class="body"><p><b>Where the job keeps a record.</b> The job writes each request to the <code>api_state</code> table. You can use this table to see what the job sent.</p></div>
</div>
```

Bad: "About this page. This page uses simple English."
Why it is bad: it is about the page, not about the task. The reader gets nothing from it. Do not
use an info panel for page information, history or jokes.

## 4. Caveats

A caveat is a condition or a limit that changes what is true. There are three kinds. Each kind has
a different place.

### A. A limit of the feature

The limit is true and you verified it in the code, the docs or the tests.

- Put it in the **Rules** section as a bullet: "Each field in the list must be in the row."
- If the reader breaks the job when they ignore the limit, use a **warning** panel instead, where
  the mistake can occur.

### B. A condition that the reader must check first

Examples are a minimum version, a permission, a setting that must be on, or a platform.

- If the reader must **do** something, put it in **"Before you start"**: "Make sure that you have
  write access to the `config` folder."
- If the reader must only **know** it, put it in a **note** panel. Give the exact check: the
  version number, the file, the setting.

### C. Something that you could not verify

Examples are a version that you inferred from a branch name, a default that the docs do not state,
or a behavior that has no test.

1. **First, try to verify it.** Look at the tags, the changelog, the tests and the config model.
   Or ask the user.
2. **If it is still not verified when you show the page, mark it on the page.** Put a red "To be
   confirmed" lozenge directly after the statement:

   ```html
   <p>Use version 1.2.49 or a later version. <span class="lozenge red">To be confirmed</span></p>
   ```

   Do not write a guess as a fact. Do not hide it with "probably" or "should".
3. **List each marked item in your reply to the user**, with the reason that you could not verify it.
4. **Before the final PDF**, look for every "To be confirmed" mark. Remove each one that the user
   confirmed, and correct the text if the user gave a different value. Keep a mark only if the user
   asks to keep it.
