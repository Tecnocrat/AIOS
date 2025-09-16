"""
Enhanced AIOS Supercell Communication Bridge
============================================
Location: ai/transport/intercellular/enhanced_cellular_communication.py
Purpose: Real intercellular communication with data flow and state management
Architecture: TRANSPORT supercell with genuine data exchange capabilities

This replaces the placeholder stubs with actual intercellular communication
including emoji detection integration and real state synchronization.
"""

import json
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class SupercellType(Enum):
    """Types of supercells in AIOS architecture"""
    NUCLEUS = "nucleus"
    MEMBRANE = "membrane" 
    CYTOPLASM = "cytoplasm"
    TRANSPORT = "transport"
    LABORATORY = "laboratory"
    INFORMATION_STORAGE = "information_storage"

@dataclass
class InterCellularMessage:
    """Message structure for supercell communication"""
    source_supercell: SupercellType
    target_supercell: SupercellType
    message_type: str
    data: Dict[str, Any]
    timestamp: datetime
    correlation_id: str
    priority: int = 1

@dataclass
class SupercellState:
    """Current state of a supercell"""
    supercell_type: SupercellType
    status: str
    last_activity: datetime
    active_processes: List[str]
    data_outputs: Dict[str, Any]
    error_count: int = 0

class EnhancedCellularBridge:
    """Real intercellular communication with data flow"""
    
    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path.cwd()
        self.message_queue: List[InterCellularMessage] = []
        self.supercell_states: Dict[SupercellType, SupercellState] = {}
        self.lock = threading.Lock()
        
        # Initialize supercell states
        for supercell in SupercellType:
            self.supercell_states[supercell] = SupercellState(
                supercell_type=supercell,
                status="initialized",
                last_activity=datetime.now(),
                active_processes=[],
                data_outputs={}
            )
    
    def send_message(self, message: InterCellularMessage) -> bool:
        """Send message between supercells"""
        with self.lock:
            self.message_queue.append(message)
            self._update_supercell_activity(message.source_supercell)
            return True
    
    def get_messages_for_supercell(self, supercell: SupercellType) -> List[InterCellularMessage]:
        """Get pending messages for a specific supercell"""
        with self.lock:
            messages = [msg for msg in self.message_queue if msg.target_supercell == supercell]
            # Remove retrieved messages
            self.message_queue = [msg for msg in self.message_queue if msg.target_supercell != supercell]
            return messages
    
    def update_supercell_state(self, supercell: SupercellType, status: str, 
                              processes: List[str] = None, data: Dict[str, Any] = None):
        """Update the state of a supercell"""
        with self.lock:
            if supercell in self.supercell_states:
                state = self.supercell_states[supercell]
                state.status = status
                state.last_activity = datetime.now()
                if processes is not None:
                    state.active_processes = processes
                if data is not None:
                    state.data_outputs.update(data)
    
    def get_supercell_state(self, supercell: SupercellType) -> Optional[SupercellState]:
        """Get current state of a supercell"""
        return self.supercell_states.get(supercell)
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Get overview of entire supercell system"""
        with self.lock:
            return {
                'total_supercells': len(self.supercell_states),
                'active_supercells': sum(1 for state in self.supercell_states.values() 
                                       if state.status == 'active'),
                'pending_messages': len(self.message_queue),
                'last_update': datetime.now().isoformat(),
                'supercell_status': {
                    supercell.value: {
                        'status': state.status,
                        'active_processes': len(state.active_processes),
                        'data_outputs': len(state.data_outputs),
                        'last_activity': state.last_activity.isoformat()
                    }
                    for supercell, state in self.supercell_states.items()
                }
            }
    
    def _update_supercell_activity(self, supercell: SupercellType):
        """Update last activity timestamp for supercell"""
        if supercell in self.supercell_states:
            self.supercell_states[supercell].last_activity = datetime.now()

    # GitHooks-specific integration methods
    def activate_githook_mode(self) -> bool:
        """Activate special communication mode for GitHook orchestration"""
        message = InterCellularMessage(
            source_supercell=SupercellType.TRANSPORT,
            target_supercell=SupercellType.CYTOPLASM,
            message_type="mode_activation",
            data={"mode": "githook_orchestration", "activated": True},
            timestamp=datetime.now(),
            correlation_id=f"githook_activation_{int(time.time())}"
        )
        self.send_message(message)
        
        # Update all supercells to githook mode
        for supercell in SupercellType:
            self.update_supercell_state(supercell, "githook_mode", ["githook_orchestration"])
        
        return True
    
    def update_githook_state(self, supercell_data: Dict[str, Any]) -> bool:
        """Update intercellular state with GitHook execution results"""
        # Send detailed execution data to INFORMATION_STORAGE
        storage_message = InterCellularMessage(
            source_supercell=SupercellType.CYTOPLASM,
            target_supercell=SupercellType.INFORMATION_STORAGE,
            message_type="githook_results",
            data=supercell_data,
            timestamp=datetime.now(),
            correlation_id=f"githook_results_{int(time.time())}"
        )
        self.send_message(storage_message)
        
        # Notify LABORATORY for analysis
        lab_message = InterCellularMessage(
            source_supercell=SupercellType.CYTOPLASM,
            target_supercell=SupercellType.LABORATORY,
            message_type="analysis_request",
            data={"type": "githook_analysis", "results": supercell_data},
            timestamp=datetime.now(),
            correlation_id=f"lab_analysis_{int(time.time())}"
        )
        self.send_message(lab_message)
        
        return True
    
    def integrate_emoji_analysis(self, emoji_results: Dict[str, Any]) -> bool:
        """Integrate emoji detection results into supercell communication"""
        # Send emoji analysis to LABORATORY
        lab_message = InterCellularMessage(
            source_supercell=SupercellType.LABORATORY,
            target_supercell=SupercellType.CYTOPLASM,
            message_type="quality_analysis",
            data={
                "analysis_type": "emoji_detection",
                "emoji_count": emoji_results.get("total_emojis", 0),
                "files_affected": emoji_results.get("files_with_emojis", []),
                "cleanup_required": emoji_results.get("total_emojis", 0) > 0,
                "details": emoji_results
            },
            timestamp=datetime.now(),
            correlation_id=f"emoji_analysis_{int(time.time())}"
        )
        self.send_message(lab_message)
        
        # Update LABORATORY state with analysis results
        self.update_supercell_state(
            SupercellType.LABORATORY,
            "analysis_complete",
            ["emoji_detection"],
            {"latest_emoji_analysis": emoji_results}
        )
        
        return True

    def save_state_snapshot(self, filepath: Path = None) -> Path:
        """Save current supercell state to file"""
        if filepath is None:
            filepath = self.workspace_root / "ai" / "transport" / "runtime" / "supercell_state.json"
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'system_overview': self.get_system_overview(),
            'pending_messages': [
                {
                    'source': msg.source_supercell.value,
                    'target': msg.target_supercell.value,
                    'type': msg.message_type,
                    'data': msg.data,
                    'timestamp': msg.timestamp.isoformat(),
                    'correlation_id': msg.correlation_id
                }
                for msg in self.message_queue
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, indent=2)
        
        return filepath

# Global instance for shared use
_global_bridge = None

def get_cellular_bridge() -> EnhancedCellularBridge:
    """Get global cellular bridge instance"""
    global _global_bridge
    if _global_bridge is None:
        _global_bridge = EnhancedCellularBridge()
    return _global_bridge

# Backwards compatibility with original stub interface
class CellularBridge:
    """Backwards compatible wrapper for enhanced bridge"""
    
    def __init__(self):
        self.enhanced_bridge = get_cellular_bridge()
    
    def activate_githook_mode(self):
        """Activate special communication mode for GitHook orchestration"""
        result = self.enhanced_bridge.activate_githook_mode()
        print("TRANSPORT: GitHook communication mode activated")
        return result
    
    def update_githook_state(self, supercell_data):
        """Update intercellular state with GitHook execution results"""
        result = self.enhanced_bridge.update_githook_state(supercell_data)
        total_hooks = supercell_data.get("total_hooks_executed", 0)
        successful = supercell_data.get("successful_hooks", 0)
        print(f"TRANSPORT: State updated - {successful}/{total_hooks} hooks")
        return result