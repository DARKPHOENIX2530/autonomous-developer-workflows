"""
Sample target application containing bugs to demonstrate the autonomous verification script.
"""

def calculate_average(items):
    # Bug 1: Can trigger ZeroDivisionError if items is empty
    count = len(items)
    # Bug 2: Can trigger TypeError if strings are passed
    total = sum(items)
    return total / count

def test_suite():
    print("Executing unit tests...")
    
    # Test 1: Standard list
    assert calculate_average([10, 20, 30]) == 20.0, "Test 1 Failed"
    
    # Test 2: Empty list (Edge case)
    result = calculate_average([])
    assert result == 0.0, "Test 2 Failed on Empty List"

    print("All assertions passed!")

if __name__ == "__main__":
    test_suite()