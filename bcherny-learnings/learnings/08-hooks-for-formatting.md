# PostToolUse Hooks for Auto-Formatting

## Key Learning
Use a PostToolUse hook to automatically format Claude's code after edits. Claude usually generates well-formatted code, but the hook handles the last 10% to prevent CI formatting failures.

## Why It Matters
- Eliminates formatting issues in CI
- No manual formatting step needed
- Consistent code style automatically
- Claude focuses on logic, hook handles style

## Practical 2026 Implementation

### Hook Configuration
Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "prettier --write \"$FILE\""
      }
    ]
  }
}
```

### Language-Specific Formatters

#### JavaScript/TypeScript
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "if [[ \"$FILE\" =~ \\.(js|ts|jsx|tsx)$ ]]; then prettier --write \"$FILE\"; fi"
      }
    ]
  }
}
```

#### Python
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "if [[ \"$FILE\" =~ \\.py$ ]]; then black \"$FILE\" && isort \"$FILE\"; fi"
      }
    ]
  }
}
```

#### Go
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "if [[ \"$FILE\" =~ \\.go$ ]]; then gofmt -w \"$FILE\"; fi"
      }
    ]
  }
}
```

### Multi-Language Setup
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "~/.claude/scripts/format-file.sh \"$FILE\""
      }
    ]
  }
}
```

```bash
#!/bin/bash
# ~/.claude/scripts/format-file.sh
FILE="$1"

case "$FILE" in
  *.js|*.ts|*.jsx|*.tsx|*.json|*.md)
    prettier --write "$FILE" 2>/dev/null
    ;;
  *.py)
    black "$FILE" 2>/dev/null
    isort "$FILE" 2>/dev/null
    ;;
  *.go)
    gofmt -w "$FILE" 2>/dev/null
    ;;
  *.rs)
    rustfmt "$FILE" 2>/dev/null
    ;;
esac
```

### Other Useful Hooks

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "format-file.sh \"$FILE\""
      }
    ],
    "Stop": [
      {
        "command": "notify-send 'Claude finished' 'Session complete'"
      }
    ]
  }
}
```
