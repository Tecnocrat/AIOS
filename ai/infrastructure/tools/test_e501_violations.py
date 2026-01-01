#!/usr/bin/env python3
"""
Test file for hierarchical E501 pipeline testing.
Contains intentional E501 violations for validation.
"""

def
    test_function_with_very_long_parameter_list_that_exceeds_seventy_nine_characters(param1, param2, param3, param4):
    """Function with E501 violation in signature."""
    result =
    some_very_long_function_name_that_causes_line_length_issues(param1, param2, param3, param4)
    message = f"This is a very long string message that definitely exceeds the
    seventy-nine character limit for PEP 8 compliance"
    return result


class TestClass:
    """Test class with E501 violations."""
    
    def method_with_long_line(self):
        """Method with multiple E501 violations."""
        data = {"key1": "value1", "key2": "value2", "key3": "value3",
    "key4": "value4", "key5": "value5"}
        condition = (some_variable > 100 and another_variable < 200 and
    third_variable == "test" and fourth_variable != None)
        return data if condition else {}
