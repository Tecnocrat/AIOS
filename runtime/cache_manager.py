"""
AIOS Cache Manager - Phase 12 Task A
=====================================
Purpose: Centralized LRU caching infrastructure for runtime intelligence
Scope: In-memory caching with TTL, file caching, memoization decorators
Pattern: AINLP.performance-caching

Usage:
    from runtime_intelligence.cache_manager import cache, file_cache
    
    @cache(maxsize=1000, ttl=300)
    def expensive_operation(param):
        return compute_result(param)
    
    @file_cache(ttl=3600)
    def load_large_file(filepath):
        return read_and_process(filepath)
"""

import functools
import time
import json
import hashlib
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple
from datetime import datetime, timedelta


class CacheManager:
    """Centralized cache management with LRU and TTL support."""
    
    def __init__(self, maxsize: int = 1000, default_ttl: int = 300):
        """
        Initialize cache manager.
        
        Args:
            maxsize: Maximum cache entries (default 1000)
            default_ttl: Default time-to-live in seconds (default 300s)
        """
        self.maxsize = maxsize
        self.default_ttl = default_ttl
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._access_order = []
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def _make_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Create cache key from function name and arguments."""
        key_parts = [func_name]
        
        # Add args
        for arg in args:
            if isinstance(arg, (str, int, float, bool, type(None))):
                key_parts.append(str(arg))
            elif isinstance(arg, Path):
                key_parts.append(str(arg))
            else:
                # Hash complex objects
                key_parts.append(
                    hashlib.md5(str(arg).encode()).hexdigest()[:8]
                )
        
        # Add kwargs (sorted for consistency)
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}={v}")
        
        return ":".join(key_parts)
    
    def _evict_lru(self):
        """Evict least recently used entry."""
        if not self._access_order:
            return
        
        lru_key = self._access_order.pop(0)
        if lru_key in self._cache:
            del self._cache[lru_key]
            self.evictions += 1
    
    def _is_expired(self, timestamp: float, ttl: int) -> bool:
        """Check if cache entry is expired."""
        return time.time() - timestamp > ttl
    
    def get(
        self, 
        func_name: str, 
        args: tuple, 
        kwargs: dict, 
        ttl: int = None
    ) -> Optional[Any]:
        """Get cached value if exists and not expired."""
        key = self._make_key(func_name, args, kwargs)
        
        if key in self._cache:
            value, timestamp = self._cache[key]
            ttl = ttl or self.default_ttl
            
            if not self._is_expired(timestamp, ttl):
                # Update access order (move to end)
                if key in self._access_order:
                    self._access_order.remove(key)
                self._access_order.append(key)
                
                self.hits += 1
                return value
            else:
                # Expired - remove
                del self._cache[key]
                if key in self._access_order:
                    self._access_order.remove(key)
        
        self.misses += 1
        return None
    
    def set(self, func_name: str, args: tuple, kwargs: dict, value: Any):
        """Set cached value with current timestamp."""
        key = self._make_key(func_name, args, kwargs)
        
        # Evict if at capacity
        if len(self._cache) >= self.maxsize:
            self._evict_lru()
        
        self._cache[key] = (value, time.time())
        
        # Update access order
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)
    
    def clear(self):
        """Clear all cache entries."""
        self._cache.clear()
        self._access_order.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.hits + self.misses
        hit_rate = (
            self.hits / total_requests * 100 
            if total_requests > 0 
            else 0
        )
        
        return {
            "size": len(self._cache),
            "maxsize": self.maxsize,
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "hit_rate_percent": round(hit_rate, 2),
            "total_requests": total_requests
        }


# Global cache instance
_global_cache = CacheManager(maxsize=1000, default_ttl=300)


def cache(maxsize: int = 1000, ttl: int = 300) -> Callable:
    """
    Decorator for caching function results with TTL.
    
    Args:
        maxsize: Maximum cache size (shared across all cached functions)
        ttl: Time-to-live in seconds
    
    Example:
        @cache(maxsize=500, ttl=600)
        def expensive_computation(x, y):
            return x ** y
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Try to get from cache
            cached = _global_cache.get(func.__name__, args, kwargs, ttl)
            if cached is not None:
                return cached
            
            # Cache miss - compute and store
            result = func(*args, **kwargs)
            _global_cache.set(func.__name__, args, kwargs, result)
            return result
        
        # Add cache stats method
        wrapper.cache_stats = lambda: _global_cache.stats()
        wrapper.cache_clear = lambda: _global_cache.clear()
        
        return wrapper
    return decorator


class FileCache:
    """File-based caching with TTL for large data structures."""
    
    def __init__(self, cache_dir: Path = None):
        """Initialize file cache."""
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent / "temp" / "cache"
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Statistics
        self.hits = 0
        self.misses = 0
    
    def _make_cache_path(self, key: str) -> Path:
        """Create cache file path from key."""
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{safe_key}.json"
    
    def get(self, key: str, ttl: int = 3600) -> Optional[Any]:
        """Get cached value from file if exists and not expired."""
        cache_path = self._make_cache_path(key)
        
        if not cache_path.exists():
            self.misses += 1
            return None
        
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            timestamp = data.get("timestamp", 0)
            if time.time() - timestamp > ttl:
                # Expired
                cache_path.unlink()
                self.misses += 1
                return None
            
            self.hits += 1
            return data.get("value")
        
        except (json.JSONDecodeError, KeyError, OSError):
            self.misses += 1
            return None
    
    def set(self, key: str, value: Any):
        """Set cached value to file."""
        cache_path = self._make_cache_path(key)
        
        data = {
            "timestamp": time.time(),
            "value": value
        }
        
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except (OSError, TypeError):
            # Fail silently - caching is optional
            pass
    
    def clear(self):
        """Clear all cached files."""
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except OSError:
                pass
    
    def cleanup_expired(self, ttl: int = 3600):
        """Remove expired cache files."""
        current_time = time.time()
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                mtime = cache_file.stat().st_mtime
                if current_time - mtime > ttl:
                    cache_file.unlink()
            except OSError:
                pass


# Global file cache instance
_global_file_cache = FileCache()


def file_cache(ttl: int = 3600) -> Callable:
    """
    Decorator for file-based caching (for large data).
    
    Args:
        ttl: Time-to-live in seconds (default 1 hour)
    
    Example:
        @file_cache(ttl=7200)
        def load_large_dataset(filepath):
            return expensive_load_operation(filepath)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = f"{func.__name__}:{args}:{kwargs}"
            
            # Try to get from cache
            cached = _global_file_cache.get(key, ttl)
            if cached is not None:
                return cached
            
            # Cache miss - compute and store
            result = func(*args, **kwargs)
            _global_file_cache.set(key, result)
            return result
        
        return wrapper
    return decorator


def memoize(func: Callable) -> Callable:
    """
    Simple memoization decorator (no TTL, unlimited cache).
    Use for pure functions with deterministic outputs.
    
    Example:
        @memoize
        def fibonacci(n):
            if n < 2:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
    """
    cache_dict = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create hashable key
        key = (args, tuple(sorted(kwargs.items())))
        
        if key not in cache_dict:
            cache_dict[key] = func(*args, **kwargs)
        
        return cache_dict[key]
    
    wrapper.cache = cache_dict
    wrapper.cache_clear = lambda: cache_dict.clear()
    
    return wrapper


# Utility functions
def get_global_cache_stats() -> Dict[str, Any]:
    """Get statistics for global cache."""
    return _global_cache.stats()


def clear_all_caches():
    """Clear all caches (memory and file)."""
    _global_cache.clear()
    _global_file_cache.clear()


def cleanup_expired_file_cache(ttl: int = 3600):
    """Cleanup expired file cache entries."""
    _global_file_cache.cleanup_expired(ttl)


# Example usage and testing
if __name__ == "__main__":
    print("AIOS Cache Manager - Phase 12 Task A")
    print("=" * 80)
    
    # Test memory cache
    @cache(maxsize=10, ttl=5)
    def expensive_function(x, y):
        time.sleep(0.1)  # Simulate expensive operation
        return x ** y
    
    print("\nTesting memory cache:")
    print(f"First call (cache miss): {expensive_function(2, 10)}")
    print(f"Second call (cache hit): {expensive_function(2, 10)}")
    print(f"Stats: {expensive_function.cache_stats()}")
    
    # Test file cache
    @file_cache(ttl=3600)
    def load_data(filepath):
        return {"data": f"Loaded from {filepath}"}
    
    print("\nTesting file cache:")
    print(f"First call: {load_data('test.json')}")
    print(f"Second call: {load_data('test.json')}")
    
    # Test memoization
    @memoize
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    print("\nTesting memoization:")
    start = time.time()
    result = fibonacci(30)
    duration = (time.time() - start) * 1000
    print(f"Fibonacci(30) = {result} (computed in {duration:.2f}ms)")
    
    print("\n" + "=" * 80)
    print("Cache Manager Ready for Phase 12 Task A optimization!")
