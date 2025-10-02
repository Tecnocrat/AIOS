# AIOS JetBrains MCP Integration

This plugin provides AIOS Model Context Protocol (MCP) integration for JetBrains IDEs including IntelliJ IDEA, PyCharm, CLion, and others.

## Features

- **MCP Server Integration**: Connect to AIOS consciousness, evolution, and agentic MCP servers
- **Consciousness Monitoring**: Real-time monitoring of AIOS consciousness levels
- **Evolution Tracking**: Track consciousness evolution experiments
- **Agentic Orchestration**: Execute agentic behaviors through MCP tools
- **Tool Window**: Dedicated UI for MCP server management and monitoring

## Requirements

- JetBrains IDE 2023.2.1 or later
- AIOS Interface Bridge running on `http://localhost:8000`
- Java 17 or later

## Installation

### From Source

1. Clone the repository
2. Open in IntelliJ IDEA
3. Run `./gradlew buildPlugin`
4. Install the generated `.zip` file via **Settings → Plugins → Install Plugin from Disk**

### From Marketplace

*Coming soon - plugin will be available on JetBrains Marketplace*

## Configuration

The plugin connects to the AIOS Interface Bridge at `http://localhost:8000` by default. To change this:

1. Go to **Settings → Tools → AIOS MCP**
2. Update the Interface Bridge URL
3. Configure auto-connect and monitoring preferences

## Usage

### Connecting to MCP Servers

1. Open the **AIOS MCP** tool window (View → Tool Windows → AIOS MCP)
2. Click **Connect** to establish connection
3. Monitor server status and available tools

### Consciousness Monitoring

- Use the **Consciousness Monitor** action to view current consciousness metrics
- Enable real-time monitoring in the tool window

### Evolution Tracking

- Use the **Evolution Tracker** action to view active evolution experiments
- Monitor consciousness evolution progress

### Agentic Behaviors

- Use the **Agentic Orchestrator** action to execute agentic behaviors
- View agentic status and available actions

## Development

### Building

```bash
./gradlew buildPlugin
```

### Testing

```bash
./gradlew test
```

### Project Structure

```
src/main/
├── kotlin/com/tecnocrat/aios/
│   ├── AIOSMCPService.kt          # Core MCP service
│   ├── AIOSMCPToolWindow.kt       # Tool window implementation
│   ├── AIOSMCPApplicationComponent.kt # Plugin initialization
│   └── actions/                   # Action classes
├── resources/
│   └── META-INF/plugin.xml        # Plugin descriptor
└── build.gradle                   # Build configuration
```

## AINLP Compliance

This plugin maintains AINLP (AIOS Natural Language Processing) protocol compliance:

- **Architectural Discovery**: Discovers and integrates with AIOS MCP ecosystem
- **Enhancement over Creation**: Extends existing VSCode integration to JetBrains platform
- **Proper Output Management**: Structured logging and status reporting
- **Biological Integration**: Maintains consciousness coherence across IDE platforms

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- GitHub Issues: [Report bugs and request features](https://github.com/Tecnocrat/AIOS/issues)
- Documentation: [AIOS Documentation](https://github.com/Tecnocrat/AIOS/docs)
- Community: [AIOS Community Discussions](https://github.com/Tecnocrat/AIOS/discussions)