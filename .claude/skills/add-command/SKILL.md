---
name: add-command
description: Add a new subcommand to the todo CLI (todo.py). Use when asked to add a command like "done", "delete", "edit", "clear", etc. Walks through the function, subparser, dispatch branch, and test, following the existing code patterns and CLAUDE.md rules.
---

# Add a command to the todo CLI

Add exactly one new subcommand to `todo.py`, following the project's layered
structure.

**First read [`../_shared-conventions.md`](../_shared-conventions.md)** — it
covers the patterns every command must follow (persistence layer, single file,
terse print style, matching test) and the project rules. The steps below only
cover what's specific to adding a command.

## Steps

### 1. Write the command function

Add a `<name>_task()` function near the other command functions (`add_task`,
`list_tasks`, `done_task`, `delete_task`). Per the shared conventions, it must
go through `load_tasks()` / `save_tasks()`.

Command-specific details:
- Tasks use the dict schema `{"task": <str>, "done": <bool>}`. Don't change it.
- The CLI is 1-indexed for the user; convert with `index - 1` and validate the
  range before mutating, printing a clear message on bad input (mirror
  `done_task` / `delete_task`).

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

Add a test that mirrors the existing tests' style (see the shared conventions
for the fixture and assertion approach). Cover the happy path and, if the
command takes a task number, the out-of-range case — matching tests like
`test_done_*` and `test_delete_*`.

### 5. Run the tests

```bash
python -m pytest -v
```
