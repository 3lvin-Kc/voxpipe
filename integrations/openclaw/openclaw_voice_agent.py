"""
OpenClaw Voice Agent

A voice-enabled AI companion using Voxpipe + OpenClaw.

Usage:
    python openclaw_voice_agent.py

Requirements:
    - Voxpipe running (for audio I/O)
    - open-engine running (for state persistence)
    - OpenClaw gateway (for AI reasoning)
"""

import asyncio
import sys
import os

# Add parent to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from integrations.openclaw.bridge import VoxpipeOpenClawController

# Import Voxpipe components
from controller import AudioController


class OpenClawVoiceAgent:
    """
    Voice agent combining Voxpipe + OpenClaw.
    """
    
    def __init__(self):
        self.audio = AudioController()
        self.brain = VoxpipeOpenClawController()
        self.is_running = False
        
    async def start(self):
        """Initialize all components"""
        print("🔮 Doremon Voice Agent")
        print("=" * 50)
        print()
        
        # Initialize bridge
        print("Connecting to OpenClaw...")
        if not await self.brain.start():
            print("⚠️  Warning: Could not connect to open-engine")
            print("Running without persistence...")
        else:
            print("✅ Connected to OpenClaw")
        
        print()
        print("Say 'wake' to start listening")
        print("Say 'sleep' to pause")
        print("Press Ctrl+C to stop")
        print("-" * 50)
        
        self.is_running = True
        await self._main_loop()
        
    async def _main_loop(self):
        """Main voice interaction loop"""
        try:
            while self.is_running:
                # Listen for wake word or command
                print("\n👂 Listening...")
                
                # TODO: Replace with actual Voxpipe audio capture
                # For now, use text input for testing
                user_input = input("You (type for test): ").strip()
                
                if user_input.lower() == 'quit':
                    break
                    
                if user_input.lower() == 'sleep':
                    print("😴 Going to sleep. Say 'wake' to resume.")
                    await self._sleep_mode()
                    continue
                    
                # Process through OpenClaw
                print("🧠 Thinking...")
                response = await self.brain.handle_speech(user_input)
                
                # Speak response
                print(f"🔮 Doremon: {response}")
                
                # TODO: Integrate Voxpipe TTS here
                # self.audio.speak(response)
                
                await asyncio.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
        finally:
            await self.stop()
            
    async def _sleep_mode(self):
        """Listen only for 'wake'"""
        while self.is_running:
            user_input = input("(Sleeping - type 'wake'): ").strip()
            if user_input.lower() == 'wake':
                print("✨ Waking up!")
                break
                
    async def stop(self):
        """Clean shutdown"""
        self.is_running = False
        await self.brain.shutdown()
        print("\n🛑 Shutdown complete")


def main():
    """Entry point"""
    import sys
    
    # Check for dependencies
    try:
        from integrations.openclaw.bridge import OpenClawVoiceBridge
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install: pip install requests")
        sys.exit(1)
    
    # Run agent
    agent = OpenClawVoiceAgent()
    asyncio.run(agent.start())


if __name__ == "__main__":
    main()
