# Permission Pre-Approval (Not --dangerously-skip)

## Key Learning
Don't use `--dangerously-skip-permissions`. Instead, use `/permissions` to pre-allow safe bash commands in your environment. Share these in `.claude/settings.json` with your team.

## Why It Matters
- Security without friction
- Team-wide consistent permissions
- Avoids unnecessary prompts for safe commands
- Maintains safety guardrails for dangerous commands

## Practical 2026 Implementation

### Setting Permissions
```bash
# Interactive permission management
claude /permissions

# Or directly in settings
```

### settings.json Configuration
```json
{
  "permissions": {
    "allow": [
      "npm test",
      "npm run lint",
      "npm run build",
      "npm run dev",
      "git status",
      "git diff",
      "git log",
      "git branch",
      "git checkout",
      "git add",
      "git commit",
      "git push",
      "ls",
      "cat",
      "head",
      "tail",
      "grep",
      "find",
      "pwd",
      "echo"
    ],
    "deny": [
      "rm -rf",
      "sudo",
      "chmod 777"
    ]
  }
}
```

### Pattern-Based Permissions
```json
{
  "permissions": {
    "allow": [
      "npm *",
      "yarn *",
      "pnpm *",
      "git *",
      "bun *"
    ]
  }
}
```

### Environment-Specific Permissions
```json
{
  "permissions": {
    "allow": [
      "docker compose *",
      "kubectl get *",
      "kubectl describe *",
      "aws s3 ls *"
    ],
    "deny": [
      "kubectl delete *",
      "aws * --delete",
      "docker system prune"
    ]
  }
}
```

### Team Sharing
```bash
# Check settings into git
git add .claude/settings.json
git commit -m "Add shared Claude permissions"

# Team members get consistent experience
```

### When to Use --dangerously-skip-permissions
Only in sandboxed/isolated environments:
- CI/CD pipelines
- Docker containers
- VMs for testing
- Ephemeral cloud instances

Never on your main development machine.

### Permission Decision Matrix
| Command Type | Recommendation |
|--------------|----------------|
| Read-only commands | Pre-allow |
| Build/test commands | Pre-allow |
| Git operations | Pre-allow with care |
| File modifications | Case-by-case |
| System commands | Always prompt |
| Destructive commands | Always deny |
