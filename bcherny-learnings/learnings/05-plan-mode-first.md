# Start with Plan Mode

## Key Learning
Most sessions should start in Plan mode (Shift+Tab twice). Iterate with Claude until you like the plan, then switch to auto-accept mode for implementation. A good plan is critical.

## Why It Matters
- Plans catch issues before code is written
- Reduces wasted implementation effort
- Claude can often one-shot with a solid plan
- Aligns human and AI on approach before execution

## Practical 2026 Implementation

### Keyboard Shortcuts
```
Shift+Tab (once)  → Toggle auto-accept edits
Shift+Tab (twice) → Enter Plan mode
```

### Plan Mode Workflow
```
1. Enter Plan mode (Shift+Tab x2)
2. Describe what you want to build
3. Review Claude's proposed plan
4. Ask clarifying questions / request changes
5. Iterate until plan is solid
6. Exit Plan mode, enable auto-accept
7. Say "execute the plan"
8. Claude implements (usually 1-shot)
```

### What Makes a Good Plan
- **Specific file changes** listed
- **Order of operations** defined
- **Edge cases** addressed
- **Testing strategy** included
- **Potential issues** acknowledged

### Example Planning Session
```
You: I want to add user authentication to our API

Claude (Plan mode):
## Plan
1. Add auth middleware in src/middleware/auth.ts
2. Create user model in src/models/user.ts
3. Add login/register routes in src/routes/auth.ts
4. Update existing routes to require auth
5. Add tests in tests/auth.test.ts

## Approach
- Use JWT tokens stored in httpOnly cookies
- bcrypt for password hashing
- Middleware checks token on protected routes

## Potential Issues
- Need to handle token refresh
- Existing tests may need auth mocking

You: Let's use sessions instead of JWT, and add rate limiting

Claude: Updated plan...
[Iterate until satisfied]

You: [Exit plan mode, enable auto-accept]
You: Execute the plan

Claude: [Implements everything]
```

### When to Skip Planning
- Single-line fixes
- Adding console.log for debugging
- Formatting changes
- Very simple, well-defined tasks
