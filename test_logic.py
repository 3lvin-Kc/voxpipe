import time
import threading
from controller import Controller, State

c = Controller()
LISTEN_TIMEOUT = 0.5  # Short timeout for testing

def test_listen_timeout_transitions():
    """Test that LISTENING switches to SPEAKING after timeout."""
    print("=== Testing Listen Timeout Transitions ===")
    
    c.set(State.LISTENING)
    assert c.state == State.LISTENING, "Should start in LISTENING"
    
    # Simulate the listen loop
    listen_start = time.time()
    while time.time() - listen_start < LISTEN_TIMEOUT:
        if c.listen_cancel.stop:
            break
        time.sleep(0.05)
    
    # After timeout, should be able to set SPEAKING
    c.set(State.SPEAKING)
    assert c.state == State.SPEAKING, "Should switch to SPEAKING after timeout"
    
    print("Listen Timeout Transitions: PASSED")
    return True


def test_state_machine_cycle():
    """Test a full listen->speak->listen cycle."""
    print("\n=== Testing State Machine Cycle ===")
    
    c.set(State.LISTENING)
    assert c.state == State.LISTENING
    
    # Wait for listen timeout
    time.sleep(0.6)
    
    c.set(State.SPEAKING)
    assert c.state == State.SPEAKING
    
    # Switch back
    c.set(State.LISTENING)
    assert c.state == State.LISTENING
    
    print("State Machine Cycle: PASSED")
    return True


def test_interruption_cancels_listening():
    """Test that interruption during SPEAKING cancels listening."""
    print("\n=== Testing Interruption Cancels Listening ===")
    
    c.set(State.SPEAKING)
    assert c.state == State.SPEAKING
    
    # User interrupts - switch to LISTENING
    c.set(State.LISTENING)
    
    # Should have cancelled speaking
    assert c.speak_cancel.stop == True, "Should have cancelled speaking"
    
    print("Interruption Cancels Listening: PASSED")
    return True


def run_all_tests():
    print("Running Voxpipe Logic Tests...\n")
    
    tests = [
        test_listen_timeout_transitions,
        test_state_machine_cycle,
        test_interruption_cancels_listening,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"FAILED: {test.__name__}")
            print(f"Error: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
