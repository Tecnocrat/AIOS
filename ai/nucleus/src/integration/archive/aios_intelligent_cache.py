#!/usr/bin/env python3
"""
AIOS Intelligent Caching System
Advanced Multi-Layer Caching Implementation

Implements comprehensive caching strategy identified in /optimization.context:
- Memory caching for hot data
- Disk caching for persistence
- Intelligent cache invalidation
- Performance metrics and monitoring

Author: AIOS Development Team
Date: July 10, 2025
Version: 1.0
"""

import hashlib
import json
import pickle
import threading
import time
import weakref
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union


@dataclass
class CacheMetrics:
    """Cache performance metrics"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_requests: int = 0
    total_size_bytes: int = 0
    avg_response_time_ms: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)

    @property
    def hit_ratio(self) -> float:
        """Calculate cache hit ratio"""
        if self.total_requests == 0:
            return 0.0
        return self.hits / self.total_requests

    @property
    def miss_ratio(self) -> float:
        """Calculate cache miss ratio"""
        return 1.0 - self.hit_ratio


@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    size_bytes: int = 0
    ttl_seconds: Optional[int] = None

    @property
    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        if self.ttl_seconds is None:
            return False
        return datetime.now(
        ) > self.created_at + timedelta(seconds=self.ttl_seconds)

    @property
    def age_seconds(self) -> float:
        """Get age of cache entry in seconds"""
        return (datetime.now() - self.created_at).total_seconds()


class CacheStrategy(ABC):
    """Abstract base class for cache strategies"""

    @abstractmethod
    def should_evict(
    self, entry: CacheEntry, cache_size: int, max_size: int) -> bool:
        """Determine if entry should be evicted"""
        pass

    @abstractmethod
    def get_eviction_priority(self, entry: CacheEntry) -> float:
        """Get eviction priority (higher = more likely to evict)"""
        pass


class LRUStrategy(CacheStrategy):
    """Least Recently Used cache strategy"""

    def should_evict(
    self, entry: CacheEntry, cache_size: int, max_size: int) -> bool:
        return cache_size > max_size

    def get_eviction_priority(self, entry: CacheEntry) -> float:
        return (datetime.now() - entry.last_accessed).total_seconds()


class LFUStrategy(CacheStrategy):
    """Least Frequently Used cache strategy"""

    def should_evict(
    self, entry: CacheEntry, cache_size: int, max_size: int) -> bool:
        return cache_size > max_size

    def get_eviction_priority(self, entry: CacheEntry) -> float:
        # Combine frequency and recency
        frequency_score = 1.0 / (entry.access_count + 1)
        recency_scor
        e = (datetime.now() - entry.last_accessed).total_seconds() / 3600  # Hours
        return frequency_score + recency_score * 0.1


class IntelligentStrategy(CacheStrategy):
    """Intelligent cache strategy based on access patterns and size"""

    def should_evict(
    self, entry: CacheEntry, cache_size: int, max_size: int) -> bool:
        return cache_size > max_size

    def get_eviction_priority(self, entry: CacheEntry) -> float:
        # Multi-factor scoring
        frequency_score = 1.0 / (entry.access_count + 1)
        recency_scor
        e = (datetime.now() - entry.last_accessed).total_seconds() / 3600
        size_score = entry.size_bytes / 1024 / 1024  # MB
        age_score = entry.age_seconds / (24 * 3600)  # Days

        # Weighted combination
        return (frequency_score * 0.4 + recency_score * 0.3 +
                size_score * 0.2 + age_score * 0.1)


class AIOSMemoryCache:
    """High-performance in-memory cache for AIOS"""

    def __init__(self, max_size: int = 1000, strategy: CacheStrategy = None):
        self.max_size = max_size
        self.strategy = strategy or IntelligentStrategy()
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
        self.metrics = CacheMetrics()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        start_time = time.perf_counter()

        with self._lock:
            self.metrics.total_requests += 1

            if key not in self._cache:
                self.metrics.misses += 1
                return None

            entry = self._cache[key]

            # Check expiration
            if entry.is_expired:
                del self._cache[key]
                self.metrics.misses += 1
                return None

            # Update access metadata
            entry.last_accessed = datetime.now()
            entry.access_count += 1

            self.metrics.hits += 1

            # Update response time
            response_time_ms = (time.perf_counter() - start_time) * 1000
            self.metrics.avg_response_time_ms = (
                (
                self.metrics.avg_response_time_ms * (self.metrics.total_requests - 1) +
                 response_time_ms) / self.metrics.total_requests
            )

            return entry.value

    def put(
    self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """Put value into cache"""
        with self._lock:
            # Calculate size
            try:
                size_bytes = len(pickle.dumps(value))
            except:
                size_bytes = 1024  # Default size estimate

            # Create cache entry
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                size_bytes=size_bytes,
                ttl_seconds=ttl_seconds
            )

            # Check if eviction is needed
            current_size = len(self._cache)
            if current_size >= self.max_size:
                self._evict_entries()

            # Store entry
            self._cache[key] = entry
            self.metrics.total_size_bytes += size_bytes

            return True

    def invalidate(self, key: str) -> bool:
        """Invalidate cache entry"""
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                self.metrics.total_size_bytes -= entry.size_bytes
                del self._cache[key]
                return True
            return False

    def clear(self):
        """Clear all cache entries"""
        with self._lock:
            self._cache.clear()
            self.metrics.total_size_bytes = 0

    def _evict_entries(self):
        """Evict entries based on strategy"""
        if not self._cache:
            return

        # Sort entries by eviction priority
        entries_with_priority = [
            (self.strategy.get_eviction_priority(entry), key, entry)
            for key, entry in self._cache.items()
        ]
        entries_with_priority.sort(reverse=True)  # Highest priority first

        # Evict 20% of entries
        evict_count = max(1, len(self._cache) // 5)

        for i in range(min(evict_count, len(entries_with_priority))):
            _, key, entry = entries_with_priority[i]
            self.metrics.total_size_bytes -= entry.size_bytes
            del self._cache[key]
            self.metrics.evictions += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self._lock:
            return {
                'size': len(self._cache),
                'max_size': self.max_size,
                'hit_ratio': self.metrics.hit_ratio,
                'miss_ratio': self.metrics.miss_ratio,
                'total_requests': self.metrics.total_requests,
                'total_size_mb': self.metrics.total_size_bytes / 1024 / 1024,
                'avg_response_time_ms': self.metrics.avg_response_time_ms,
                'evictions': self.metrics.evictions
            }


class AIOSDiskCache:
    """Persistent disk cache for AIOS"""

    def __init__(self, cache_dir: str = "cache", max_size_mb: int = 100):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_size_mb = max_size_mb
        self.metrics_file = self.cache_dir / "cache_metrics.json"
        self._lock = threading.RLock()
        self.metrics = self._load_metrics()

    def get(self, key: str) -> Optional[Any]:
        """Get value from disk cache"""
        cache_file = self._get_cache_file(key)

        with self._lock:
            self.metrics.total_requests += 1

            if not cache_file.exists():
                self.metrics.misses += 1
                return None

            try:
                with open(cache_file, 'rb') as f:
                    data = pickle.load(f)

                # Check expiration
                if 'expires_at' in data and
                 datetime.now() > data['expires_at']:
                    cache_file.unlink(missing_ok=True)
                    self.metrics.misses += 1
                    return None

                # Update access time
                data['last_accessed'] = datetime.now()
                with open(cache_file, 'wb') as f:
                    pickle.dump(data, f)

                self.metrics.hits += 1
                return data['value']

            except Exception:
                cache_file.unlink(missing_ok=True)
                self.metrics.misses += 1
                return None

    def put(
    self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """Put value into disk cache"""
        cache_file = self._get_cache_file(key)

        with self._lock:
            try:
                data = {
                    'value': value,
                    'created_at': datetime.now(),
                    'last_accessed': datetime.now(),
                    'expires_at': (
                    datetime.now() + timedelta(seconds=ttl_seconds)
                                 if ttl_seconds else None)
                }

                with open(cache_file, 'wb') as f:
                    pickle.dump(data, f)

                # Check cache size and cleanup if needed
                self._cleanup_if_needed()

                return True

            except Exception:
                return False

    def invalidate(self, key: str) -> bool:
        """Invalidate cache entry"""
        cache_file = self._get_cache_file(key)

        with self._lock:
            if cache_file.exists():
                cache_file.unlink(missing_ok=True)
                return True
            return False

    def clear(self):
        """Clear all cache entries"""
        with self._lock:
            for cache_file in self.cache_dir.glob("*.cache"):
                cache_file.unlink(missing_ok=True)

    def _get_cache_file(self, key: str) -> Path:
        """Get cache file path for key"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"

    def _cleanup_if_needed(self):
        """Cleanup cache if size exceeds limit"""
        total_size = sum(
        f.stat().st_size for f in self.cache_dir.glob("*.cache"))
        max_size_bytes = self.max_size_mb * 1024 * 1024

        if total_size > max_size_bytes:
            # Delete oldest files
            cache_files = list(self.cache_dir.glob("*.cache"))
            cache_files.sort(key=lambda f: f.stat().st_mtime)

            # Delete 20% of files
            delete_count = max(1, len(cache_files) // 5)
            for i in range(delete_count):
                cache_files[i].unlink(missing_ok=True)

    def _load_metrics(self) -> CacheMetrics:
        """Load cache metrics from disk"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)
                return CacheMetrics(**data)
            except:
                pass
        return CacheMetrics()

    def _save_metrics(self):
        """Save cache metrics to disk"""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump({
                    'hits': self.metrics.hits,
                    'misses': self.metrics.misses,
                    'total_requests': self.metrics.total_requests,
                    'last_updated': self.metrics.last_updated.isoformat()
                }, f)
        except:
            pass


class AIOSIntelligentCacheManager:
    """
    Intelligent multi-layer cache manager for AIOS

    Provides comprehensive caching strategy with:
    - L1: Memory cache for hot data
    - L2: Disk cache for persistence
    - Intelligent cache warming and invalidation
    - Performance monitoring and optimization
    """

    def __init__(self,
                 memory_cache_size: int = 1000,
                 disk_cache_size_mb: int = 100,
                 cache_dir: str = "cache"):

        self.memory_cache = AIOSMemoryCache(max_size=memory_cache_size)
        self.disk_cache = AIOSDiskCache(
        cache_dir=cache_dir, max_size_mb=disk_cache_size_mb)
        self._warming_strategies: Dict[str, Callable] = {}
        self._cache_namespaces: Dict[str, str] = {}

        print(f"""
 AIOS Intelligent Cache Manager Initialized
    Memory Cache: {memory_cache_size} entries
    Disk Cache: {disk_cache_size_mb} MB
    Cache Directory: {cache_dir}
    Multi-layer caching strategy active
""")

    def get(self, key: str, namespace: str = "default") -> Optional[Any]:
        """Get value with multi-layer lookup"""
        namespaced_key = f"{namespace}:{key}"

        # L1: Try memory cache first
        value = self.memory_cache.get(namespaced_key)
        if value is not None:
            return value

        # L2: Try disk cache
        value = self.disk_cache.get(namespaced_key)
        if value is not None:
            # Promote to memory cache
            self.memory_cache.put(namespaced_key, value)
            return value

        # Try cache warming if strategy exists
        if namespace in self._warming_strategies:
            value = self._warming_strategies[namespace](key)
            if value is not None:
                self.put(key, value, namespace=namespace)
                return value

        return None

    def put(self, key: str, value: Any,
            namespace: str = "default",
            ttl_seconds: Optional[int] = None,
            memory_only: bool = False) -> bool:
        """Put value into cache with intelligent placement"""
        namespaced_key = f"{namespace}:{key}"

        # Always put in memory cache
        memor
        y_success = self.memory_cache.put(namespaced_key, value, ttl_seconds)

        # Put in disk cache unless memory_only
        disk_success = True
        if not memory_only:
            disk_success = self.disk_cache.put(
            namespaced_key, value, ttl_seconds)

        return memory_success and disk_success

    def invalidate(self, key: str, namespace: str = "default") -> bool:
        """Invalidate cache entry from all layers"""
        namespaced_key = f"{namespace}:{key}"

        memory_result = self.memory_cache.invalidate(namespaced_key)
        disk_result = self.disk_cache.invalidate(namespaced_key)

        return memory_result or disk_result

    def invalidate_namespace(self, namespace: str) -> int:
        """Invalidate all entries in a namespace"""
        # This is a simplified implementation
        # In production, you'd want more efficient namespace tracking
        invalidated = 0

        # Memory cache invalidation
        keys_to_remove = [key for key in self.memory_cache._cache.keys()
                         if key.startswith(f"{namespace}:")]
        for key in keys_to_remove:
            if self.memory_cache.invalidate(key):
                invalidated += 1

        return invalidated

    def register_warming_strategy(
    self, namespace: str, strategy: Callable[[str], Any]):
        """Register cache warming strategy for namespace"""
        self._warming_strategies[namespace] = strategy
        print(
        f"    Cache warming strategy registered for namespace: {namespace}")

    def warm_cache(self, namespace: str, keys: List[str]):
        """Warm cache with predefined keys"""
        if namespace not in self._warming_strategies:
            return

        strategy = self._warming_strategies[namespace]
        warmed = 0

        for key in keys:
            try:
                value = strategy(key)
                if value is not None:
                    self.put(key, value, namespace=namespace)
                    warmed += 1
            except Exception:
                continue

        print(
        f"    Cache warmed: {warmed}/{len(keys)} entries for {namespace}")

    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        memory_stats = self.memory_cache.get_stats()

        return {
            'memory_cache': memory_stats,
            'disk_cache': {
                'hits': self.disk_cache.metrics.hits,
                'misses': self.disk_cache.metrics.misses,
                'hit_ratio': self.disk_cache.metrics.hit_ratio,
                'total_requests': self.disk_cache.metrics.total_requests
            },
            'overall': {
                'total_requests': (memory_stats['total_requests'] +
                                 self.disk_cache.metrics.total_requests),
                'effective_hit_ratio': self._calculate_effective_hit_ratio(),
                'warming_strategies': len(self._warming_strategies)
            }
        }

    def _calculate_effective_hit_ratio(self) -> float:
        """Calculate effective hit ratio across all cache layers"""
        total_requests = (self.memory_cache.metrics.total_requests +
                         self.disk_cache.metrics.total_requests)
        total_hits = (self.memory_cache.metrics.hits +
                     self.disk_cache.metrics.hits)

        if total_requests == 0:
            return 0.0

        return total_hits / total_requests


# AINLP-specific cache warming strategies
class AINLPCacheWarming:
    """Cache warming strategies for AINLP components"""

    @staticmethod
    def ainlp_compilation_cache(key: str) -> Optional[Any]:
        """Cache warming for AINLP compilation results"""
        # Simulate AINLP compilation cache warming
        if key.startswith("compile:"):
            return {
                'compiled_code': f"// Generated code for {key}",
                'compilation_time': 0.15,
                'optimizations': ['performance', 'memory']
            }
        return None

    @staticmethod
    def context_analysis_cache(key: str) -> Optional[Any]:
        """Cache warming for context analysis results"""
        if key.startswith("context:"):
            return {
                'analysis_result': f"Context analysis for {key}",
                'dependencies': ['core', 'ai', 'interface'],
                'complexity_score': 0.7
            }
        return None


def create_optimized_aios_cache() -> AIOSIntelligentCacheManager:
    """Create optimized AIOS cache manager with default configuration"""

    cache_manager = AIOSIntelligentCacheManager(
        memory_cache_size=2000,    # Increased for better performance
        disk_cache_size_mb=500,    # Larger disk cache
        cache_dir="cache/aios"
    )

    # Register AINLP cache warming strategies
    cache_manager.register_warming_strategy(
        "ainlp_compilation",
        AINLPCacheWarming.ainlp_compilation_cache
    )

    cache_manager.register_warming_strategy(
        "context_analysis",
        AINLPCacheWarming.context_analysis_cache
    )

    return cache_manager


def main():
    """Demonstration of AIOS intelligent caching system"""
    print("""
\

                    AIOS Intelligent Caching System Demo                     
                     Multi-Layer Performance Optimization                    
\

""")

    # Create optimized cache manager
    cache_manager = create_optimized_aios_cache()

    # Demo cache operations
    print("\n🧪 Testing cache operations...")

    # Test AINLP compilation caching
    cache_manager.put(
    "test_function", "compiled_code_here", namespace="ainlp_compilation")
    result = cache_manager.get("test_function", namespace="ainlp_compilation")
    print(f"    AINLP cache test: {'PASSED' if result else 'FAILED'}")

    # Test context analysis caching
    cache_manager.put(
    "main_context", {"files": 49, "analysis": "complete"}, namespace="context_analysis")
    result = cache_manager.get("main_context", namespace="context_analysis")
    print(f"    Context cache test: {'PASSED' if result else 'FAILED'}")

    # Test cache warming
    print("\n Testing cache warming...")
    cache_manager.warm_cache(
    "ainlp_compilation", ["compile:test1", "compile:test2"])

    # Display cache statistics
    print("\n Cache Performance Statistics:")
    stats = cache_manager.get_comprehensive_stats()

    print(f"""
    Memory Cache:
      - Size: {
      stats['memory_cache']['size']}/{stats['memory_cache']['max_size']}
      - Hit Ratio: {stats['memory_cache']['hit_ratio']:.2%}
      - Avg Response: {stats['memory_cache']['avg_response_time_ms']:.2f}ms

    Disk Cache:
      - Hit Ratio: {stats['disk_cache']['hit_ratio']:.2%}
      - Total Requests: {stats['disk_cache']['total_requests']}

    Overall Performance:
      - Effective Hit Ratio: {stats['overall']['effective_hit_ratio']:.2%}
      - Warming Strategies: {stats['overall']['warming_strategies']}
""")

    print(" AIOS Intelligent Caching System ready for integration!")


if __name__ == "__main__":
    main()
