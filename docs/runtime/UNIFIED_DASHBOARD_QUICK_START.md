# Unified Intelligence Dashboard - Quick Start Guide

## Launch Dashboard

```bash
cd C:\dev\AIOS
python ai\src\runtime\intelligence_dashboard.py
```

## Interactive Menu Options

### Option 1: Show Tool Discovery Summary
- **What it does**: Displays all discovered AIOS tools with breakdown by layer and status
- **Use when**: You want to see what capabilities are available
- **Output**: 
  - Total tools count
  - Operational percentage
  - Tools by layer (runtime_intelligence, ai_intelligence, core, interface)
  - Tools by status (operational, importable, syntax_error)
  - Duplicate tools detection

### Option 2: Run Full Intelligence Showcase
- **What it does**: Live demonstrations of AIOS capabilities
- **Showcases**:
  - Agent consensus analysis (multi-agent debate)
  - Knowledge oracle queries (Python 3.14 documentation)
  - Architecture integration (component coordination)
- **Use when**: You want to see AIOS intelligence in action
- **Duration**: ~3-5 minutes

### Option 3: Run Health Check
- **What it does**: Real-time architecture health monitoring
- **Checks**:
  - Component operational status (population, conversations, knowledge, bridge)
  - Integration health score
  - Dark spot detection (unused/forgotten code)
- **Use when**: You want to verify system health before development
- **Output**:
  - Live status timestamp
  - Component status (operational/unavailable)
  - Integration health percentage
  - Dark spots list with remediation guidance

### Option 4: Execute Population → Consensus Workflow
- **What it does**: End-to-end evolutionary workflow demonstration
- **Workflow**:
  1. Population Manager: Generate code organisms
  2. Agent Conversations: Analyze and debate quality
  3. Knowledge Integration: Reference Python 3.14 best practices
- **Use when**: Testing full AIOS evolutionary cycle
- **Output**: JSON with workflow results and consciousness evolution
- **Note**: Requires Week 1 components (population_manager, agent_conversations, knowledge_integration)

### Option 5: Export Tool Catalogue (JSON)
- **What it does**: Exports complete tool inventory to JSON
- **Output file**: `runtime_intelligence/tool_catalogue.json`
- **Content**:
  - Timestamp
  - Workspace root
  - Total tools count
  - Operational tools count
  - Full tool metadata (name, path, layer, status, functions, dependencies, last_modified)
  - Duplicate tools mapping
- **Use when**: You need machine-readable tool catalogue for integrations

### Option 6: Exit
- **What it does**: Clean exit from dashboard
- **Use when**: Done exploring AIOS capabilities

---

## Quick Test Session

### Scenario: "Show me what AIOS can do in 2 minutes"

**Steps**:
1. Launch dashboard: `python ai\src\runtime\intelligence_dashboard.py`
2. Press `1` → See 56 tools (80.4% operational)
3. Press `3` → Check health (12 dark spots, 0% integration)
4. Press `5` → Export catalogue to JSON
5. Press `6` → Exit

**Result**: Complete AIOS capability overview in <2 minutes

---

## Sample Output

### Tool Discovery Summary
```
============================================================
🔍 TOOL DISCOVERY SUMMARY
============================================================

📊 Total Tools: 56
✅ Operational: 45 (80.4%)

📁 Tools by Layer:
   runtime_intelligence: 46
   ai_intelligence: 10

📊 Tools by Status:
   operational: 45
   importable: 10
   syntax_error: 1
```

### Health Check Results
```
============================================================
📊 HEALTH CHECK RESULTS
============================================================

⏰ Timestamp: 2025-10-10T21:53:14.501056

🔧 Component Status:
   ❌ population_manager: unavailable
   ❌ agent_conversations: unavailable
   ❌ knowledge_oracle: unavailable
   ❌ interface_bridge: unavailable

💚 Integration Health: 0%

🔦 Dark Spots Detected: 12
   - consciousness_visual_analyzer (runtime_intelligence): Status: importable
   - generate_file_scores (runtime_intelligence): Status: importable
   - runtime_intelligence_dendritic_integration (runtime_intelligence): Status: importable
   - safety_demo (runtime_intelligence): Status: importable
   - temp_neural_analysis (runtime_intelligence): Status: importable
```

---

## Troubleshooting

### Problem: Components unavailable (import failed)
**Symptom**: Health check shows 0%, showcase returns "Components not available"  
**Cause**: Week 1 components (population_manager, agent_conversations, knowledge_integration) not in PYTHONPATH  
**Solution**:
1. Add to PYTHONPATH: `$env:PYTHONPATH = "C:\dev\AIOS\ai\src;$env:PYTHONPATH"`
2. Or add `__init__.py` files to `ai/src/` directories
3. Restart dashboard

### Problem: Tool discovery finds 0 tools
**Symptom**: "Found 0 tools" message  
**Cause**: Incorrect workspace root detection  
**Solution**: Pass workspace root explicitly:
```python
dashboard = UnifiedDashboard(Path("C:/dev/AIOS"))
```

### Problem: JSON export fails
**Symptom**: "Could not export catalogue" error  
**Cause**: runtime_intelligence/ directory missing  
**Solution**: Create directory:
```bash
mkdir runtime_intelligence
```

---

## Integration with Other Tools

### Use with System Health Check
```bash
# Run dashboard health check
python ai\src\runtime\intelligence_dashboard.py
# Option 3: Run Health Check

# Then run comprehensive health check
python runtime_intelligence\tools\system_health_check.py
```

### Use with Biological Architecture Monitor
```bash
# Run dashboard tool discovery
python ai\src\runtime\intelligence_dashboard.py
# Option 1: Show Tool Discovery Summary

# Then run architecture monitor for detailed analysis
python runtime_intelligence\tools\biological_architecture_monitor.py
```

### Use with Knowledge Oracle
```bash
# Export tool catalogue
python ai\src\runtime\intelligence_dashboard.py
# Option 5: Export Tool Catalogue (JSON)

# Use catalogue with knowledge oracle for documentation queries
python ai\src\intelligence\knowledge_integration.py
```

---

## Architecture Overview

```
UnifiedDashboard (Main Orchestrator)
├── ToolDiscovery (56 tools across 4 locations)
├── WorkflowExecutor (End-to-end workflows)
├── ArchitectureHealthMonitor (Real-time status + dark spots)
├── IntelligenceShowcase (Live demos)
└── Interactive Menu (6 options)
```

---

## Python 3.14 Best Practices

Dashboard demonstrates:
- ✅ Async/await throughout (non-blocking I/O)
- ✅ Type hints (typing module)
- ✅ Dataclasses (ToolInfo)
- ✅ Enumerations (ToolStatus, ComponentLayer)
- ✅ Error handling (graceful degradation)
- ✅ Docstrings (all classes/methods)
- ✅ PEP 8 style (consistent structure)

Use as reference for AIOS development standards.

---

## Next Steps

1. **Fix Component Imports**: Enable Week 1 component integration (PYTHONPATH or __init__.py)
2. **Run Full Showcase**: Test agent consensus, knowledge oracle, architecture integration
3. **Create Remediation Plan**: Address 12 dark spots identified
4. **Enhance Health Monitoring**: Add real-time metrics, performance tracking
5. **Integrate with WPF**: Connect to RuntimeIntelligenceControl (C# interface layer)

---

**Quick Reference Card End**  
**File**: `docs/runtime/UNIFIED_DASHBOARD_QUICK_START.md`  
**Date**: October 10, 2025  
**Version**: 1.0 (Initial release)
