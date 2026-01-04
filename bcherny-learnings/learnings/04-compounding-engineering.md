# Compounding Engineering via @claude in PRs

## Key Learning
During code review, tag `@claude` on coworkers' PRs to add learnings to `CLAUDE.md` as part of the PR. Use the Claude Code GitHub Action for this.

## Why It Matters
- Every PR becomes a learning opportunity
- Knowledge compounds across the team
- Reviews produce permanent improvements
- Inspired by Dan Shipper's "Compounding Engineering" concept

## Practical 2026 Implementation

### Setup GitHub Action
```bash
# Install the Claude Code GitHub Action
claude /install-github-action
```

### PR Review Workflow
1. Review teammate's PR
2. Spot a pattern Claude should know about
3. Comment: `@claude add to CLAUDE.md: always use X pattern when doing Y`
4. Claude updates CLAUDE.md in the same PR
5. PR includes both feature + improved AI context

### Example PR Comments
```
@claude add to CLAUDE.md: when creating React components,
always include a displayName for debugging

@claude add rule: never use synchronous file operations
in API routes

@claude document: our error handling pattern uses
Result<T, E> types, not try/catch
```

### Compounding Effect
```
Week 1:  Team has 10 rules
Week 4:  Team has 40 rules
Week 12: Team has 100+ rules
         Claude rarely makes repeated mistakes
         New team members get AI that knows all tribal knowledge
```

### Integration with CI
```yaml
# .github/workflows/claude.yml
name: Claude PR Assistant
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

# Claude responds to @claude mentions in PRs
```

### Best Practices
1. **Be specific** - Vague rules don't help
2. **Include examples** - Show right vs wrong
3. **Add context** - Explain *why* the rule exists
4. **Review accumulation** - Prune conflicts monthly
