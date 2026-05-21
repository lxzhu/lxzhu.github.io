---
applyTo: "pyscripts/**/*.py"
description: "Guide Copilot when creating or editing Python scripts under pyscripts with consistent CLI, style, and safety defaults"
---

# Python Script Guidelines For pyscripts

When generating Python code in this folder, follow these rules.

## Script shape
- Prefer a single-purpose script with small functions.
- Add `main()` and the `if __name__ == "__main__":` entrypoint.
- Use `argparse` for CLI inputs instead of hard-coded values.
- Return exit codes from `main()` and raise `SystemExit(main())`.

## Style and typing
- Target Python 3.11+ syntax.
- Add type hints for public functions and key local variables.
- Use clear names and keep functions short.
- Add concise docstrings to module and public functions.

## IO and paths
- Use `pathlib.Path` instead of string path concatenation.
- Accept input and output paths as CLI arguments.
- Validate file and directory existence with helpful error messages.
- Use UTF-8 when reading and writing text files.

## Errors and logging
- Prefer `logging` over `print` for operational messages.
- Handle expected exceptions with actionable messages.
- Avoid bare `except:`; catch specific exceptions.

## Dependencies
- Use Python standard library first.
- If a third-party package is truly needed, mention it explicitly and keep usage minimal.

## Safety and maintainability
- Do not delete or overwrite files unless explicitly requested by arguments.
- Keep side effects inside `main()` or dedicated functions.
- Include an example CLI usage snippet in comments when helpful.
