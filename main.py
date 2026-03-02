import sounddevice as sd
import numpy as np
import time
import threading
import pyttsx3
import sys
from controller import Controller, State

# Initialize the controller - this manages our state machine
c = Controller()

# Set up text-to-speech engine
tts_engine = pyttsx3.init()

# Shutdown flag
shutdown_requested = False

# Interruption Handler Config
VOLUME_THRESHOLD = 2.0  # Adjust based on your microphone


def signal_handler(sig, frame):
    global shutdown_requested
    print("\n\nShutdown requested...")
    shutdown_requested = True


import signal
signal.signal(signal.SIGINT, signal_handler)


def speak(text):
    """Speaks the given text if we're in SPEAKING state and not cancelled."""
    if c.state != State.SPEAKING:
        return
    if c.speak_cancel.stop:
        return
    if shutdown_requested:
        return
    
    tts_engine.say(text)
    tts_engine.runAndWait()


def callback(indata, frames, time_info, status):
    """Called every time we get new audio data from the microphone."""
    
    if shutdown_requested:
        raise sd.CallbackStop
    
    volume = np.linalg.norm(indata) * 10
    print("volume:", volume)

    # INTERRUPTION HANDLER: If user speaks while app is talking, interrupt
    if c.state == State.SPEAKING and volume > VOLUME_THRESHOLD:
        print("\n>>> USER INTERRUPTED - Switching to LISTENING <<<\n")
        c.set(State.LISTENING)
    
    if c.listen_cancel.stop:
        raise sd.CallbackStop


def tts_worker():
    """Background thread that handles speaking."""
    while not shutdown_requested:
        if c.state == State.SPEAKING and not c.speak_cancel.stop:
            speak("Hello, I am Voxpipe. Say something to interrupt me.")
            time.sleep(2)
        time.sleep(0.1)


# Start the TTS worker thread
tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

print("Voxpipe started. Say something while I'm talking to interrupt me.")
print("Press Ctrl+C to stop.")

# Initialize: start in LISTENING state
c.set(State.LISTENING)

# Keep audio stream always running to detect interruptions
try:
    with sd.InputStream(callback=callback):
        print("audio stream active...")
        while not shutdown_requested:
            # Auto-demo: switch between states if no interruption
            if c.state == State.LISTENING:
                while not c.listen_cancel.stop and not shutdown_requested:
                    time.sleep(0.1)
                if not shutdown_requested:
                    c.set(State.SPEAKING)
            elif c.state == State.SPEAKING:
                time.sleep(0.5)
                c.set(State.LISTENING)
except Exception:
    pass
finally:
    shutdown_requested = True
    c.set(State.IDLE)
    print("\nVoxpipe stopped.")
