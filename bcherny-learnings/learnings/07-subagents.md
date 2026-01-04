# Subagents for Common Workflows

## Key Learning
Use subagents for common workflows like code simplification, app verification, and other tasks you do for most PRs. Think of subagents as automated common workflows.

## Why It Matters
- Automates quality checks
- Consistent standards across all PRs
- Runs in parallel with main work
- Encapsulates complex verification logic

## Practical 2026 Implementation

### Subagent Examples
```
code-simplifier   → Simplifies code after Claude is done
verify-app        → Detailed E2E testing instructions
security-review   → Checks for common vulnerabilities
perf-check        → Identifies performance issues
```

### Creating a Subagent
Store in `.claude/agents/` or define inline:

```markdown
# .claude/agents/code-simplifier.md
---
name: code-simplifier
description: Simplify and clean up code after implementation
---

Review the recently changed files and simplify:

1. Remove unnecessary complexity
2. Extract repeated code into functions
3. Simplify conditional logic
4. Remove dead code
5. Improve variable names

Do not change functionality, only improve readability.
```

### Using Subagents
```bash
# Invoke during session
/agent code-simplifier

# Or Claude invokes automatically based on context
```

### verify-app Subagent Example
```markdown
---
name: verify-app
description: End-to-end verification of Claude Code changes
---

Test the application thoroughly:

1. Build the project: $(npm run build 2>&1)
2. Run unit tests: $(npm test 2>&1)
3. Start the dev server
4. Test the UI manually:
   - [ ] Feature X works as expected
   - [ ] No console errors
   - [ ] Responsive on mobile
5. Run E2E tests if available
6. Check for regressions

Report any issues found with specific reproduction steps.
```

### Subagent Patterns for 2026

| Subagent | When to Use |
|----------|-------------|
| `code-simplifier` | After completing feature |
| `verify-app` | Before creating PR |
| `security-review` | After auth/data changes |
| `accessibility-check` | After UI changes |
| `api-validator` | After API changes |
| `docs-updater` | After public API changes |

### Integration with PR Workflow
```
1. Implement feature
2. Run code-simplifier subagent
3. Run verify-app subagent
4. If all pass → create PR
5. If issues → fix and re-verify
```
