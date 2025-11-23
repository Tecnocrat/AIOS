"""Test file for E501 auto-fix validation"""

def very_long_function_name_that_exceeds_79_characters_limit_aaaaaaaaaaaaaa(param1, param2):
    """Function with E501 in signature"""
    return param1 + param2


# This is a very long comment that exceeds 79 characters and needs to be fixed by the autonomous monitor
x = 1
