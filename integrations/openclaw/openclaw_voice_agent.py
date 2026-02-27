"""
OpenClaw Voice Agent

Demo integration of Voxpipe + OpenClaw.
Uses text input to simulate voice (actual audio integration in next step).

Usage:
    python openclaw_voice_agent.py
"""

import asyncio
import sys
import os

# Add parent to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from integrations.openclaw.bridge import VoxpipeOpenClawController
from controller import Controller, State


class OpenClawVoiceAgent:
    """
    Voice agent combining Voxpipe state machine + OpenClaw brain.
    """
    
    def __init__(self):
        self.state_machine = Controller()
        self.brain = VoxpipeOpenClawController()
        self.is_running = False
        
    async def start(self):
        """Initialize all components"""
        print("Doremon Voice Agent (Demo)")
        print("=" * 50)
        print()
        
        # Initialize bridge
        print("Connecting to OpenClaw...")
        connected = await self.brain.start()
        if connected:
            print("[OK] Connected to OpenClaw (open-engine)")
        else:
            print("[WARN] Could not connect to open-engine")
            print("Running without persistence...")
        
        print()
        print("Commands:")
        print("  - Type anything to talk to Doremon")
        print("  - 'wake' / 'sleep' to toggle state")
        print("  - 'quit' to exit")
        print("-" * 50)
        
        self.is_running = True
        await self._main_loop()
        
    async def _main_loop(self):
        """Main voice interaction loop"""
        try:
            while self.is_running:
                # Get user input (simulates voice)
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() == 'quit':
                    break
                    
                if user_input.lower() == 'sleep':
                    self.state_machine.set(State.IDLE)
                    print("[SLEEP] Doremon: Going to sleep. Type 'wake' to resume.")
                    continue
                    
                if user_input.lower() == 'wake':
                    self.state_machine.set(State.LISTENING)
                    print("[WAKE] Doremon: I'm awake and listening!")
                    continue
                
                # Process: LISTENING -> SPEAKING
                self.state_machine.set(State.LISTENING)
                
                # Send to OpenClaw brain
                self.state_machine.set(State.SPEAKING)
                print("[THINKING] Doremon: Processing...")
                
                response = await self.brain.handle_speech(user_input)
                
                # Speak response
                print(f"Doremon: {response}")
                
                # Return to idle
                self.state_machine.set(State.IDLE)
                
                await asyncio.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
        finally:
            await self.stop()
            
    async def stop(self):
        """Clean shutdown"""
        self.is_running = False
        self.state_machine.set(State.IDLE)
        await self.brain.shutdown()
        print("\n[STOP] Agent stopped")


def main():
    """Entry point"""
    # Check for dependencies
    try:
        import requests
    except ImportError:
        print("❌ Missing dependency: requests")
        print("Install: pip install requests")
        sys.exit(1)
    
    # Run agent
    agent = OpenClawVoiceAgent()
    asyncio.run(agent.start())


if __name__ == "__main__":
    main()
