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
