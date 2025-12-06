"""AIOS Optional Dependency Shadow Module

Purpose:
    Provide lightweight symbolic references (AINLP synthetic logic shadow)
    for optional stacks removed from the canonical requirements set. This
    preserves architectural intent and enables future activation without
    breaking import expectations.

Usage:
    from ai.deps.shadows.optional_stacks_shadow import OPTIONAL_STACKS

Structure:
    Each entry documents: category, packages (list), activation_hint.
    No heavy imports executed here; purely declarative.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class OptionalStack:
    name: str
    category: str
    packages: List[str]
    activation_hint: str


# pyproject.toml now exposes these groups as extras; keep this list authoritative.
OPTIONAL_STACKS: List[OptionalStack] = [
    OptionalStack(
        name="vector_embeddings",
        category="embeddings/vector_db",
        packages=["chromadb", "faiss-cpu", "sentence-transformers"],
        activation_hint=(
            "Install ai/deps/requirements_extras.txt to enable embedding "
            "search and vector storage."
        ),
    ),
    OptionalStack(
        name="quantum_core",
        category="quantum/hyperdimensional",
        packages=["qiskit", "cirq", "pennylane"],
        activation_hint=(
            "Install ai/deps/requirements_quantum.txt for quantum " "experimentation."
        ),
    ),
    OptionalStack(
        name="advanced_plotting",
        category="visualization/plotting",
        packages=["matplotlib", "seaborn", "plotly", "bokeh"],
        activation_hint=(
            "Install ai/deps/requirements_extras.txt for full plotting " "suite."
        ),
    ),
    OptionalStack(
        name="graph_theory",
        category="graph/community",
        packages=["networkx", "igraph", "python-louvain"],
        activation_hint=(
            "Install ai/deps/requirements_future_graph.txt for graph " "analytics."
        ),
    ),
    OptionalStack(
        name="stats_forecasting",
        category="statistics/time_series",
        packages=["statsmodels", "prophet"],
        activation_hint=(
            "Install ai/deps/requirements_extras.txt for advanced " "forecasting."
        ),
    ),
    OptionalStack(
        name="perf_serialization",
        category="performance/serialization",
        packages=[
            "orjson",
            "msgspec",
            "cloudpickle",
            "dill",
            "multiprocessing-logging",
        ],
        activation_hint=(
            "Install ai/deps/requirements_perf_serial.txt for "
            "high-performance (de)serialization."
        ),
    ),
]

if __name__ == "__main__":  # simple introspection aid
    import json

    print(json.dumps([s.__dict__ for s in OPTIONAL_STACKS], indent=2))
