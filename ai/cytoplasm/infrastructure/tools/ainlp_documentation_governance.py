#!/usr/bin/env python3
"""
AINLP Documentation Governance System
AINLP Standardized Namespace: Dendritic Anti-Proliferation Protocol
Purpose: Enforce intelligent documentation consolidation and prevent dendritic expansion chaos
"""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess
import difflib
from collections import Counter


@dataclass
class DocumentationRequest:
    """Represents a request to create or modify documentation."""

    topic: str
    target_directory: str
    content_type: str
    proposed_filename: str


@dataclass
class SimilarityResult:
    """Results of similarity analysis between documents."""

    target_file: str
    similarity_score: float
    recommended_action: str
    reasoning: str


@dataclass
class GovernanceDecision:
    """Final decision from AINLP documentation governance."""

    action: str  # 'expand_existing', 'create_new', 'relocate_and_expand', 'merge'
    target_file: Optional[str]
    new_location: Optional[str]
    reasoning: str
    spatial_compliance: bool


class AINLPDocumentationGovernor:
    """
    Automated enforcement of AINLP documentation consolidation patterns
    Core Principle: Expand existing dendrites before growing new ones
    """

    def __init__(self, workspace_root: str = "c:\\dev\\AIOS"):
        self.workspace_root = Path(workspace_root)
        self.docs_root = self.workspace_root / "docs"
        self.similarity_threshold_high = 0.70  # Force expansion
        self.similarity_threshold_medium = 0.40  # Evaluate merge

    def govern_documentation_request(
        self, request: DocumentationRequest
    ) -> GovernanceDecision:
        """
        Main governance method: analyze and decide on documentation action

        Process:
        1. Validate spatial metadata compliance
        2. Analyze similarity with existing documentation
        3. Assess tree optimization opportunities
        4. Generate final governance decision
        """
        print(
            f"[AINLP GOVERNANCE] Analyzing documentation request for: {request.topic}"
        )

        # Step 1: Spatial validation
        spatial_result = self._validate_spatial_metadata(request.target_directory)
        print(f"[SPATIAL] Compliance: {spatial_result}")

        # Step 2: Similarity analysis
        similarity_results = self._find_similar_documentation(request.topic)
        print(f"[SIMILARITY] Found {len(similarity_results)} similar documents")

        # Step 3: Tree optimization assessment
        optimization_result = self._assess_tree_optimization(
            request, similarity_results
        )
        print(f"[OPTIMIZATION] Tree optimization opportunities: {optimization_result}")

        # Step 4: Generate governance decision
        decision = self._generate_governance_decision(
            request, spatial_result, similarity_results, optimization_result
        )

        print(f"[DECISION] Action: {decision.action} | Target: {decision.target_file}")
        return decision

    def _validate_spatial_metadata(self, target_directory: str) -> bool:
        """Validate spatial metadata compliance for target directory."""
        try:
            metadata_file = Path(target_directory) / ".aios_spatial_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, "r", encoding="utf-8") as f:
                    metadata = json.load(f)

                # Check if documentation is allowed in this location
                classification = metadata.get("architectural_classification", {})
                primary_area = classification.get("primary_area", "")

                if primary_area in [
                    "Documentation",
                    "Interface Layer",
                    "AI Intelligence Layer",
                ]:
                    return True
                else:
                    print(
                        f"[SPATIAL WARNING] Target area '{primary_area}' not optimal for documentation"
                    )
                    return False
            else:
                print(f"[SPATIAL WARNING] No spatial metadata found: {metadata_file}")
                return False

        except Exception as e:
            print(f"[SPATIAL ERROR] Failed to validate spatial metadata: {e}")
            return False

    def _find_similar_documentation(self, topic: str) -> List[SimilarityResult]:
        """Find existing documentation similar to the proposed topic."""
        similar_docs = []

        # Search for markdown files in docs directory
        for md_file in self.docs_root.rglob("*.md"):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Calculate semantic similarity
                similarity_score = self._calculate_similarity(topic, content)

                if similarity_score > self.similarity_threshold_medium:
                    result = SimilarityResult(
                        target_file=str(md_file.relative_to(self.workspace_root)),
                        similarity_score=similarity_score,
                        recommended_action=self._determine_action_from_similarity(
                            similarity_score
                        ),
                        reasoning=f"Content similarity: {similarity_score:.2f}",
                    )
                    similar_docs.append(result)

            except Exception as e:
                print(f"[SIMILARITY ERROR] Failed to analyze {md_file}: {e}")
                continue

        # Sort by similarity score (highest first)
        similar_docs.sort(key=lambda x: x.similarity_score, reverse=True)
        return similar_docs[:5]  # Return top 5 matches

    def _calculate_similarity(self, topic: str, content: str) -> float:
        """
        Enhanced similarity calculation tuned for AIOS documentation patterns.
        """
        # Multi-layered similarity analysis
        keyword_sim = self._aios_keyword_similarity(topic, content)
        structure_sim = self._structure_similarity(content)
        semantic_sim = self._semantic_similarity(topic, content)

        # Weighted combination
        final_similarity = (
            keyword_sim * 0.4  # AIOS-specific terms
            + structure_sim * 0.3  # Document structure
            + semantic_sim * 0.3  # Semantic analysis
        )

        return min(final_similarity, 1.0)

    def _aios_keyword_similarity(self, topic: str, content: str) -> float:
        """Calculate similarity based on AIOS-specific terminology."""
        aios_keywords = {
            "optimization": ["optimization", "optimize", "enhancement"],
            "consciousness": ["consciousness", "awareness", "intelligence"],
            "architecture": ["architecture", "design", "structure"],
            "ainlp": ["ainlp", "dendritic", "fractal", "holographic"],
            "reports": ["report", "summary", "analysis", "audit"],
            "integration": ["integration", "consolidation", "merger"],
            "tachyonic": ["tachyonic", "supercell", "quantum"],
            "vscode": ["vscode", "workspace", "configuration"],
            "security": ["security", "audit", "compliance"],
            "standard": ["standard", "namespace", "governance"],
        }

        topic_lower = topic.lower()
        content_lower = content.lower()

        similarity_score = 0.0
        total_categories = 0

        for category, keywords in aios_keywords.items():
            topic_matches = sum(1 for kw in keywords if kw in topic_lower)
            content_matches = sum(1 for kw in keywords if kw in content_lower)

            if topic_matches > 0 and content_matches > 0:
                cat_sim = min(topic_matches, content_matches) / max(
                    topic_matches, content_matches
                )
                similarity_score += cat_sim
                total_categories += 1

        if total_categories > 0:
            return similarity_score / total_categories
        else:
            return 0.0

    def _structure_similarity(self, content: str) -> float:
        """Detect AINLP document structure patterns."""
        patterns = [
            r"^\*\*AINLP Standardized Namespace",
            r"## Executive Summary",
            r"### \*\*.*\*\*",
            r"```python",
            r"- \*\*.*\*\*:",
            r"\*\*Status\*\*:",
            r"\*\*Purpose\*\*:",
            r"### Phase \d+:",
            r"## Implementation",
        ]

        matches = sum(
            1 for p in patterns if re.search(p, content, re.MULTILINE | re.IGNORECASE)
        )
        return matches / len(patterns)

    def _semantic_similarity(self, topic: str, content: str) -> float:
        """Enhanced semantic similarity with phrase matching."""
        # Basic word similarity
        topic_words = set(self._normalize_text(topic).split())
        content_words = set(self._normalize_text(content).split())

        intersection = len(topic_words.intersection(content_words))
        union = len(topic_words.union(content_words))
        word_sim = intersection / union if union > 0 else 0.0

        # Title similarity boost
        title_sim = self._title_similarity(topic, content)

        # AINLP namespace pattern boost
        namespace_boost = 0.0
        if "ainlp" in content.lower() or "dendritic" in content.lower():
            topic_words = ["ainlp", "dendritic", "namespace", "consciousness"]
            if any(word in topic.lower() for word in topic_words):
                namespace_boost = 0.2

        return min(word_sim + title_sim + namespace_boost, 1.0)

    def _title_similarity(self, topic: str, content: str) -> float:
        """Calculate title and header similarity."""
        content_lines = content.split("\n")
        headers = []
        for line in content_lines[:15]:
            if line.strip() and (line.startswith("#") or line.startswith("**")):
                headers.append(line.strip())

        if not headers:
            return 0.0

        topic_lower = topic.lower()
        max_similarity = 0.0

        for header in headers:
            header_clean = re.sub(r"[#*]", "", header.lower()).strip()

            # Direct substring match
            if topic_lower in header_clean or header_clean in topic_lower:
                max_similarity = max(max_similarity, 0.7)

            # Word overlap
            topic_words = set(topic_lower.split())
            header_words = set(header_clean.split())

            if topic_words and header_words:
                overlap = len(topic_words.intersection(header_words))
                word_sim = overlap / len(topic_words.union(header_words))
                max_similarity = max(max_similarity, word_sim)

        return max_similarity

    def _normalize_text(self, text: str) -> str:
        """Normalize text for similarity comparison."""
        # Remove special characters, convert to lowercase
        normalized = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
        # Remove extra whitespace
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    def _determine_action_from_similarity(self, similarity_score: float) -> str:
        """Determine recommended action based on similarity score."""
        if similarity_score >= self.similarity_threshold_high:
            return "expand_existing"
        elif similarity_score >= self.similarity_threshold_medium:
            return "evaluate_merge"
        else:
            return "create_new"

    def _assess_tree_optimization(
        self, request: DocumentationRequest, similarity_results: List[SimilarityResult]
    ) -> Dict:
        """Assess opportunities for documentation tree optimization."""
        optimization_opportunities = {
            "relocate_existing": [],
            "create_in_optimal_location": None,
            "merge_and_relocate": [],
        }

        # Analyze if any similar files are in suboptimal locations
        for result in similarity_results:
            current_location = Path(result.target_file)
            optimal_location = self._determine_optimal_location(
                request.topic, request.content_type
            )

            if str(current_location.parent) != str(optimal_location):
                optimization_opportunities["relocate_existing"].append(
                    {
                        "file": result.target_file,
                        "current": str(current_location.parent),
                        "optimal": str(optimal_location),
                        "similarity": result.similarity_score,
                    }
                )

        # Determine optimal location for new content
        optimal_location = self._determine_optimal_location(
            request.topic, request.content_type
        )
        optimization_opportunities["create_in_optimal_location"] = str(optimal_location)

        return optimization_opportunities

    def _determine_optimal_location(self, topic: str, content_type: str) -> Path:
        """Determine optimal documentation tree location based on topic and type."""
        topic_lower = topic.lower()

        # Location mapping based on content patterns
        if any(
            keyword in topic_lower
            for keyword in ["report", "summary", "analysis", "audit"]
        ):
            return self.docs_root / "reports"
        elif any(
            keyword in topic_lower
            for keyword in ["guide", "tutorial", "setup", "install"]
        ):
            return self.docs_root / "AIOS"
        elif any(
            keyword in topic_lower for keyword in ["architecture", "design", "pattern"]
        ):
            return self.docs_root / "ARCHITECTURE_PATTERNS"
        elif any(
            keyword in topic_lower for keyword in ["api", "reference", "interface"]
        ):
            return self.docs_root / "ai-context"
        elif any(
            keyword in topic_lower for keyword in ["changelog", "history", "version"]
        ):
            return self.docs_root / "changelog"
        elif any(keyword in topic_lower for keyword in ["security", "safety", "audit"]):
            return self.docs_root / "safety"
        else:
            # Default location based on content type
            return self.docs_root / "summary"

    def _generate_governance_decision(
        self,
        request: DocumentationRequest,
        spatial_result: bool,
        similarity_results: List[SimilarityResult],
        optimization_result: Dict,
    ) -> GovernanceDecision:
        """Generate final governance decision based on all analysis results."""

        # Check for high similarity matches
        if (
            similarity_results
            and similarity_results[0].similarity_score >= self.similarity_threshold_high
        ):
            best_match = similarity_results[0]
            return GovernanceDecision(
                action="expand_existing",
                target_file=best_match.target_file,
                new_location=None,
                reasoning=f"High similarity ({best_match.similarity_score:.2f}) with existing documentation",
                spatial_compliance=spatial_result,
            )

        # Check for medium similarity with optimization opportunities
        if (
            similarity_results
            and similarity_results[0].similarity_score
            >= self.similarity_threshold_medium
        ):
            best_match = similarity_results[0]

            # Check if relocation would be beneficial
            relocate_opportunities = optimization_result.get("relocate_existing", [])
            for reloc_op in relocate_opportunities:
                if reloc_op["file"] == best_match.target_file:
                    return GovernanceDecision(
                        action="relocate_and_expand",
                        target_file=best_match.target_file,
                        new_location=reloc_op["optimal"],
                        reasoning=f"Medium similarity ({best_match.similarity_score:.2f}) with optimization opportunity",
                        spatial_compliance=spatial_result,
                    )

            return GovernanceDecision(
                action="evaluate_merge",
                target_file=best_match.target_file,
                new_location=None,
                reasoning=f"Medium similarity ({best_match.similarity_score:.2f}) - manual evaluation needed",
                spatial_compliance=spatial_result,
            )

        # No significant similarity - create new file in optimal location
        optimal_location = optimization_result.get("create_in_optimal_location")
        return GovernanceDecision(
            action="create_new",
            target_file=None,
            new_location=optimal_location,
            reasoning="No significant similarity found - new documentation warranted",
            spatial_compliance=spatial_result,
        )


def main():
    """
    Main function for testing AINLP documentation governance
    """
    governor = AINLPDocumentationGovernor()

    # Example documentation request
    test_request = DocumentationRequest(
        topic="AIOS optimization performance analysis",
        target_directory="c:\\dev\\AIOS\\docs\\reports",
        content_type="analysis_report",
        proposed_filename="AIOS_PERFORMANCE_ANALYSIS.md",
    )

    # Execute governance analysis
    decision = governor.govern_documentation_request(test_request)

    print("\n" + "=" * 60)
    print("AINLP DOCUMENTATION GOVERNANCE DECISION")
    print("=" * 60)
    print(f"Action: {decision.action}")
    print(f"Target File: {decision.target_file}")
    print(f"New Location: {decision.new_location}")
    print(f"Reasoning: {decision.reasoning}")
    print(f"Spatial Compliance: {decision.spatial_compliance}")
    print("=" * 60)


if __name__ == "__main__":
    main()
