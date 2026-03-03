"""
Test Race Condition Arbiter - User always wins
"""
import time
import sys
sys.path.insert(0, '.')
from controller import Controller, State

def test_queue_speech():
    """Test that speech can be queued."""
    print("=== Testing Queue Speech ===")
    
    c = Controller()
    
    assert c.has_pending_speech() == False, "Queue should be empty initially"
    
    c.queue_speech("Hello there")
    assert c.has_pending_speech() == True, "Queue should have one item"
    assert c.get_next_speech() == "Hello there", "Should return queued speech"
    assert c.has_pending_speech() == False, "Queue should be empty after getting"
    
    print("Queue Speech: PASSED")
    return True


def test_multiple_speeches():
    """Test multiple speeches can be queued."""
    print("\n=== Testing Multiple Speeches ===")
    
    c = Controller()
    
    c.queue_speech("First")
    c.queue_speech("Second")
    c.queue_speech("Third")
    
    assert c.get_next_speech() == "First"
    assert c.get_next_speech() == "Second"
    assert c.get_next_speech() == "Third"
    assert c.get_next_speech() == None, "Should return None when empty"
    
    print("Multiple Speeches: PASSED")
    return True


def test_user_wins_interruption():
    """Test that user interrupting queues app speech (user wins)."""
    print("\n=== Testing User Wins Interruption ===")
    
    c = Controller()
    
    # App is speaking
    c.set(State.SPEAKING)
    assert c.state == State.SPEAKING
    
    # User interrupts - app queues its speech
    c.queue_speech("I was going to say this")
    c.set(State.LISTENING)
    
    assert c.state == State.LISTENING
    assert c.speak_cancel.stop == True, "Speaking should be cancelled"
    assert c.has_pending_speech() == True, "Speech should be queued"
    
    print("User Wins Interruption: PASSED")
    return True


def test_pending_speech_after_user_finishes():
    """Test that queued speech is processed after user finishes."""
    print("\n=== Testing Pending Speech After User Finishes ===")
    
    c = Controller()
    
    # User interrupted - speech queued
    c.queue_speech("Hello after you finish")
    c.set(State.LISTENING)
    
    # User finished, switch to SPEAKING
    c.set(State.SPEAKING)
    
    # TTS worker would call get_next_speech()
    speech = c.get_next_speech()
    assert speech == "Hello after you finish"
    
    print("Pending Speech After User Finishes: PASSED")
    return True


def test_user_speaking_flag():
    """Test tracking when user is speaking."""
    print("\n=== Testing User Speaking Flag ===")
    
    c = Controller()
    
    c.user_is_speaking = True
    assert c.user_is_speaking == True
    
    c.user_is_speaking = False
    assert c.user_is_speaking == False
    
    print("User Speaking Flag: PASSED")
    return True


def test_race_condition_scenario():
    """Full scenario: app speaking -> user interrupts -> user finishes -> app resumes."""
    print("\n=== Testing Race Condition Full Scenario ===")
    
    c = Controller()
    
    # 1. App starts speaking
    c.set(State.SPEAKING)
    assert c.state == State.SPEAKING
    
    # 2. User interrupts (volume detected) - USER WINS
    print("  -> User interrupts!")
    c.queue_speech("App response that was interrupted")
    c.set(State.LISTENING)
    assert c.state == State.LISTENING
    assert c.has_pending_speech() == True, "Speech should be queued"
    
    # 3. User finishes speaking (LISTENING timeout)
    time.sleep(0.1)
    
    # 4. Switch back to SPEAKING
    c.set(State.SPEAKING)
    assert c.state == State.SPEAKING
    
    # 5. Get queued speech
    speech = c.get_next_speech()
    assert speech == "App response that was interrupted"
    assert c.has_pending_speech() == False, "Queue should be empty"
    
    print("Race Condition Full Scenario: PASSED")
    return True


def run_all_tests():
    print("Running Race Condition Arbiter Tests...\n")
    
    tests = [
        test_queue_speech,
        test_multiple_speeches,
        test_user_wins_interruption,
        test_pending_speech_after_user_finishes,
        test_user_speaking_flag,
        test_race_condition_scenario,
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
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*50)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
