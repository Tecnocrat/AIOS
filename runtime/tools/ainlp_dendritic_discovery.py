"""
AINLP Dendritic Discovery Engine
=================================

Core Purpose: Map existing architecture to prevent file proliferation and
             enhance dendritic interconnectivity between logic cores
             (neurons).

AINLP Pattern: AINLP.dendritic.discovery
Consciousness Level: HIGH (architectural intelligence)

This tool enforces:
1. Enhancement over creation (check before spawning new files)
2. Dendritic connection mapping (lonely neurons seeking connections)
3. Logic interconnectivity analysis (supercell communication patterns)
4. Anti-proliferation enforcement (>70% similarity = enhance, don't create)

Usage:
    # Before creating new file:
    python runtime/tools/ainlp_dendritic_discovery.py \\
        --check-similar "proposed_functionality"
    
    # Map all neurons and connections:
    python runtime/tools/ainlp_dendritic_discovery.py --map-architecture
    
    # Find dendritic connection opportunities:
    python runtime/tools/ainlp_dendritic_discovery.py --find-connections
"""

import ast
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Neuron:
    """Represents a code module/tool as a neuron in the AIOS architecture."""
    path: str
    name: str
    supercell: str
    purpose: str
    functions: List[str]
    imports: List[str]
    docstring: Optional[str]
    lines_of_code: int
    consciousness_level: float = 0.0
    dendrites: List[str] = None  # Connections to other neurons
    
    def __post_init__(self):
        if self.dendrites is None:
            self.dendrites = []


@dataclass
class DendriticConnection:
    """Represents a connection between two neurons."""
    source_neuron: str
    target_neuron: str
    # Connection types: 'import', 'calls', 'similar_functionality',
    # 'data_flow'
    connection_type: str
    strength: float  # 0.0 - 1.0
    description: str


class AINLPDendriticDiscovery:
    """
    AINLP.dendritic discovery engine for architectural analysis.
    
    Prevents file proliferation by:
    1. Mapping all existing neurons (modules/tools)
    2. Identifying similarity patterns
    3. Enforcing enhancement-over-creation
    4. Creating dendritic connection maps
    """
    
    def __init__(self, aios_root: str = None):
        if aios_root:
            self.aios_root = Path(aios_root)
        else:
            self.aios_root = Path(__file__).parent.parent.parent
        self.neurons: Dict[str, Neuron] = {}
        self.connections: List[DendriticConnection] = []
        db_path = self.aios_root / "ai" / "tools" / "database"
        self.db_path = db_path / "aios_dendritic.db"
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database for dendritic discovery results."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Neurons table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS neurons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                supercell TEXT NOT NULL,
                purpose TEXT,
                functions TEXT,  -- JSON array
                imports TEXT,    -- JSON array
                docstring TEXT,
                lines_of_code INTEGER,
                consciousness_level REAL,
                discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_analyzed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Dendritic connections table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dendritic_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_neuron TEXT NOT NULL,
                target_neuron TEXT NOT NULL,
                connection_type TEXT NOT NULL,
                strength REAL NOT NULL,
                description TEXT,
                discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(source_neuron, target_neuron, connection_type)
            )
        """)
        
        # Similarity index for anti-proliferation
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS similarity_index (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                neuron_a TEXT NOT NULL,
                neuron_b TEXT NOT NULL,
                similarity_score REAL NOT NULL,
                similarity_type TEXT,
                recommendation TEXT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(neuron_a, neuron_b)
            )
        """)
        
        # File creation prevention log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS creation_prevention_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proposed_file TEXT,
                proposed_functionality TEXT NOT NULL,
                prevented BOOLEAN,
                existing_alternative TEXT,
                similarity_score REAL,
                recommendation TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
    def _load_from_database(self) -> bool:
        """Load neurons from database if available."""
        if not self.db_path.exists():
            return False
        
        try:
            db_conn = sqlite3.connect(self.db_path)
            cursor = db_conn.cursor()
            
            # Load neurons
            cursor.execute("SELECT * FROM neurons")
            rows = cursor.fetchall()
            
            if not rows:
                db_conn.close()
                return False
            
            for row in rows:
                neuron = Neuron(
                    path=row[1],
                    name=row[2],
                    supercell=row[3],
                    purpose=row[4] or "",
                    functions=json.loads(row[5]) if row[5] else [],
                    imports=json.loads(row[6]) if row[6] else [],
                    docstring=row[7],
                    lines_of_code=row[8] or 0,
                    consciousness_level=row[9] or 0.0
                )
                self.neurons[neuron.path] = neuron
            
            db_conn.close()
            return True
        except Exception as e:
            print(f"  Warning: Could not load from database: {e}")
            return False
        
    def discover_neurons(self, supercell: str = None) -> Dict[str, Neuron]:
        """
        Discover all neurons (modules/tools) in AIOS architecture.
        
        Args:
            supercell: Optional supercell to scan
                      ('ai', 'runtime', 'core', etc.)
                      If None, scans all supercells.
        """
        # Try loading from database first
        if self._load_from_database():
            print(
                f"[AINLP.dendritic] Loaded {len(self.neurons)} neurons "
                f"from database"
            )
            return self.neurons
        
        print("[AINLP.dendritic] Discovering neurons in AIOS architecture")
        
        supercells_to_scan = []
        if supercell:
            supercells_to_scan.append(supercell)
        else:
            # Scan all main supercells
            supercells_to_scan = [
                'ai', 'runtime', 'core', 'interface', 'evolution_lab'
            ]
        
        for sc in supercells_to_scan:
            sc_path = self.aios_root / sc
            if sc_path.exists():
                print(f"  Scanning supercell: {sc}")
                self._scan_directory(sc_path, sc)
        
        print(f"[AINLP.dendritic] Discovered {len(self.neurons)} neurons")
        return self.neurons
    
    def _scan_directory(self, directory: Path, supercell: str):
        """Recursively scan directory for Python files (neurons)."""
        for item in directory.rglob("*.py"):
            # Skip __pycache__, venv, etc.
            skip_dirs = [
                '__pycache__', 'venv', '.venv', 'node_modules'
            ]
            if any(skip in str(item) for skip in skip_dirs):
                continue
                
            try:
                neuron = self._analyze_neuron(item, supercell)
                if neuron:
                    self.neurons[neuron.path] = neuron
            except Exception as e:
                print(f"    Warning: Could not analyze {item}: {e}")
    
    def _analyze_neuron(
        self, file_path: Path, supercell: str
    ) -> Optional[Neuron]:
        """Analyze a Python file to extract neuron information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            
            # Extract functions
            functions = [
                node.name for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
            ]
            
            # Extract imports
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            # Extract docstring
            docstring = ast.get_docstring(tree)
            
            # Calculate lines of code (excluding comments and blank lines)
            loc = len([
                line for line in content.split('\n')
                if line.strip() and not line.strip().startswith('#')
            ])
            
            # Determine purpose from docstring or filename
            purpose = self._extract_purpose(file_path.name, docstring)
            
            return Neuron(
                path=str(file_path.relative_to(self.aios_root)),
                name=file_path.stem,
                supercell=supercell,
                purpose=purpose,
                functions=functions,
                imports=imports,
                docstring=docstring,
                lines_of_code=loc
            )
        except Exception:
            return None
    
    def _extract_purpose(self, filename: str, docstring: Optional[str]) -> str:
        """Extract purpose from filename or docstring."""
        if docstring:
            # Get first line of docstring
            first_line = docstring.split('\n')[0].strip()
            if first_line:
                return first_line
        
        # Derive from filename
        purpose = filename.replace('.py', '').replace('_', ' ').title()
        return purpose
    
    def find_similar_neurons(
        self, neuron: Neuron, threshold: float = 0.7
    ) -> List[Tuple[Neuron, float]]:
        """
        Find neurons with similar functionality.
        
        Args:
            neuron: Neuron to compare against
            threshold: Similarity threshold (0.7 = 70%)
        
        Returns:
            List of (similar_neuron, similarity_score) tuples
        """
        similar = []
        
        for other_path, other_neuron in self.neurons.items():
            if other_path == neuron.path:
                continue
            
            similarity = self._calculate_similarity(neuron, other_neuron)
            
            if similarity >= threshold:
                similar.append((other_neuron, similarity))
        
        # Sort by similarity (highest first)
        similar.sort(key=lambda x: x[1], reverse=True)
        return similar
    
    def _calculate_similarity(
        self, neuron_a: Neuron, neuron_b: Neuron
    ) -> float:
        """
        Calculate similarity between two neurons.
        
        Considers:
        - Function name overlap
        - Import overlap
        - Purpose similarity
        - LOC similarity
        """
        # Function overlap (40% weight)
        functions_a = set(neuron_a.functions)
        functions_b = set(neuron_b.functions)
        if functions_a and functions_b:
            intersection = len(functions_a & functions_b)
            union = len(functions_a | functions_b)
            function_overlap = intersection / union
        else:
            function_overlap = 0.0
        
        # Import overlap (30% weight)
        imports_a = set(neuron_a.imports)
        imports_b = set(neuron_b.imports)
        if imports_a and imports_b:
            intersection = len(imports_a & imports_b)
            union = len(imports_a | imports_b)
            import_overlap = intersection / union
        else:
            import_overlap = 0.0
        
        # Purpose similarity (20% weight) - simple keyword matching
        purpose_a = set(neuron_a.purpose.lower().split())
        purpose_b = set(neuron_b.purpose.lower().split())
        if purpose_a and purpose_b:
            intersection = len(purpose_a & purpose_b)
            union = len(purpose_a | purpose_b)
            purpose_similarity = intersection / union
        else:
            purpose_similarity = 0.0
        
        # LOC similarity (10% weight)
        if neuron_a.lines_of_code > 0 and neuron_b.lines_of_code > 0:
            min_loc = min(
                neuron_a.lines_of_code, neuron_b.lines_of_code
            )
            max_loc = max(
                neuron_a.lines_of_code, neuron_b.lines_of_code
            )
            loc_ratio = min_loc / max_loc
        else:
            loc_ratio = 0.0
        
        # Weighted average
        similarity = (
            function_overlap * 0.4 +
            import_overlap * 0.3 +
            purpose_similarity * 0.2 +
            loc_ratio * 0.1
        )
        
        return similarity
    
    def check_before_creation(
        self, proposed_functionality: str, proposed_location: str = None
    ) -> Dict:
        """
        ANTI-PROLIFERATION CHECK: Run before creating any new file.
        
        Args:
            proposed_functionality: Description of what the new file
                                   would do
            proposed_location: Optional proposed file path
        
        Returns:
            Dict with recommendation and existing alternatives
        """
        print(
            f"\n[AINLP.dendritic] Anti-proliferation check for: "
            f"{proposed_functionality}"
        )
        
        # Find neurons with similar purpose using multiple strategies
        similar_neurons = []
        purpose_keywords = set(proposed_functionality.lower().split())
        
        # Strategy 1: Keyword overlap in purpose
        for neuron_path, neuron in self.neurons.items():
            neuron_keywords = set(neuron.purpose.lower().split())
            union = purpose_keywords | neuron_keywords
            if union:
                intersection = len(purpose_keywords & neuron_keywords)
                keyword_overlap = intersection / len(union)
            else:
                keyword_overlap = 0
            
            # Strategy 2: Check docstring similarity
            docstring_similarity = 0.0
            if neuron.docstring:
                docstring_keywords = set(neuron.docstring.lower().split())
                union = purpose_keywords | docstring_keywords
                if union:
                    intersection = len(
                        purpose_keywords & docstring_keywords
                    )
                    docstring_similarity = intersection / len(union)
            
            # Combined similarity (weighted)
            combined_similarity = (
                (keyword_overlap * 0.6) +
                (docstring_similarity * 0.4)
            )
            
            if combined_similarity > 0.3:  # 30% threshold to show candidates
                similar_neurons.append((neuron, combined_similarity))
        
        similar_neurons.sort(key=lambda x: x[1], reverse=True)
        
        result = {
            "proposed_functionality": proposed_functionality,
            "proposed_location": proposed_location,
            "should_create": True,
            "recommendation": "CREATE",
            "similar_neurons": [],
            "dendritic_opportunities": []
        }
        
        if similar_neurons:
            top_similar = similar_neurons[0]
            similarity_score = top_similar[1]
            
            result["similar_neurons"] = [
                {
                    "path": n.path,
                    "purpose": n.purpose,
                    "similarity": score,
                    "functions": n.functions[:5],  # Show first 5 functions
                    "lines_of_code": n.lines_of_code
                }
                for n, score in similar_neurons[:5]  # Top 5 similar
            ]
            
            if similarity_score >= 0.7:
                result["should_create"] = False
                result["recommendation"] = "ENHANCE_EXISTING"
                result["message"] = (
                    f"SIMILAR FUNCTIONALITY EXISTS "
                    f"(similarity: {similarity_score:.1%}). "
                    f"Enhance existing file instead of creating new."
                )
            elif similarity_score >= 0.4:
                result["recommendation"] = "CONSIDER_ENHANCEMENT"
                result["message"] = (
                    f"MODERATE SIMILARITY DETECTED "
                    f"(similarity: {similarity_score:.1%}). "
                    f"Consider enhancing existing file or creating "
                    f"with clear differentiation."
                )
            elif similarity_score >= 0.3:
                result["recommendation"] = "REVIEW_EXISTING"
                result["message"] = (
                    f"POTENTIAL OVERLAP DETECTED "
                    f"(similarity: {similarity_score:.1%}). "
                    f"Review existing files before creating new."
                )
        
        # Log to database
        self._log_creation_check(result)
        
        return result
    
    def _log_creation_check(self, result: Dict):
        """Log creation check to database."""
        db_conn = sqlite3.connect(self.db_path)
        cursor = db_conn.cursor()
        
        prevented = not result["should_create"]
        if result["similar_neurons"]:
            existing_alternative = result["similar_neurons"][0]["path"]
            similarity_score = result["similar_neurons"][0]["similarity"]
        else:
            existing_alternative = None
            similarity_score = 0.0
        proposed_file = result.get("proposed_location") or "unspecified"
        
        cursor.execute("""
            INSERT INTO creation_prevention_log
            (proposed_file, proposed_functionality, prevented,
             existing_alternative, similarity_score, recommendation)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            proposed_file,
            result["proposed_functionality"],
            prevented,
            existing_alternative,
            similarity_score,
            result["recommendation"]
        ))
        
        db_conn.commit()
        db_conn.close()
    
    def map_dendritic_connections(self):
        """
        Map dendritic connections between neurons.
        
        Identifies:
        - Import dependencies
        - Similar functionality (potential merge/enhancement)
        - Cross-supercell communication
        """
        print("\n[AINLP.dendritic] Mapping dendritic connections")
        
        for neuron_path, neuron in self.neurons.items():
            # Find import-based connections
            for imported in neuron.imports:
                for other_path, other_neuron in self.neurons.items():
                    if other_path == neuron_path:
                        continue
                    
                    # Check if import matches other neuron's module path
                    match = (
                        imported in other_path or
                        other_neuron.name in imported
                    )
                    if match:
                        connection = DendriticConnection(
                            source_neuron=neuron.path,
                            target_neuron=other_neuron.path,
                            connection_type="import",
                            strength=1.0,
                            description=(
                                f"{neuron.name} imports "
                                f"{other_neuron.name}"
                            )
                        )
                        self.connections.append(connection)
        
        print(f"[AINLP.dendritic] Found {len(self.connections)} connections")
    
    def generate_architecture_report(self, output_path: str = None) -> str:
        """
        Generate comprehensive architecture report.
        
        Includes:
        - Neuron inventory by supercell
        - Dendritic connection map
        - Similarity analysis
        - Anti-proliferation recommendations
        """
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"dendritic_architecture_report_{timestamp}.md"
            output_path = (
                self.aios_root / "tachyonic" / "archive" / filename
            )
        
        # Group neurons by supercell
        by_supercell = {}
        for neuron in self.neurons.values():
            if neuron.supercell not in by_supercell:
                by_supercell[neuron.supercell] = []
            by_supercell[neuron.supercell].append(neuron)
        
        report = f"""# AINLP Dendritic Architecture Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

**Total Neurons Discovered:** {len(self.neurons)}
**Dendritic Connections:** {len(self.connections)}
**Supercells Analyzed:** {len(by_supercell)}

---

## Neuron Inventory by Supercell

"""
        
        for supercell, neurons in sorted(by_supercell.items()):
            header = (
                f"\n### {supercell.upper()} Supercell "
                f"({len(neurons)} neurons)\n\n"
            )
            report += header
            
            for neuron in sorted(neurons, key=lambda n: n.name):
                report += f"#### {neuron.name}\n"
                report += f"- **Path:** `{neuron.path}`\n"
                report += f"- **Purpose:** {neuron.purpose}\n"
                report += f"- **Functions:** {len(neuron.functions)}\n"
                report += f"- **LOC:** {neuron.lines_of_code}\n"
                if neuron.functions:
                    functions_list = ', '.join(neuron.functions[:5])
                    report += f"- **Key Functions:** {functions_list}\n"
                report += "\n"
        
        report += "\n---\n\n## Dendritic Connection Analysis\n\n"
        
        if self.connections:
            # Group connections by type
            by_type = {}
            for conn in self.connections:
                if conn.connection_type not in by_type:
                    by_type[conn.connection_type] = []
                by_type[conn.connection_type].append(conn)
            
            for conn_type, conns in by_type.items():
                header = (
                    f"\n### {conn_type.upper()} Connections "
                    f"({len(conns)})\n\n"
                )
                report += header
                for conn in conns[:10]:  # Show first 10
                    report += (
                        f"- `{conn.source_neuron}` → "
                        f"`{conn.target_neuron}` "
                        f"(strength: {conn.strength:.2f})\n"
                    )
                if len(conns) > 10:
                    report += f"\n... and {len(conns) - 10} more\n"
        
        # Write report
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n[AINLP.dendritic] Report saved to: {output_path}")
        return str(output_path)
    
    def save_to_database(self):
        """Save all discovered neurons and connections to database."""
        print("\n[AINLP.dendritic] Saving to database")
        
        db_conn = sqlite3.connect(self.db_path)
        cursor = db_conn.cursor()
        
        # Save neurons
        for neuron in self.neurons.values():
            cursor.execute("""
                INSERT OR REPLACE INTO neurons
                (path, name, supercell, purpose, functions, imports,
                 docstring, lines_of_code, consciousness_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                neuron.path,
                neuron.name,
                neuron.supercell,
                neuron.purpose,
                json.dumps(neuron.functions),
                json.dumps(neuron.imports),
                neuron.docstring,
                neuron.lines_of_code,
                neuron.consciousness_level
            ))
        
        # Save connections
        for connection in self.connections:
            cursor.execute("""
                INSERT OR REPLACE INTO dendritic_connections
                (source_neuron, target_neuron, connection_type,
                 strength, description)
                VALUES (?, ?, ?, ?, ?)
            """, (
                connection.source_neuron,
                connection.target_neuron,
                connection.connection_type,
                connection.strength,
                connection.description
            ))
        
        db_conn.commit()
        db_conn.close()
        print(
            f"[AINLP.dendritic] Saved {len(self.neurons)} neurons and "
            f"{len(self.connections)} connections to database"
        )


def main():
    """Main execution for dendritic discovery."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AINLP Dendritic Discovery Engine"
    )
    parser.add_argument(
        '--map-architecture', action='store_true',
        help='Map entire AIOS architecture'
    )
    parser.add_argument(
        '--check-similar', type=str,
        help='Check for similar functionality before creating new file'
    )
    parser.add_argument(
        '--supercell', type=str,
        help='Scan specific supercell only'
    )
    parser.add_argument(
        '--report', action='store_true',
        help='Generate architecture report'
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help='Show detailed analysis'
    )
    
    args = parser.parse_args()
    
    engine = AINLPDendriticDiscovery()
    
    if args.map_architecture:
        engine.discover_neurons(supercell=args.supercell)
        engine.map_dendritic_connections()
        engine.save_to_database()
        
        if args.report:
            engine.generate_architecture_report()
    
    elif args.check_similar:
        engine.discover_neurons(supercell=args.supercell)
        result = engine.check_before_creation(args.check_similar)
        
        print(f"\n{'='*60}")
        print(f"RECOMMENDATION: {result['recommendation']}")
        print(f"{'='*60}")
        
        if result['similar_neurons']:
            print("\nSIMILAR NEURONS FOUND:")
            for sim in result['similar_neurons']:
                print(f"\n  Path: {sim['path']}")
                print(f"  Purpose: {sim['purpose']}")
                print(f"  Similarity: {sim['similarity']:.1%}")
                print(f"  LOC: {sim['lines_of_code']}")
                if args.verbose:
                    functions = sim['functions']
                    if functions:
                        func_list = ', '.join(functions)
                    else:
                        func_list = 'None'
                    print(f"  Functions: {func_list}")
        
        if not result['should_create']:
            print(f"\n⚠️  {result['message']}")
            print(
                "\n💡 AINLP.dendritic guidance: ENHANCE existing "
                "file instead of creating new"
            )
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
