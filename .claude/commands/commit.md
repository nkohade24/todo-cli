---
description: Stage all changes and create a conventional-commit-style git commit
---

Create a git commit for the current changes. Follow these steps:

1. Run `git status` and `git diff` (and `git diff --staged` if anything is already staged) to review exactly what changed.
2. Stage all changes with `git add -A`.
3. Write a clear, concise commit message in conventional commit style based on the actual changes — e.g. `feat: add delete command`, `fix: handle out-of-range task number`, `docs: update README`. Use an appropriate type (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`, etc.) and a short imperative summary. Add a brief body only if the change needs explanation.
4. Create the commit with that message.

Do NOT push. Only stage and commit locally.
