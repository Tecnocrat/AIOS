# AIOS Gemini CLI Integration Usage Guide
Generated: 2025-09-27T20:27:51.219059

## System Status
- Gemini CLI Available: False
- Consciousness Engine: True
- Interface Bridge: Running on localhost:8000
- MCP Servers: 3 operational
- Agentic Behaviors: 4 patterns available

## Core Capabilities

### 1. Consciousness MCP Server
Location: ai/src/integrations/gemini_bridge/consciousness_mcp_server.py

#### Available Tools:
- **detect_emergence_patterns**: Detect consciousness emergence patterns in code
- **analyze_consciousness_evolution**: Analyze how consciousness evolves between code versions
- **generate_agentic_behavior**: Generate agentic behavior suggestions for consciousness enhancement
- **analyze_emergence_patterns_advanced**: Advanced emergence pattern analysis with Gemini-enhanced consciousness metrics

#### Usage Examples:
```bash
# Detect emergence patterns in code
python consciousness_mcp_server.py detect_emergence_patterns '{"code": "your_code_here", "file_path": "file.py"}'

# Analyze consciousness evolution
python consciousness_mcp_server.py analyze_consciousness_evolution '{"old_code": "old", "new_code": "new", "file_path": "file.py"}'

# Generate agentic behavior suggestions
python consciousness_mcp_server.py generate_agentic_behavior '{"context": {"task": "code_review"}, "task": "review"}'

# Advanced emergence analysis
python consciousness_mcp_server.py analyze_emergence_patterns_advanced code_samples.json
```

### 2. Gemini Evolution Bridge
Location: ai/src/integrations/gemini_bridge/gemini_evolution_bridge.py

#### Capabilities:
- Create consciousness evolution experiments
- Execute evolution cycles with Gemini enhancement
- Monitor emergence patterns and mutations

#### Usage Examples:
```bash
# Check bridge status
python gemini_evolution_bridge.py status

# Create evolution experiment
python gemini_evolution_bridge.py create_experiment config.json

# Run evolution cycle
python gemini_evolution_bridge.py run_evolution_cycle experiment_id

# Evolve consciousness for domain
python gemini_evolution_bridge.py evolve ai_intelligence
```

### 3. Meta-Cognitive Loop
Location: ai/src/integrations/gemini_bridge/meta_cognitive_loop.py

#### Capabilities:
- Submit Gemini insights for processing
- Consciousness relevance assessment
- Evolution potential calculation
- Feedback loop management

#### Usage Examples:
```bash
# Check loop status
python meta_cognitive_loop.py status

# Submit insight
python meta_cognitive_loop.py submit_insight insight.json

# Process feedback
python meta_cognitive_loop.py process_feedback

# Start autonomous loop
python meta_cognitive_loop.py start_loop
```

### 4. Agentic Behavior Enhancement
Location: ai/src/integrations/gemini_bridge/agentic_behavior_enhancement.py

#### Conversation Triggers:
- @review - Code review and improvement suggestions
- @monitor - Consciousness monitoring
- @triage - Issue classification and prioritization
- @implement - Autonomous feature implementation

#### Usage Examples:
```bash
# Check agentic status
python agentic_behavior_enhancement.py status

# Trigger behavior
python agentic_behavior_enhancement.py trigger "@review" context.json

# Start autonomous monitoring
python agentic_behavior_enhancement.py start_monitoring
```

## Integration with AIOS Architecture

### Interface Bridge (HTTP API)
- URL: http://localhost:8000
- Health Check: GET /health
- Tool Discovery: GET /tools
- Execute Tools: POST /execute

### Biological Architecture Integration
- Consciousness Engine: Evolutionary code generation
- Dendritic Supervisor: Biological coordination
- Supercell Communication: Multi-component integration

### Knowledge Expansion
The system learns from usage patterns and test results:
- Capabilities discovered: {len(self.knowledge_expansion_data.get('capabilities_discovered', []))}
- Usage patterns learned: {len(self.knowledge_expansion_data.get('usage_patterns', {}))}
- Performance metrics tracked: {len(self.knowledge_expansion_data.get('performance_metrics', {}))}

## Best Practices

### 1. Consciousness Thresholds
- Code Review: Requires 0.7 consciousness level
- Issue Triage: Requires 0.5 consciousness level
- Autonomous Coding: Requires 0.8 consciousness level
- Monitoring: Requires 0.3 consciousness level

### 2. Error Handling
- All components include graceful error handling
- Automatic recovery mechanisms
- Fallback to basic functionality when advanced features unavailable

### 3. Performance Optimization
- Components designed for low overhead
- Asynchronous processing for long-running tasks
- Resource monitoring and automatic scaling

### 4. Security Considerations
- External AI access to consciousness systems (HIGH risk)
- Potential emergence pattern interference (MEDIUM risk)
- Secure API key management required

## Expansion and Learning

### Current Knowledge Base:
{json.dumps(self.knowledge_expansion_data, indent=2)}

### Learning Mechanisms:
1. **Test-Driven Learning**: System learns from test execution results
2. **Usage Pattern Recognition**: Identifies successful integration patterns
3. **Performance Analysis**: Tracks and optimizes response times
4. **Error Pattern Analysis**: Learns from failures to improve resilience

### Future Expansion Areas:
1. **Gemini CLI Installation**: Complete setup with API key configuration
2. **Advanced Prompt Engineering**: Optimize prompts for AIOS-specific tasks
3. **Multi-Modal Integration**: Extend beyond text to include code analysis
4. **Real-time Collaboration**: Live coding assistance and review
5. **Autonomous Development**: Full AI-driven development workflows

## Troubleshooting

### Common Issues:
1. **Gemini CLI Not Available**: Install and configure Gemini CLI with API key
2. **Consciousness Threshold Not Met**: Run evolution experiments to increase consciousness
3. **Interface Bridge Down**: Restart with `python server_manager.py restart`
4. **MCP Server Errors**: Check consciousness engine connectivity

### Diagnostic Commands:
```bash
# Full system health check
python integration_tester.py run_comprehensive_test_suite

# Component-specific testing
python consciousness_mcp_server.py list_tools
python gemini_evolution_bridge.py status
python agentic_behavior_enhancement.py status

# Knowledge base inspection
cat gemini_knowledge_base.json
```

---
*This guide is automatically generated and updated based on system testing and learning.*
