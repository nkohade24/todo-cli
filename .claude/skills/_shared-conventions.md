# Shared conventions (boilerplate — not a skill)

> The leading underscore in this filename marks it as a **shared helper**, not a
> skill. It has no `name`/`description` frontmatter and is never invoked on its
> own. Other skills in `.claude/skills/` reference it instead of repeating these
> rules.

Every command added to this project must follow these core patterns. Skills that
modify `todo.py` should link here rather than restate them.

## Core patterns

- **File access goes through the persistence layer.** Only `load_tasks()` and
  `save_tasks()` touch `tasks.json`. Command functions call those — never read
  or write the file directly.
- **Keep `todo.py` a single file.** No new modules or packages.
- **Match the terse print style of the existing commands.** A short, plain
  confirmation of what happened — mirror `add_task` / `done_task` /
  `delete_task`. No banners, decoration, or extra chatter.
- **Always add a matching test in `test_todo.py`.** Every command change ships
  with a test in the same style as the existing ones (the autouse
  `temp_tasks_file` fixture monkeypatches `todo.TASKS_FILE` to a throwaway file,
  so call the command functions directly and assert on `todo.load_tasks()` or on
  printed output via `capsys`). Cover the happy path, and the out-of-range case
  when the command takes a task number.

## Project rules (from CLAUDE.md)

- Standard library only — no third-party packages.
- Build **one** command at a time. Don't add commands that weren't asked for.
- Don't change unrelated code.
- After changing code, run `python -m pytest -v` to confirm it works.
