"""
Test and Debug file for Voxpipe

Run this to verify everything works:
    .venv\\Scripts\\python.exe test_debug.py
"""

import sys
import time
import threading
from controller import Controller, State, CancelToken


def test_cancel_token():
    """Test that CancelToken works correctly."""
    print("=== Testing CancelToken ===")
    
    token = CancelToken()
    assert token.stop == False, "Initial state should be False"
    
    token.cancel()
    assert token.stop == True, "After cancel(), should be True"
    
    print("CancelToken: PASSED")
    return True


def test_state_enum():
    """Test that State enum has all expected values."""
    print("\n=== Testing State Enum ===")
    
    assert State.IDLE.value == 0
    assert State.LISTENING.value == 1
    assert State.SPEAKING.value == 2
    
    print("State Enum: PASSED")
    return True


def test_controller_initial_state():
    """Test that controller starts in IDLE state."""
    print("\n=== Testing Controller Initial State ===")
    
    c = Controller()
    assert c.state == State.IDLE, "Should start in IDLE"
    assert c.listen_cancel.stop == False
    assert c.speak_cancel.stop == False
    
    print("Controller Initial State: PASSED")
    return True


def test_state_transitions():
    """Test that state transitions work correctly."""
    print("\n=== Testing State Transitions ===")
    
    c = Controller()
    
    # Initial state
    assert c.state == State.IDLE
    
    # Switch to LISTENING
    c.set(State.LISTENING)
    assert c.state == State.LISTENING
    
    # Switch to SPEAKING (should cancel listening)
    c.set(State.SPEAKING)
    assert c.state == State.SPEAKING
    assert c.listen_cancel.stop == True, "Should cancel listening"
    
    # Switch back to LISTENING (should cancel speaking)
    c.set(State.LISTENING)
    assert c.state == State.LISTENING
    assert c.speak_cancel.stop == True, "Should cancel speaking"
    
    print("State Transitions: PASSED")
    return True


def test_cancellation_prevents_overlap():
    """Test that starting one mode cancels the other."""
    print("\n=== Testing Cancellation Prevents Overlap ===")
    
    c = Controller()
    
    # Start listening
    c.set(State.LISTENING)
    assert c.state == State.LISTENING
    
    # Now speak - should cancel listening
    c.set(State.SPEAKING)
    assert c.listen_cancel.stop == True, "Should have cancelled listening"
    
    # Start listening again - should cancel speaking
    c.set(State.LISTENING)
    assert c.speak_cancel.stop == True, "Should have cancelled speaking"
    
    print("Cancellation Prevents Overlap: PASSED")
    return True


def test_listening_loop():
    """Test the listening loop with cancellation."""
    print("\n=== Testing Listening Loop ===")
    
    c = Controller()
    c.set(State.LISTENING)
    
    # Simulate listening for a bit
    count = 0
    max_count = 10
    while count < max_count and not c.listen_cancel.stop:
        time.sleep(0.1)
        count += 1
    
    # Now cancel it
    c.set(State.SPEAKING)
    assert c.listen_cancel.stop == True
    
    print("Listening Loop: PASSED")
    return True


def test_full_demo_cycle():
    """Test a full cycle: listen -> speak -> listen."""
    print("\n=== Testing Full Demo Cycle ===")
    
    c = Controller()
    
    # Start listening
    c.set(State.LISTENING)
    assert c.state == State.LISTENING
    time.sleep(0.5)
    
    # Switch to speaking
    c.set(State.SPEAKING)
    assert c.state == State.SPEAKING
    assert c.listen_cancel.stop == True
    time.sleep(0.5)
    
    # Switch back to listening
    c.set(State.LISTENING)
    assert c.state == State.LISTENING
    assert c.speak_cancel.stop == True
    
    print("Full Demo Cycle: PASSED")
    return True


def run_all_tests():
    """Run all tests."""
    print("Starting Voxpipe Tests...\n")
    
    tests = [
        test_cancel_token,
        test_state_enum,
        test_controller_initial_state,
        test_state_transitions,
        test_cancellation_prevents_overlap,
        test_listening_loop,
        test_full_demo_cycle,
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
    
    if failed == 0:
        print("\nAll tests passed! Voxpipe infrastructure is working.")
    else:
        print("\nSome tests failed. Check the output above.")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
