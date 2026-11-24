# readme

[**English**](./README.md) | [中文](./README.zh-CN.md)

Rules and bilingual templates an agent follows when writing a GitHub README. This file is the documentation-shaped result of those templates.

## Overview

Instruction version 1.2.0. Read it here or clone it. There is nothing to install.

An agent writing someone else's README starts at [AGENTS.md](./AGENTS.md), then follows [README-AGENT-INSTRUCTIONS.md](./README-AGENT-INSTRUCTIONS.md).

| File | Role |
|---|---|
| `AGENTS.md` | Short entry for an agent. |
| `README-AGENT-INSTRUCTIONS.md` | The rules. This is not a project README. |
| `README.template.md` | English template. The filled result is `README.md` in the target repository. |
| `README.zh-CN.template.md` | Chinese template. The filled result is `README.zh-CN.md` in the target repository. |
| `scripts/check_readme.py` | Checks a finished pair, and checks that the two templates still match. |
| `examples/sample-cli/` | A finished CLI pair beside a one-file command that runs. |

## Check

From this repository:

```bash
python3 scripts/check_readme.py all
```

That checks the templates, this README pair, and `examples/sample-cli/`. Python 3 is enough.
