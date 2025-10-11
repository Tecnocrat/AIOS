# VSCode Extension Development - Quick Reference

## Critical Workflow

### Source vs Compiled Code
- **Source**: `vscode-extension/src/**/*.ts` (TypeScript)
- **Compiled**: `vscode-extension/dist/**/*.js` (JavaScript)
- **Extension Runs**: Compiled code from `dist/`, NOT source!

### Development Cycle

```powershell
# Step 1: Start watch mode (auto-compile on save)
cd c:\dev\AIOS\vscode-extension
npm run watch

# Step 2: Edit TypeScript in src/
# (Save triggers auto-compilation)

# Step 3: Reload VSCode to see changes
# Ctrl+Shift+P → "Developer: Reload Window"

# Step 4: Test in AIOS OUTPUT panel
# Verify logs show expected behavior
```

### Manual Compilation

```powershell
# Compile once
npm run compile

# Clean build
npm run clean
npm run compile

# Lint check
npm run lint
```

## Context Configuration

### Location
`vscode-extension/src/config/contextSections.json`

### Adding New Section

```json
{
  "id": "new_section",
  "title": "New Section Title",
  "enabled": true,
  "priority": 7,
  "items": [
    {
      "label": "Item Label",
      "value": "Item Value",
      "critical": false
    }
  ]
}
```

### Dynamic Data Resolution

```json
{
  "id": "dynamic_section",
  "dynamic": true,
  "source": "aiosContext",
  "items": [
    {
      "label": "Version",
      "path": "version",
      "fallback": "unknown"
    },
    {
      "label": "Status",
      "path": "project_metadata.status",
      "fallback": "Unknown"
    }
  ]
}
```

### Conditional Rendering

```json
{
  "id": "conditional_section",
  "conditional": {
    "source": "aiosContext",
    "path": "consciousness_crystal_framework",
    "required": true
  },
  "items": [...]
}
```

## Debugging

### View Extension Logs
1. Open OUTPUT panel (`Ctrl+Shift+U`)
2. Select "AIOS" from dropdown
3. Watch for initialization sequence

### Enable Debug Mode
```json
// In settings.json
{
  "aios.debug.enabled": true
}
```

### Debug Extension Development
1. Open `vscode-extension` folder in VSCode
2. Press `F5` to launch Extension Development Host
3. Test extension in new window
4. Console shows debug output

## Common Issues

### Extension Not Updating
**Symptom**: Code changes not reflected in extension behavior

**Solution**:
1. Check if `npm run watch` is running
2. Verify compilation succeeded (no errors)
3. Reload VSCode window (`Ctrl+Shift+P` → "Reload Window")
4. Check OUTPUT for old vs new log messages

### Context Not Injecting
**Symptom**: @aios chat doesn't have AIOS context

**Solution**:
1. Check AIOS OUTPUT for "context loaded successfully"
2. Verify `contextSections.json` is valid JSON
3. Check ContextGenerator logs for errors
4. Verify MultiEngineContext has data

### TypeScript Compilation Errors
**Symptom**: `npm run compile` fails

**Solution**:
1. Check error messages for specific issues
2. Verify JSON imports have correct path
3. Check tsconfig.json has `resolveJsonModule: true`
4. Run `npm install` to update dependencies

## File Structure

```
vscode-extension/
├── src/
│   ├── config/
│   │   └── contextSections.json     # Context configuration
│   ├── extension.ts                 # Main entry point
│   ├── contextGenerator.ts          # Dynamic context engine
│   ├── aiosBridge.ts                # AIOS communication
│   ├── chatParticipant.ts           # Chat integration
│   ├── contextManager.ts            # Context persistence
│   ├── logger.ts                    # Logging system
│   └── mcpClient.ts                 # MCP integration
├── dist/                            # Compiled output (gitignored)
├── package.json                     # Extension manifest
├── tsconfig.json                    # TypeScript config
└── README.md                        # Extension documentation
```

## Key Commands

### Extension Commands
- `AIOS: Reset Context` - Clear chat history
- `AIOS: Save Context` - Persist current state
- `AIOS: Load Context` - Restore saved state
- `AIOS: Show System Status` - Display health
- `AIOS: Connect to MCP Servers` - Enable consciousness/evolution
- `AIOS: MCP Status` - Check MCP connection

### Chat Commands
- `@aios` - Start conversation
- `@aios /reset` - Reset context
- `@aios /status` - System status
- `@aios /help` - Show commands

## Architecture Patterns

### Data-Driven Configuration
- Store configuration in JSON
- Use TypeScript for logic only
- Separate concerns (data vs behavior)

### Async/Await Pattern
- Prefer async/await over Promise.then
- Handle errors with try/catch
- Log success AFTER completion

### AINLP Compliance
- Check spatial metadata before file ops
- Use data-driven patterns
- Document architectural decisions

## Quick Fixes

### Stale Extension Cache
```powershell
# Force clean rebuild
npm run clean
npm run compile

# Reload VSCode
Ctrl+Shift+P → "Developer: Reload Window"
```

### Version Mismatch
- Update `contextSections.json` fallback values
- Recompile extension
- Reload window

### Context Generation Errors
- Validate JSON syntax in `contextSections.json`
- Check ContextGenerator logs in OUTPUT
- Verify MultiEngineContext data structure

## Testing Checklist

- [ ] `npm run compile` succeeds
- [ ] No TypeScript errors
- [ ] No lint errors
- [ ] Extension loads in VSCode
- [ ] AIOS OUTPUT shows initialization logs
- [ ] Context injection completes
- [ ] @aios chat responds
- [ ] No duplicate logs
- [ ] "activated successfully" appears LAST

## References

- Extension manifest: `package.json`
- Context config: `src/config/contextSections.json`
- Architecture doc: `tachyonic/archive/EXTENSION_DATA_DRIVEN_ARCHITECTURE_20251012.md`
- Dev Path: `docs/development/AIOS_DEV_PATH.md`
