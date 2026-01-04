# Use Opus 4.5 with Extended Thinking

## Key Learning
Despite being larger and slower, Opus 4.5 with extended thinking is almost always faster in practice because it requires less steering and is better at tool use.

## Why It Matters
- Less back-and-forth correction = faster overall completion
- Better tool use = fewer failed attempts
- Higher first-attempt success rate
- Quality > raw speed

## Practical 2026 Implementation

### Configuration
```bash
# Set as default model in Claude Code
claude config set model opus

# Or per-session
claude --model opus
```

### When to Use Opus vs Sonnet

| Use Opus 4.5 | Use Sonnet |
|--------------|------------|
| Complex multi-step tasks | Simple single-file edits |
| Architectural decisions | Quick lookups |
| Debugging intricate issues | Formatting/linting |
| New feature implementation | Repetitive tasks |
| Code review | Simple refactors |

### Mental Model
```
Time with smaller model:
  Quick response + Correction + Another correction + Finally works = SLOW

Time with Opus:
  Thoughtful response + Works first time = FAST
```

### Best Practices for 2026
1. **Default to Opus** for any task requiring judgment
2. **Enable thinking** for complex problems
3. **Trust the process** - don't switch models because it "feels slow"
4. **Measure outcomes** not response times
5. **Use parallel sessions** to offset any perceived slowness
