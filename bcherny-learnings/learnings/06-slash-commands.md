# Slash Commands for Inner Loop Workflows

## Key Learning
Create slash commands for workflows you do many times daily. Commands save prompting effort and let Claude use them too. Store in `.claude/commands/` and check into git.

## Why It Matters
- Eliminates repetitive prompting
- Ensures consistency across team
- Commands can use inline bash for speed
- Claude can invoke them during its work

## Practical 2026 Implementation

### Directory Structure
```
.claude/
  commands/
    commit-push-pr.md
    test-and-lint.md
    deploy-staging.md
    review-changes.md
```

### Command File Format
```markdown
---
description: Short description shown in /help
---

Your prompt here. Can include:
- Instructions for Claude
- Inline bash: $(git status)
- Multi-step workflows
```

### Example: commit-push-pr.md
```markdown
---
description: Commit changes, push, and create PR
---

Review the current changes and create a commit, push, and PR:

Current branch: $(git branch --show-current)
Git status: $(git status --short)
Recent commits: $(git log --oneline -5)
Diff stats: $(git diff --stat)

1. Create a concise commit message based on the changes
2. Commit all staged changes
3. Push to origin
4. Create a PR with a clear description
```

### Example: test-and-lint.md
```markdown
---
description: Run tests and fix lint errors
---

Run the test suite and fix any issues:

$(npm test 2>&1 | head -50)
$(npm run lint 2>&1 | head -30)

Fix any failing tests or lint errors, then verify everything passes.
```

### Using Inline Bash
```markdown
# Pre-compute expensive operations
Current user: $(whoami)
Changed files: $(git diff --name-only)
Package version: $(node -p "require('./package.json').version")

# Avoids back-and-forth with Claude asking for this info
```

### High-Value Commands to Create
| Command | Purpose |
|---------|---------|
| `/commit-push-pr` | Full commit workflow |
| `/test` | Run and fix tests |
| `/review` | Review current changes |
| `/deploy` | Deploy to environment |
| `/debug` | Debug current error |
| `/refactor` | Refactor selected code |

### Team Sharing
```bash
# Commands checked into git = team consistency
git add .claude/commands/
git commit -m "Add team slash commands"
```
