from enum import Enum


class CancelToken:
    """Used to signal that an operation should stop."""
    
    def __init__(self):
        self.stop = False

    def cancel(self):
        self.stop = True


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
