"""PostToolUse hook: run pytest after a .py file is edited.

Reads the hook JSON payload from stdin, extracts the edited file path, and if it
ends in .py runs pytest with the current (miniconda) Python interpreter.

Behaviour (the script always exits 0):
- File is not .py, or tests pass -> exit 0 with no output (no block).
- Tests fail -> print a JSON decision to stdout so Claude Code surfaces the
  failure reason directly:
      {"decision": "block", "reason": "<pytest output here>"}
"""

import json
import subprocess
import sys


def main():
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as exc:
        print(f"[run_tests_hook] could not parse hook JSON from stdin: {exc}",
              file=sys.stderr)
        return 0

    file_path = (payload.get("tool_input") or {}).get("file_path") or ""

    if not file_path.endswith(".py"):
        # Not a Python file — nothing to test.
        return 0

    print(f"[run_tests_hook] {file_path} changed - running pytest...",
          file=sys.stderr)

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        # Tests passed — no block.
        return 0

    # Tests failed — emit a block decision with the pytest output as the reason.
    reason = (result.stdout or "") + (result.stderr or "")
    if not reason.strip():
        reason = f"pytest exited with code {result.returncode} (no output)."

    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
