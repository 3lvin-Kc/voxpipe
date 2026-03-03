from enum import Enum
from collections import deque


class CancelToken:
    """Used to signal that an operation should stop."""
    
    def __init__(self):
        self.stop = False

    def cancel(self):
        self.stop = True

    def reset(self):
        self.stop = False


class State(Enum):
    """Our app can be in one of these states."""
    IDLE = 0
    LISTENING = 1
    SPEAKING = 2


class Controller:
    """Manages the state machine. Makes sure we don't listen and speak at the same time."""
    
    def __init__(self):
        self.state = State.IDLE
        self.listen_cancel = CancelToken()
        self.speak_cancel = CancelToken()
        
        # Race condition arbiter: queue for app's pending speech
        self.pending_speech = deque()
        self.user_is_speaking = False

    def queue_speech(self, text):
        """Queue app speech to be spoken after user finishes."""
        self.pending_speech.append(text)

    def get_next_speech(self):
        """Get next queued speech, returns None if queue empty."""
        if self.pending_speech:
            return self.pending_speech.popleft()
        return None

    def has_pending_speech(self):
        """Check if there are pending speeches."""
        return len(self.pending_speech) > 0

    def set(self, state):
        """Switch to a new state. Automatically cancels the old operation."""
        print("STATE:", self.state, "->", state)

        # If we're starting to listen, cancel any speaking
        if state == State.LISTENING:
            self.speak_cancel.cancel()
            self.listen_cancel = CancelToken()

        # If we're starting to speak, cancel any listening
        if state == State.SPEAKING:
            self.listen_cancel.cancel()
            self.speak_cancel = CancelToken()

        self.state = state
