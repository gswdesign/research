# Shared Team CLAUDE.md

## Key Learning
Maintain a single `CLAUDE.md` file checked into git that the whole team contributes to. When Claude makes a mistake, add it to `CLAUDE.md` so it doesn't happen again.

## Why It Matters
- Team-wide consistency in Claude interactions
- Institutional memory for AI behavior
- Prevents repeating the same corrections
- Compounds improvements over time

## Practical 2026 Implementation

### File Structure
```
your-repo/
  CLAUDE.md          # Team-shared context file
  .claude/
    commands/        # Slash commands
    settings.json    # Shared permissions
```

### CLAUDE.md Template
```markdown
# Project Context

## Architecture
- [Key architectural patterns]
- [Important conventions]

## Code Style
- [Style preferences Claude should follow]
- [Anti-patterns to avoid]

## Known Issues
- [Things Claude gets wrong repeatedly]

## Do NOT
- [Explicit prohibitions]
- [Patterns that cause bugs]

## Testing Requirements
- [How to verify changes]
- [Required test coverage]
```

### Contribution Workflow
1. Claude makes a mistake during development
2. Fix the issue manually
3. **Immediately** add rule to `CLAUDE.md`
4. Commit with message: `docs: add CLAUDE.md rule for [issue]`
5. PR review catches new rules for team awareness

### Team Cadence
- **Daily**: Add rules as issues discovered
- **Weekly**: Review CLAUDE.md in team standup
- **Monthly**: Prune outdated rules, reorganize

### Example Rules to Add
```markdown
## Do NOT
- Never use `any` type in TypeScript - always define proper types
- Never commit directly to main - always use feature branches
- Never skip error handling in async functions
- Do not add console.log statements - use the logger utility
```
