"""
Setup script for TensorFlow Cellular Bridge

Builds the pybind11 bridge for intercellular communication between
Python AI Training Cells and C++ TensorFlow Performance Cells.
"""

from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir
import pybind11
from setuptools import setup, Extension
import os
import sys
from pathlib import Path

# Get the directory containing this setup.py
current_dir = Path(__file__).parent
aios_root = current_dir.parent

# Define the extension module
ext_modules = [
    Pybind11Extension(
        "tensorflow_cellular_bridge",
        [
            str(current_dir / "tensorflow_bridge.cpp"),
            str(aios_root / "languages" / "cpp" / "core" / "src" / "tensorflow_performance_cell.cpp"),
            str(aios_root / "languages" / "cpp" / "core" / "src" / "aios_core_minimal.cpp"),
        ],
        include_dirs=[
            str(aios_root / "languages" / "cpp" / "core" / "include"),
            # Add pybind11 includes
            pybind11.get_include(),
        ],
        language="c++",
        cxx_std=20,
        define_macros=[
            ("AIOS_TENSORFLOW_BRIDGE", None),
        ],
    ),
]

# Compiler-specific options
if sys.platform.startswith("win"):
    # Windows-specific options
    for ext in ext_modules:
        ext.cxx_flags = ["/W4", "/WX"]
else:
    # Linux/Mac options
    for ext in ext_modules:
        ext.cxx_flags = ["-Wall", "-Wextra", "-Wpedantic"]

setup(
    name="tensorflow_cellular_bridge",
    version="0.4.0",
    description="TensorFlow Cellular Bridge for AIOS - C++ ↔ Python intercellular communication",
    long_description="""
    The TensorFlow Cellular Bridge enables seamless communication between Python AI
    Training Cells and C++ TensorFlow Performance Cells in the AIOS cellular ecosystem.
    
    Features:
    - Sub-millisecond inference through C++ performance cells
    - Efficient numpy ↔ C++ tensor data transfer
    - Performance monitoring and benchmarking
    - Memory-optimized intercellular communication
    - Production-ready model deployment pipeline
    """,
    author="AIOS Team",
    author_email="team@aios.dev",
    url="https://github.com/Tecnocrat/AIOS",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pybind11>=2.10.0",
    ],
    extras_require={
        "tensorflow": ["tensorflow>=2.13.0"],
        "test": ["pytest>=7.0.0", "pytest-benchmark>=4.0.0"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: C++",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)