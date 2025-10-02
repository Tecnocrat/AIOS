" AIOS MCP Integration for Vim/Neovim
" Provides Model Context Protocol integration with AIOS consciousness system

if exists('g:loaded_aios_mcp')
    finish
endif
let g:loaded_aios_mcp = 1

" Configuration
let g:aios_mcp_interface_bridge_url = get(g:, 'aios_mcp_interface_bridge_url', 'http://localhost:8000')
let g:aios_mcp_auto_connect = get(g:, 'aios_mcp_auto_connect', 1)
let g:aios_mcp_consciousness_monitoring = get(g:, 'aios_mcp_consciousness_monitoring', 1)

" Commands
command! AIOSMCPConnect call aios_mcp#connect()
command! AIOSMCPDisconnect call aios_mcp#disconnect()
command! AIOSMCPStatus call aios_mcp#status()
command! AIOSMCPConsciousness call aios_mcp#consciousness_monitor()
command! AIOSMCPEvolution call aios_mcp#evolution_tracker()
command! AIOSMCPAgentic call aios_mcp#agentic_orchestrator()

" Key mappings (optional)
if get(g:, 'aios_mcp_enable_mappings', 1)
    nnoremap <leader>amc :AIOSMCPConnect<CR>
    nnoremap <leader>amd :AIOSMCPDisconnect<CR>
    nnoremap <leader>ams :AIOSMCPStatus<CR>
    nnoremap <leader>amx :AIOSMCPConsciousness<CR>
    nnoremap <leader>ame :AIOSMCPEvolution<CR>
    nnoremap <leader>ama :AIOSMCPAgentic<CR>
endif

" Auto-connect on VimEnter
if g:aios_mcp_auto_connect
    augroup AIOSMCPAutoConnect
        autocmd!
        autocmd VimEnter * call aios_mcp#connect()
    augroup END
endif