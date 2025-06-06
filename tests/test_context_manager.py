"""
Test suite for ContextManager energy detection.

Tests the 10 scenarios specified in work request #001 plus edge cases
to ensure accurate energy level detection.
"""

from context_manager import ContextManager


def test_context_manager():
    """Run all test scenarios for ContextManager."""
    
    cm = ContextManager()
    
    # Test scenarios from work request #001
    test_cases = [
        # High Energy Examples
        {
            "text": "I'm pumped up and ready to build something ambitious today!",
            "expected": "high",
            "description": "High energy - enthusiasm + action + exclamation"
        },
        {
            "text": "Let's tackle something challenging and complex!",
            "expected": "high", 
            "description": "High energy - action-oriented + challenging"
        },
        {
            "text": "I'm feeling motivated and want to dive deep into this!",
            "expected": "high",
            "description": "High energy - motivation + action + exclamation"
        },
        
        # Medium Energy Examples
        {
            "text": "What should we work on today?",
            "expected": "medium",
            "description": "Medium energy - neutral question"
        },
        {
            "text": "I'm ready to get started on something.",
            "expected": "medium",
            "description": "Medium energy - moderate readiness"
        },
        {
            "text": "Let's see what we can accomplish.",
            "expected": "medium",
            "description": "Medium energy - neutral planning"
        },
        
        # Low Energy Examples
        {
            "text": "Not feeling super focused today, maybe something small?",
            "expected": "low",
            "description": "Low energy - lack of focus + uncertainty + small scope"
        },
        {
            "text": "I'm a bit tired, what's a simple task we could do?",
            "expected": "low",
            "description": "Low energy - fatigue + simple task"
        },
        {
            "text": "Let me think... maybe something easy to start with?",
            "expected": "low",
            "description": "Low energy - hesitation + easy task + uncertainty"
        },
        
        # Edge Cases
        {
            "text": "",
            "expected": "medium",
            "description": "Edge case - empty string"
        }
    ]
    
    # Additional edge cases
    additional_tests = [
        {
            "text": "???",
            "expected": "medium",
            "description": "Edge case - unclear input"
        },
        {
            "text": "I'm excited but also tired",
            "expected": "medium",  # Mixed signals should reduce to medium
            "description": "Edge case - mixed signals"
        }
    ]
    
    # Combine all tests
    all_tests = test_cases + additional_tests
    
    print("=== ContextManager Test Results ===\n")
    
    passed = 0
    total = len(all_tests)
    
    for i, test in enumerate(all_tests, 1):
        result = cm.detect_energy_level(test["text"])
        
        success = result["energy"] == test["expected"]
        status = "✅ PASS" if success else "❌ FAIL"
        
        print(f"Test {i}: {status}")
        print(f"  Input: '{test['text']}'")
        print(f"  Expected: {test['expected']}")
        print(f"  Got: {result['energy']} (confidence: {result['confidence']:.2f})")
        print(f"  Reasoning: {result['reasoning']}")
        print(f"  Description: {test['description']}")
        print()
        
        if success:
            passed += 1
    
    print(f"=== SUMMARY ===")
    print(f"Passed: {passed}/{total} ({passed/total*100:.1f}%)")
    print(f"Required: 9/10 obvious cases (90%)")
    print(f"Status: {'✅ MEETS REQUIREMENT' if passed >= 9 else '❌ NEEDS IMPROVEMENT'}")
    
    return passed >= 9


def test_error_handling():
    """Test error handling scenarios."""
    
    cm = ContextManager()
    
    print("\n=== Error Handling Tests ===\n")
    
    error_tests = [
        {"text": None, "description": "None input"},
        {"text": "   ", "description": "Whitespace only"},
        {"text": "!@#$%^&*()", "description": "Special characters only"},
        {"text": "A" * 1000, "description": "Very long input"},
    ]
    
    for i, test in enumerate(error_tests, 1):
        try:
            result = cm.detect_energy_level(test["text"])
            print(f"Error Test {i}: ✅ HANDLED")
            print(f"  Input: {test['description']}")
            print(f"  Result: {result['energy']} (confidence: {result['confidence']:.2f})")
            print(f"  Reasoning: {result['reasoning']}")
        except Exception as e:
            print(f"Error Test {i}: ❌ EXCEPTION")
            print(f"  Input: {test['description']}")
            print(f"  Error: {str(e)}")
        print()


if __name__ == "__main__":
    print("Testing ContextManager...")
    
    # Run main tests
    main_success = test_context_manager()
    
    # Run error handling tests
    test_error_handling()
    
    print(f"\n=== FINAL RESULT ===")
    print(f"Main tests: {'✅ PASSED' if main_success else '❌ FAILED'}")
    print("Ready for Checkpoint 1!" if main_success else "Needs refinement before Checkpoint 1")