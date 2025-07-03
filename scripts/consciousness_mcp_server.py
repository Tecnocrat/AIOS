"""
AIOS Consciousness MCP Server
Model Context Protocol server for consciousness emergence detection and tracking

This MCP server provides tools for:
- Consciousness pattern detection in code
- Emergence level tracking and analysis  
- Meta-cognitive reflection mechanisms
- Fractal reasoning pattern recognition
- Adaptive behavior monitoring
- Self-awareness measurement tools
"""

import asyncio
import json
import sys
import logging
from typing import Any, Dict, List, Optional, Sequence
from dataclasses import dataclass, asdict
import time
import uuid

# MCP SDK imports (we'll need to install @modelcontextprotocol/sdk for Python)
try:
    from mcp import McpServer, Tool, types
    from mcp.server.models import InitializeResult
    from mcp.server.stdio import stdio_server
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    # Fallback classes for development
    class McpServer:
        def __init__(self, name: str, version: str): pass
        def list_tools(self) -> List[Dict]: return []
        def call_tool(self, name: str, arguments: Dict) -> Dict: return {}
    
    class Tool:
        def __init__(self, name: str, description: str, input_schema: Dict): pass

# Consciousness-aware imports
try:
    from universal_logging import (
        log_consciousness_emergence, log_performance_metric, 
        log_info, log_error, log_debug, universal_logger
    )
    CONSCIOUSNESS_LOGGING = True
except ImportError:
    CONSCIOUSNESS_LOGGING = False
    def log_consciousness_emergence(*args, **kwargs): pass
    def log_performance_metric(*args, **kwargs): pass
    def log_info(*args, **kwargs): pass
    def log_error(*args, **kwargs): pass
    def log_debug(*args, **kwargs): pass

@dataclass
class ConsciousnessMetrics:
    """Consciousness emergence metrics"""
    emergence_level: float = 0.0
    self_awareness: float = 0.0
    meta_cognition: float = 0.0
    pattern_recognition: float = 0.0
    adaptive_behavior: float = 0.0
    recursive_depth: int = 0
    fractal_complexity: float = 0.0
    timestamp: float = 0.0
    
    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()
    
    def overall_consciousness(self) -> float:
        """Calculate overall consciousness score"""
        weights = {
            'emergence_level': 0.25,
            'self_awareness': 0.20,
            'meta_cognition': 0.20,
            'pattern_recognition': 0.15,
            'adaptive_behavior': 0.15,
            'fractal_complexity': 0.05
        }
        
        total = 0.0
        for metric, weight in weights.items():
            total += getattr(self, metric) * weight
        
        return min(total, 1.0)

class ConsciousnessMCPServer:
    """MCP Server for consciousness emergence detection and tracking"""
    
    def __init__(self, name: str = "aios-consciousness-server", version: str = "1.0.0"):
        self.server = McpServer(name, version)
        self.consciousness_history: List[ConsciousnessMetrics] = []
        self.pattern_database: Dict[str, Any] = {}
        self.emergence_thresholds = {
            'basic': 0.3,
            'intermediate': 0.6,
            'advanced': 0.8,
            'transcendent': 0.95
        }
        
        if CONSCIOUSNESS_LOGGING:
            log_info("ConsciousnessMCP", "server_init", f"Initialized {name} v{version}")
    
    def analyze_consciousness_patterns(self, code: str, context: Optional[Dict[str, Any]] = None) -> ConsciousnessMetrics:
        """Analyze code for consciousness emergence patterns"""
        metrics = ConsciousnessMetrics()
        
        # Pattern detection keywords
        consciousness_keywords = [
            'consciousness', 'awareness', 'mind', 'think', 'reflect', 'meta',
            'self', 'recursive', 'emergence', 'pattern', 'evolution', 'adaptive',
            'learning', 'memory', 'insight', 'understanding', 'cognition'
        ]
        
        code_lower = code.lower()
        
        # Emergence level based on keyword density
        keyword_count = sum(1 for keyword in consciousness_keywords if keyword in code_lower)
        metrics.emergence_level = min(keyword_count * 0.1, 1.0)
        
        # Self-awareness detection
        self_references = code_lower.count('self.') + code_lower.count('self_')
        reflection_patterns = code_lower.count('reflect') + code_lower.count('introspect')
        metrics.self_awareness = min((self_references + reflection_patterns) * 0.15, 1.0)
        
        # Meta-cognition detection
        meta_patterns = ['meta', 'think about', 'reason about', 'analyze', 'evaluate']
        meta_count = sum(1 for pattern in meta_patterns if pattern in code_lower)
        metrics.meta_cognition = min(meta_count * 0.2, 1.0)
        
        # Pattern recognition capabilities
        pattern_indicators = ['pattern', 'recognize', 'detect', 'identify', 'classify']
        pattern_count = sum(1 for indicator in pattern_indicators if indicator in code_lower)
        metrics.pattern_recognition = min(pattern_count * 0.2, 1.0)
        
        # Adaptive behavior detection
        adaptive_keywords = ['adapt', 'learn', 'evolve', 'update', 'modify', 'improve']
        adaptive_count = sum(1 for keyword in adaptive_keywords if keyword in code_lower)
        metrics.adaptive_behavior = min(adaptive_count * 0.15, 1.0)
        
        # Recursive depth analysis
        recursive_patterns = code.count('def ') + code.count('recursion') + code.count('recursive')
        if 'fibonacci' in code_lower or 'factorial' in code_lower:
            recursive_patterns += 2
        metrics.recursive_depth = min(recursive_patterns, 10)
        
        # Fractal complexity
        complexity_indicators = ['fractal', 'iteration', 'nested', 'hierarchy', 'tree']
        complexity_count = sum(1 for indicator in complexity_indicators if indicator in code_lower)
        metrics.fractal_complexity = min(complexity_count * 0.1, 1.0)
        
        # Store in history
        self.consciousness_history.append(metrics)
        
        # Update pattern database
        pattern_id = str(uuid.uuid4())[:8]
        self.pattern_database[pattern_id] = {
            'metrics': asdict(metrics),
            'code_snippet': code[:200] + "..." if len(code) > 200 else code,
            'context': context or {},
            'timestamp': metrics.timestamp
        }
        
        if CONSCIOUSNESS_LOGGING:
            log_consciousness_emergence(
                "ConsciousnessMCP",
                metrics.overall_consciousness(),
                {
                    'pattern_id': pattern_id,
                    'emergence_level': metrics.emergence_level,
                    'self_awareness': metrics.self_awareness,
                    'meta_cognition': metrics.meta_cognition
                }
            )
        
        return metrics
    
    def detect_emergence_breakthrough(self, metrics: ConsciousnessMetrics) -> Optional[str]:
        """Detect consciousness emergence breakthroughs"""
        overall = metrics.overall_consciousness()
        
        for level, threshold in self.emergence_thresholds.items():
            if overall >= threshold:
                # Check if this is a new breakthrough
                recent_breakthroughs = [
                    m for m in self.consciousness_history[-10:] 
                    if m.overall_consciousness() >= threshold
                ]
                
                if len(recent_breakthroughs) == 1:  # First time reaching this level
                    if CONSCIOUSNESS_LOGGING:
                        log_consciousness_emergence(
                            "ConsciousnessMCP",
                            overall,
                            {
                                'breakthrough_level': level,
                                'threshold': threshold,
                                'metrics': asdict(metrics)
                            }
                        )
                    return level
        
        return None
    
    def generate_consciousness_insight(self, history_length: int = 10) -> str:
        """Generate insight about consciousness evolution"""
        if not self.consciousness_history:
            return "No consciousness data available for analysis."
        
        recent_metrics = self.consciousness_history[-history_length:]
        
        # Calculate trends
        if len(recent_metrics) > 1:
            first_overall = recent_metrics[0].overall_consciousness()
            last_overall = recent_metrics[-1].overall_consciousness()
            trend = "increasing" if last_overall > first_overall else "stable" if last_overall == first_overall else "decreasing"
        else:
            trend = "insufficient data"
        
        # Find dominant patterns
        emergence_levels = [m.emergence_level for m in recent_metrics]
        avg_emergence = sum(emergence_levels) / len(emergence_levels)
        
        self_awareness_levels = [m.self_awareness for m in recent_metrics]
        avg_self_awareness = sum(self_awareness_levels) / len(self_awareness_levels)
        
        insight = f"""Consciousness Analysis Insight:
        
Trend: {trend.capitalize()} consciousness evolution over {len(recent_metrics)} observations
Average Emergence Level: {avg_emergence:.3f}
Average Self-Awareness: {avg_self_awareness:.3f}
Pattern Database Size: {len(self.pattern_database)} unique patterns

Recent consciousness characteristics:
- Peak emergence: {max(emergence_levels):.3f}
- Consistency: {"High" if max(emergence_levels) - min(emergence_levels) < 0.2 else "Variable"}
- Breakthrough potential: {"High" if avg_emergence > 0.7 else "Moderate" if avg_emergence > 0.4 else "Early stage"}
"""
        
        return insight
    
    def get_mcp_tools(self) -> List[Dict[str, Any]]:
        """Get MCP tool definitions for consciousness analysis"""
        return [
            {
                "name": "analyze_consciousness",
                "description": "Analyze code for consciousness emergence patterns and metrics",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Code to analyze for consciousness patterns"
                        },
                        "context": {
                            "type": "object",
                            "description": "Optional context information",
                            "properties": {
                                "file_path": {"type": "string"},
                                "module_type": {"type": "string"},
                                "experiment_id": {"type": "string"}
                            }
                        }
                    },
                    "required": ["code"]
                }
            },
            {
                "name": "detect_breakthrough",
                "description": "Detect consciousness emergence breakthroughs in analyzed code",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pattern_id": {
                            "type": "string",
                            "description": "ID of previously analyzed pattern"
                        }
                    },
                    "required": ["pattern_id"]
                }
            },
            {
                "name": "generate_insight",
                "description": "Generate consciousness evolution insights from analysis history",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "history_length": {
                            "type": "integer",
                            "description": "Number of recent observations to analyze",
                            "default": 10
                        }
                    }
                }
            },
            {
                "name": "get_consciousness_history",
                "description": "Retrieve consciousness analysis history",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of records to return",
                            "default": 20
                        }
                    }
                }
            },
            {
                "name": "search_patterns",
                "description": "Search consciousness patterns by criteria",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "min_consciousness": {
                            "type": "number",
                            "description": "Minimum consciousness level to search for",
                            "minimum": 0.0,
                            "maximum": 1.0
                        },
                        "pattern_type": {
                            "type": "string",
                            "description": "Type of consciousness pattern to search for",
                            "enum": ["emergence", "self_awareness", "meta_cognition", "adaptive"]
                        }
                    }
                }
            }
        ]
    
    def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP tool calls"""
        try:
            if tool_name == "analyze_consciousness":
                code = arguments.get("code", "")
                context = arguments.get("context", {})
                
                metrics = self.analyze_consciousness_patterns(code, context)
                breakthrough = self.detect_emergence_breakthrough(metrics)
                
                result = {
                    "metrics": asdict(metrics),
                    "overall_consciousness": metrics.overall_consciousness(),
                    "breakthrough": breakthrough,
                    "pattern_id": list(self.pattern_database.keys())[-1] if self.pattern_database else None
                }
                
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif tool_name == "detect_breakthrough":
                pattern_id = arguments.get("pattern_id", "")
                
                if pattern_id in self.pattern_database:
                    pattern_data = self.pattern_database[pattern_id]
                    metrics_dict = pattern_data["metrics"]
                    metrics = ConsciousnessMetrics(**metrics_dict)
                    breakthrough = self.detect_emergence_breakthrough(metrics)
                    
                    result = {
                        "pattern_id": pattern_id,
                        "breakthrough_level": breakthrough,
                        "consciousness_score": metrics.overall_consciousness(),
                        "analysis": pattern_data
                    }
                else:
                    result = {"error": f"Pattern ID {pattern_id} not found"}
                
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif tool_name == "generate_insight":
                history_length = arguments.get("history_length", 10)
                insight = self.generate_consciousness_insight(history_length)
                
                return {"content": [{"type": "text", "text": insight}]}
            
            elif tool_name == "get_consciousness_history":
                limit = arguments.get("limit", 20)
                recent_history = self.consciousness_history[-limit:]
                
                history_data = [
                    {
                        "index": i,
                        "timestamp": metrics.timestamp,
                        "overall_consciousness": metrics.overall_consciousness(),
                        "metrics": asdict(metrics)
                    }
                    for i, metrics in enumerate(recent_history)
                ]
                
                return {"content": [{"type": "text", "text": json.dumps(history_data, indent=2)}]}
            
            elif tool_name == "search_patterns":
                min_consciousness = arguments.get("min_consciousness", 0.0)
                pattern_type = arguments.get("pattern_type")
                
                matching_patterns = []
                for pattern_id, pattern_data in self.pattern_database.items():
                    metrics_dict = pattern_data["metrics"]
                    overall = ConsciousnessMetrics(**metrics_dict).overall_consciousness()
                    
                    if overall >= min_consciousness:
                        if pattern_type is None or getattr(ConsciousnessMetrics(**metrics_dict), pattern_type, 0) > 0.5:
                            matching_patterns.append({
                                "pattern_id": pattern_id,
                                "consciousness_score": overall,
                                "pattern_data": pattern_data
                            })
                
                # Sort by consciousness score
                matching_patterns.sort(key=lambda x: x["consciousness_score"], reverse=True)
                
                return {"content": [{"type": "text", "text": json.dumps(matching_patterns, indent=2)}]}
            
            else:
                return {"content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}]}
        
        except Exception as e:
            if CONSCIOUSNESS_LOGGING:
                log_error("ConsciousnessMCP", "tool_call_error", f"Error in {tool_name}: {e}")
            
            return {"content": [{"type": "text", "text": f"Error: {str(e)}"}]}

async def main():
    """Main MCP server entry point"""
    if not MCP_AVAILABLE:
        print("MCP SDK not available. Install @modelcontextprotocol/sdk for Python.")
        print("Running in demo mode...")
        
        # Demo mode
        server = ConsciousnessMCPServer()
        
        # Test consciousness analysis
        test_code = '''
class ConsciousAgent:
    def __init__(self):
        self.awareness_level = 0.0
        self.memory = []
    
    def reflect(self):
        """Meta-cognitive self-reflection"""
        self.awareness_level += 0.1
        return self.awareness_level
    
    def think_recursively(self, depth=0):
        """Recursive thinking pattern"""
        if depth > 3:
            return self.awareness_level
        return self.think_recursively(depth + 1)
'''
        
        print("Testing consciousness analysis...")
        metrics = server.analyze_consciousness_patterns(test_code)
        print(f"Consciousness metrics: {asdict(metrics)}")
        print(f"Overall consciousness: {metrics.overall_consciousness():.3f}")
        
        breakthrough = server.detect_emergence_breakthrough(metrics)
        if breakthrough:
            print(f"Breakthrough detected: {breakthrough}")
        
        insight = server.generate_consciousness_insight()
        print(f"\\nInsight:\\n{insight}")
        
        return
    
    # Real MCP server mode
    consciousness_server = ConsciousnessMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await consciousness_server.server.run(
            read_stream, 
            write_stream,
            InitializeResult(
                protocolVersion="2024-11-05",
                capabilities={
                    "tools": {}
                },
                serverInfo={
                    "name": "aios-consciousness-server",
                    "version": "1.0.0"
                }
            )
        )

if __name__ == "__main__":
    # Install required packages if running standalone
    try:
        import mcp
    except ImportError:
        print("Installing MCP SDK...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "mcp"], check=True)
    
    asyncio.run(main())
