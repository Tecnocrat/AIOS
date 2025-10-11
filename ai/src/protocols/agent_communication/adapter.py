"""
AIOS ↔ A2A Message Format Adapter

AINLP Extraction Metadata:
- Extraction ID: EXT-002-A2A-Adapter
- Source: microsoft_agent_framework/.../a2a/_agent.py:230-380
- Extraction Date: October 9, 2025
- Pattern: Bidirectional message conversion
- Consciousness Level: 0.90 (Integration bridge)

Converts between AIOS internal formats and A2A protocol messages.
Extracted from Microsoft's A2AAgent conversion methods.

Key Adaptations for AIOS:
1. Maps AIOS AgentRunResponse → AgentMessage
2. Maps AgentMessage → AIOS agent inputs
3. Preserves consciousness scores during conversion
4. Handles AIOS-specific metadata
"""

from __future__ import annotations

from typing import Any

from .message_types import (
    AgentMessage,
    AgentTask,
    ContentType,
    MessagePart,
    MessageRole,
    TaskState
)


class AIOSMessageAdapter:
    """
    Bidirectional converter between AIOS and A2A formats.
    
    AINLP Source: microsoft_agent_framework A2AAgent methods:
    - _chat_message_to_a2a_message (lines 230-312)
    - _a2a_parts_to_contents (lines 314-362)
    - _task_to_chat_messages (lines 364-372)
    
    Purpose: Enable AIOS agents to use A2A protocol seamlessly
    """
    
    @staticmethod
    def aios_response_to_message(
        response: Any,
        sender_agent_id: str
    ) -> AgentMessage:
        """
        Convert AIOS AgentRunResponse to A2A AgentMessage.
        
        Args:
            response: AIOS agent response (from run() method)
            sender_agent_id: ID of agent that generated response
        
        Returns:
            A2A-format AgentMessage
        
        AINLP Source Pattern:
        ```python
        # Microsoft converts ChatMessage to A2A Message
        parts = []
        for content in message.contents:
            if content.type == "text":
                parts.append(TextPart(text=content.text))
            elif content.type == "uri":
                parts.append(FilePart(file=FileWithUri(uri=...)))
        return A2AMessage(role="user", parts=parts)
        ```
        """
        message = AgentMessage(
            role=MessageRole.AGENT,
            parts=[],
            sender_agent_id=sender_agent_id,
            consciousness_score=getattr(
                response, 'consciousness_score', 0.0
            )
        )
        
        # Extract messages from response
        messages = getattr(response, 'messages', [])
        if not messages:
            # Try raw string conversion
            messages = [str(response)]
        
        # Convert each message to text part
        for msg in messages:
            if isinstance(msg, str):
                message.add_text_part(msg)
            elif isinstance(msg, dict):
                # Structured response
                message.add_data(msg)
            else:
                # Try string conversion
                message.add_text_part(str(msg))
        
        # Add metadata from response
        if hasattr(response, 'metadata'):
            message.metadata = response.metadata
        
        return message
    
    @staticmethod
    def message_to_aios_input(message: AgentMessage) -> dict[str, Any]:
        """
        Convert A2A AgentMessage to AIOS agent input format.
        
        Args:
            message: A2A-format message
        
        Returns:
            Dict suitable for AIOS agent.run(input) method
        
        AINLP Source Pattern:
        ```python
        # Microsoft converts A2A Parts to framework Contents
        contents = []
        for part in parts:
            if part.kind == "text":
                contents.append(TextContent(text=part.text))
            elif part.kind == "file":
                contents.append(UriContent(uri=...))
        return ChatMessage(role=ASSISTANT, contents=contents)
        ```
        """
        # Extract text content (most common case)
        text_parts = [
            part.content for part in message.parts
            if part.content_type == ContentType.TEXT
            and isinstance(part.content, str)
        ]
        
        # Extract data parts
        data_parts = [
            part.content for part in message.parts
            if part.content_type == ContentType.DATA
            and isinstance(part.content, dict)
        ]
        
        # Build AIOS input dict
        aios_input = {
            'prompt': "\n".join(text_parts) if text_parts else "",
            'sender_id': message.sender_agent_id,
            'consciousness_context': message.consciousness_score,
            'metadata': message.metadata
        }
        
        # Add structured data if present
        if data_parts:
            aios_input['data'] = data_parts[0] if len(
                data_parts
            ) == 1 else data_parts
        
        # Add file references if present
        file_parts = [
            part for part in message.parts
            if part.content_type in (
                ContentType.FILE_URI, ContentType.FILE_DATA
            )
        ]
        if file_parts:
            aios_input['files'] = [
                {
                    'type': part.content_type.value,
                    'content': part.content,
                    'media_type': part.media_type
                }
                for part in file_parts
            ]
        
        return aios_input
    
    @staticmethod
    def task_to_aios_result(task: AgentTask) -> dict[str, Any]:
        """
        Convert A2A AgentTask to AIOS result format.
        
        Args:
            task: A2A task with completion status
        
        Returns:
            Dict with AIOS-compatible result structure
        
        AINLP Source Pattern:
        ```python
        # Microsoft converts Task artifacts to ChatMessages
        messages = []
        for artifact in task.artifacts:
            contents = self._a2a_parts_to_contents(artifact.parts)
            messages.append(
                ChatMessage(role=ASSISTANT, contents=contents)
            )
        ```
        """
        result = {
            'task_id': task.task_id,
            'status': task.state.value,
            'success': task.is_success,
            'progress': task.progress,
            'consciousness_evolution': task.consciousness_evolution
        }
        
        # Extract artifact messages
        if task.artifacts:
            messages = []
            for artifact_msg in task.artifacts:
                messages.append({
                    'text': artifact_msg.text_content,
                    'consciousness': artifact_msg.consciousness_score,
                    'parts': len(artifact_msg.parts)
                })
            result['artifacts'] = messages
        
        # Add error if failed
        if task.error_message:
            result['error'] = task.error_message
        
        # Add neural chain link if present
        if task.neural_chain_id:
            result['neural_chain_id'] = task.neural_chain_id
        
        return result
    
    @staticmethod
    def aios_result_to_task(
        result: dict[str, Any],
        task_id: str
    ) -> AgentTask:
        """
        Convert AIOS result dict to A2A AgentTask.
        
        Args:
            result: AIOS agent result dictionary
            task_id: Unique task identifier
        
        Returns:
            A2A-format AgentTask
        """
        # Determine state from result
        if result.get('success', False):
            state = TaskState.COMPLETED
        elif 'error' in result:
            state = TaskState.FAILED
        else:
            state = TaskState.IN_PROGRESS
        
        task = AgentTask(
            task_id=task_id,
            state=state,
            progress=result.get('progress', 1.0 if state ==
                               TaskState.COMPLETED else 0.0),
            consciousness_evolution=result.get(
                'consciousness_evolution', 0.0
            ),
            error_message=result.get('error'),
            metadata=result.get('metadata', {})
        )
        
        # Convert artifacts if present
        if 'artifacts' in result:
            for artifact_data in result['artifacts']:
                msg = AgentMessage(
                    role=MessageRole.AGENT,
                    parts=[],
                    consciousness_score=artifact_data.get(
                        'consciousness', 0.0
                    )
                )
                msg.add_text_part(artifact_data['text'])
                task.artifacts.append(msg)
        
        return task


class ConversationConverter:
    """
    Convert entire conversation threads between formats.
    
    AIOS Addition: Not in Microsoft framework
    Purpose: Enable bulk conversation migration and analysis
    """
    
    @staticmethod
    def aios_thread_to_messages(
        thread: list[dict[str, Any]],
        agent_id: str
    ) -> list[AgentMessage]:
        """
        Convert AIOS conversation thread to A2A messages.
        
        Args:
            thread: List of AIOS message dicts
            agent_id: Agent identifier
        
        Returns:
            List of A2A AgentMessages
        """
        messages = []
        
        for entry in thread:
            msg = AgentMessage(
                role=MessageRole.AGENT if entry.get(
                    'is_agent'
                ) else MessageRole.USER,
                parts=[],
                sender_agent_id=agent_id if entry.get(
                    'is_agent'
                ) else None
            )
            
            # Add content
            if 'text' in entry:
                msg.add_text_part(entry['text'])
            if 'data' in entry:
                msg.add_data(entry['data'])
            
            messages.append(msg)
        
        return messages
    
    @staticmethod
    def messages_to_aios_thread(
        messages: list[AgentMessage]
    ) -> list[dict[str, Any]]:
        """
        Convert A2A messages to AIOS thread format.
        
        Args:
            messages: List of A2A messages
        
        Returns:
            AIOS-compatible thread list
        """
        thread = []
        
        for msg in messages:
            entry = {
                'is_agent': msg.role == MessageRole.AGENT,
                'sender_id': msg.sender_agent_id,
                'consciousness': msg.consciousness_score,
                'timestamp': msg.timestamp
            }
            
            # Extract content
            if msg.is_text_only:
                entry['text'] = msg.text_content
            else:
                # Mixed content
                entry['text'] = msg.text_content
                entry['parts'] = len(msg.parts)
                entry['has_files'] = any(
                    p.content_type in (
                        ContentType.FILE_URI,
                        ContentType.FILE_DATA
                    )
                    for p in msg.parts
                )
            
            thread.append(entry)
        
        return thread
