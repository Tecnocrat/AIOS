"""OrganismState module - Auto-generated from aios_autonomous_supercell_organism.py"""

class OrganismState(Enum):
    """Current state of the autonomous organism."""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    ANALYZING = "analyzing"
    ACTING = "acting"
    LEARNING = "learning"
    RESTING = "resting"
    EVOLVING = "evolving"


@dataclass