# Agent entry

Write or update a target repository's README from the facts in that repository.

1. Read `README-AGENT-INSTRUCTIONS.md`. Use the version printed at the top.
2. Fill `README.template.md` and `README.zh-CN.template.md`. Delete every unused OPTIONAL block.
3. Write `README.md` and `README.zh-CN.md` in the target repository. Keep the language-switch links pointed at those final names.
4. From this repository, run:

```bash
python3 scripts/check_readme.py pair /path/to/README.md /path/to/README.zh-CN.md
```

`examples/sample-cli/` is a finished CLI pair next to a command that runs. This repository's own README pair is the finished documentation shape.

Do not copy this file, the instruction file, or the templates into the target repository. Record the spec version in the delivery notes.
