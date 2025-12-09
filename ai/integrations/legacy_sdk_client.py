#!/usr/bin/env python3
"""
Legacy SDK Client - Python 3.14t client for Legacy SDK Bridge

This client runs in the primary Python 3.14t venv and communicates
with the Legacy SDK Bridge (Python 3.12) via HTTP.

Usage:
    from ai.integrations.legacy_sdk_client import LegacySDKClient

    async with LegacySDKClient() as client:
        response = await client.gemini_generate("Hello, world!")
        print(response.text)
"""

import asyncio
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import httpx


@dataclass
class GeminiResponse:
    """Response from Gemini generation."""

    text: str
    model: str
    finish_reason: str | None = None


class LegacySDKClient:
    """Client for Legacy SDK Bridge."""

    BRIDGE_URL = "http://127.0.0.1:8099"
    LEGACY_VENV = Path(__file__).parent.parent.parent.parent / ".venvs" / "legacy"

    def __init__(self, auto_start: bool = True, timeout: float = 30.0):
        """Initialize client.

        Args:
            auto_start: Automatically start bridge if not running
            timeout: HTTP request timeout in seconds
        """
        self.auto_start = auto_start
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None
        self._bridge_process: subprocess.Popen | None = None

    async def __aenter__(self) -> Self:
        """Async context manager entry."""
        self._client = httpx.AsyncClient(base_url=self.BRIDGE_URL, timeout=self.timeout)

        if self.auto_start and not await self._is_bridge_running():
            await self._start_bridge()

        return self

    async def __aexit__(self, *args) -> None:
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    async def _is_bridge_running(self) -> bool:
        """Check if bridge is running."""
        try:
            response = await self._client.get("/health")
            return response.status_code == 200
        except httpx.ConnectError:
            return False

    async def _start_bridge(self) -> None:
        """Start the legacy SDK bridge."""
        python_exe = self.LEGACY_VENV / "Scripts" / "python.exe"
        bridge_script = self.LEGACY_VENV / "legacy_sdk_bridge.py"

        if not python_exe.exists():
            raise RuntimeError(f"Legacy venv not found: {python_exe}")
        if not bridge_script.exists():
            raise RuntimeError(f"Bridge script not found: {bridge_script}")

        # Start bridge process
        self._bridge_process = subprocess.Popen(
            [str(python_exe), str(bridge_script)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )

        # Wait for bridge to start
        for _ in range(50):  # 5 seconds max
            await asyncio.sleep(0.1)
            if await self._is_bridge_running():
                return

        raise RuntimeError("Failed to start legacy SDK bridge")

    async def health(self) -> dict:
        """Check bridge health."""
        response = await self._client.get("/health")
        response.raise_for_status()
        return response.json()

    async def gemini_generate(
        self,
        prompt: str,
        model: str = "gemini-2.0-flash",
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> GeminiResponse:
        """Generate text using Gemini.

        Args:
            prompt: Text prompt
            model: Gemini model name
            max_tokens: Maximum output tokens
            temperature: Sampling temperature

        Returns:
            GeminiResponse with generated text
        """
        payload = {"prompt": prompt, "model": model}
        if max_tokens:
            payload["max_tokens"] = max_tokens
        if temperature is not None:
            payload["temperature"] = temperature

        response = await self._client.post("/gemini/generate", json=payload)
        response.raise_for_status()
        data = response.json()

        return GeminiResponse(
            text=data["text"], model=data["model"], finish_reason=data.get("finish_reason")
        )

    async def gemini_list_models(self) -> list[dict]:
        """List available Gemini models."""
        response = await self._client.get("/gemini/models")
        response.raise_for_status()
        return response.json()["models"]


# Synchronous wrapper for non-async code
class LegacySDKClientSync:
    """Synchronous wrapper for LegacySDKClient."""

    def __init__(self, auto_start: bool = True, timeout: float = 30.0):
        self._async_client = LegacySDKClient(auto_start=auto_start, timeout=timeout)

    def __enter__(self) -> Self:
        asyncio.run(self._async_client.__aenter__())
        return self

    def __exit__(self, *args) -> None:
        asyncio.run(self._async_client.__aexit__(*args))

    def health(self) -> dict:
        return asyncio.run(self._async_client.health())

    def gemini_generate(self, prompt: str, **kwargs) -> GeminiResponse:
        return asyncio.run(self._async_client.gemini_generate(prompt, **kwargs))

    def gemini_list_models(self) -> list[dict]:
        return asyncio.run(self._async_client.gemini_list_models())


async def _test():
    """Test the client."""
    print("Testing Legacy SDK Client...")

    async with LegacySDKClient(auto_start=False) as client:
        # Health check
        health = await client.health()
        print(f"Bridge health: {health}")

        # Generate text
        response = await client.gemini_generate("Say 'Hello from AIOS' in exactly 4 words")
        print(f"Gemini response: {response.text}")


if __name__ == "__main__":
    asyncio.run(_test())
