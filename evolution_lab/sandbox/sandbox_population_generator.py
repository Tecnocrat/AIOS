"""
AINLP Sandbox Population Generator
Generates synthetic code organisms from population JSON blueprints

AINLP Protocol: OS0.6.4.claude
Created: 2025-12-05
Purpose: Materialize population JSON into executable sandbox organisms

Usage:
    python sandbox_population_generator.py [population_json]
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


# Seed code templates by archetype (from population_manager.py)
ARCHETYPE_TEMPLATES = {
    "os_tools": '''"""
OS Tools Organism - {organism_id}
Archetype: os_tools
Generation: {generation}
Fitness: {fitness_score}
"""

import os
from pathlib import Path
from typing import List, Optional


class FileSystemTool:
    """File system operations utility"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path.cwd()
    
    def list_directory(self, path: Optional[str] = None) -> List[str]:
        """List contents of directory"""
        target = self.base_path / path if path else self.base_path
        if not target.exists():
            return []
        return [item.name for item in target.iterdir()]
    
    def file_exists(self, filename: str) -> bool:
        """Check if file exists"""
        return (self.base_path / filename).exists()
    
    def get_file_size(self, filename: str) -> int:
        """Get file size in bytes"""
        filepath = self.base_path / filename
        return filepath.stat().st_size if filepath.exists() else 0


def run_organism():
    """Organism entry point"""
    tool = FileSystemTool()
    contents = tool.list_directory()
    print(f"Directory contents: {{len(contents)}} items")
    return contents


if __name__ == "__main__":
    run_organism()
''',

    "cli_applications": '''"""
CLI Application Organism - {organism_id}
Archetype: cli_applications
Generation: {generation}
Fitness: {fitness_score}
"""

import argparse
import sys
from typing import Optional


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="CLI Application Organism"
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        help="Input value"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    return parser.parse_args()


def process(value: str, verbose: bool = False) -> str:
    """Process input value"""
    result = value.upper() if value else "No input"
    if verbose:
        print(f"Processing: {{value}} -> {{result}}")
    return result


def run_organism():
    """Organism entry point"""
    args = parse_arguments()
    result = process(args.input, args.verbose)
    print(f"Result: {{result}}")
    return result


if __name__ == "__main__":
    run_organism()
''',

    "web_services": '''"""
Web Services Organism - {organism_id}
Archetype: web_services
Generation: {generation}
Fitness: {fitness_score}
"""

import json
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Response:
    """HTTP-like response"""
    status: int
    data: Any
    headers: Dict[str, str]


class APIEndpoint:
    """Simple API endpoint handler"""
    
    def __init__(self, name: str):
        self.name = name
        self.routes: Dict[str, callable] = {{}}
    
    def route(self, path: str):
        """Decorator to register routes"""
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
    
    def handle(self, path: str, **kwargs) -> Response:
        """Handle incoming request"""
        if path in self.routes:
            data = self.routes[path](**kwargs)
            return Response(200, data, {{"Content-Type": "application/json"}})
        return Response(404, {{"error": "Not found"}}, {{}})


# Create endpoint instance
api = APIEndpoint("organism_api")


@api.route("/health")
def health_check():
    return {{"status": "healthy", "organism": "{organism_id}"}}


@api.route("/info")
def get_info():
    return {{
        "organism_id": "{organism_id}",
        "generation": {generation},
        "fitness": {fitness_score}
    }}


def run_organism():
    """Organism entry point"""
    response = api.handle("/health")
    print(f"API Response: {{response.data}}")
    return response


if __name__ == "__main__":
    run_organism()
''',

    "abstract_objects": '''"""
Abstract Objects Organism - {organism_id}
Archetype: abstract_objects
Generation: {generation}
Fitness: {fitness_score}
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from dataclasses import dataclass


T = TypeVar('T')


class AbstractEntity(ABC, Generic[T]):
    """Abstract base entity"""
    
    @abstractmethod
    def process(self, data: T) -> T:
        """Process data"""
        pass
    
    @abstractmethod
    def validate(self, data: T) -> bool:
        """Validate data"""
        pass


@dataclass
class EntityState:
    """Entity state container"""
    value: any
    timestamp: str
    valid: bool = True


class ConcreteEntity(AbstractEntity[str]):
    """Concrete implementation"""
    
    def __init__(self, name: str = "{organism_id}"):
        self.name = name
        self.state: Optional[EntityState] = None
    
    def process(self, data: str) -> str:
        """Process string data"""
        result = data.strip().title()
        self.state = EntityState(result, "{generation}", True)
        return result
    
    def validate(self, data: str) -> bool:
        """Validate string data"""
        return isinstance(data, str) and len(data) > 0


def run_organism():
    """Organism entry point"""
    entity = ConcreteEntity()
    result = entity.process("test input")
    print(f"Processed: {{result}}")
    return result


if __name__ == "__main__":
    run_organism()
''',

    "network_tools": '''"""
Network Tools Organism - {organism_id}
Archetype: network_tools
Generation: {generation}
Fitness: {fitness_score}
"""

import socket
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class NetworkInfo:
    """Network information container"""
    hostname: str
    ip_address: str
    port: Optional[int] = None


class NetworkScanner:
    """Basic network scanning utility"""
    
    def __init__(self):
        self.local_info = self._get_local_info()
    
    def _get_local_info(self) -> NetworkInfo:
        """Get local network info"""
        hostname = socket.gethostname()
        try:
            ip = socket.gethostbyname(hostname)
        except socket.gaierror:
            ip = "127.0.0.1"
        return NetworkInfo(hostname, ip)
    
    def check_port(self, host: str, port: int, timeout: float = 1.0) -> bool:
        """Check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except socket.error:
            return False
    
    def scan_common_ports(self, host: str) -> dict:
        """Scan common ports"""
        common = [22, 80, 443, 8080, 11434]  # Including Ollama!
        return {{port: self.check_port(host, port) for port in common}}


def run_organism():
    """Organism entry point"""
    scanner = NetworkScanner()
    print(f"Local: {{scanner.local_info}}")
    return scanner.local_info


if __name__ == "__main__":
    run_organism()
''',

    "data_science": '''"""
Data Science Organism - {organism_id}
Archetype: data_science
Generation: {generation}
Fitness: {fitness_score}
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import statistics


@dataclass
class DataStats:
    """Statistical summary"""
    mean: float
    median: float
    stdev: float
    min_val: float
    max_val: float


class DataAnalyzer:
    """Basic data analysis tool"""
    
    def __init__(self):
        self.data: List[float] = []
    
    def load_data(self, values: List[float]):
        """Load data for analysis"""
        self.data = values
    
    def compute_stats(self) -> Optional[DataStats]:
        """Compute statistical summary"""
        if len(self.data) < 2:
            return None
        
        return DataStats(
            mean=statistics.mean(self.data),
            median=statistics.median(self.data),
            stdev=statistics.stdev(self.data),
            min_val=min(self.data),
            max_val=max(self.data)
        )
    
    def normalize(self) -> List[float]:
        """Normalize data to 0-1 range"""
        if not self.data:
            return []
        min_v, max_v = min(self.data), max(self.data)
        range_v = max_v - min_v
        if range_v == 0:
            return [0.5] * len(self.data)
        return [(x - min_v) / range_v for x in self.data]


def run_organism():
    """Organism entry point"""
    analyzer = DataAnalyzer()
    analyzer.load_data([1.0, 2.5, 3.7, 4.2, 5.8, 6.1])
    stats = analyzer.compute_stats()
    print(f"Stats: {{stats}}")
    return stats


if __name__ == "__main__":
    run_organism()
''',

    "automation": '''"""
Automation Organism - {organism_id}
Archetype: automation
Generation: {generation}
Fitness: {fitness_score}
"""

import time
from typing import Callable, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Automation task"""
    name: str
    action: Callable
    interval_seconds: float = 60.0
    last_run: Optional[datetime] = None
    run_count: int = 0


class TaskScheduler:
    """Simple task scheduler"""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.running = False
    
    def add_task(self, name: str, action: Callable, interval: float = 60.0):
        """Add task to scheduler"""
        self.tasks.append(Task(name, action, interval))
    
    def run_once(self):
        """Run all tasks once"""
        results = []
        for task in self.tasks:
            try:
                result = task.action()
                task.last_run = datetime.now()
                task.run_count += 1
                results.append((task.name, result))
            except Exception as e:
                results.append((task.name, f"Error: {{e}}"))
        return results
    
    def get_status(self) -> dict:
        """Get scheduler status"""
        return {{
            "tasks": len(self.tasks),
            "total_runs": sum(t.run_count for t in self.tasks)
        }}


def sample_task():
    """Sample automation task"""
    return "Task executed at " + datetime.now().isoformat()


def run_organism():
    """Organism entry point"""
    scheduler = TaskScheduler()
    scheduler.add_task("sample", sample_task, 30.0)
    results = scheduler.run_once()
    print(f"Results: {{results}}")
    return results


if __name__ == "__main__":
    run_organism()
''',

    "game_logic": '''"""
Game Logic Organism - {organism_id}
Archetype: game_logic
Generation: {generation}
Fitness: {fitness_score}
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class CellState(Enum):
    EMPTY = " "
    X = "X"
    O = "O"


@dataclass
class GameBoard:
    """Simple game board"""
    size: int = 3
    cells: List[List[CellState]] = None
    
    def __post_init__(self):
        if self.cells is None:
            self.cells = [
                [CellState.EMPTY] * self.size 
                for _ in range(self.size)
            ]
    
    def place(self, row: int, col: int, state: CellState) -> bool:
        """Place piece on board"""
        if 0 <= row < self.size and 0 <= col < self.size:
            if self.cells[row][col] == CellState.EMPTY:
                self.cells[row][col] = state
                return True
        return False
    
    def check_winner(self) -> Optional[CellState]:
        """Check for winner"""
        # Check rows
        for row in self.cells:
            if row[0] != CellState.EMPTY and all(c == row[0] for c in row):
                return row[0]
        
        # Check columns
        for col in range(self.size):
            if self.cells[0][col] != CellState.EMPTY:
                if all(self.cells[row][col] == self.cells[0][col] 
                       for row in range(self.size)):
                    return self.cells[0][col]
        
        return None
    
    def __str__(self) -> str:
        lines = []
        for row in self.cells:
            lines.append("|" + "|".join(c.value for c in row) + "|")
        return "\\n".join(lines)


def run_organism():
    """Organism entry point"""
    board = GameBoard()
    board.place(0, 0, CellState.X)
    board.place(1, 1, CellState.X)
    board.place(2, 2, CellState.X)
    winner = board.check_winner()
    print(f"Board:\\n{{board}}")
    print(f"Winner: {{winner}}")
    return board


if __name__ == "__main__":
    run_organism()
'''
}


class SandboxPopulationGenerator:
    """Generates synthetic code from population blueprints"""
    
    def __init__(self, sandbox_dir: Path):
        self.sandbox_dir = sandbox_dir
        self.generated_files: List[Path] = []
    
    def load_population(self, population_file: Path) -> Dict[str, Any]:
        """Load population JSON blueprint"""
        with open(population_file) as f:
            return json.load(f)
    
    def generate_organism_code(
        self, 
        organism: Dict[str, Any]
    ) -> str:
        """Generate code for organism based on archetype"""
        archetype = organism.get("archetype", "abstract_objects")
        template = ARCHETYPE_TEMPLATES.get(
            archetype, 
            ARCHETYPE_TEMPLATES["abstract_objects"]
        )
        
        # Format template with organism data
        code = template.format(
            organism_id=organism.get("organism_id", "unknown"),
            generation=organism.get("generation", 0),
            fitness_score=organism.get("fitness_score", 0.5)
        )
        
        return code
    
    def create_experiment_folder(
        self, 
        population: Dict[str, Any]
    ) -> Path:
        """Create experiment folder for population"""
        pop_id = population.get("population_id", "unknown")
        gen = population.get("generation", 0)
        
        folder_name = f"exp_{pop_id}_gen{gen:03d}"
        folder_path = self.sandbox_dir / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        
        return folder_path
    
    def generate_population(
        self, 
        population_file: Path
    ) -> Path:
        """Generate all organisms from population blueprint"""
        population = self.load_population(population_file)
        exp_folder = self.create_experiment_folder(population)
        
        print(f"\n🧬 Generating population: {population.get('population_id')}")
        print(f"   Generation: {population.get('generation')}")
        print(f"   Organisms: {population.get('organism_count')}")
        print(f"   Output: {exp_folder.name}")
        
        # Generate each organism
        for organism in population.get("organisms", []):
            org_id = organism.get("organism_id", "unknown")
            archetype = organism.get("archetype", "unknown")
            
            # Generate code
            code = self.generate_organism_code(organism)
            
            # Write to file
            filename = f"{org_id}.py"
            filepath = exp_folder / filename
            with open(filepath, 'w') as f:
                f.write(code)
            
            self.generated_files.append(filepath)
            print(f"   ✅ {filename} ({archetype})")
        
        # Create manifest
        manifest = {
            "population_id": population.get("population_id"),
            "generation": population.get("generation"),
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "organisms": [
                {
                    "file": f.name,
                    "organism_id": f.stem
                }
                for f in self.generated_files
            ],
            "source_blueprint": population_file.name
        }
        
        manifest_file = exp_folder / "manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"   📋 Manifest: {manifest_file.name}")
        
        return exp_folder


def main():
    """Main entry point"""
    # Determine paths
    script_dir = Path(__file__).parent
    sandbox_dir = script_dir
    populations_dir = script_dir.parent / "populations"
    
    # Find latest Mistral population
    tachyonic_dir = populations_dir / "tachyonic"
    
    # Use command line arg or find latest
    if len(sys.argv) > 1:
        pop_file = Path(sys.argv[1])
    else:
        # Find latest generation file
        gen_files = sorted(tachyonic_dir.glob("*_gen*_*.json"))
        if not gen_files:
            print("❌ No population files found")
            return
        pop_file = gen_files[-1]
    
    print("=" * 60)
    print("AINLP SANDBOX POPULATION GENERATOR")
    print("=" * 60)
    print(f"Source: {pop_file.name}")
    
    generator = SandboxPopulationGenerator(sandbox_dir)
    exp_folder = generator.generate_population(pop_file)
    
    print("\n" + "=" * 60)
    print(f"✅ Generated {len(generator.generated_files)} organisms")
    print(f"📁 Location: {exp_folder}")
    print("=" * 60)


if __name__ == "__main__":
    main()
