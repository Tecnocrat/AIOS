import asyncio
import hashlib
import json
import os
import time
from typing import Optional, Dict, Any, List


class FractalTTLCache:
    def __init__(
        self,
        memory_ttl: int = 30,
        disk_ttl: int = 300,
        base_dir: Optional[str] = None,
    ):
        self.memory_ttl = memory_ttl
        self.disk_ttl = disk_ttl
        self._memory: Dict[str, Any] = {}
        self._memory_expiry: Dict[str, float] = {}
        self.base_dir = base_dir or os.path.join(
            os.path.dirname(__file__),
            "..",
            "logs",
            "cache",
        )
        os.makedirs(self.base_dir, exist_ok=True)

    def _key_to_path(self, key: str) -> str:
        digest = hashlib.sha1(key.encode("utf-8")).hexdigest()
        return os.path.join(self.base_dir, f"{digest}.json")

    def get(self, key: str) -> Optional[Any]:
        now = time.time()
        if key in self._memory and self._memory_expiry.get(key, 0) > now:
            return self._memory[key]
        path = self._key_to_path(key)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                if payload.get("_expiry", 0) > now:
                    self._memory[key] = payload["data"]
                    self._memory_expiry[key] = now + self.memory_ttl
                    return payload["data"]
            except Exception:
                pass
        return None

    def set(self, key: str, value: Any) -> None:
        now = time.time()
        self._memory[key] = value
        self._memory_expiry[key] = now + self.memory_ttl
        path = self._key_to_path(key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        payload = {"_expiry": now + self.disk_ttl, "data": value}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)


class AsyncSubprocessManager:
    def __init__(
        self,
        cache: Optional[FractalTTLCache] = None,
        log_dir: Optional[str] = None,
    ):
        self.cache = cache or FractalTTLCache()
        self.log_dir = log_dir or os.path.join(
            os.path.dirname(__file__),
            "..",
            "logs",
            "subprocess",
        )
        os.makedirs(self.log_dir, exist_ok=True)

    async def run(
        self,
        cmd: List[str],
        timeout: Optional[float] = 30.0,
        cache_ttl: Optional[int] = None,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        key = (
            "cmd:" + " ".join(cmd)
            + "|cwd:" + (cwd or "")
            + "|env_keys:" + ",".join(sorted((env or {}).keys()))
        )
        if cache_ttl and cache_ttl > 0:
            cached = self.cache.get(key)
            if cached is not None:
                return {**cached, "_cached": True}

        started = time.time()
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
            env=env,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=timeout
            )
            rc = proc.returncode
        except asyncio.TimeoutError:
            proc.kill()
            stdout, stderr = await proc.communicate()
            rc = -9

        duration_ms = int((time.time() - started) * 1000)
        result = {
            "cmd": cmd,
            "returncode": rc,
            "stdout": stdout.decode(errors="replace"),
            "stderr": stderr.decode(errors="replace"),
            "duration_ms": duration_ms,
            "timestamp": int(time.time()),
        }
        self._log_result(result)

        if cache_ttl and cache_ttl > 0 and rc == 0:
            prev_memory_ttl = self.cache.memory_ttl
            prev_disk_ttl = self.cache.disk_ttl
            self.cache.memory_ttl = min(cache_ttl, 60)
            self.cache.disk_ttl = cache_ttl
            try:
                self.cache.set(key, result)
            finally:
                self.cache.memory_ttl = prev_memory_ttl
                self.cache.disk_ttl = prev_disk_ttl

        return result

    async def run_parallel(
        self,
        commands: List[List[str]],
        timeout: float = 30.0,
        cache_ttl: Optional[int] = None,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> List[Dict[str, Any]]:
        tasks = [
            self.run(
                cmd,
                timeout=timeout,
                cache_ttl=cache_ttl,
                cwd=cwd,
                env=env,
            )
            for cmd in commands
        ]
        return await asyncio.gather(*tasks)

    def _log_result(self, result: Dict[str, Any]) -> None:
        ts = time.strftime(
            "%Y%m%d_%H%M%S",
            time.localtime(result.get("timestamp", time.time())),
        )
        digest = hashlib.sha1(
            " ".join(result.get("cmd", [])).encode("utf-8")
        ).hexdigest()[:8]
        path = os.path.join(self.log_dir, f"{ts}_{digest}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
