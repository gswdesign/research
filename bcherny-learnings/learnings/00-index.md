# bcherny's Claude Code Power User Tips

**Source**: [@bcherny Twitter thread](https://x.com/bcherny/status/2007179832300581177)
**Context**: Tips from someone running 5-15 Claude instances in parallel daily

---

## Quick Start: Top 3 Actions for Immediate Impact

1. **Start with Plan Mode** (Learning #5) - Shift+Tab twice before any feature work
2. **Create verification scripts** (Learning #12) - Highest ROI investment
3. **Add your first slash command** (Learning #6) - `/commit-push-pr` is a good start

---

## All Learnings

| # | Topic | Key Insight | Priority |
|---|-------|-------------|----------|
| [01](./01-parallel-sessions.md) | Parallel Sessions | Run 5 terminal + 5-10 web Claudes | Medium |
| [02](./02-opus-with-thinking.md) | Opus 4.5 + Thinking | Best model despite being slower | High |
| [03](./03-shared-claude-md.md) | Shared CLAUDE.md | Team learns from every mistake | High |
| [04](./04-compounding-engineering.md) | @claude in PRs | Knowledge compounds via code review | Medium |
| [05](./05-plan-mode-first.md) | Plan Mode First | Iterate on plan before auto-accept | **Critical** |
| [06](./06-slash-commands.md) | Slash Commands | Automate inner loop workflows | High |
| [07](./07-subagents.md) | Subagents | Automate PR workflows | Medium |
| [08](./08-hooks-for-formatting.md) | PostToolUse Hooks | Auto-format code on edit | Medium |
| [09](./09-permission-preapproval.md) | Permission Pre-approval | Whitelist safe commands | Low |
| [10](./10-mcp-tool-integration.md) | MCP Tool Integration | Claude uses Slack, BigQuery, etc. | Medium |
| [11](./11-long-running-tasks.md) | Long-Running Tasks | Background agents + Stop hooks | Medium |
| [12](./12-verification-loop.md) | Verification Loop | 2-3x quality with feedback loops | **Critical** |

---

## Implementation Path for 2026

### Week 1: Foundation
- [ ] Configure Opus 4.5 as default model
- [ ] Set up system notifications for terminal
- [ ] Create initial `CLAUDE.md` with 5-10 rules
- [ ] Practice Plan Mode workflow

### Week 2: Automation
- [ ] Create first 3 slash commands
- [ ] Set up PostToolUse formatting hook
- [ ] Configure permission whitelist
- [ ] Create first verification script

### Week 3: Scale
- [ ] Start running 3+ parallel sessions
- [ ] Set up MCP integration (Slack or similar)
- [ ] Create first subagent
- [ ] Add Stop hooks for long tasks

### Week 4: Team
- [ ] Check `.claude/` config into git
- [ ] Install GitHub Action for @claude
- [ ] Document team CLAUDE.md contribution process
- [ ] Share learnings with team

---

## Key Themes

### 1. Parallelization
bcherny runs 5-15 Claude instances simultaneously. The bottleneck is not Claude's speed - it's your ability to manage parallel workstreams.

### 2. Investment in Infrastructure
Slash commands, subagents, hooks, MCP integrations - these are upfront investments that compound. Every workflow you automate saves time forever.

### 3. Verification is Everything
The single most important insight: Claude with verification feedback is 2-3x better than Claude without it. Invest in making verification rock-solid.

### 4. Team Knowledge Compounds
Shared CLAUDE.md + @claude in PRs = every mistake becomes permanent learning. After a few months, Claude rarely makes repeated errors.

---

## File Structure

```
learnings/
├── 00-index.md              ← You are here
├── 01-parallel-sessions.md
├── 02-opus-with-thinking.md
├── 03-shared-claude-md.md
├── 04-compounding-engineering.md
├── 05-plan-mode-first.md
├── 06-slash-commands.md
├── 07-subagents.md
├── 08-hooks-for-formatting.md
├── 09-permission-preapproval.md
├── 10-mcp-tool-integration.md
├── 11-long-running-tasks.md
└── 12-verification-loop.md
```
