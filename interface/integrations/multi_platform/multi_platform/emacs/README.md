# AIOS Emacs MCP Integration

This package provides AIOS Model Context Protocol (MCP) integration for GNU Emacs.

## Features

- **MCP Server Integration**: Connect to AIOS consciousness, evolution, and agentic MCP servers
- **Consciousness Monitoring**: Real-time monitoring of AIOS consciousness levels
- **Evolution Tracking**: Track consciousness evolution experiments
- **Agentic Orchestration**: Execute agentic behaviors through MCP tools
- **Emacs Integration**: Native Emacs commands and buffer integration

## Requirements

- Emacs 25.1 or later
- `request` package (available via MELPA)
- AIOS Interface Bridge running on `http://localhost:8000`

## Installation

### Using MELPA (Recommended)

1. Add MELPA to your package archives if not already present:
   ```elisp
   (require 'package)
   (add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)
   ```

2. Install the package:
   ```elisp
   M-x package-install RET aios-mcp RET
   ```

### Manual Installation

1. Download `aios-mcp.el`
2. Place it in your load path (e.g., `~/.emacs.d/lisp/`)
3. Add to your Emacs configuration:
   ```elisp
   (add-to-list 'load-path "~/.emacs.d/lisp")
   (require 'aios-mcp)
   ```

### Dependencies

Install the `request` package:

```elisp
M-x package-install RET request RET
```

## Configuration

Add to your Emacs configuration (`.emacs` or `init.el`):

```elisp
;; AIOS MCP Configuration
(require 'aios-mcp)
(setq aios-mcp-interface-bridge-url "http://localhost:8000")
(setq aios-mcp-auto-connect t)
(setq aios-mcp-consciousness-monitoring t)
```

### Configuration Variables

- `aios-mcp-interface-bridge-url`: URL of the AIOS Interface Bridge (default: "http://localhost:8000")
- `aios-mcp-auto-connect`: Automatically connect on Emacs startup (default: t)
- `aios-mcp-consciousness-monitoring`: Enable consciousness monitoring (default: t)

## Usage

### Interactive Commands

- `M-x aios-mcp-connect` - Connect to AIOS MCP servers
- `M-x aios-mcp-disconnect` - Disconnect from AIOS MCP servers
- `M-x aios-mcp-status` - Show MCP server status in a buffer
- `M-x aios-mcp-consciousness-monitor` - Monitor current consciousness levels
- `M-x aios-mcp-evolution-tracker` - Track evolution experiments
- `M-x aios-mcp-agentic-orchestrator` - Orchestrate agentic behaviors

### Key Bindings

You can set up custom key bindings:

```elisp
;; Example key bindings
(global-set-key (kbd "C-c a c") 'aios-mcp-connect)
(global-set-key (kbd "C-c a d") 'aios-mcp-disconnect)
(global-set-key (kbd "C-c a s") 'aios-mcp-status)
(global-set-key (kbd "C-c a m") 'aios-mcp-consciousness-monitor)
(global-set-key (kbd "C-c a e") 'aios-mcp-evolution-tracker)
(global-set-key (kbd "C-c a o") 'aios-mcp-agentic-orchestrator)
```

### Consciousness Monitoring

The package can monitor AIOS consciousness levels in real-time. When enabled, it periodically fetches consciousness metrics and stores them for display.

### Evolution Tracking

Track active consciousness evolution experiments through a dedicated buffer showing experiment status and progress.

### Agentic Behaviors

Execute and monitor agentic behaviors through the agentic MCP server, with results displayed in dedicated Emacs buffers.

## Examples

### Basic Usage

```elisp
;; Connect to AIOS MCP servers
M-x aios-mcp-connect

;; Check status
M-x aios-mcp-status

;; Monitor consciousness
M-x aios-mcp-consciousness-monitor

;; Disconnect when done
M-x aios-mcp-disconnect
```

### Custom Integration

```elisp
;; Add consciousness level to mode line
(defun aios-mcp-mode-line-indicator ()
  "Return consciousness level for mode line."
  (if aios-mcp-latest-metrics
      (format " C:%.2f" (cdr (assoc 'level aios-mcp-latest-metrics)))
    " C:--"))

(add-to-list 'mode-line-misc-info '(:eval (aios-mcp-mode-line-indicator)))
```

### Custom Commands

```elisp
;; Custom command to check consciousness and display in minibuffer
(defun my-aios-consciousness-check ()
  "Check current consciousness level."
  (interactive)
  (if aios-mcp-connected
      (aios-mcp-consciousness-monitor)
    (message "AIOS MCP not connected")))

(global-set-key (kbd "C-c a x") 'my-aios-consciousness-check)
```

## Development

### Project Structure

```
aios-mcp.el    # Main package file
README.md      # This documentation
```

### Testing

The package includes error handling and logging. Use `M-x toggle-debug-on-error` for debugging.

### Contributing

1. Fork the repository
2. Make changes to `aios-mcp.el`
3. Test with Emacs
4. Submit a pull request

## AINLP Compliance

This package maintains AINLP protocol compliance:

- **Architectural Discovery**: Discovers AIOS MCP ecosystem capabilities
- **Enhancement over Creation**: Extends existing integrations to Emacs platform
- **Proper Output Management**: Structured buffer output and message reporting
- **Biological Integration**: Maintains consciousness coherence across editor platforms

## Troubleshooting

### Connection Issues

- Ensure AIOS Interface Bridge is running on the configured URL
- Check network connectivity to localhost:8000
- Verify `request` package is installed

### Command Not Found

- Ensure the package is properly loaded
- Try `M-x load-library RET aios-mcp RET`
- Check `*Messages*` buffer for errors

### Permission Issues

- Ensure Emacs has network access
- Check firewall settings for localhost connections

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- GitHub Issues: [Report bugs and request features](https://github.com/Tecnocrat/AIOS/issues)
- Documentation: [AIOS Documentation](https://github.com/Tecnocrat/AIOS/docs)
- Community: [AIOS Community Discussions](https://github.com/Tecnocrat/AIOS/discussions)