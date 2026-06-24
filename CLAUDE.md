# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A minimal command-line todo manager written in a single Python file (`todo.py`) with no third-party dependencies — only the standard library (`argparse`, `json`, `os`). Tasks are persisted to a `tasks.json` file in the working directory.

## Commands

```bash
python todo.py add "task description"   # Append a task to tasks.json (creates the file if missing)
python todo.py list                     # Print tasks numbered from 1; prints "No tasks yet." when empty
```

There is no build step, test suite, or linter configured.

## Architecture

`todo.py` follows a simple layered structure:

- **Persistence layer** — `load_tasks()` / `save_tasks()` are the only functions that touch `tasks.json`. `load_tasks()` returns `[]` when the file is absent, so callers never deal with a missing-file case. Tasks are stored as a JSON array of `{"task": <description>}` objects.
- **Command layer** — one function per subcommand (`add_task`, `list_tasks`), each calling `load_tasks()` / `save_tasks()` rather than accessing the file directly.
- **CLI layer** — `main()` builds an `argparse` parser with a required subcommand (`dest="command"`) and dispatches to the matching command function.

### Adding a new command

1. Write a `<name>_task()` (or similar) function that goes through `load_tasks()` / `save_tasks()`.
2. Register it in `main()` with `subparsers.add_parser("<name>", ...)`, adding `add_argument` calls for any arguments.
3. Add an `elif args.command == "<name>":` dispatch branch.

The task dict schema (`{"task": ...}`) is the implicit contract between every command — changing it means updating all commands that read or write tasks.

## Project rules

- Use only the Python standard library. No third-party packages.
- Build one command at a time. Do not add commands that weren't asked for.
- Keep `todo.py` as a single file.
- After changing code, run a quick test to confirm it works.
- When editing, do not change unrelated code.
