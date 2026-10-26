# knowledge-sharing: working notes for Claude

This repository is a public collection of Claude Code skills, packaged as one plugin
(`knowledge-sharing`) with a marketplace file. People outside the author's company will read and
install it.

## Layout

- `.claude-plugin/plugin.json`: plugin manifest. Increase `version` (semver) when a skill changes
  in a way that users will notice.
- `.claude-plugin/marketplace.json`: one plugin entry with `"source": "./"`. Claude Code finds the
  skills in `skills/` automatically, so a new skill needs no entry here.
- `skills/<skill-name>/SKILL.md`: one folder per skill. The folder name and the `name` in the
  frontmatter are the same, in kebab-case.

## Conventions

- **No private data.** Examples, templates and test prompts must not contain company names,
  internal repository names, table names, people, URLs or secrets. Use generic examples
  (`sales.orders`, `record_id`, "Ada Byron").
- **Self-contained skills.** A skill must work in any project. Do not refer to files outside its own
  folder.
- **Scripts use only the Python standard library**, and they work on Windows, macOS and Linux.
  Run them with `python -I` when you test them.
- **Progressive disclosure.** Keep `SKILL.md` under about 300 lines. Put long material in
  `references/` and say in `SKILL.md` when to read it.
- **Explain why** in skill instructions, instead of strong "ALWAYS / NEVER" rules without a reason.
- **Copyright.** Do not copy text from standards or other people's docs. Write summaries in your own
  words and link to the source (for example, the ASD-STE100 spec at asd-ste100.org).
- **Docs in this repository** follow the same STE style as the `ste-tech-guide` skill: short
  sentences, active voice, one instruction per sentence.

## Add or change a skill

1. Use the `skill-creator` skill to draft or improve the skill.
2. Put test prompts in `skills/<skill-name>/evals/` (the skill-creator case-folder format).
3. Keep test runs in `<skill-name>-workspace/` next to the skill folder. Git ignores these folders.
4. Add or update the row for the skill in the `README.md` table.
5. Increase the version in `.claude-plugin/plugin.json`.

## Check before a commit

```bash
python -I skills/ste-tech-guide/scripts/ste_check.py skills/ste-tech-guide/assets/template.html
python -I skills/ste-tech-guide/scripts/html_to_pdf.py skills/ste-tech-guide/assets/template.html
```

The template must give "0 item(s) to fix", and the PDF export must finish with a page count.
Git ignores the PDF.
