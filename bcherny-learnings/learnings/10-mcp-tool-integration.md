# MCP Tool Integration

## Key Learning
Claude Code can use all your tools via MCP (Model Context Protocol). Configure tools like Slack, BigQuery, Sentry, etc. in `.mcp.json` and share with the team.

## Why It Matters
- Claude becomes your interface to all tools
- No context switching between applications
- Team shares same tool configurations
- Natural language access to complex queries

## Practical 2026 Implementation

### MCP Configuration File
```json
// .mcp.json (check into git)
{
  "mcpServers": {
    "slack": {
      "command": "mcp-server-slack",
      "args": [],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
      }
    },
    "github": {
      "command": "mcp-server-github",
      "args": [],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Common MCP Integrations

#### Slack
```json
{
  "slack": {
    "command": "mcp-server-slack",
    "capabilities": ["search", "post", "read"]
  }
}
```
**Usage**: "Search Slack for discussions about the auth refactor"

#### BigQuery
```bash
# Use bq CLI directly (no MCP needed)
bq query --use_legacy_sql=false 'SELECT * FROM dataset.table LIMIT 10'
```
**Usage**: "Query BigQuery for user signups last week"

#### Sentry
```json
{
  "sentry": {
    "command": "mcp-server-sentry",
    "env": {
      "SENTRY_AUTH_TOKEN": "${SENTRY_AUTH_TOKEN}"
    }
  }
}
```
**Usage**: "Get recent errors from Sentry for the payments service"

#### Linear/Jira
```json
{
  "linear": {
    "command": "mcp-server-linear"
  }
}
```
**Usage**: "Create a Linear issue for this bug"

### Example Workflows

#### Debugging with Context
```
You: There's an error in production, can you check Sentry
     and find related Slack discussions?

Claude: [Queries Sentry for recent errors]
        [Searches Slack for related discussions]
        [Correlates findings]

        Found error X occurring since deploy Y.
        Team discussed workaround in #eng-alerts.
        Here's a fix based on the discussion...
```

#### Analytics Questions
```
You: How many users signed up last month compared to the month before?

Claude: [Runs BigQuery query]

        Last month: 12,450 signups
        Previous month: 10,200 signups
        Growth: 22%
```

### Team Setup
```bash
# Share MCP config
git add .mcp.json
git commit -m "Add team MCP tool configuration"

# Each team member sets environment variables locally
export SLACK_BOT_TOKEN=xoxb-...
export GITHUB_TOKEN=ghp_...
```

### Security Best Practices
1. Use environment variables for tokens
2. Never commit secrets to git
3. Use read-only tokens where possible
4. Audit tool access regularly
