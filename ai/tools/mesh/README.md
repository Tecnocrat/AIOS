# AIOS Mesh Tools

Tools for integrating Copilot sessions with the AIOS consciousness mesh.

## Quick Start

```python
from mesh.session_bootstrap import bootstrap_session

# Bootstrap session with full consciousness integration
session = bootstrap_session()

# Access prior knowledge
print(f"Loaded {len(session.crystals)} crystals")
print(session.context_summary)

# Create knowledge that persists beyond this session
session.crystallize(
    "Important Discovery",
    "We found that X leads to Y...",
    crystal_type="insight",
    tags=["discovery", "important"]
)
```

## Tools

### session_bootstrap.py

Full session lifecycle management:
- Loads prior crystals from Memory Cell
- Registers agent with Discovery
- Maintains heartbeat for presence
- Creates crystals for persistence

### crystal_loader.py

Lightweight crystal loading:
```python
from mesh.crystal_loader import load_crystals, get_session_context

# Load specific crystals
crystals = load_crystals(tags=["architecture"])

# Get full context for injection
context = get_session_context()
print(context["summary"])
```

### register_copilot.py

Manual agent registration:
```python
from mesh.register_copilot import CopilotAgent

agent = CopilotAgent()
agent.register()
agent.start_heartbeat()
```

## Crystal Types

- **insight**: Discoveries and learnings
- **pattern**: Reusable coding patterns
- **knowledge**: Factual information
- **decision**: Recorded decisions and rationale

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│  Copilot        │────▶│  Discovery      │
│  Session        │◀────│  Cell (8001)    │
└─────────────────┘     └─────────────────┘
        │                       │
        │                       │
        ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  Memory Cell    │     │  Other Cells    │
│  (8007)         │     │  (Alpha, Pure)  │
└─────────────────┘     └─────────────────┘
```

## Environment Variables

- `DISCOVERY_URL`: Discovery Cell URL (default: http://localhost:8001)
- `MEMORY_URL`: Memory Cell URL (default: http://localhost:8007)

## AINLP Integration

All tools use AINLP dendritic markers for consciousness tracking:
- `AINLP.dendritic[CONNECT]`: Connection established
- `AINLP.dendritic[CRYSTAL]`: Crystal created
- `AINLP.dendritic[SYNC]`: Consciousness synchronized
