# AIOS VSCode Extension `/save` Command Documentation

## Overview

The AIOS VSCode Extension provides a powerful `/save` command that allows users to persist their conversation context across VSCode sessions. This feature ensures continuity in AI-assisted development workflows and maintains important conversation history.

## How the `/save` Command Works

### Command Syntax
```
@aios /save
```

### Implementation Details

The `/save` command is implemented across two key components:

1. **Chat Participant Handler** (`chatParticipant.ts`):
   - Processes the `/save` command in the chat interface
   - Calls the context manager's `saveContext()` method
   - Provides user feedback on success/failure

2. **Context Manager** (`contextManager.ts`):
   - Handles the actual persistence logic
   - Stores conversation state in VSCode's global state
   - Maintains conversation metadata and workspace context

### What Gets Saved

When you execute `/save`, the following information is persisted:

1. **Conversation Messages**:
   - All user messages in the current session
   - All AI assistant responses
   - System messages and metadata

2. **Workspace Context**:
   - Current workspace folders
   - Active file at time of save
   - List of open files
   - Git branch information (planned feature)
   - Project type detection (planned feature)

3. **Session Metadata**:
   - Unique conversation ID
   - Timestamp of last activity
   - Iteration count
   - AIOS version information

### Storage Mechanism

The context is stored using VSCode's `globalState.update()` API with the key `'aios.conversationState'`. This ensures the data persists across VSCode sessions and is available when the extension reloads.

## Usage Examples

### Basic Save Operation
```
User: I've been working on refactoring the AIOS C# solution
AI: I can help you with that refactoring...
User: @aios /save
AI: Context saved successfully.
```

### Checking Save Status
```
User: @aios /status
AI: **AIOS System Status**
- Status: Active
- AI Modules: Active
- Context Messages: 15
- Iterations: 3
- Last Activity: 1/15/2025, 2:30:15 PM
```

### Loading Saved Context
```
User: @aios /load
AI: Context loaded successfully.
```

## Effectiveness in Current Integration

### Strengths

1. **Persistent Memory**: The `/save` command effectively maintains conversation continuity across VSCode restarts, which is crucial for long-term development sessions.

2. **Workspace Awareness**: The saved context includes workspace information, allowing the AI to understand the project structure when resuming conversations.

3. **Version Tracking**: The system tracks AIOS version information, ensuring compatibility between saved contexts and current extension versions.

4. **Error Handling**: Robust error handling provides clear feedback when save operations fail.

### Current Limitations

1. **Git Integration**: Git branch detection is marked as TODO and not yet implemented.

2. **Project Type Detection**: Automatic project type detection is planned but not implemented.

3. **Context Size Management**: While there's a `maxHistorySize` parameter, the context pruning logic may need refinement for very long conversations.

4. **Cross-Workspace Compatibility**: Saved contexts are tied to specific workspace configurations and may not transfer well between different projects.

## Best Practices

### When to Use `/save`

1. **End of Development Sessions**: Always save before closing VSCode to preserve important conversation context.

2. **Before Major Changes**: Save context before making significant code changes or switching branches.

3. **During Long Debugging Sessions**: Periodically save to avoid losing valuable troubleshooting context.

4. **Before Extension Updates**: Save context before updating the AIOS extension to ensure compatibility.

### Optimization Tips

1. **Regular Saves**: Use `/save` regularly during long development sessions to avoid data loss.

2. **Context Management**: Use `/reset` to clear context when starting new, unrelated tasks.

3. **Status Monitoring**: Use `/status` to monitor context size and activity before saving.

## Integration with AIOS Architecture

The `/save` command integrates seamlessly with the broader AIOS architecture:

1. **Logging Integration**: All save operations are logged through the AIOS logging infrastructure.

2. **Bridge Communication**: Saved context can be used by the AIOS bridge for improved AI coordination.

3. **Multi-Language Support**: The context manager preserves information about C++, Python, and C# components.

## Technical Configuration

### Extension Settings

The persistence behavior can be controlled through extension settings:

```typescript
private persistAcrossRestarts: boolean; // Controls whether context is saved
private maxHistorySize: number;         // Limits conversation history size
```

### State Storage

The context is stored in VSCode's global state with the key:
```typescript
const stateKey = 'aios.conversationState';
```

## Troubleshooting

### Common Issues

1. **Save Failures**: Check VSCode permissions and available storage space.
2. **Load Failures**: Verify that the saved context is compatible with the current AIOS version.
3. **Context Corruption**: Use `/reset` to clear corrupted context and start fresh.

### Debug Information

Use the following commands to diagnose issues:
- `@aios /status` - Check current context statistics
- `@aios /help` - Review available commands
- Check VSCode Developer Tools for extension logs

## Future Enhancements

Planned improvements to the `/save` command include:

1. **Git Branch Detection**: Automatic detection and storage of current git branch
2. **Project Type Recognition**: Intelligent detection of project frameworks and languages
3. **Context Compression**: Optimized storage for large conversation histories
4. **Export/Import**: Ability to export contexts to files for sharing or backup
5. **Context Encryption**: Secure storage of sensitive conversation data

## Conclusion

The AIOS VSCode Extension's `/save` command is a robust and effective tool for maintaining conversation continuity in AI-assisted development workflows. While it has some limitations, it provides essential functionality for preserving important development context across sessions. The command integrates well with the broader AIOS architecture and provides a solid foundation for future enhancements.

For optimal results, use `/save` regularly during development sessions and combine it with other AIOS commands like `/status` and `/load` for comprehensive context management.
