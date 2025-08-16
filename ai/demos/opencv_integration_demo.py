#!/usr/bin/env python3
"""
AIOS OpenCV Integration Demonstration (Relocated)

Root harmonization: original root/demo_opencv_integration.py moved under
ai/demos/ per Agentic File Creation Policy.

Enhancements:
- Added CLI arg parsing (select subset of demo phases)
- Added optional output directory override
- Added JSON summary report emission for governance / metrics ingestion
- Removed hard-coded /tmp path; uses platform temp or provided output dir
- Context-aware import path resolution relative to repository root.
"""
from __future__ import annotations
import os
import sys
import json
import argparse
import tempfile
import time
import math
import subprocess
from dataclasses import dataclass, asdict
from typing import Dict, List

try:
    import cv2  # type: ignore
    import numpy as np  # type: ignore
except Exception as e:  # pragma: no cover
    print(f"[FATAL] OpenCV/Numpy import failure: {e}")
    raise

# Resolve repo root (two levels up from this file)
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(FILE_DIR, '..', '..'))
SCRIPTS_DIR = os.path.join(REPO_ROOT, 'scripts')
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

try:
    from main import initialize_services, get_service, shutdown_services
    from opencv_vision_module import OpenCVVisionModule
except ImportError as e:
    print(
        f"[WARN] Service modules not directly importable: {e}. "
        "Proceeding with limited demo mode."
    )
    OpenCVVisionModule = None  # type: ignore

@dataclass
class ImageDemoResult:
    kind: str
    path: str
    features_detected: int | None = None
    consciousness_resonance: float | None = None
    coherence_level: float | None = None
    image_entropy: float | None = None
    emergence_probability: float | None = None
    fractal_dimension: float | None = None
    symmetry_score: float | None = None
    error: str | None = None


def _entropy(gray: 'np.ndarray') -> float:
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).ravel()
    hist /= (hist.sum() or 1)
    nz = hist[hist > 0]
    return float(-(nz * np.log2(nz)).sum())


def create_demo_images(output_dir: str) -> Dict[str, str]:
    os.makedirs(output_dir, exist_ok=True)
    results: Dict[str, str] = {}
    # Simple geometric pattern
    simple = np.zeros((200, 200), dtype=np.uint8)
    cv2.circle(simple, (100, 100), 80, 255, 2)
    cv2.circle(simple, (100, 100), 40, 128, -1)
    for angle in range(0, 360, 45):
        x = int(100 + 60 * math.cos(math.radians(angle)))
        y = int(100 + 60 * math.sin(math.radians(angle)))
        cv2.circle(simple, (x, y), 8, 200, -1)
    simple_path = os.path.join(output_dir, 'simple_consciousness.png')
    cv2.imwrite(simple_path, simple)
    results['simple'] = simple_path
    # Mandala pattern
    mandala = np.zeros((200, 200), dtype=np.uint8)
    center = (100, 100)
    for ring in range(3):
        radius = 30 + ring * 25
        for angle in range(0, 360, 30):
            x = int(100 + radius * math.cos(math.radians(angle)))
            y = int(100 + radius * math.sin(math.radians(angle)))
            cv2.circle(mandala, (x, y), max(1, 8 - ring * 2), 255 - ring * 50, -1)
            if ring < 2:
                cv2.line(mandala, center, (x, y), 100, 1)
    cv2.circle(mandala, center, 12, 255, -1)
    cv2.circle(mandala, center, 6, 0, -1)
    mandala_path = os.path.join(output_dir, 'mandala_consciousness.png')
    cv2.imwrite(mandala_path, mandala)
    results['mandala'] = mandala_path
    # Fractal-like pattern
    fractal = np.zeros((200, 200), dtype=np.uint8)
    def branch(img, start, angle, length, depth):
        if depth == 0 or length < 2:
            return
        end = (
            int(start[0] + length * math.cos(angle)),
            int(start[1] + length * math.sin(angle)),
        )
        if 0 <= end[0] < 200 and 0 <= end[1] < 200:
            cv2.line(img, start, end, 255 - depth * 30, 1)
            branch(img, end, angle - 0.5, length * 0.7, depth - 1)
            branch(img, end, angle + 0.5, length * 0.7, depth - 1)
    for start_angle in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
        sx = int(100 + 30 * math.cos(start_angle))
        sy = int(100 + 30 * math.sin(start_angle))
        branch(fractal, (sx, sy), start_angle, 30, 4)
    fractal_path = os.path.join(output_dir, 'fractal_consciousness.png')
    cv2.imwrite(fractal_path, fractal)
    results['fractal'] = fractal_path
    return results


def process_with_direct_module(images: Dict[str, str]) -> List[ImageDemoResult]:
    out: List[ImageDemoResult] = []
    if not OpenCVVisionModule:
        for k, p in images.items():
            out.append(
                ImageDemoResult(
                    kind=k,
                    path=p,
                    error='opencv_vision_module unavailable',
                )
            )
        return out
    vision = OpenCVVisionModule()
    if not vision.initialize():
        return [ImageDemoResult(kind='init', path='', error='Vision module init failed')]
    for kind, path in images.items():
        res = vision.process_image(path, 'consciousness_emergence')
        if res.success:
            meta = res.metadata
            out.append(
                ImageDemoResult(
                    kind=kind,
                    path=path,
                    features_detected=res.features_detected,
                    consciousness_resonance=res.consciousness_resonance,
                    coherence_level=res.coherence_level,
                    image_entropy=res.image_entropy,
                    emergence_probability=meta.get(
                        'consciousness_emergence_probability'
                    ),
                    fractal_dimension=meta.get('fractal_dimension'),
                    symmetry_score=meta.get('symmetry_score'),
                )
            )
        else:
            out.append(
                ImageDemoResult(
                    kind=kind, path=path, error=res.error_message
                )
            )
    try:
        state = vision.get_consciousness_state()
        out.append(
            ImageDemoResult(
                kind='final_state',
                path='',
                features_detected=state.get('pattern_recognition_depth'),
                consciousness_resonance=state.get('quantum_coherence'),
                coherence_level=state.get('holographic_information_density'),
            )
        )
    finally:
        vision.shutdown()
    return out


def process_via_service(images: Dict[str, str]) -> List[ImageDemoResult]:
    if not OpenCVVisionModule:
        return [
            ImageDemoResult(
                kind='service', path='', error='Service modules unavailable'
            )
        ]
    initialize_services()
    try:
        svc = get_service('opencv_vision')
        if not svc:
            return [
                ImageDemoResult(
                    kind='service',
                    path='',
                    error='opencv_vision service not found',
                )
            ]
        results: List[ImageDemoResult] = []
        # sample: process mandala only (most complex)
        mandala = images.get('mandala')
        if mandala:
            resp = svc.process_request(
                {
                    'action': 'process_image',
                    'image_path': mandala,
                    'analysis_type': 'consciousness_emergence',
                }
            )
            if resp.get('success'):
                meta = resp.get('metadata', {})
                results.append(
                    ImageDemoResult(
                        kind='service_mandala',
                        path=mandala,
                        features_detected=resp.get('features_detected'),
                        consciousness_resonance=resp.get(
                            'consciousness_resonance'
                        ),
                        coherence_level=resp.get('consciousness_resonance'),
                        image_entropy=resp.get('image_entropy'),
                        emergence_probability=meta.get(
                            'consciousness_emergence_probability'
                        ),
                        fractal_dimension=meta.get('fractal_dimension'),
                        symmetry_score=meta.get('symmetry_score'),
                    )
                )
            else:
                results.append(
                    ImageDemoResult(
                        kind='service_mandala',
                        path=mandala,
                        error=resp.get('error'),
                    )
                )
        return results
    finally:
        shutdown_services()


def run_cli_example(mandala_path: str) -> ImageDemoResult:
    cmd = [
        sys.executable,
        os.path.join('scripts', 'main.py'),
        '--invoke-service', 'opencv_vision',
        '--action', 'process_image',
        '--image-path', mandala_path,
        '--analysis-type', 'consciousness_emergence',
    ]
    try:
        proc = subprocess.run(
            cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=30
        )
        if proc.returncode == 0:
            return ImageDemoResult(
                kind='cli_demo',
                path=mandala_path,
                features_detected=0,
                consciousness_resonance=0.0,
                coherence_level=0.0,
                image_entropy=0.0,
            )
        return ImageDemoResult(
            kind='cli_demo',
            path=mandala_path,
            error=f'return_code={proc.returncode} stderr={proc.stderr[:160]}',
        )
    except Exception as e:
        return ImageDemoResult(
            kind='cli_demo', path=mandala_path, error=str(e)
        )


def emit_summary(results: List[ImageDemoResult], output_dir: str) -> str:
    def _normalize(obj):
        # Convert numpy / float32 types if present
        if isinstance(obj, dict):
            return {k: _normalize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_normalize(v) for v in obj]
        try:
            import numpy as np  # local import
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, (np.integer,)):
                return int(obj)
        except Exception:  # pragma: no cover
            pass
        return obj
    raw_results = [asdict(r) for r in results]
    summary = _normalize({
        'timestamp': time.time(),
        'results': raw_results,
        'count': len(results),
        'source': 'opencv_integration_demo'
    })
    path = os.path.join(output_dir, 'opencv_demo_summary.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    return path


def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description='AIOS OpenCV integration demo (segmented).')
    p.add_argument(
        '--phases',
        nargs='*',
        default=['direct', 'service', 'cli'],
        choices=['direct', 'service', 'cli'],
        help='Which demo phases to run',
    )
    p.add_argument(
        '--output-dir',
        default=os.path.join(tempfile.gettempdir(), 'aios_opencv_demo'),
        help='Output directory for generated images & summary',
    )
    p.add_argument('--no-cli', action='store_true', help='Disable CLI phase (alias for excluding cli)')
    return p.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    ns = parse_args(argv or sys.argv[1:])
    if ns.no_cli and 'cli' in ns.phases:
        ns.phases.remove('cli')
    images = create_demo_images(ns.output_dir)
    results: List[ImageDemoResult] = []
    if 'direct' in ns.phases:
        results.extend(process_with_direct_module(images))
    if 'service' in ns.phases:
        results.extend(process_via_service(images))
    if 'cli' in ns.phases and 'mandala' in images:
        results.append(run_cli_example(images['mandala']))
    summary_path = emit_summary(results, ns.output_dir)
    print(f"Summary written: {summary_path}")
    print(f"Images: {list(images.values())}")
    return 0

if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
