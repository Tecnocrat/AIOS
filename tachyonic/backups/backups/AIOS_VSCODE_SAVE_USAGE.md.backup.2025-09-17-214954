# AIOS VSCode Extension `/save` Command - Practical Usage Guide

## Quick Start Examples

### Basic Workflow
```
# Start a development session
User: I need help refactoring the AIOS C# solution
AI: I can help you with that. Let me analyze the current structure...

# Continue working...
User: Can you show me the current compilation errors?
AI: Sure, let me check the build output...

# Save your progress
User: @aios /save
AI: Context saved successfully.

# Later, after restarting VSCode
User: @aios /load
AI: Context loaded successfully.
User: Where did we leave off with the refactoring?
AI: We were working on the AIOS C# solution refactoring. The last thing we discussed was...
```

### Status Monitoring
```
User: @aios /status
AI: **AIOS System Status**
- Status: Active
- AI Modules: Active
- Context Messages: 23
- Iterations: 5
- Last Activity: 1/15/2025, 3:45:22 PM
```

### Context Management
```
# Reset when starting a new task
User: @aios /reset
AI: AIOS conversation context has been reset.

# Save after important discussions
User: @aios /save
AI: Context saved successfully.
```

## Integration with AIOS Development Workflow

### 1. Daily Development Session
```
Morning:
1. @aios /load        # Load yesterday's context
2. @aios /status      # Check current state
3. Continue working...
4. @aios /save        # Save progress periodically

Evening:
1. @aios /save        # Save final state
2. Close VSCode
```

### 2. Long-term Project Work
```
Project Start:
1. @aios /reset       # Start fresh
2. "Let's work on the AIOS C# refactoring"
3. @aios /save        # Save initial context

Weekly:
1. @aios /save        # Save progress
2. @aios /status      # Monitor context size
3. If context too large: @aios /reset and summarize key points
```

### 3. Debugging Sessions
```
Bug Discovery:
1. "I found a compilation error in AIOS.UI"
2. Work through debugging...
3. @aios /save        # Save debugging context

Bug Resolution:
1. @aios /load        # Resume debugging context
2. "Let's continue fixing the compilation error"
3. @aios /save        # Save solution
```

## Command Reference

### Available Commands
- `@aios /save` - Save current context
- `@aios /load` - Load saved context
- `@aios /reset` - Reset conversation context
- `@aios /status` - Show system status
- `@aios /help` - Show command help

### Error Handling
If save fails:
```
User: @aios /save
AI: Failed to save context: [error details]

# Try again or reset
User: @aios /reset
AI: AIOS conversation context has been reset.
```

## Best Practices

### Do Save When:
-  Completing important discussions
-  Before closing VSCode
-  After solving complex problems
-  Before switching to different tasks
-  During long debugging sessions

### Don't Save When:
-  Context is corrupted or confusing
-  Starting completely new, unrelated work
-  Testing or experimenting temporarily
-  Context has grown too large (>100 messages)

### Optimization Tips:
1. **Regular Saves**: Save every 30-60 minutes during active development
2. **Context Pruning**: Use `/reset` when context becomes unwieldy
3. **Status Monitoring**: Check `/status` before saving large contexts
4. **Session Planning**: Plan save points around natural breakpoints

## Technical Details

### What's Stored
- All conversation messages (user + AI)
- Workspace folder paths
- Active file information
- Open files list
- Session metadata
- Iteration counts

### Storage Location
VSCode Global State: `'aios.conversationState'`

### Persistence
Survives VSCode restarts and extension reloads

## Troubleshooting

### Common Issues
1. **Save Fails**: Check VSCode permissions
2. **Load Fails**: Context may be corrupted, try `/reset`
3. **Large Context**: Use `/status` to monitor size
4. **Missing Features**: Git branch detection coming soon

### Debug Commands
```
@aios /status    # Check current state
@aios /help      # Review available commands
@aios /reset     # Clear corrupted context
```

## Future Enhancements

### Planned Features
- Git branch detection and storage
- Project type auto-detection
- Context compression for large histories
- Export/import functionality
- Context encryption for sensitive data

### Extension Architecture
The `/save` command integrates with:
- AIOS Context Manager
- VSCode Extension API
- AIOS Bridge System
- Logging Infrastructure

## Conclusion

The AIOS VSCode Extension's `/save` command is essential for maintaining development continuity. Use it regularly to preserve important conversations and resume work seamlessly across sessions.

**Key Takeaway**: Think of `/save` as version control for your AI conversations - use it frequently and strategically to maintain productive development workflows.
