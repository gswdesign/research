# Parallel Claude Sessions

## Key Learning
Run multiple Claude instances simultaneously - 5 in terminal (numbered tabs 1-5) plus 5-10 on claude.ai/code. Use system notifications to know when a session needs input.

## Why It Matters
- Parallelizes your cognitive work across multiple tasks
- Hand off local sessions to web using `&` or `--teleport`
- Start sessions from phone (iOS app) and check in later
- Eliminates waiting as your primary bottleneck

## Practical 2026 Implementation

### Terminal Setup (iTerm2)
```bash
# Configure system notifications for Claude Code
# See: https://code.claude.com/docs/en/terminal-config#iterm-2-system-notifications

# Number your tabs 1-5 for quick reference
# When notification fires, switch to that tab
```

### Daily Workflow
1. **Morning**: Start 2-3 sessions from iOS app for background tasks
2. **Working hours**: Run 5 terminal Claudes for active development
3. **Web sessions**: Keep 5-10 claude.ai/code tabs for parallel research/coding
4. **Handoffs**: Use `&` to send local context to web, `--teleport` to switch environments

### Session Types to Run in Parallel
- **Terminal 1**: Main feature development
- **Terminal 2**: Bug fixes / debugging
- **Terminal 3**: Code review assistance
- **Terminal 4**: Documentation / tests
- **Terminal 5**: Research / exploration
- **Web tabs**: Long-running tasks, secondary features, experiments

### Quick Reference
| Platform | Max Sessions | Use Case |
|----------|--------------|----------|
| Terminal | 5 | Active development |
| Web | 5-10 | Parallel tasks |
| iOS | 2-3 | Background tasks |
