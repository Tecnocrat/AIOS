# AIOS Segmented Environments

This directory replaces the monolithic root `environment.yml` with layered environment specifications per the AIOS Agentic File Creation Policy and tachyonic harmonization principles.

## Rationale
- Reduce solve time and dependency conflicts.
- Enable minimal bootstrap for tooling (`environment.base.yml`).
- Allow opt-in heavyweight AI/LLM stack (`environment.ai.yml`).
- Isolate dev / lint / test tools (`environment.dev.yml`).
- Keep quantum / experimental packages separate (`environment.quantum.yml`).

## Usage
Create only what you need; compose via `conda activate` layering + `pip install -r ai/requirements.txt` if required.

### Base
```
conda env create -f ai/env/environment.base.yml
conda activate aios-base
```

### AI Stack (optionally create from scratch or clone base then install extras)
```
conda env create -f ai/env/environment.ai.yml
conda activate aios-ai
```

### Dev Tooling
```
conda env create -f ai/env/environment.dev.yml
conda activate aios-dev
```

### Quantum / Experimental
```
conda env create -f ai/env/environment.quantum.yml
conda activate aios-quantum
```

## Future Enhancements
- Lock files via `conda-lock`.
- Scripted composition (merge base + ai + dev into unified ephemeral env).
- Automated drift detection in CI comparing `pip list` vs frozen spec.
