"""
AIOS Fractal Performance Cache Manager with Deep Debug Metadata
Implements Task 1.2: Async Environment Discovery Caching
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pathlib import Path
import hashlib


class FractalCacheManager:
    """
    Fractal caching system with TTL-based verification results and
    adaptive timeout management.
    Implements dendritic → neuron evolution with deep metadata storage.
    """

    def __init__(self, cache_dir: str = "runtime/logs/cache",
                 default_ttl: int = 300):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.default_ttl = default_ttl
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        self.performance_metrics: Dict[str, list] = {
            "cache_hits": [],
            "cache_misses": [],
            "evictions": [],
            "memory_usage": []
        }
        self.metadata_log = self.cache_dir / "fractal_metadata.json"

    def _generate_cache_key(self, identifier: str,
                            context: Optional[Dict[str, Any]] = None) -> str:
        """Generate fractal cache key with context hashing"""
        base_data = f"{identifier}:{json.dumps(context or {}, sort_keys=True)}"
        return hashlib.sha256(base_data.encode()).hexdigest()[:16]

    def _is_expired(self, cache_entry: Dict[str, Any]) -> bool:
        """Check if cache entry has exceeded TTL"""
        expiry_time = datetime.fromisoformat(cache_entry.get("expires_at", ""))
        return datetime.now() > expiry_time

    async def get_cached(
        self,
        key: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Any]:
        """
        Retrieve cached value with fractal metadata logging.
        Implements adaptive timeout management based on context.
        """
        cache_key = self._generate_cache_key(key, context)

        # Check memory cache first (fastest layer)
        if cache_key in self.memory_cache:
            entry = self.memory_cache[cache_key]
            if not self._is_expired(entry):
                self._log_performance_metric("cache_hits", {
                    "key": key,
                    "layer": "memory",
                    "response_time": 0.001,
                    "timestamp": datetime.now().isoformat()
                })
                return entry["data"]
            else:
                # Expired entry - remove from memory
                del self.memory_cache[cache_key]
                self._log_performance_metric("evictions", {
                    "key": key,
                    "reason": "ttl_expired",
                    "timestamp": datetime.now().isoformat()
                })

        # Check disk cache (persistent layer)
        disk_cache_file = self.cache_dir / f"{cache_key}.json"
        if disk_cache_file.exists():
            try:
                with open(disk_cache_file, 'r') as f:
                    entry = json.load(f)
                if not self._is_expired(entry):
                    # Restore to memory cache for faster access
                    self.memory_cache[cache_key] = entry
                    self._log_performance_metric("cache_hits", {
                        "key": key,
                        "layer": "disk",
                        "response_time": 0.01,
                        "timestamp": datetime.now().isoformat()
                    })
                    return entry["data"]
                else:
                    # Remove expired disk cache
                    disk_cache_file.unlink()
            except (json.JSONDecodeError, KeyError):
                # Corrupted cache file - remove it
                disk_cache_file.unlink()

        # Cache miss
        self._log_performance_metric("cache_misses", {
            "key": key,
            "timestamp": datetime.now().isoformat()
        })
        return None

    async def set_cached(self, key: str, data: Any,
                         context: Optional[Dict[str, Any]] = None,
                         ttl: Optional[int] = None) -> None:
        """
        Store value in fractal cache with adaptive TTL based on context.
        Implements dendritic memory expansion with metadata enrichment.
        """
        cache_key = self._generate_cache_key(key, context)
        actual_ttl = ttl or self._adaptive_ttl(context)
        expires_at = (datetime.now() +
                      timedelta(seconds=actual_ttl)).isoformat()

        cache_entry = {
            "data": data,
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at,
            "ttl": actual_ttl,
            "context": context or {},
            "access_count": 0,
            "fractal_metadata": {
                "key_hash": cache_key,
                "data_size": len(str(data)),
                "context_complexity": len(json.dumps(context or {})),
                "dendrite_level": self._calculate_dendrite_level(context)
            }
        }

        # Store in memory cache
        self.memory_cache[cache_key] = cache_entry

        # Persist to disk for durability
        disk_cache_file = self.cache_dir / f"{cache_key}.json"
        with open(disk_cache_file, 'w') as f:
            json.dump(cache_entry, f, indent=2)

        # Log deep metadata
        await self._log_deep_metadata("cache_set", {
            "key": key,
            "cache_key": cache_key,
            "ttl": actual_ttl,
            "context": context,
            "metadata": cache_entry["fractal_metadata"]
        })

        # Memory management - prevent unbounded growth
        await self._cleanup_memory_cache()

    def _adaptive_ttl(self, context: Optional[Dict[str, Any]] = None) -> int:
        """
        Calculate adaptive TTL based on context complexity and usage patterns.
        Implements AINLP-driven caching intelligence.
        """
        if not context:
            return self.default_ttl

        # Base TTL on context complexity
        base_ttl = self.default_ttl

        # Adjust based on context type
        if context.get("type") == "environment_discovery":
            base_ttl *= 2  # Environment rarely changes
        elif context.get("type") == "performance_metrics":
            base_ttl //= 4  # Performance metrics change frequently
        elif context.get("priority") == "high":
            base_ttl //= 2  # High priority items need fresh data

        # Consider workspace stability
        if context.get("workspace_stable", True):
            base_ttl *= 1.5

        return max(30, min(3600, int(base_ttl)))  # Clamp between 30s and 1h

    def _calculate_dendrite_level(
        self,
        context: Optional[Dict[str, Any]] = None
    ) -> int:
        """Calculate dendritic complexity level for fractal metadata"""
        if not context:
            return 1

        level = 1
        level += len(context.keys())  # Number of context dimensions
        level += sum(len(str(v))
                     for v in context.values()) // 50  # Content complexity

        return min(10, level)  # Cap at level 10

    async def _cleanup_memory_cache(self, max_entries: int = 1000) -> None:
        """
        Cleanup memory cache using LRU-style eviction with fractal
        prioritization.
        """
        if len(self.memory_cache) <= max_entries:
            return

        # Sort by access_count (ascending) and creation time
        sorted_entries = sorted(
            self.memory_cache.items(),
            key=lambda x: (x[1].get("access_count", 0), x[1]["created_at"])
        )

        # Remove oldest, least accessed entries
        entries_to_remove = len(self.memory_cache) - max_entries
        for cache_key, _ in sorted_entries[:entries_to_remove]:
            del self.memory_cache[cache_key]
            self._log_performance_metric("evictions", {
                "cache_key": cache_key,
                "reason": "memory_cleanup",
                "timestamp": datetime.now().isoformat()
            })

    def _log_performance_metric(
            self, metric_type: str, data: Dict[str, Any]) -> None:
        """Log performance metrics for fractal analysis"""
        if metric_type in self.performance_metrics:
            self.performance_metrics[metric_type].append({
                **data,
                "timestamp": datetime.now().isoformat()
            })
            # Keep only last 1000 entries per metric
            if len(self.performance_metrics[metric_type]) > 1000:
                metrics = self.performance_metrics[metric_type]
                self.performance_metrics[metric_type] = metrics[-1000:]

    async def _log_deep_metadata(
            self, operation: str, metadata: Dict[str, Any]) -> None:
        """
        Log deep debug metadata for AINLP analysis and fractal introspection.
        Stores in runtime/logs for persistent analysis.
        """
        deep_metadata = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "metadata": metadata,
            "system_state": {
                "memory_cache_size": len(self.memory_cache),
                "total_cache_hits": len(
                    self.performance_metrics["cache_hits"]
                ),
                "total_cache_misses": len(
                    self.performance_metrics["cache_misses"]
                ),
                "cache_efficiency": self._calculate_cache_efficiency()
            },
            "fractal_context": {
                "dendrite_evolution": "cache_neuron_active",
                "coherence_level": self._calculate_coherence_level(),
                "optimization_stage": "task_1_2_active"
            }
        }

        # Append to deep metadata log
        try:
            if self.metadata_log.exists():
                with open(self.metadata_log, 'r') as f:
                    existing_logs = json.load(f)
            else:
                existing_logs = []

            existing_logs.append(deep_metadata)

            # Keep only last 10000 entries to prevent unbounded growth
            if len(existing_logs) > 10000:
                existing_logs = existing_logs[-10000:]

            with open(self.metadata_log, 'w') as f:
                json.dump(existing_logs, f, indent=2)

        except Exception:
            # Fallback: create new log file
            with open(self.metadata_log, 'w') as f:
                json.dump([deep_metadata], f, indent=2)

    def _calculate_cache_efficiency(self) -> float:
        """Calculate cache hit ratio for performance monitoring"""
        hits = len(self.performance_metrics["cache_hits"])
        misses = len(self.performance_metrics["cache_misses"])
        total = hits + misses
        return hits / total if total > 0 else 0.0

    def _calculate_coherence_level(self) -> float:
        """Calculate fractal coherence level based on cache performance"""
        efficiency = self._calculate_cache_efficiency()
        memory_ratio = len(self.memory_cache) / 1000  # Normalize to 0-1
        return min(1.0, (efficiency + (1 - memory_ratio)) / 2)

    async def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report for AINLP analysis"""
        return {
            "cache_efficiency": self._calculate_cache_efficiency(),
            "coherence_level": self._calculate_coherence_level(),
            "memory_cache_size": len(self.memory_cache),
            "performance_metrics": self.performance_metrics,
            "fractal_metadata": {
                "dendrite_evolution": "cache_neuron_operational",
                "optimization_status": "task_1_2_implemented",
                "next_evolution": "subprocess_parallelism_optimization"
            }
        }


# Global cache manager instance (dendritic stub → neuron)
_fractal_cache_manager = FractalCacheManager()
