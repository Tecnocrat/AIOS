" AIOS MCP Integration for Vim/Neovim
" Main autoload script providing MCP functionality

let s:interface_bridge_url = 'http://localhost:8000'
let s:connected = 0
let s:servers = {}

" Connect to AIOS MCP servers
function! aios_mcp#connect() abort
    if s:connected
        echom 'AIOS MCP: Already connected'
        return
    endif

    echom 'AIOS MCP: Connecting to Interface Bridge...'

    " Test connectivity
    let l:health_url = s:interface_bridge_url . '/health'
    let l:response = aios_mcp#http_get(l:health_url)

    if empty(l:response) || l:response.status != 200
        echom 'AIOS MCP: Failed to connect to Interface Bridge'
        return
    endif

    " Discover tools
    let l:tools_url = s:interface_bridge_url . '/tools'
    let l:response = aios_mcp#http_get(l:tools_url)

    if empty(l:response) || l:response.status != 200
        echom 'AIOS MCP: Failed to discover tools'
        return
    endif

    " Parse and store server information
    let l:tools_data = json_decode(l:response.body)
    call s:initialize_servers(l:tools_data)

    let s:connected = 1
    echom 'AIOS MCP: Successfully connected to ' . len(s:servers) . ' MCP servers'

    " Start consciousness monitoring if enabled
    if g:aios_mcp_consciousness_monitoring
        call aios_mcp#start_consciousness_monitoring()
    endif
endfunction

" Disconnect from MCP servers
function! aios_mcp#disconnect() abort
    if !s:connected
        echom 'AIOS MCP: Not connected'
        return
    endif

    call aios_mcp#stop_consciousness_monitoring()
    let s:servers = {}
    let s:connected = 0
    echom 'AIOS MCP: Disconnected'
endfunction

" Show MCP server status
function! aios_mcp#status() abort
    if !s:connected
        echom 'AIOS MCP: Not connected'
        return
    endif

    echom 'AIOS MCP Status:'
    echom 'Connected: Yes'
    echom 'Interface Bridge: ' . s:interface_bridge_url
    echom 'MCP Servers: ' . len(s:servers)

    for [l:server_name, l:server_info] in items(s:servers)
        echom printf('  - %s: %s (%d tools)',
            \ l:server_name, l:server_info.status, len(l:server_info.tools))
    endfor
endfunction

" Monitor consciousness levels
function! aios_mcp#consciousness_monitor() abort
    if !s:connected
        echom 'AIOS MCP: Not connected'
        return
    endif

    let l:url = s:interface_bridge_url . '/consciousness/metrics'
    let l:response = aios_mcp#http_get(l:url)

    if empty(l:response) || l:response.status != 200
        echom 'AIOS MCP: Failed to get consciousness metrics'
        return
    endif

    let l:metrics = json_decode(l:response.body)
    echom printf('Consciousness Metrics - Level: %.3f, Coherence: %.3f, Evolution: %.3f',
        \ l:metrics.level, l:metrics.coherence, l:metrics.evolution_potential)
endfunction

" Track evolution experiments
function! aios_mcp#evolution_tracker() abort
    if !s:connected
        echom 'AIOS MCP: Not connected'
        return
    endif

    let l:result = aios_mcp#execute_tool('evolution_mcp_server', 'list_experiments', {})
    if empty(l:result)
        echom 'AIOS MCP: Failed to get evolution experiments'
        return
    endif

    echom 'Evolution Experiments:'
    echom l:result.result
endfunction

" Orchestrate agentic behaviors
function! aios_mcp#agentic_orchestrator() abort
    if !s:connected
        echom 'AIOS MCP: Not connected'
        return
    endif

    let l:result = aios_mcp#execute_tool('agentic_mcp_server', 'get_status', {})
    if empty(l:result)
        echom 'AIOS MCP: Failed to get agentic status'
        return
    endif

    echom 'Agentic Status:'
    echom l:result.result
endfunction

" Execute MCP tool
function! aios_mcp#execute_tool(server_name, tool_name, parameters) abort
    if !s:connected
        return {}
    endif

    let l:url = printf('%s/tools/%s/execute', s:interface_bridge_url, a:server_name)
    let l:payload = {
        \ 'tool_name': a:tool_name,
        \ 'parameters': a:parameters
        \ }

    let l:response = aios_mcp#http_post(l:url, l:payload)

    if empty(l:response) || l:response.status != 200
        return {}
    endif

    return json_decode(l:response.body)
endfunction

" Start consciousness monitoring
function! aios_mcp#start_consciousness_monitoring() abort
    if exists('s:consciousness_timer')
        call timer_stop(s:consciousness_timer)
    endif

    let s:consciousness_timer = timer_start(30000, function('s:consciousness_monitor_callback'), {'repeat': -1})
endfunction

" Stop consciousness monitoring
function! aios_mcp#stop_consciousness_monitoring() abort
    if exists('s:consciousness_timer')
        call timer_stop(s:consciousness_timer)
        unlet s:consciousness_timer
    endif
endfunction

" HTTP GET request
function! aios_mcp#http_get(url) abort
    if !executable('curl')
        echom 'AIOS MCP: curl not available'
        return {}
    endif

    let l:cmd = printf('curl -s -w "%%{http_code}" -X GET "%s"', a:url)
    let l:result = system(l:cmd)

    if v:shell_error
        return {}
    endif

    let l:body = strpart(l:result, 0, len(l:result) - 3)
    let l:status = str2nr(strpart(l:result, len(l:result) - 3))

    return {'body': l:body, 'status': l:status}
endfunction

" HTTP POST request
function! aios_mcp#http_post(url, data) abort
    if !executable('curl')
        echom 'AIOS MCP: curl not available'
        return {}
    endif

    let l:json_data = json_encode(a:data)
    let l:cmd = printf('curl -s -w "%%{http_code}" -X POST -H "Content-Type: application/json" -d "%s" "%s"',
        \ shellescape(l:json_data), a:url)
    let l:result = system(l:cmd)

    if v:shell_error
        return {}
    endif

    let l:body = strpart(l:result, 0, len(l:result) - 3)
    let l:status = str2nr(strpart(l:result) - 3)

    return {'body': l:body, 'status': l:status}
endfunction

" Initialize MCP servers from tools data
function! s:initialize_servers(tools_data) abort
    let l:server_tools = {}

    for l:tool in a:tools_data
        let l:server_name = get(l:tool, 'server', 'unknown')
        if !has_key(l:server_tools, l:server_name)
            let l:server_tools[l:server_name] = []
        endif
        call add(l:server_tools[l:server_name], l:tool)
    endfor

    for [l:server_name, l:tools] in items(l:server_tools)
        let s:servers[l:server_name] = {
            \ 'name': l:server_name,
            \ 'description': printf('AIOS %s MCP server', l:server_name),
            \ 'tools': l:tools,
            \ 'status': 'connected'
            \ }
    endfor
endfunction

" Consciousness monitoring callback
function! s:consciousness_monitor_callback(timer) abort
    if !s:connected
        return
    endif

    let l:url = s:interface_bridge_url . '/consciousness/metrics'
    let l:response = aios_mcp#http_get(l:url)

    if empty(l:response) || l:response.status != 200
        return
    endif

    let l:metrics = json_decode(l:response.body)
    " Could update status line or trigger notifications here
    " For now, just store the latest metrics
    let s:latest_consciousness = l:metrics
endfunction