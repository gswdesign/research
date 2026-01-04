# Verification Loop (Most Important)

## Key Learning
The most important thing for great Claude Code results: **give Claude a way to verify its work**. This feedback loop 2-3x's the quality of the final result.

## Why It Matters
- Claude can iterate until the code actually works
- Catches bugs before you review
- Tests the UX, not just the code
- Verification looks different per domain

## Practical 2026 Implementation

### Verification Types by Domain

#### Web Development
```
You: Implement the login page. Test it in the browser using
     the Chrome extension until login works correctly and
     the UX feels good.

# Claude uses: Chrome extension for visual testing
# Iterates until: UI works, no console errors, good UX
```

#### Backend/API
```
You: Add the /users endpoint. Run curl commands to test it
     until all edge cases are handled.

# Claude uses: curl, httpie, or test scripts
# Iterates until: All status codes correct, validation works
```

#### CLI Tools
```
You: Implement the export command. Run it with various inputs
     until it handles all cases correctly.

# Claude uses: Direct command execution
# Iterates until: All inputs produce correct output
```

#### Mobile (Simulator)
```
You: Build the settings screen. Test in the iOS simulator
     until it works on all device sizes.

# Claude uses: Simulator + screenshot verification
# Iterates until: Works across device sizes
```

### Chrome Extension Testing
```
# Claude Code can control Chrome via the extension
# https://code.claude.com/docs/en/chrome

1. Opens browser to your app
2. Performs actions (click, type, navigate)
3. Observes results
4. Iterates on code until UX is correct
```

### Building Verification into Your Workflow

#### Project Setup
```bash
# Ensure these scripts exist:
npm run test          # Unit tests
npm run test:e2e      # End-to-end tests
npm run dev           # Local server for manual testing
npm run lint          # Linting
npm run typecheck     # Type checking
```

#### CLAUDE.md Instructions
```markdown
## Verification Requirements

Before considering any task complete:
1. Run `npm test` - all tests must pass
2. Run `npm run lint` - no lint errors
3. Run `npm run typecheck` - no type errors
4. For UI changes: Test in browser, verify UX
5. For API changes: Test with curl, verify responses
```

### Verification Investment Priorities

| Priority | Investment | Impact |
|----------|------------|--------|
| 1 | Unit tests | Catch logic errors |
| 2 | Type checking | Catch type errors |
| 3 | E2E tests | Catch integration issues |
| 4 | Visual testing | Catch UX issues |
| 5 | Manual spot checks | Catch edge cases |

### The Quality Multiplier
```
Without verification:
  Claude writes code → Done → Hope it works → Debug later

With verification:
  Claude writes code → Tests → Fails → Fixes → Tests →
  Fails → Fixes → Tests → Passes → Actually done

Result: 2-3x better quality, less debugging for you
```

### Make Verification Rock-Solid
This is the highest-ROI investment you can make:
1. Fast test suite (< 30 seconds for unit tests)
2. Clear pass/fail signals
3. Good error messages
4. Easy local testing setup
5. Browser automation for UI
