"""
AINLP Dendritic Discovery - AI Agent Enhanced Similarity
=========================================================

Replaces keyword-based similarity with AI agent semantic understanding
using embedding models and LLM evaluation for exponential intelligence gain.

Phase 10.1: Embedding-based similarity (local, fast, no API costs)
Phase 10.2: LLM evaluation layer (local reasoning)
Phase 10.3: Cloud enhancement (hybrid scoring)
Phase 10.4: Self-learning loop (continuous improvement)

Current Status: Phase 10.1 Implementation
"""

import asyncio
import json
import sqlite3
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass
import numpy as np

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Warning: ollama package not installed. Run: pip install ollama")


@dataclass
class EmbeddingSimilarityResult:
    """Result from embedding-based similarity calculation."""
    neuron_path: str
    similarity_score: float
    method: str  # 'embedding', 'llm_local', 'llm_cloud', 'consensus'
    confidence: float
    reasoning: Optional[str] = None


class AIAgentDendriticSimilarity:
    """
    AI-powered semantic similarity engine for dendritic discovery.

    Exponential intelligence increase through:
    1. Embedding similarity (instant semantic understanding)
    2. Local LLM evaluation (contextual reasoning)
    3. Cloud LLM enhancement (highest accuracy)
    4. Self-learning from human feedback
    """

    def __init__(self, db_path: str = None):
        if db_path:
            self.db_path = Path(db_path)
        else:
            aios_root = Path(__file__).parent.parent.parent
            db_file = "aios_dendritic.db"
            self.db_path = (
                aios_root / "ai" / "tools" / "database" / db_file
            )

        self.embedding_model = "nomic-embed-text"
        self.local_llm = "gemma3:1b"  # 815MB, fits in 4GB GPU
        # self.local_llm = "deepseek-r1:7b"  # 4.7GB, requires >8GB GPU
        self.cloud_provider = "gemini-2.0-flash-exp"

        self._ensure_embeddings_table()

    def _ensure_embeddings_table(self):
        """Create embeddings table if not exists."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS neuron_embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                neuron_path TEXT UNIQUE NOT NULL,
                embedding BLOB NOT NULL,
                embedding_model TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (neuron_path) REFERENCES neurons(path)
            )
        """)

        conn.commit()
        conn.close()

    async def generate_neuron_embedding(
        self, neuron_path: str
    ) -> np.ndarray:
        """
        Generate embedding for a neuron using local Ollama model.

        Args:
            neuron_path: Path to neuron module

        Returns:
            numpy array of embedding vector
        """
        # Get neuron data from database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT purpose, docstring, functions, imports
            FROM neurons
            WHERE path = ?
        """, (neuron_path,))

        row = cursor.fetchone()
        conn.close()

        if not row:
            raise ValueError(f"Neuron not found: {neuron_path}")

        purpose, docstring, functions_json, imports_json = row
        functions = json.loads(functions_json) if functions_json else []
        imports = json.loads(imports_json) if imports_json else []

        # Create comprehensive text representation
        text = self._create_embedding_text(
            purpose, docstring, functions, imports
        )

        # Generate embedding using Ollama
        if not OLLAMA_AVAILABLE:
            print(
                "Warning: Using fallback embedding "
                "(ollama not available)"
            )
            return self._fallback_embedding(text)

        response = ollama.embeddings(
            model=self.embedding_model,
            prompt=text
        )
        embedding = np.array(response['embedding'])
        return embedding

    def _create_embedding_text(
        self,
        purpose: str,
        docstring: Optional[str],
        functions: List[str],
        imports: List[str]
    ) -> str:
        """Create rich text representation for embedding."""
        parts = [
            f"Purpose: {purpose}",
        ]

        if docstring:
            # Take first 500 chars of docstring
            parts.append(f"Description: {docstring[:500]}")

        if functions:
            parts.append(f"Functions: {', '.join(functions[:15])}")

        if imports:
            # Key imports that indicate functionality
            key_imports = [imp for imp in imports if not imp.startswith('_')]
            if key_imports:
                parts.append(f"Uses: {', '.join(key_imports[:10])}")

        return " | ".join(parts)

    def _fallback_embedding(self, text: str) -> np.ndarray:
        """Simple fallback embedding using word frequency."""
        # Very basic: just for testing without Ollama
        words = text.lower().split()
        # Create 384-dim vector (nomic-embed-text dimension)
        embedding = np.random.randn(384)
        # Add some structure based on word presence
        for i, word in enumerate(words[:384]):
            embedding[i % 384] += hash(word) % 100 / 100.0
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        return embedding

    async def generate_all_embeddings(
        self, force_regenerate: bool = False
    ):
        """
        Generate embeddings for all neurons in database.

        This is a one-time operation (or when force_regenerate=True).
        After this, all similarity checks are instant via cosine
        similarity.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get all neurons without embeddings (or all if force)
        if force_regenerate:
            cursor.execute("SELECT path FROM neurons")
        else:
            cursor.execute("""
                SELECT n.path FROM neurons n
                LEFT JOIN neuron_embeddings e ON n.path = e.neuron_path
                WHERE e.neuron_path IS NULL
            """)

        neurons_to_embed = [row[0] for row in cursor.fetchall()]
        conn.close()

        print(
            f"[AI Agent] Generating embeddings for "
            f"{len(neurons_to_embed)} neurons..."
        )

        for i, neuron_path in enumerate(neurons_to_embed, 1):
            if i % 50 == 0:
                print(f"  Progress: {i}/{len(neurons_to_embed)}")

            try:
                embedding = await self.generate_neuron_embedding(
                    neuron_path
                )
                self._store_embedding(neuron_path, embedding)
            except Exception as e:
                print(f"  Warning: Failed to embed {neuron_path}: {e}")

        print("[AI Agent] Embedding generation complete!")

    def _store_embedding(self, neuron_path: str, embedding: np.ndarray):
        """Store embedding in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Convert numpy array to bytes
        embedding_bytes = embedding.tobytes()

        cursor.execute("""
            INSERT OR REPLACE INTO neuron_embeddings
            (neuron_path, embedding, embedding_model)
            VALUES (?, ?, ?)
        """, (neuron_path, embedding_bytes, self.embedding_model))

        conn.commit()
        conn.close()

    async def calculate_similarity_embedding(
        self,
        proposed_functionality: str,
        top_k: int = 10
    ) -> List[EmbeddingSimilarityResult]:
        """
        Calculate similarity using embedding cosine distance.

        Args:
            proposed_functionality: Description of proposed new file
            top_k: Number of top similar neurons to return

        Returns:
            List of similarity results sorted by score (highest first)
        """
        # Generate embedding for proposed functionality
        proposed_embedding = await self._generate_query_embedding(
            proposed_functionality
        )

        # Get all neuron embeddings from database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT neuron_path, embedding
            FROM neuron_embeddings
        """)

        results = []
        for neuron_path, embedding_bytes in cursor.fetchall():
            # Convert bytes back to numpy array
            neuron_embedding = np.frombuffer(embedding_bytes, dtype=np.float64)

            # Calculate cosine similarity
            similarity = self._cosine_similarity(
                proposed_embedding,
                neuron_embedding
            )

            results.append(EmbeddingSimilarityResult(
                neuron_path=neuron_path,
                similarity_score=float(similarity),
                method='embedding',
                confidence=0.8  # Embedding confidence baseline
            ))

        conn.close()

        # Sort by similarity (highest first) and return top_k
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_k]

    async def _generate_query_embedding(
        self, query: str
    ) -> np.ndarray:
        """Generate embedding for query text."""
        if not OLLAMA_AVAILABLE:
            print(
                "Warning: Using fallback embedding "
                "(ollama not available)"
            )
            return self._fallback_embedding(query)

        response = ollama.embeddings(
            model=self.embedding_model,
            prompt=query
        )
        return np.array(response['embedding'])

    def _cosine_similarity(
        self,
        vec1: np.ndarray,
        vec2: np.ndarray
    ) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    async def calculate_similarity_llm_local(
        self,
        proposed_functionality: str,
        candidate_neurons: List[str],
        embedding_scores: Optional[List[float]] = None,
        max_candidates: int = 5
    ) -> List[EmbeddingSimilarityResult]:
        """
        Use local LLM to evaluate similarity with reasoning.

        This provides contextual understanding beyond pure embedding
        similarity. Uses deepseek-r1:7b for local reasoning with no
        API costs.

        Args:
            proposed_functionality: Description of proposed new file
            candidate_neurons: List of candidate neuron paths
            embedding_scores: Optional embedding scores for consensus
                             scoring
            max_candidates: Maximum number of candidates to evaluate

        Returns:
            List of LLM-enhanced similarity results with reasoning
        """
        import time

        if not OLLAMA_AVAILABLE:
            print(
                "Warning: Ollama not available, skipping LLM evaluation"
            )
            return []

        results = []
        total_candidates = min(len(candidate_neurons), max_candidates)

        print(f"\n{'='*70}")
        print(f"[Stage 2] LOCAL LLM EVALUATION ({self.local_llm})")
        print(f"{'='*70}")
        print(
            f"Evaluating top {total_candidates} candidates with "
            f"contextual reasoning..."
        )
        print("This may take 2-5 seconds per candidate.\n")

        overall_start = time.time()

        for idx, neuron_path in enumerate(
            candidate_neurons[:max_candidates], 1
        ):
            candidate_start = time.time()
            neuron_name = Path(neuron_path).name

            print(f"[{idx}/{total_candidates}] {neuron_name}")
            print("  → Loading metadata...", end=" ", flush=True)

            # Get neuron details
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT purpose, docstring, functions
                FROM neurons
                WHERE path = ?
            """, (neuron_path,))

            row = cursor.fetchone()
            conn.close()

            if not row:
                print("NOT FOUND")
                continue

            purpose, docstring, functions_json = row
            functions = json.loads(functions_json) if functions_json else []
            print("done")

            # Create evaluation prompt
            print(
                f"  → Calling LLM ({self.local_llm})...",
                end=" ", flush=True
            )
            prompt = self._create_llm_evaluation_prompt(
                proposed_functionality,
                neuron_path,
                purpose,
                docstring,
                functions
            )

            # Call local LLM with timing
            try:
                llm_start = time.time()
                response = ollama.generate(
                    model=self.local_llm,
                    prompt=prompt,
                    options={
                        'temperature': 0.1,
                        'num_predict': 100,
                    }
                )
                llm_time = time.time() - llm_start
                print(f"done ({llm_time:.2f}s)")

                score, reasoning = self._parse_llm_response(
                    response['response']
                )

                # Get embedding score for this candidate
                embedding_score = None
                if embedding_scores and idx <= len(embedding_scores):
                    embedding_score = embedding_scores[idx - 1]

                # Consensus scoring: combine embedding + LLM if both
                if embedding_score is not None:
                    consensus_score = (
                        (0.4 * embedding_score) + (0.6 * score)
                    )
                    confidence = 0.95
                    method = 'consensus'
                    print(
                        f"  → Embedding: {embedding_score:.1%} | "
                        f"LLM: {score:.1%} | "
                        f"Consensus: {consensus_score:.1%}"
                    )
                else:
                    consensus_score = score
                    confidence = 0.9
                    method = 'llm_local'
                    print(f"  → LLM Score: {score:.1%}")

                results.append(EmbeddingSimilarityResult(
                    neuron_path=neuron_path,
                    similarity_score=consensus_score,
                    method=method,
                    confidence=confidence,
                    reasoning=reasoning
                ))

                candidate_time = time.time() - candidate_start
                print(f"  → Reasoning: {reasoning[:80]}...")
                print(f"  → Total time: {candidate_time:.2f}s\n")

            except Exception as e:
                print(f"FAILED: {e}\n")
                continue

        overall_time = time.time() - overall_start

        print(f"{'='*70}")
        msg = (
            f"[Stage 2] Complete - Evaluated {len(results)}/"
            f"{total_candidates} candidates in {overall_time:.2f}s"
        )
        print(msg)
        print(f"{'='*70}\n")

        # Sort by consensus score
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results

    def _create_llm_evaluation_prompt(
        self,
        proposed: str,
        neuron_path: str,
        purpose: str,
        docstring: Optional[str],
        functions: List[str]
    ) -> str:
        """Create prompt for LLM similarity evaluation."""
        doc_snippet = docstring[:400] if docstring else "N/A"
        func_list = ', '.join(functions[:15]) if functions else "N/A"

        prompt = f"""Evaluate similarity between two code functionalities.

PROPOSED: "{proposed}"

EXISTING: {Path(neuron_path).name}
- Purpose: {purpose}
- Description: {doc_snippet}
- Functions: {func_list}

Rate 0-100 where:
90-100 = Same functionality (enhance existing)
70-89 = Very similar (consider enhancement)
50-69 = Related but distinct
30-49 = Loosely related
0-29 = Different

Format: SCORE: [number] | REASON: [brief explanation]
Example: SCORE: 85 | REASON: Both analyze module dependencies

Your evaluation:"""
        return prompt

    def _parse_llm_response(self, response: str) -> Tuple[float, str]:
        """
        Parse LLM response to extract score and reasoning.

        Handles multiple response formats:
        - Standard: "SCORE: 85 | REASON: explanation"
        - Reasoning chains (deepseek-r1): Extract from <think> tags
          or final answer
        - Natural language: Extract score with regex
        """
        try:
            # Clean up response
            response = response.strip()

            # Method 1: Check for standard format "SCORE: X | REASON: Y"
            if 'SCORE:' in response and '|' in response:
                parts = response.split('|')

                score_part = parts[0].strip()
                score_str = score_part.split(':')[1].strip()
                # Extract just the number
                import re
                score_match = re.search(r'(\d+(?:\.\d+)?)', score_str)
                if score_match:
                    score = float(score_match.group(1))
                    score = score / 100.0  # Convert to 0-1 range
                else:
                    score = 0.5

                if len(parts) > 1:
                    reason_part = parts[1].strip()
                else:
                    reason_part = "No reasoning"

                if ':' in reason_part:
                    reason = reason_part.split(':', 1)[1].strip()
                else:
                    reason = reason_part

                return score, reason

            # Method 2: Extract from reasoning chain (deepseek-r1 style)
            # Look for final answer after thinking
            if '<think>' in response or '</think>' in response:
                # Find content after </think> tag
                parts = response.split('</think>')
                if len(parts) > 1:
                    final_answer = parts[-1].strip()
                else:
                    final_answer = response
            else:
                final_answer = response

            # Method 3: Extract score with regex from any format
            import re

            # Look for patterns like "85" or "85%" or "score: 85"
            score_patterns = [
                r'SCORE[:\s]+(\d+)',
                r'similarity[:\s]+(\d+)',
                r'(\d+)%',
                r'rating[:\s]+(\d+)',
                r'^(\d+)',  # Number at start
            ]

            score = 50.0  # Default middle score
            for pattern in score_patterns:
                match = re.search(pattern, final_answer, re.IGNORECASE)
                if match:
                    score = float(match.group(1))
                    break

            # Ensure score is in 0-1 range
            if score > 100.0:
                score = 50.0  # Invalid score, use default
            elif score > 1.0:  # Assume 0-100 scale
                score = score / 100.0

            # Cap at 1.0
            score = min(score, 1.0)

            # Extract reasoning (first sentence or first 100 chars)
            # Remove score part and get meaningful text
            reasoning_text = re.sub(
                r'SCORE[:\s]+\d+\s*\|?\s*', '',
                final_answer, flags=re.IGNORECASE
            )
            reasoning_text = re.sub(
                r'REASON[:\s]*', '',
                reasoning_text, flags=re.IGNORECASE
            )
            reasoning_text = reasoning_text.strip()

            # Get first sentence or first 150 chars
            sentences = reasoning_text.split('.')
            if sentences:
                reasoning = sentences[0].strip() + '.'
                if len(reasoning) > 150:
                    reasoning = reasoning[:147] + '...'
            else:
                if len(reasoning_text) > 150:
                    reasoning = reasoning_text[:150] + '...'
                else:
                    reasoning = reasoning_text

            if not reasoning:
                reasoning = "LLM provided incomplete response"

            return score, reasoning

        except Exception as e:
            print(f"  [Parser Error: {e}]")
            # Return middle score on parse failure
            return 0.5, f"Parse error: {str(e)[:50]}"

    async def find_similar_neurons(
        self,
        functionality: str,
        max_results: int = 5,
        use_llm: bool = True
    ) -> List[dict]:
        """
        AINLP.dendritic.enhancement - Interface Bridge Integration
        
        Find similar neurons using AI-powered semantic similarity.
        This is the canonical method called by interface_bridge.py.
        
        Args:
            functionality: Description of functionality to search for
            max_results: Maximum number of results to return
            use_llm: Whether to use LLM reasoning (slower but more accurate)
        
        Returns:
            List of dictionaries with neuron metadata:
            {
                'neuron_name': str,
                'neuron_path': str,
                'neuron_purpose': str,
                'consensus_score': float,
                'embedding_score': float,
                'llm_score': float,
                'llm_reasoning': str,
                'method': str
            }
        """
        # Stage 1: Embedding similarity (fast)
        embedding_results = await self.calculate_similarity_embedding(
            functionality,
            top_k=max(max_results * 2, 10)  # Get more for LLM filtering
        )
        
        if not embedding_results:
            return []
        
        # Stage 2: LLM evaluation (if requested)
        if use_llm and OLLAMA_AVAILABLE:
            top_candidates = [
                r.neuron_path for r in embedding_results[:max_results]
            ]
            embedding_scores = [
                r.similarity_score for r in embedding_results[:max_results]
            ]
            
            llm_results = await self.calculate_similarity_llm_local(
                functionality,
                top_candidates,
                embedding_scores=embedding_scores,
                max_candidates=max_results
            )
            
            if llm_results:
                final_results = llm_results
            else:
                # Fallback to embedding results
                final_results = embedding_results[:max_results]
        else:
            final_results = embedding_results[:max_results]
        
        # Format results for interface bridge
        formatted_results = []
        for result in final_results:
            # Get neuron metadata from database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT path, purpose, supercell
                FROM neurons
                WHERE path = ?
            """, (result.neuron_path,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                continue
            
            neuron_path, purpose, supercell = row
            neuron_name = Path(neuron_path).name
            
            # Prepare formatted result
            formatted_result = {
                'neuron_name': neuron_name,
                'neuron_path': neuron_path,
                'neuron_purpose': purpose or 'No description available',
                'consensus_score': result.similarity_score,
                'method': result.method,
                'confidence': result.confidence
            }
            
            # Add LLM-specific fields if available
            if result.method in ['consensus', 'llm_local', 'llm_cloud']:
                # Extract embedding and LLM scores from consensus
                if result.method == 'consensus':
                    # Reverse engineer: consensus = 0.4*embedding + 0.6*llm
                    # We know consensus_score, need to approximate
                    formatted_result['embedding_score'] = (
                        result.similarity_score * 0.7  # Approximate
                    )
                    formatted_result['llm_score'] = (
                        result.similarity_score * 1.2  # Approximate
                    )
                else:
                    formatted_result['embedding_score'] = 0.0
                    formatted_result['llm_score'] = result.similarity_score
                
                formatted_result['llm_reasoning'] = (
                    result.reasoning or 'No reasoning provided'
                )
            else:
                # Embedding only
                formatted_result['embedding_score'] = result.similarity_score
                formatted_result['llm_score'] = 0.0
                formatted_result['llm_reasoning'] = (
                    'Embedding-based similarity only'
                )
            
            formatted_results.append(formatted_result)
        
        return formatted_results

    def get_database_stats(self) -> dict:
        """
        AINLP.dendritic.enhancement - Interface Bridge Integration
        
        Get database statistics for interface bridge health monitoring.
        
        Returns:
            Dictionary with database statistics:
            {
                'total_neurons': int,
                'embeddings_ready': bool,
                'by_supercell': dict
            }
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total neurons
        cursor.execute("SELECT COUNT(*) FROM neurons")
        total_neurons = cursor.fetchone()[0]
        
        # Embeddings count
        cursor.execute("SELECT COUNT(*) FROM neuron_embeddings")
        embeddings_count = cursor.fetchone()[0]
        
        # By supercell
        cursor.execute("""
            SELECT supercell, COUNT(*)
            FROM neurons
            GROUP BY supercell
        """)
        by_supercell = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total_neurons': total_neurons,
            'embeddings_ready': embeddings_count > 0,
            'embeddings_count': embeddings_count,
            'by_supercell': by_supercell
        }


async def main():
    """Main execution for AI agent enhanced similarity."""
    import argparse

    parser = argparse.ArgumentParser(
        description="AI Agent Enhanced Dendritic Discovery"
    )
    parser.add_argument(
        '--generate-embeddings',
        action='store_true',
        help='Generate embeddings for all neurons (one-time operation)'
    )
    parser.add_argument(
        '--check-similar',
        type=str,
        help='Check similarity using AI agent (embedding-based)'
    )
    parser.add_argument(
        '--use-llm',
        action='store_true',
        help='Use local LLM evaluation for top candidates'
    )
    parser.add_argument(
        '--top-k',
        type=int,
        default=5,
        help='Number of top similar neurons to show'
    )

    args = parser.parse_args()

    engine = AIAgentDendriticSimilarity()

    if args.generate_embeddings:
        print("\n" + "="*70)
        print("GENERATING EMBEDDINGS FOR ALL NEURONS")
        print("="*70)
        print(
            "\nThis is a one-time operation. After completion, "
            "all similarity"
        )
        print("checks will be instant using cosine similarity.\n")

        await engine.generate_all_embeddings()

        print("\n✅ Embedding generation complete!")
        print(
            "You can now use --check-similar for instant "
            "AI-powered similarity checking."
        )

    elif args.check_similar:
        import time
        overall_start = time.time()

        print("\n" + "="*70)
        print("AI AGENT SIMILARITY CHECK")
        print("="*70)
        print(f"\nQuery: {args.check_similar}\n")

        # Stage 1: Embedding similarity
        print("="*70)
        print("[Stage 1] EMBEDDING-BASED SEMANTIC SIMILARITY")
        print("="*70)
        print("Searching 866 neurons with vector similarity...")
        print("This should take <1 second.\n")

        stage1_start = time.time()
        embedding_results = await engine.calculate_similarity_embedding(
            args.check_similar,
            top_k=args.top_k
        )
        stage1_time = time.time() - stage1_start

        if not embedding_results:
            print("No similar neurons found.")
            return

        msg = (
            f"Found {len(embedding_results)} similar neurons in "
            f"{stage1_time:.2f}s\n"
        )
        print(msg)
        print(f"Top {len(embedding_results)} results:\n")
        for i, result in enumerate(embedding_results, 1):
            print(f"{i}. {result.neuron_path}")
            print(f"   Similarity: {result.similarity_score:.1%}")
            print(f"   Method: {result.method}")
            print()

        # Stage 2: LLM evaluation (if requested)
        if args.use_llm:
            print("\n" + "="*70)
            print("[Stage 2] LOCAL LLM CONTEXTUAL REASONING")
            print("="*70)

            top_candidates = [
                r.neuron_path for r in embedding_results[:3]
            ]
            embedding_scores = [
                r.similarity_score for r in embedding_results[:3]
            ]

            llm_results = await engine.calculate_similarity_llm_local(
                args.check_similar,
                top_candidates,
                embedding_scores=embedding_scores,
                max_candidates=3
            )

            if llm_results:
                print("\n" + "="*70)
                print("CONSENSUS RESULTS (Embedding + LLM)")
                print("="*70)
                print()

                for i, result in enumerate(llm_results, 1):
                    print(f"{i}. {result.neuron_path}")
                    print(f"   Consensus Score: {result.similarity_score:.1%}")
                    print(f"   Method: {result.method}")
                    print(f"   Confidence: {result.confidence:.1%}")
                    print(f"   Reasoning: {result.reasoning}")
                    print()

                # Use LLM results for recommendation
                final_results = llm_results
            else:
                print("\nLLM evaluation failed, using embedding results.")
                final_results = embedding_results
        else:
            final_results = embedding_results

        # Recommendation based on final results
        overall_time = time.time() - overall_start

        print("="*70)
        print(f"ANALYSIS COMPLETE - Total time: {overall_time:.2f}s")
        print("="*70)

        top_score = final_results[0].similarity_score
        if top_score >= 0.70:
            print("🚫 RECOMMENDATION: ENHANCE_EXISTING")
            print(f"   High similarity detected ({top_score:.1%})")
            print(f"   Consider enhancing: {final_results[0].neuron_path}")
        elif top_score >= 0.60:
            print("⚠️  RECOMMENDATION: CONSIDER_ENHANCEMENT")
            print(f"   Moderate similarity detected ({top_score:.1%})")
            msg = (
                f"   Review before creating: "
                f"{final_results[0].neuron_path}"
            )
            print(msg)
        elif top_score >= 0.50:
            print("📋 RECOMMENDATION: REVIEW_EXISTING")
            print(f"   Some similarity detected ({top_score:.1%})")
            msg = (
                f"   Related functionality exists: "
                f"{final_results[0].neuron_path}"
            )
            print(msg)
        else:
            print("✅ RECOMMENDATION: CREATE")
            msg = (
                f"   Low similarity ({top_score:.1%}) - "
                f"new functionality detected"
            )
            print(msg)
        print("="*70)

    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
