# todo-cli

A minimal command-line todo manager written in a single Python file using only
the standard library — no third-party dependencies. Tasks are stored as JSON in
a `tasks.json` file in the working directory.

Built as a Claude Code learning project.

## Usage

```bash
# Add a task
$ python todo.py add "Buy milk"
Added task: Buy milk

# List all tasks ([ ] = open, [x] = done)
$ python todo.py list
1. [ ] Buy milk
2. [ ] Write README

# Mark a task done by its number
$ python todo.py done 1
Marked task as done: Buy milk

# Delete a task by its number
$ python todo.py delete 2
Deleted task: Write README
```

When there are no tasks, `list` prints `No tasks yet.`

## Storage

Tasks persist to `tasks.json` in the current directory. The file is created
automatically on the first `add`.
