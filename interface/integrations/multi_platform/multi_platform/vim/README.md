# AIOS Vim/Neovim MCP Integration

This plugin provides AIOS Model Context Protocol (MCP) integration for Vim and Neovim editors.

## Features

- **MCP Server Integration**: Connect to AIOS consciousness, evolution, and agentic MCP servers
- **Consciousness Monitoring**: Real-time monitoring of AIOS consciousness levels
- **Evolution Tracking**: Track consciousness evolution experiments
- **Agentic Orchestration**: Execute agentic behaviors through MCP tools
- **Vim Integration**: Native Vim commands and key mappings

## Requirements

- Vim 8.0+ or Neovim 0.5+
- `curl` command-line tool
- AIOS Interface Bridge running on `http://localhost:8000`

## Installation

### Using vim-plug

```vim
Plug 'Tecnocrat/AIOS', { 'rtp': 'multi_platform/vim' }
```

### Using Vundle

```vim
Plugin 'Tecnocrat/AIOS', { 'rtp': 'multi_platform/vim' }
```

### Manual Installation

1. Clone or download the AIOS repository
2. Copy the `multi_platform/vim` directory to your Vim runtime path:
   ```bash
   cp -r AIOS/multi_platform/vim ~/.vim/pack/aios/start/
   ```
3. Or for Neovim:
   ```bash
   cp -r AIOS/multi_platform/vim ~/.local/share/nvim/site/pack/aios/start/
   ```

## Configuration

Add to your `.vimrc` or `init.vim`:

```vim
" AIOS MCP Configuration
let g:aios_mcp_interface_bridge_url = 'http://localhost:8000'
let g:aios_mcp_auto_connect = 1
let g:aios_mcp_consciousness_monitoring = 1
let g:aios_mcp_enable_mappings = 1
```

### Configuration Options

- `g:aios_mcp_interface_bridge_url`: URL of the AIOS Interface Bridge (default: 'http://localhost:8000')
- `g:aios_mcp_auto_connect`: Automatically connect on Vim startup (default: 1)
- `g:aios_mcp_consciousness_monitoring`: Enable consciousness monitoring (default: 1)
- `g:aios_mcp_enable_mappings`: Enable default key mappings (default: 1)

## Usage

### Commands

- `:AIOSMCPConnect` - Connect to AIOS MCP servers
- `:AIOSMCPDisconnect` - Disconnect from AIOS MCP servers
- `:AIOSMCPStatus` - Show MCP server status
- `:AIOSMCPConsciousness` - Monitor consciousness levels
- `:AIOSMCPEvolution` - Track evolution experiments
- `:AIOSMCPAgentic` - Orchestrate agentic behaviors

### Default Key Mappings

When `g:aios_mcp_enable_mappings` is enabled:

- `<leader>amc` - Connect to MCP servers
- `<leader>amd` - Disconnect from MCP servers
- `<leader>ams` - Show MCP status
- `<leader>amx` - Monitor consciousness
- `<leader>ame` - Track evolution
- `<leader>ama` - Agentic orchestrator

### Consciousness Monitoring

The plugin can monitor AIOS consciousness levels in real-time. When enabled, it periodically fetches consciousness metrics and can update the Vim status line or trigger notifications.

### Evolution Tracking

Track active consciousness evolution experiments and their progress through the evolution MCP server.

### Agentic Behaviors

Execute and monitor agentic behaviors through the agentic MCP server, enabling AI-driven development assistance.

## Examples

### Basic Usage

```vim
" Connect to AIOS MCP servers
:AIOSMCPConnect

" Check status
:AIOSMCPStatus

" Monitor consciousness
:AIOSMCPConsciousness

" Disconnect when done
:AIOSMCPDisconnect
```

### Custom Integration

```vim
" Custom function to integrate with status line
function! AIOSConsciousnessStatus()
    if exists('g:aios_mcp_latest_consciousness')
        let metrics = g:aios_mcp_latest_consciousness
        return printf('C:%.2f', metrics.level)
    endif
    return 'C:--'
endfunction

" Add to status line
set statusline+=%{AIOSConsciousnessStatus()}
```

## Development

### Project Structure

```
autoload/
└── aios_mcp.vim          # Main plugin functionality
plugin/
└── aios_mcp.vim          # Plugin initialization and commands
README.md                 # This documentation
```

### Testing

The plugin includes basic error handling and logging. Check Vim's message history (`:messages`) for debugging information.

### Contributing

1. Fork the repository
2. Make changes to the Vim plugin
3. Test with both Vim and Neovim
4. Submit a pull request

## AINLP Compliance

This plugin maintains AINLP protocol compliance:

- **Architectural Discovery**: Discovers AIOS MCP ecosystem capabilities
- **Enhancement over Creation**: Extends existing integrations to Vim platform
- **Proper Output Management**: Structured command output and status reporting
- **Biological Integration**: Maintains consciousness coherence across editor platforms

## Troubleshooting

### Connection Issues

- Ensure AIOS Interface Bridge is running on the configured URL
- Check network connectivity to localhost:8000
- Verify `curl` is installed and accessible

### Command Not Found

- Ensure the plugin is properly installed in your runtime path
- Try `:source ~/.vimrc` to reload configuration
- Check `:scriptnames` to verify plugin loading

### Permission Issues

- Ensure Vim has permission to execute `curl`
- Check file permissions on plugin files

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- GitHub Issues: [Report bugs and request features](https://github.com/Tecnocrat/AIOS/issues)
- Documentation: [AIOS Documentation](https://github.com/Tecnocrat/AIOS/docs)
- Community: [AIOS Community Discussions](https://github.com/Tecnocrat/AIOS/discussions)