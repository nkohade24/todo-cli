---
name: add-command
description: Add a new subcommand to the todo CLI (todo.py). Use when asked to add a command like "done", "delete", "edit", "clear", etc. Walks through the function, subparser, dispatch branch, and test, following the existing code patterns and CLAUDE.md rules.
---

# Add a command to the todo CLI

Add exactly one new subcommand to `todo.py`, following the project's layered
structure. Do only what was asked — see the rules at the end.

## Steps

### 1. Write the command function

Add a `<name>_task()` function near the other command functions (`add_task`,
`list_tasks`, `done_task`, `delete_task`). It must go through the persistence
layer — call `load_tasks()` and `save_tasks()`, never touch `tasks.json`
directly.

Follow the existing conventions:
- Tasks use the dict schema `{"task": <str>, "done": <bool>}`. Don't change it.
- The CLI is 1-indexed for the user; convert with `index - 1` and validate the
  range before mutating, printing a clear message on bad input (mirror
  `done_task` / `delete_task`).
- `print()` a short confirmation of what happened.

```python
def <name>_task(...):
    tasks = load_tasks()
    # ... read / mutate tasks ...
    save_tasks(tasks)
    print(...)
```

### 2. Register the subparser in main()

In `main()`, add a `subparsers.add_parser("<name>", ...)` and an
`add_argument(...)` for each argument the command needs (match how the existing
parsers are defined).

### 3. Add the dispatch branch

Add an `elif args.command == "<name>":` branch that calls `<name>_task(...)`
with the parsed args. Keep it next to the other branches.

### 4. Add a test in test_todo.py

Add a test that mirrors the existing tests' style. An autouse fixture
(`temp_tasks_file`) already monkeypatches `todo.TASKS_FILE` to a throwaway file,
so just call the command functions directly and assert on `todo.load_tasks()`
(or on printed output via `capsys`). Cover the happy path
and, if the command takes a task number, the out-of-range case — matching tests
like `test_done_*` and `test_delete_*`.

### 5. Run the tests

Confirm everything passes:

```bash
python -m pytest -v
```

## Rules (from CLAUDE.md)

- Standard library only — no third-party packages.
- Build **one** command at a time. Don't add commands that weren't asked for.
- Keep `todo.py` a single file.
- Don't change unrelated code.
- After changing code, run the tests to confirm it works.
