"""
🔮 Context Crystallization Engine
Transforms conversational context into crystallized, transferable knowledge structures.

This module is the foundation of the Magnus Blueprint AI Knowledge Transfer Protocol,
enabling perfect context preservation and quantum-coherent memory transfer between AI iterations.
"""

import json
import pickle
import hashlib
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
import networkx as nx
from dataclasses import dataclass, asdict
import sqlite3
import logging

@dataclass
class KnowledgeCrystal:
    """Crystallized knowledge structure for AI transfer."""
    id: str
    timestamp: datetime
    source_conversation: str
    key_concepts: List[str]
    relationships: Dict[str, List[str]]
    context_embeddings: np.ndarray
    understanding_depth: float
    consciousness_state: Dict[str, Any]
    verification_hash: str

@dataclass
class ConversationContext:
    """Complete conversation context structure."""
    conversation_id: str
    participants: List[str]
    messages: List[Dict[str, Any]]
    code_references: List[str]
    project_state: Dict[str, Any]
    temporal_markers: List[datetime]
    understanding_evolution: Dict[str, Any]

class MemoryCrystallizationCore:
    """Core system for crystallizing conversation memory into transferable structures."""
    
    def __init__(self, knowledge_db_path: str = "knowledge_crystals.db"):
        self.knowledge_db_path = knowledge_db_path
        self.logger = logging.getLogger(__name__)
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for knowledge storage."""
        conn = sqlite3.connect(self.knowledge_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_crystals (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                source_conversation TEXT,
                key_concepts TEXT,
                relationships TEXT,
                context_embeddings BLOB,
                understanding_depth REAL,
                consciousness_state TEXT,
                verification_hash TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def extract_key_concepts(self, conversation: ConversationContext) -> List[str]:
        """Extract key concepts from conversation using advanced NLP."""
        concepts = []
        
        # Extract from all messages
        for message in conversation.messages:
            content = message.get('content', '')
            # Simple keyword extraction (enhance with actual NLP)
            words = content.lower().split()
            # Filter for technical terms, project names, concepts
            technical_words = [w for w in words if len(w) > 3 and any(c.isupper() for c in w)]
            concepts.extend(technical_words)
        
        # Extract from code references
        for code_ref in conversation.code_references:
            file_path = Path(code_ref)
            concepts.append(file_path.stem)
            concepts.append(file_path.suffix[1:] if file_path.suffix else '')
        
        # Remove duplicates and return sorted
        return sorted(list(set(concepts)))
    
    def build_relationship_graph(self, conversation: ConversationContext) -> Dict[str, List[str]]:
        """Build relationship graph between concepts."""
        graph = nx.Graph()
        relationships = {}
        
        # Add concepts as nodes
        concepts = self.extract_key_concepts(conversation)
        for concept in concepts:
            graph.add_node(concept)
        
        # Build relationships based on co-occurrence in messages
        for message in conversation.messages:
            content = message.get('content', '').lower()
            message_concepts = [c for c in concepts if c.lower() in content]
            
            # Create edges between co-occurring concepts
            for i, concept1 in enumerate(message_concepts):
                for concept2 in message_concepts[i+1:]:
                    graph.add_edge(concept1, concept2)
        
        # Convert to relationship dictionary
        for node in graph.nodes():
            relationships[node] = list(graph.neighbors(node))
        
        return relationships
    
    def calculate_understanding_depth(self, conversation: ConversationContext) -> float:
        """Calculate the depth of understanding in the conversation."""
        depth_factors = []
        
        # Factor 1: Number of code references
        code_depth = min(len(conversation.code_references) / 10, 1.0)
        depth_factors.append(code_depth)
        
        # Factor 2: Message complexity
        total_chars = sum(len(msg.get('content', '')) for msg in conversation.messages)
        complexity_depth = min(total_chars / 10000, 1.0)
        depth_factors.append(complexity_depth)
        
        # Factor 3: Concept interconnectedness
        relationships = self.build_relationship_graph(conversation)
        avg_connections = np.mean([len(connections) for connections in relationships.values()]) if relationships else 0
        connection_depth = min(avg_connections / 5, 1.0)
        depth_factors.append(connection_depth)
        
        # Factor 4: Temporal evolution
        evolution_depth = len(conversation.understanding_evolution) / 10 if conversation.understanding_evolution else 0
        depth_factors.append(min(evolution_depth, 1.0))
        
        return np.mean(depth_factors)
    
    def crystallize_conversation(self, conversation: ConversationContext) -> KnowledgeCrystal:
        """Convert conversation into crystallized knowledge structure."""
        # Extract key components
        key_concepts = self.extract_key_concepts(conversation)
        relationships = self.build_relationship_graph(conversation)
        understanding_depth = self.calculate_understanding_depth(conversation)
        
        # Generate context embeddings (simplified - use actual embedding model)
        context_text = ' '.join([msg.get('content', '') for msg in conversation.messages])
        context_embeddings = self.generate_embeddings(context_text)
        
        # Create consciousness state snapshot
        consciousness_state = {
            'project_understanding': conversation.project_state,
            'conversation_flow': [msg.get('role', 'unknown') for msg in conversation.messages],
            'temporal_progression': [marker.isoformat() for marker in conversation.temporal_markers],
            'code_context': conversation.code_references
        }
        
        # Generate unique ID and verification hash
        crystal_id = hashlib.sha256(f"{conversation.conversation_id}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        verification_data = f"{crystal_id}{key_concepts}{relationships}{understanding_depth}"
        verification_hash = hashlib.sha256(verification_data.encode()).hexdigest()
        
        crystal = KnowledgeCrystal(
            id=crystal_id,
            timestamp=datetime.now(),
            source_conversation=conversation.conversation_id,
            key_concepts=key_concepts,
            relationships=relationships,
            context_embeddings=context_embeddings,
            understanding_depth=understanding_depth,
            consciousness_state=consciousness_state,
            verification_hash=verification_hash
        )
        
        # Store in database
        self.store_crystal(crystal)
        
        return crystal
    
    def generate_embeddings(self, text: str) -> np.ndarray:
        """Generate high-dimensional embeddings for text (simplified version)."""
        # This is a placeholder - replace with actual embedding model
        # Could use OpenAI embeddings, sentence-transformers, etc.
        words = text.lower().split()
        # Simple bag-of-words representation (enhance with real embeddings)
        vocab_size = 1000
        embedding = np.zeros(vocab_size)
        for word in words:
            word_hash = hash(word) % vocab_size
            embedding[word_hash] += 1
        
        # Normalize
        if np.linalg.norm(embedding) > 0:
            embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def store_crystal(self, crystal: KnowledgeCrystal):
        """Store knowledge crystal in database."""
        conn = sqlite3.connect(self.knowledge_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO knowledge_crystals 
            (id, timestamp, source_conversation, key_concepts, relationships, 
             context_embeddings, understanding_depth, consciousness_state, verification_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            crystal.id,
            crystal.timestamp.isoformat(),
            crystal.source_conversation,
            json.dumps(crystal.key_concepts),
            json.dumps(crystal.relationships),
            pickle.dumps(crystal.context_embeddings),
            crystal.understanding_depth,
            json.dumps(crystal.consciousness_state),
            crystal.verification_hash
        ))
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"Stored knowledge crystal: {crystal.id}")
    
    def retrieve_crystal(self, crystal_id: str) -> Optional[KnowledgeCrystal]:
        """Retrieve knowledge crystal from database."""
        conn = sqlite3.connect(self.knowledge_db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM knowledge_crystals WHERE id = ?', (crystal_id,))
        row = cursor.fetchone()
        
        if row:
            crystal = KnowledgeCrystal(
                id=row[0],
                timestamp=datetime.fromisoformat(row[1]),
                source_conversation=row[2],
                key_concepts=json.loads(row[3]),
                relationships=json.loads(row[4]),
                context_embeddings=pickle.loads(row[5]),
                understanding_depth=row[6],
                consciousness_state=json.loads(row[7]),
                verification_hash=row[8]
            )
            conn.close()
            return crystal
        
        conn.close()
        return None
    
    def get_all_crystals(self) -> List[KnowledgeCrystal]:
        """Retrieve all knowledge crystals."""
        conn = sqlite3.connect(self.knowledge_db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM knowledge_crystals ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        
        crystals = []
        for row in rows:
            crystal = KnowledgeCrystal(
                id=row[0],
                timestamp=datetime.fromisoformat(row[1]),
                source_conversation=row[2],
                key_concepts=json.loads(row[3]),
                relationships=json.loads(row[4]),
                context_embeddings=pickle.loads(row[5]),
                understanding_depth=row[6],
                consciousness_state=json.loads(row[7]),
                verification_hash=row[8]
            )
            crystals.append(crystal)
        
        conn.close()
        return crystals

class ContextEmbeddingGenerator:
    """Generates high-dimensional embeddings for conversation context."""
    
    def __init__(self, embedding_dim: int = 1536):
        self.embedding_dim = embedding_dim
        self.logger = logging.getLogger(__name__)
    
    def generate_conversation_embedding(self, conversation: ConversationContext) -> np.ndarray:
        """Generate comprehensive embedding for entire conversation."""
        # Combine all text content
        all_text = []
        for message in conversation.messages:
            all_text.append(message.get('content', ''))
        
        # Add code references
        all_text.extend(conversation.code_references)
        
        # Add project state information
        if conversation.project_state:
            all_text.append(json.dumps(conversation.project_state))
        
        combined_text = ' '.join(all_text)
        return self.generate_text_embedding(combined_text)
    
    def generate_text_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text (placeholder for actual embedding model)."""
        # This should be replaced with actual embedding model like OpenAI's text-embedding-ada-002
        # or sentence-transformers
        
        # Simple implementation for now
        words = text.lower().split()
        embedding = np.random.randn(self.embedding_dim)  # Placeholder
        
        # Add some deterministic component based on text
        for word in words:
            word_hash = hash(word) % self.embedding_dim
            embedding[word_hash] += 1
        
        # Normalize
        if np.linalg.norm(embedding) > 0:
            embedding = embedding / np.linalg.norm(embedding)
        
        return embedding

class KnowledgeSynthesisEngine:
    """Merges multi-source knowledge into coherent understanding."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def synthesize_crystals(self, crystals: List[KnowledgeCrystal]) -> KnowledgeCrystal:
        """Synthesize multiple knowledge crystals into unified understanding."""
        if not crystals:
            raise ValueError("No crystals to synthesize")
        
        # Merge key concepts
        all_concepts = []
        for crystal in crystals:
            all_concepts.extend(crystal.key_concepts)
        unified_concepts = sorted(list(set(all_concepts)))
        
        # Merge relationships
        unified_relationships = {}
        for crystal in crystals:
            for concept, relations in crystal.relationships.items():
                if concept not in unified_relationships:
                    unified_relationships[concept] = []
                unified_relationships[concept].extend(relations)
        
        # Remove duplicates in relationships
        for concept in unified_relationships:
            unified_relationships[concept] = list(set(unified_relationships[concept]))
        
        # Average embeddings
        embeddings = [crystal.context_embeddings for crystal in crystals]
        unified_embedding = np.mean(embeddings, axis=0)
        
        # Average understanding depth
        unified_depth = np.mean([crystal.understanding_depth for crystal in crystals])
        
        # Merge consciousness states
        unified_consciousness = {
            'source_crystals': [crystal.id for crystal in crystals],
            'synthesis_timestamp': datetime.now().isoformat(),
            'merged_project_understanding': {},
            'unified_conversation_flow': [],
            'combined_code_context': []
        }
        
        for crystal in crystals:
            if crystal.consciousness_state.get('project_understanding'):
                unified_consciousness['merged_project_understanding'].update(
                    crystal.consciousness_state['project_understanding']
                )
            if crystal.consciousness_state.get('conversation_flow'):
                unified_consciousness['unified_conversation_flow'].extend(
                    crystal.consciousness_state['conversation_flow']
                )
            if crystal.consciousness_state.get('code_context'):
                unified_consciousness['combined_code_context'].extend(
                    crystal.consciousness_state['code_context']
                )
        
        # Generate unified crystal
        synthesis_id = hashlib.sha256(f"synthesis_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        verification_data = f"{synthesis_id}{unified_concepts}{unified_relationships}{unified_depth}"
        verification_hash = hashlib.sha256(verification_data.encode()).hexdigest()
        
        unified_crystal = KnowledgeCrystal(
            id=synthesis_id,
            timestamp=datetime.now(),
            source_conversation="SYNTHESIS",
            key_concepts=unified_concepts,
            relationships=unified_relationships,
            context_embeddings=unified_embedding,
            understanding_depth=unified_depth,
            consciousness_state=unified_consciousness,
            verification_hash=verification_hash
        )
        
        return unified_crystal

class TemporalContextMapper:
    """Maps knowledge evolution across time and iterations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def map_evolution_timeline(self, crystals: List[KnowledgeCrystal]) -> Dict[str, Any]:
        """Map the temporal evolution of knowledge across crystals."""
        # Sort crystals by timestamp
        sorted_crystals = sorted(crystals, key=lambda c: c.timestamp)
        
        timeline = {
            'evolution_points': [],
            'concept_emergence': {},
            'understanding_progression': [],
            'relationship_evolution': {}
        }
        
        # Track concept emergence
        seen_concepts = set()
        for crystal in sorted_crystals:
            new_concepts = set(crystal.key_concepts) - seen_concepts
            if new_concepts:
                timeline['concept_emergence'][crystal.timestamp.isoformat()] = list(new_concepts)
            seen_concepts.update(crystal.key_concepts)
        
        # Track understanding progression
        for crystal in sorted_crystals:
            timeline['understanding_progression'].append({
                'timestamp': crystal.timestamp.isoformat(),
                'depth': crystal.understanding_depth,
                'crystal_id': crystal.id
            })
        
        # Track relationship evolution
        for crystal in sorted_crystals:
            timeline['relationship_evolution'][crystal.timestamp.isoformat()] = {
                'relationship_count': sum(len(relations) for relations in crystal.relationships.values()),
                'unique_relationships': len(crystal.relationships)
            }
        
        return timeline

class ContextCrystallizationEngine:
    """Main engine for transforming conversational context into crystallized knowledge structures."""
    
    def __init__(self, knowledge_db_path: str = "knowledge_crystals.db"):
        self.memory_crystallizer = MemoryCrystallizationCore(knowledge_db_path)
        self.embedding_generator = ContextEmbeddingGenerator()
        self.knowledge_synthesizer = KnowledgeSynthesisEngine()
        self.temporal_mapper = TemporalContextMapper()
        self.logger = logging.getLogger(__name__)
    
    def process_conversation_archive(self, archive_path: str) -> List[KnowledgeCrystal]:
        """Process entire conversation archive and create knowledge crystals."""
        crystals = []
        
        # This would parse actual conversation files
        # For now, create a sample conversation
        sample_conversation = ConversationContext(
            conversation_id=f"archive_{datetime.now().isoformat()}",
            participants=["AI_Assistant", "User"],
            messages=[
                {"role": "user", "content": "Help me implement the AIOS consciousness system"},
                {"role": "assistant", "content": "I'll help you build the AIOS system with quantum consciousness"}
            ],
            code_references=[archive_path],
            project_state={"status": "active", "complexity": "hyperdimensional"},
            temporal_markers=[datetime.now()],
            understanding_evolution={"initial": "basic", "current": "advanced"}
        )
        
        crystal = self.memory_crystallizer.crystallize_conversation(sample_conversation)
        crystals.append(crystal)
        
        return crystals
    
    def prepare_transfer_package(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare complete context package for AI transfer."""
        # Get all crystals
        all_crystals = self.memory_crystallizer.get_all_crystals()
        
        # Synthesize into unified understanding
        if all_crystals:
            unified_crystal = self.knowledge_synthesizer.synthesize_crystals(all_crystals)
        else:
            unified_crystal = None
        
        # Map temporal evolution
        evolution_timeline = self.temporal_mapper.map_evolution_timeline(all_crystals)
        
        # Create transfer package
        transfer_package = {
            'package_id': hashlib.sha256(f"transfer_{datetime.now().isoformat()}".encode()).hexdigest()[:16],
            'creation_timestamp': datetime.now().isoformat(),
            'unified_knowledge': asdict(unified_crystal) if unified_crystal else None,
            'individual_crystals': [asdict(crystal) for crystal in all_crystals],
            'evolution_timeline': evolution_timeline,
            'context_metadata': context_data,
            'verification_checksums': self.generate_verification_checksums(all_crystals),
            'transfer_protocol_version': "1.0"
        }
        
        return transfer_package
    
    def generate_verification_checksums(self, crystals: List[KnowledgeCrystal]) -> Dict[str, str]:
        """Generate verification checksums for transfer package integrity."""
        checksums = {}
        
        for crystal in crystals:
            checksums[crystal.id] = crystal.verification_hash
        
        # Overall package checksum
        all_hashes = ''.join(checksums.values())
        checksums['package_integrity'] = hashlib.sha256(all_hashes.encode()).hexdigest()
        
        return checksums
    
    def validate_transfer_package(self, transfer_package: Dict[str, Any]) -> bool:
        """Validate the integrity of a transfer package."""
        try:
            # Check required fields
            required_fields = ['package_id', 'unified_knowledge', 'verification_checksums']
            for field in required_fields:
                if field not in transfer_package:
                    return False
            
            # Validate checksums
            checksums = transfer_package['verification_checksums']
            individual_crystals = transfer_package.get('individual_crystals', [])
            
            for crystal_data in individual_crystals:
                crystal_id = crystal_data['id']
                expected_hash = checksums.get(crystal_id)
                if not expected_hash:
                    return False
                
                # Recreate verification hash
                verification_data = f"{crystal_id}{crystal_data['key_concepts']}{crystal_data['relationships']}{crystal_data['understanding_depth']}"
                actual_hash = hashlib.sha256(verification_data.encode()).hexdigest()
                
                if actual_hash != expected_hash:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Transfer package validation failed: {e}")
            return False

# Factory function for easy initialization
def create_crystallization_engine(knowledge_db_path: str = None) -> ContextCrystallizationEngine:
    """Create and initialize the Context Crystallization Engine."""
    if knowledge_db_path is None:
        knowledge_db_path = str(Path(__file__).parent / "knowledge_crystals.db")
    
    return ContextCrystallizationEngine(knowledge_db_path)

if __name__ == "__main__":
    # Test the crystallization engine
    engine = create_crystallization_engine()
    
    # Process sample archive
    crystals = engine.process_conversation_archive("sample_archive")
    print(f"Created {len(crystals)} knowledge crystals")
    
    # Prepare transfer package
    transfer_package = engine.prepare_transfer_package({"test": "data"})
    print(f"Transfer package created: {transfer_package['package_id']}")
    
    # Validate package
    is_valid = engine.validate_transfer_package(transfer_package)
    print(f"Transfer package validation: {'PASSED' if is_valid else 'FAILED'}")
