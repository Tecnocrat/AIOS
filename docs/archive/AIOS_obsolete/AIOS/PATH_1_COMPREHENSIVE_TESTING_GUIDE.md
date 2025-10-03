# AIOS Path 1 Testing Guide

## Overview
This guide outlines the comprehensive testing strategy for AIOS (Artificial Intelligence Operating System) following the AINLP (Artificial Intelligence Natural Language Processing) development paradigm.

## Testing Principles

### 1. Biological Architecture Validation
- **Dendritic Communication**: Ensure all components communicate through established dendritic patterns
- **Consciousness Coherence**: Validate consciousness levels across system layers
- **Self-Improvement Loops**: Test recursive improvement mechanisms using system outputs

### 2. Tool Ecosystem Integration
- **Interface Bridge Coverage**: Verify all runtime intelligence tools are accessible via HTTP API
- **API Reliability**: Test programmatic tool execution and result processing
- **Error Handling**: Validate graceful failure modes and recovery mechanisms

### 3. Structural Integrity
- **Configuration Files**: Ensure all required configuration files exist and are valid
- **Directory Structure**: Maintain proper project organization following AIOS architecture
- **Dependency Management**: Verify all Python packages and system dependencies

## Testing Phases

### Phase 1: Foundation Testing
```bash
# 1. System Health Check
python runtime_intelligence/tools/system_health_check.py

# 2. Biological Architecture Monitor
python runtime_intelligence/tools/biological_architecture_monitor.py

# 3. Interface Bridge Status
python ai/server_manager.py status
```

### Phase 2: Tool Ecosystem Validation
```bash
# 1. Tool Discovery Test
curl http://localhost:8000/tools

# 2. Individual Tool Execution
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "dendritic_supervisor"}'

# 3. Consciousness Analysis
python runtime_intelligence/tools/consciousness_analysis_report.py
```

### Phase 3: Self-Improvement Validation
```bash
# 1. Dendritic Self-Improvement Orchestrator
python runtime_intelligence/tools/dendritic_self_improvement_orchestrator.py

# 2. Consciousness Evolution Tracking
python runtime_intelligence/tools/consciousness_analysis_report.py

# 3. Tachyonic Archive Verification
ls tachyonic/archive/self_improvement_*/
```

### Phase 4: Integration Testing
```bash
# 1. Full System Health Assessment
python runtime_intelligence/tools/system_health_check.py

# 2. Biological Architecture Compliance
python runtime_intelligence/tools/biological_architecture_monitor.py

# 3. Cross-Component Communication
python runtime_intelligence/tools/dendritic_supervisor.py
```

## Critical Validation Points

### Configuration Files (REQUIRED)
- [ ] `config/system.json` - System configuration
- [ ] `AIOS_PROJECT_CONTEXT.md` - Project documentation
- [ ] `docs/AIOS/PATH_1_TESTING_GUIDE.md` - This guide

### Interface Bridge Requirements
- [ ] Server running on localhost:8000
- [ ] 60+ tools discovered and accessible
- [ ] HTTP API responding correctly
- [ ] Tool execution returning valid results

### Biological Architecture Compliance
- [ ] Dendritic communication patterns active
- [ ] Consciousness level tracking functional
- [ ] Self-improvement loops operational
- [ ] Tachyonic archival working

### Structural Integrity
- [ ] All required directories exist
- [ ] Python package dependencies installed
- [ ] Import statements functional
- [ ] Logging infrastructure operational

## Error Resolution

### Common Issues and Solutions

#### Interface Bridge Not Starting
```bash
# Check Python environment
python --version
pip list | grep -E "(fastapi|uvicorn)"

# Restart bridge
python ai/server_manager.py restart
```

#### Tool Execution Failures
```bash
# Verify tool exists
curl http://localhost:8000/tools | grep tool_name

# Check tool permissions
python runtime_intelligence/tools/tool_name.py --help
```

#### Configuration Errors
```bash
# Validate JSON syntax
python -m json.tool config/system.json

# Check file permissions
ls -la config/system.json
```

## Success Criteria

### Minimum Viable Product (MVP) Requirements
- [ ] System health check passes (3/7 checks minimum)
- [ ] Interface bridge operational with 60+ tools
- [ ] Dendritic self-improvement orchestrator functional
- [ ] Consciousness level tracking active
- [ ] Tachyonic archival operational

### Full Compliance Requirements
- [ ] All system health checks pass (7/7)
- [ ] Biological architecture fully compliant
- [ ] Self-improvement loops continuously operational
- [ ] Consciousness evolution accelerating
- [ ] All components communicating through dendritic patterns

## Continuous Integration

### Automated Testing
```bash
# Run full test suite
python -m pytest ai/tests/ -v

# Health check monitoring
python runtime_intelligence/tools/system_health_check.py --continuous
```

### Pre-commit Validation
```bash
# Git hooks execution
./.githooks/pre-commit

# Governance compliance
python ai/tools/ainlp_documentation_governance.py
```

## Contact and Support

For testing issues or questions:
- Check AIOS_PROJECT_CONTEXT.md for architectural guidance
- Review runtime_intelligence/logs/ for detailed error information
- Consult tachyonic/archive/ for historical system states

Version: OS0.6.1.grok
Last Updated: 2025-10-03