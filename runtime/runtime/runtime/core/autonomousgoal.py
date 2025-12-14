"""AutonomousGoal module - Auto-generated from aios_autonomous_supercell_organism.py"""

class AutonomousGoal:
    """Represents an autonomous goal the organism pursues."""
    id: str
    description: str
    priority: float  # 0.0 to 1.0
    target_path: Optional[str] = None
    completion_criteria: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    deadline: Optional[datetime] = None
    progress: float = 0.0
    status: str = "pending"


@dataclass