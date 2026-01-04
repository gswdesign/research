# Long-Running Task Management

## Key Learning
For long-running tasks: (a) prompt Claude to verify with a background agent, (b) use Stop hooks for deterministic verification, or (c) use ralph-wiggum plugin. Use `--permission-mode=dontAsk` in sandboxes to avoid blocking on prompts.

## Why It Matters
- Tasks can run for hours without intervention
- Verification ensures quality without supervision
- Sandbox mode enables fully autonomous operation
- Background agents parallelize verification

## Practical 2026 Implementation

### Option A: Background Agent Verification
```
You: Implement the authentication system. When you're done,
     spawn a background agent to verify it works end-to-end.

Claude: [Implements feature]
        [Spawns verification agent]
        [Verification agent tests the implementation]
        [Reports results]
```

### Option B: Stop Hooks
Add to `.claude/settings.json`:
```json
{
  "hooks": {
    "Stop": [
      {
        "command": "npm test && npm run lint"
      },
      {
        "command": "notify-send 'Claude' 'Task complete'"
      }
    ]
  }
}
```

When Claude finishes, hooks automatically:
1. Run tests to verify work
2. Notify you it's done

### Option C: Ralph-Wiggum Plugin
```bash
# Install the ralph-wiggum plugin
# https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-wiggum

# Provides self-healing capabilities for long-running tasks
```

### Sandbox Mode for Autonomous Operation
```bash
# In a safe environment (Docker, VM, CI):
claude --permission-mode=dontAsk

# Or full bypass (sandboxed environments ONLY):
claude --dangerously-skip-permissions
```

### Long-Running Task Patterns

#### Pattern 1: Fire and Forget
```bash
# Start task, check notifications later
claude "Refactor the entire auth module" &

# Or on web
# Start on claude.ai/code, check back in an hour
```

#### Pattern 2: Supervised Background
```bash
# Terminal 1: Main work
claude "Implement feature X"

# Terminal 2: Monitor logs
tail -f ~/.claude/logs/session.log
```

#### Pattern 3: Checkpoint-Based
```
You: Implement this in stages. After each stage:
     1. Commit your changes
     2. Run tests
     3. Post a summary to Slack
     4. Continue to next stage

     Stages:
     1. Database schema
     2. API endpoints
     3. Frontend components
     4. Integration tests
```

### Task Duration Guidelines
| Task Type | Expected Duration | Recommended Approach |
|-----------|-------------------|---------------------|
| Simple fix | < 5 min | Watch directly |
| Feature | 15-60 min | Background + notification |
| Refactor | 1-4 hours | Sandbox + Stop hooks |
| Migration | 4+ hours | Checkpoints + verification |

### Notification Setup
```bash
# macOS
brew install terminal-notifier
# In Stop hook: terminal-notifier -title "Claude" -message "Done"

# Linux
# In Stop hook: notify-send "Claude" "Task complete"
```
