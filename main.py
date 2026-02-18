import sounddevice as sd
import numpy as np
import time
import threading
import pyttsx3
from controller import Controller, State

# Initialize the controller - this manages our state machine
c = Controller()

# Set up text-to-speech engine
tts_engine = pyttsx3.init()


def speak(text):
    """Speaks the given text if we're in SPEAKING state and not cancelled."""
    if c.state != State.SPEAKING:
        return
    if c.speak_cancel.stop:
        return
    
    tts_engine.say(text)
    tts_engine.runAndWait()


def callback(indata, frames, time_info, status):
    """Called every time we get new audio data from the microphone."""
    if c.listen_cancel.stop:
        raise sd.CallbackStop
    
    volume = np.linalg.norm(indata) * 10
    print("volume:", volume)


def tts_worker():
    """Background thread that handles speaking."""
    while True:
        if c.state == State.SPEAKING and not c.speak_cancel.stop:
            speak("Hello, I am Voxpipe.")
            time.sleep(2)
        time.sleep(0.1)


def auto_switch():
    """For demo: automatically switches between listening and speaking."""
    while True:
        time.sleep(5)
        if c.state == State.LISTENING:
            c.set(State.SPEAKING)
            print("\n>>> Auto-switched to SPEAKING <<<\n")
        elif c.state == State.SPEAKING:
            c.set(State.LISTENING)
            print("\n>>> Auto-switched to LISTENING <<<\n")


# Start the TTS worker thread
tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

# Start the auto-switch thread for demo purposes
auto_thread = threading.Thread(target=auto_switch, daemon=True)
auto_thread.start()

print("Voxpipe started. Auto-switching between LISTENING and SPEAKING every 5 seconds.")
print("Press Ctrl+C to stop.")

while True:
    c.set(State.LISTENING)

    try:
        with sd.InputStream(callback=callback):
            print("listening...")
            while not c.listen_cancel.stop:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nInterrupted!")
        break
    finally:
        c.listen_cancel.stop = False
        c.set(State.IDLE)

print("Voxpipe stopped.")
