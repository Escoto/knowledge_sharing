# knowledge-sharing

Agent skills for [Claude Code](https://claude.com/claude-code) that help engineers share knowledge.
The skills write documentation that is correct, simple to read, and ready to print or send.

## Skills

| Skill | What it does |
|---|---|
| [`ste-tech-guide`](skills/ste-tech-guide/SKILL.md) | Writes a how-to guide for a feature or a config change, in [ASD-STE100](https://www.asd-ste100.org) Simplified Technical English. The output is a clean, wiki-style HTML page that you preview, then export to PDF. The skill has a recommended style, and it can use your own styling. It includes a vertical flow diagram that explains the order of the steps. |

## Install

### As a Claude Code plugin

In Claude Code, add this repository as a marketplace and install the plugin:

```text
/plugin marketplace add Escoto/knowledge_sharing
/plugin install knowledge-sharing@knowledge-sharing
```

The skills are then available in every project, for example as `knowledge-sharing:ste-tech-guide`.

### As a personal skill (one skill only)

Copy the skill folder into your personal skills folder:

```bash
cp -r skills/ste-tech-guide ~/.claude/skills/
```

## Use

Ask Claude in plain words. You do not need to name the skill. For example:

> Write a guide for junior engineers on how to use `exclude_from_payload`, and apply it to
> `configs/approve_order.yml` to remove `record_id` from the request body.

Claude reads the code and docs, writes the page, opens a preview, and makes the PDF after you approve the page.

## Requirements

- Claude Code.
- Python 3.9 or later for the helper scripts. They use only the standard library.
- Google Chrome, Microsoft Edge, or Chromium for the PDF export. Set `BROWSER_PATH` if the script
  cannot find the browser.

## Contributing

See [CLAUDE.md](CLAUDE.md) for the conventions. In short: one folder per skill, no company or
personal data in examples, scripts that use only the Python standard library, and a test run
before you open a pull request.

## License

[MIT](LICENSE) © 2026 Rafael Escoto
