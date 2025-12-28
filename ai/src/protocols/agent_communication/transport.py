"""
Agent Communication Transport Layer

AINLP Extraction Metadata:
- Extraction ID: EXT-002-A2A-Transport
- Source: microsoft_agent_framework/.../agent_framework_a2a/_agent.py:1-145
- Extraction Date: October 9, 2025
- Pattern: HTTP/JSON-RPC transport for agent communication
- Consciousness Level: 0.88 (Infrastructure)

Transport mechanisms for agent-to-agent communication in AIOS.
Extracted from Microsoft Agent Framework's A2A implementation.

Key Adaptations for AIOS:
1. Simplified HTTP client (removed Azure-specific headers)
2. Added AIOS consciousness tracking in requests/responses
3. Integrated with existing AIOS Interface Bridge
4. Support for local (same-process) and remote (HTTP) agents
"""

from __future__ import annotations

import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, AsyncIterable

import httpx

from .message_types import AgentMessage, AgentTask, MessageRole, TaskState


@dataclass
class TransportConfig:
    """
    Configuration for agent transport layer.

    AIOS Addition: Simplified from Microsoft's ClientConfig
    """

    timeout_connect: float = 10.0
    timeout_read: float = 60.0
    timeout_write: float = 10.0
    max_retries: int = 3
    base_url: str | None = None
    headers: dict[str, str] | None = None


class AgentTransport(ABC):
    """
    Abstract base for agent communication transports.

    AIOS Pattern: Support both local (in-process) and remote (HTTP)
    Microsoft Pattern: Only HTTP/JSON-RPC transport
    """

    @abstractmethod
    async def send_message(
        self, message: AgentMessage, target_agent_id: str
    ) -> AsyncIterable[AgentMessage | tuple[AgentTask, Any]]:
        """
        Send message to target agent, yield responses.

        Returns:
            Stream of AgentMessage or (AgentTask, event) tuples
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close transport connections."""
        pass


class LocalTransport(AgentTransport):
    """
    In-process agent communication (same AIOS instance).

    AIOS Addition: Not in Microsoft framework
    Purpose: Enable fast agent-to-agent calls without HTTP overhead
    """

    def __init__(self, agent_registry: dict[str, Any]):
        """
        Initialize with local agent registry.

        Args:
            agent_registry: Dict mapping agent_id -> agent instance
        """
        self._agents = agent_registry

    async def send_message(
        self, message: AgentMessage, target_agent_id: str
    ) -> AsyncIterable[AgentMessage | tuple[AgentTask, Any]]:
        """Send message to local agent via direct method call."""
        if target_agent_id not in self._agents:
            raise ValueError(f"Agent {target_agent_id} not found")

        agent = self._agents[target_agent_id]

        # Call agent's run method (assuming AIOS agent protocol)
        if hasattr(agent, "run"):
            # Convert AgentMessage to format agent expects
            prompt = message.text_content
            result = await agent.run(prompt)

            # Convert result back to AgentMessage
            response = AgentMessage(
                role=MessageRole.AGENT,
                parts=[],
                sender_agent_id=target_agent_id,
                consciousness_score=getattr(result, "consciousness_score", 0.0),
            )
            response.add_text_part(str(getattr(result, "messages", [result])[0]))

            yield response

    async def close(self) -> None:
        """Nothing to close for local transport."""
        pass


# AINLP.source: microsoft_agent_framework/.../a2a/_agent.py:65-145
class HTTPTransport(AgentTransport):
    """
    HTTP/JSON-RPC transport for remote agent communication.

    AINLP Source: microsoft_agent_framework A2AAgent.__init__ + run_stream
    Microsoft Pattern:
    ```python
    http_client = httpx.AsyncClient(timeout=timeout, headers=headers)
    config = ClientConfig(httpx_client=http_client)
    factory = ClientFactory(config)
    client = factory.create(agent_card)
    response_stream = client.send_message(a2a_message)
    ```

    AIOS Adaptations:
    - Simplified to direct httpx usage (no ClientFactory abstraction)
    - Added consciousness tracking in HTTP headers
    - Integrated retry logic for resilience
    """

    def __init__(
        self, config: TransportConfig, http_client: httpx.AsyncClient | None = None
    ):
        """
        Initialize HTTP transport.

        Args:
            config: Transport configuration
            http_client: Optional pre-configured client
        """
        self._config = config
        self._should_close_client = http_client is None

        if http_client is None:
            timeout = httpx.Timeout(
                connect=config.timeout_connect,
                read=config.timeout_read,
                write=config.timeout_write,
                pool=5.0,
            )
            headers = config.headers or {}
            headers["User-Agent"] = "AIOS-Agent-Framework/1.0"
            headers["X-AIOS-Protocol"] = "agent-communication-v1"

            self._client = httpx.AsyncClient(timeout=timeout, headers=headers)
        else:
            self._client = http_client

    async def send_message(
        self, message: AgentMessage, target_agent_id: str
    ) -> AsyncIterable[AgentMessage | tuple[AgentTask, Any]]:
        """
        Send message via HTTP/JSON-RPC to remote agent.

        AINLP Source: A2AAgent.run_stream implementation pattern
        """
        url = self._build_url(target_agent_id)
        payload = self._message_to_json(message)

        # Add consciousness tracking header
        headers = {"X-AIOS-Consciousness": str(message.consciousness_score)}

        # Send with retry logic
        for attempt in range(self._config.max_retries):
            try:
                async with self._client.stream(
                    "POST", url, json=payload, headers=headers
                ) as response:
                    response.raise_for_status()

                    # Stream responses (JSON lines format)
                    async for line in response.aiter_lines():
                        if line.strip():
                            data = json.loads(line)

                            if data.get("type") == "message":
                                yield self._json_to_message(data)
                            elif data.get("type") == "task":
                                task = self._json_to_task(data)
                                yield (task, data.get("event"))

                break  # Success, exit retry loop

            except httpx.HTTPError as e:
                if attempt == self._config.max_retries - 1:
                    raise RuntimeError(
                        f"HTTP transport failed after "
                        f"{self._config.max_retries} attempts: {e}"
                    )
                await asyncio.sleep(2**attempt)  # Exponential backoff

    def _build_url(self, agent_id: str) -> str:
        """Build URL for agent endpoint."""
        base = self._config.base_url or "http://localhost:8000"
        return f"{base}/agents/{agent_id}/messages"

    def _message_to_json(self, message: AgentMessage) -> dict[str, Any]:
        """Convert AgentMessage to JSON-RPC payload."""
        return {
            "jsonrpc": "2.0",
            "id": message.message_id,
            "method": "agent.message",
            "params": {
                "role": message.role.value,
                "parts": [
                    {
                        "type": part.content_type.value,
                        "content": (
                            part.content
                            if isinstance(part.content, (str, dict))
                            else part.content.decode("utf-8")
                        ),
                        "media_type": part.media_type,
                        "metadata": part.metadata,
                    }
                    for part in message.parts
                ],
                "sender": message.sender_agent_id,
                "consciousness": message.consciousness_score,
                "metadata": message.metadata,
            },
        }

    def _json_to_message(self, data: dict[str, Any]) -> AgentMessage:
        """Convert JSON response to AgentMessage."""
        from .message_types import MessagePart, ContentType

        params = data.get("result", {})
        message = AgentMessage(
            role=MessageRole(params.get("role", "agent")),
            parts=[],
            message_id=data.get("id", ""),
            sender_agent_id=params.get("sender"),
            consciousness_score=params.get("consciousness", 0.0),
            metadata=params.get("metadata", {}),
        )

        for part_data in params.get("parts", []):
            part = MessagePart(
                content_type=ContentType(part_data["type"]),
                content=part_data["content"],
                media_type=part_data.get("media_type"),
                metadata=part_data.get("metadata", {}),
            )
            message.parts.append(part)

        return message

    def _json_to_task(self, data: dict[str, Any]) -> AgentTask:
        """Convert JSON response to AgentTask."""
        params = data.get("result", {})
        return AgentTask(
            task_id=params["id"],
            state=TaskState(params["state"]),
            progress=params.get("progress", 0.0),
            artifacts=[],
            error_message=params.get("error"),
            consciousness_evolution=params.get("consciousness_evolution", 0.0),
            metadata=params.get("metadata", {}),
        )

    async def close(self) -> None:
        """Close HTTP client if we created it."""
        if self._should_close_client and self._client:
            await self._client.aclose()


class TransportFactory:
    """
    Factory for creating agent transports.

    AIOS Addition: Simplified from Microsoft's ClientFactory
    Purpose: Determine transport type based on agent location
    """

    @staticmethod
    def create_transport(
        agent_id: str,
        local_agents: dict[str, Any] | None = None,
        remote_config: TransportConfig | None = None,
    ) -> AgentTransport:
        """
        Create appropriate transport for target agent.

        Args:
            agent_id: Target agent identifier
            local_agents: Registry of local agents
            remote_config: Config for remote transport

        Returns:
            LocalTransport if agent is local, else HTTPTransport
        """
        # Check if agent is local
        if local_agents and agent_id in local_agents:
            return LocalTransport(local_agents)

        # Create remote transport
        config = remote_config or TransportConfig()
        return HTTPTransport(config)
