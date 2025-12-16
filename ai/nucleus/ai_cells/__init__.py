"""AIOS Cellular Training Subsystem Bootstrap

Registry & lazy adapter resolution layer for training cell implementations.

AINLP_COMPACT:
    subsystem: ai_cells
    purpose: unify training cell adapter discovery & instantiation
    design_drivers: [extensibility, lazy_imports,
    deterministic_exports_pending]
    invariants:
        - no_demo_code_in_production: true
        - adapters_require_idempotent_registration: true
    roadmap_refs: [CEL-INT-01, CEL-HASH-02]

Exports:
    register_training_adapter(name:str, loader:Callable|Type)
    list_adapters()->List[str]
    get_training_adapter(name:str)->Type
    create_training_cell(framework:str, config)->object

Notes:
    - Loader can be a class OR a zero-arg callable returning a class (lazy)
    - Deterministic model hash utility will land under CEL-HASH-02
"""



def register_training_adapter(
    name: str,
    loader: Callable[[], Type[Any]] | Type[Any],
    override: bool = False,
) -> None:
    """Register a training adapter by symbolic framework name.

    Idempotent unless ``override=True``.
    """
    key = name.strip().lower()
    if not override and key in _ADAPTER_LOADERS:
        return
    _ADAPTER_LOADERS[key] = loader
    if key in _ADAPTER_CACHE:
        _ADAPTER_CACHE.pop(key, None)


def _resolve(name: str) -> Type[Any]:
    key = name.strip().lower()
    if key in _ADAPTER_CACHE:
        return _ADAPTER_CACHE[key]
    if key not in _ADAPTER_LOADERS:
        available = list(_ADAPTER_LOADERS.keys())
        raise KeyError(f"No training adapter for '{name}'. Available: {available}")
    loader = _ADAPTER_LOADERS[key]
    if callable(loader) and not isinstance(loader, type):  # lazy factory
        cls: Type[Any] = loader()
    else:
        cls = loader  # type: ignore[assignment]
    _ADAPTER_CACHE[key] = cls
    return cls


def list_adapters() -> List[str]:
    return sorted(_ADAPTER_LOADERS.keys())


def get_training_adapter(name: str) -> Type[Any]:
    return _resolve(name)


def create_training_cell(framework: str, config: Any) -> TrainingCellProtocol:
    cls = _resolve(framework)
    inst = cls(config)  # type: ignore[call-arg]
    if not isinstance(inst, TrainingCellProtocol):  # structural check only
        import warnings

        warnings.warn(f"Adapter '{framework}' does not conform to TrainingCellProtocol")
    return inst  # type: ignore[return-value]


# Built-in lazy registrations -------------------------------------------------


def _tf_loader() -> Type[Any]:  # lazy import
    from .tensorflow_training_cell import TensorFlowTrainingCell

    return TensorFlowTrainingCell


register_training_adapter("tensorflow", _tf_loader)

__all__ = [
    "TrainingCellProtocol",
    "register_training_adapter",
    "list_adapters",
    "get_training_adapter",
    "create_training_cell",
]
