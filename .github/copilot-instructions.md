# Global Copilot Decision Rules

These rules apply to all tasks in this repository.

## Ask before deciding
- Do not guess user intent when multiple valid approaches exist.
- If a request is ambiguous, ask a concise clarifying question before making changes.
- If there are tradeoffs (speed vs quality, simple vs robust, breaking vs non-breaking), present options and ask the user to choose.

## Require explicit confirmation for impactful changes
- Ask for confirmation before destructive or irreversible actions.
- Ask for confirmation before introducing new dependencies, large refactors, or behavior changes that affect users.
- If uncertain whether a change is safe, pause and ask.

## Response style for decisions
- Offer 2 to 4 concrete options with brief pros and cons.
- Mark one recommended option and explain why in one sentence.
- Wait for user selection instead of auto-selecting.

## Fallback behavior
- If the user explicitly says to decide autonomously, proceed and state the assumption.
- If no response is received after asking, do not continue with risky changes.
