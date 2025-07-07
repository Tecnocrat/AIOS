# AIOS VSCode Extension

## Solving Chat Iteration Reset Problem

This VSCode extension addresses the critical issue of chat iteration reset that occurs when extensions restart, providing persistent context and deep integration between AIOS and VSCode.

## Features

### 🔄 **Persistent Context**
- **No More Iteration Resets**: Context preserved across VSCode restarts
- **Smart Context Management**: Automatic context trimming and optimization
- **Session Continuity**: Maintain conversation history and AI learning state

### 🧠 **AI Integration**
- **Multi-Language AI**: Coordination between C++, Python, and C# AI modules
- **AIOS Bridge**: Direct communication with AIOS core and AI services
- **Intelligent Responses**: Context-aware AI assistance

### ⚡ **VSCode Native Integration**
- **Chat Participant**: Native VSCode chat integration with `@aios`
- **Commands**: Rich command palette integration
- **Status Monitoring**: Real-time AIOS system status

## Installation

### Development Setup
```bash
cd c:\dev\AIOS\vscode-extension
npm install
npm run compile
```

### VSCode Installation
1. Open VSCode
2. Press `F1` and run "Developer: Install Extension from Location..."
3. Select the `c:\dev\AIOS\vscode-extension` folder

## Usage

### Chat Commands
- `@aios` - Start an AIOS conversation
- `@aios /reset` - Reset conversation context
- `@aios /status` - Show system status
- `@aios /help` - Show available commands
- `@aios /save` - Save current context
- `@aios /load` - Load saved context

### Command Palette
- `AIOS: Reset Context` - Reset conversation context
- `AIOS: Save Context` - Save current context
- `AIOS: Load Context` - Load saved context
- `AIOS: Show System Status` - Display AIOS system status

## Configuration

### Settings
```json
{
  "aios.core.enabled": true,
  "aios.context.persistAcrossRestarts": true,
  "aios.context.maxHistorySize": 1000,
  "aios.ai.pythonPath": "",
  "aios.ai.corePath": "",
  "aios.debug.enabled": false
}
```

## Architecture

### Components
```
vscode-extension/
├── src/
│   ├── extension.ts          # Main extension entry point
│   ├── chatParticipant.ts    # VSCode chat integration
│   ├── contextManager.ts     # Persistent context management
│   ├── aiosBridge.ts         # AIOS communication bridge
│   └── logger.ts             # Logging and debugging
├── package.json              # Extension manifest
└── dist/                     # Compiled output
```

### Context Flow
```
User Input → Chat Participant → Context Manager → AIOS Bridge → AI Modules
                ↓                      ↓              ↓
            VSCode UI ←─── Response ←─── Context ←─── AI Response
```

## Benefits

### Immediate
- ✅ **No Context Loss**: Eliminates chat iteration reset problem
- ✅ **Seamless Experience**: Natural conversation flow
- ✅ **Professional Integration**: Native VSCode chat experience

### Advanced
- 🔄 **Learning Persistence**: AI learns across sessions
- 🧠 **Multi-Language AI**: Coordinated C++/Python/C# intelligence
- ⚡ **Performance**: Optimized context management

## Development

### Build
```bash
npm run compile        # Compile TypeScript
npm run watch         # Watch mode compilation
npm run lint          # ESLint checking
```

### Testing
```bash
npm test              # Run tests
```

### Debug
1. Open extension project in VSCode
2. Press `F5` to launch Extension Development Host
3. Test extension in new VSCode window

## Integration with AIOS

This extension serves as the bridge between VSCode and the AIOS ecosystem:

### AIOS Components
- **C++ Core**: High-performance system kernel
- **Python AI**: NLP, prediction, automation, learning modules
- **C# Interface**: Desktop UI and service layer

### Communication
- **Bridge Pattern**: Clean abstraction between VSCode and AIOS
- **Service Integration**: Direct connection to AIOS services
- **Context Synchronization**: Bidirectional context sharing

## Troubleshooting

### Common Issues

**Extension not activating**
- Check VSCode version compatibility (requires 1.95.0+)
- Verify extension is enabled in Extensions panel

**Context not persisting**
- Check setting: `aios.context.persistAcrossRestarts`
- Verify VSCode global state access

**AIOS connection issues**
- Check AIOS core and AI modules are running
- Review AIOS logs in Output panel
- Use `@aios /status` to check system health

### Debug Mode
Enable debug logging:
```json
{
  "aios.debug.enabled": true
}
```

View logs in Output panel → "AIOS"

## Roadmap

### Phase 1 (Current)
- [x] Basic chat participant
- [x] Context persistence
- [x] AIOS bridge foundation

### Phase 2
- [ ] Full AIOS integration
- [ ] Advanced AI features
- [ ] Workspace intelligence

### Phase 3
- [ ] Code generation
- [ ] Multi-modal support
- [ ] Plugin ecosystem

## Contributing

This extension is part of the AIOS project. See main project documentation for contribution guidelines.

---

**AIOS VSCode Extension** - Bridging AI and Development
