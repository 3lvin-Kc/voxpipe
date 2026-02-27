"""
Voxpipe OpenClaw Integration Bridge

Connects Voxpipe voice I/O to OpenClaw AI agents.
Allows voice conversations with persistent memory.
"""

import asyncio
import json
import requests
from typing import Optional, Callable
from dataclasses import dataclass
from datetime import datetime


@dataclass
class VoiceMessage:
    """A voice message with metadata"""
    text: str
    timestamp: datetime
    speaker: str  # 'user' or 'agent'
    session_id: str
    

class OpenClawVoiceBridge:
    """
    Bridge between Voxpipe voice layer and OpenClaw AI.
    
    Handles:
    - Sending voice transcripts to OpenClaw
    - Receiving AI responses
    - Persisting conversation state via open-engine
    """
    
    def __init__(
        self,
        openclaw_url: str = "http://127.0.0.1:3030",
        user_id: str = "voxpipe-user",
        agent_id: str = "doremon"
    ):
        self.openclaw_url = openclaw_url
        self.user_id = user_id
        self.agent_id = agent_id
        self.session_id: Optional[str] = None
        self.conversation_history: list[VoiceMessage] = []
        
        # Callbacks
        self.on_response: Optional[Callable[[str], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
        
    async def initialize(self) -> bool:
        """Initialize connection to open-engine"""
        try:
            # Create user in open-engine
            response = requests.post(
                f"{self.openclaw_url}/api",
                json={
                    "jsonrpc": "2.0",
                    "method": "create_user",
                    "params": {"id": self.user_id},
                    "id": 1
                }
            )
            
            # Create session
            session_response = requests.post(
                f"{self.openclaw_url}/api",
                json={
                    "jsonrpc": "2.0",
                    "method": "create_session",
                    "params": {
                        "user_id": self.user_id,
                        "name": f"voxpipe-session-{datetime.now().isoformat()}"
                    },
                    "id": 2
                }
            )
            
            if session_response.status_code == 200:
                result = session_response.json()
                self.session_id = result.get("result", {}).get("id")
                print(f"[Bridge] Initialized session: {self.session_id}")
                return True
                
        except Exception as e:
            print(f"[Bridge] Init failed: {e}")
            if self.on_error:
                await self.on_error(e)
                
        return False
    
    async def process_utterance(self, text: str) -> Optional[str]:
        """
        Process user voice input and get AI response.
        
        Args:
            text: Transcribed user speech
            
        Returns:
            AI response text to speak
        """
        if not self.session_id:
            print("[Bridge] Not initialized")
            return None
            
        try:
            # Create goal for this utterance
            goal_response = requests.post(
                f"{self.openclaw_url}/api",
                json={
                    "jsonrpc": "2.0",
                    "method": "create_goal",
                    "params": {
                        "user_id": self.user_id,
                        "session_id": self.session_id,
                        "title": f"Respond to: {text[:30]}...",
                        "priority": "high"
                    },
                    "id": 3
                }
            )
            
            goal_id = goal_response.json().get("result", {}).get("id")
            
            # Record user message
            user_msg = VoiceMessage(
                text=text,
                timestamp=datetime.now(),
                speaker="user",
                session_id=self.session_id
            )
            self.conversation_history.append(user_msg)
            
            # TODO: Send to OpenClaw agent for response
            # For now, return placeholder
            response_text = await self._get_ai_response(text)
            
            # Record agent response
            agent_msg = VoiceMessage(
                text=response_text,
                timestamp=datetime.now(),
                speaker="agent",
                session_id=self.session_id
            )
            self.conversation_history.append(agent_msg)
            
            return response_text
            
        except Exception as e:
            print(f"[Bridge] Process error: {e}")
            if self.on_error:
                await self.on_error(e)
            return None
    
    async def _get_ai_response(self, user_text: str) -> str:
        """
        Get AI response from OpenClaw.
        
        TODO: This should call the actual OpenClaw API/session
        For now, returns placeholder responses.
        """
        # Placeholder: In production, this talks to OpenClaw session
        responses = [
            "I heard you. Tell me more.",
            "Interesting point. What do you think?",
            "I'm processing that. Give me a moment.",
            "That's a good question. Let me think.",
            "I understand. Go on."
        ]
        
        # Simple deterministic response based on input length
        index = len(user_text) % len(responses)
        return responses[index]
    
    async def resume_session(self, session_id: str) -> bool:
        """Resume a previous conversation session"""
        try:
            response = requests.post(
                f"{self.openclaw_url}/api",
                json={
                    "jsonrpc": "2.0",
                    "method": "get_session",
                    "params": {"id": session_id},
                    "id": 4
                }
            )
            
            if response.status_code == 200:
                self.session_id = session_id
                print(f"[Bridge] Resumed session: {session_id}")
                return True
                
        except Exception as e:
            print(f"[Bridge] Resume failed: {e}")
            
        return False
    
    def get_conversation_context(self, limit: int = 10) -> str:
        """Get recent conversation context for AI prompting"""
        recent = self.conversation_history[-limit:] if len(self.conversation_history) > limit else self.conversation_history
        
        context_lines = []
        for msg in recent:
            speaker = "User" if msg.speaker == "user" else "Doremon"
            context_lines.append(f"{speaker}: {msg.text}")
            
        return "\n".join(context_lines)


class VoxpipeOpenClawController:
    """
    High-level controller integrating Voxpipe with OpenClaw.
    
    Usage:
        controller = VoxpipeOpenClawController()
        await controller.start()
        # Voxpipe routes speech here
        response = await controller.handle_speech("Hello Doremon")
        # Voxpipe speaks response
    """
    
    def __init__(self):
        self.bridge = OpenClawVoiceBridge()
        self.is_listening = True
        
    async def start(self):
        """Initialize the controller"""
        success = await self.bridge.initialize()
        if success:
            print("[Controller] Voxpipe-OpenClaw bridge active")
        return success
        
    async def handle_speech(self, transcript: str) -> str:
        """
        Handle user speech and return AI response.
        
        This is the main integration point:
        1. Voxpipe captures audio
        2. STT produces transcript
        3. This method routes to OpenClaw
        4. Returns text for Voxpipe to speak
        """
        response = await self.bridge.process_utterance(transcript)
        return response or "I'm not sure how to respond to that."
        
    async def shutdown(self):
        """Clean shutdown"""
        print("[Controller] Shutting down bridge")


# Example usage
async def demo():
    """Demo the integration"""
    controller = VoxpipeOpenClawController()
    
    if await controller.start():
        print("\nDemo: Voice conversation with Doremon")
        print("-" * 50)
        
        # Simulate conversation
        user_inputs = [
            "Hello Doremon",
            "What can you do?",
            "Tell me about yourself",
            "Goodbye"
        ]
        
        for user_text in user_inputs:
            print(f"\nUser: {user_text}")
            
            response = await controller.handle_speech(user_text)
            print(f"Doremon: {response}")
            
            await asyncio.sleep(1)
            
        await controller.shutdown()


if __name__ == "__main__":
    asyncio.run(demo())
