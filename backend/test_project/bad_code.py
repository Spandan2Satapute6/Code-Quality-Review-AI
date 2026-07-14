# bad_code.py
import os
import hashlib

def calculate_complexity(n):
    # High cyclomatic complexity function
    result = 0
    if n > 0:
        if n % 2 == 0:
            for i in range(n):
                if i % 3 == 0:
                    result += i
                elif i % 4 == 0:
                    result -= i
                else:
                    result += 1
        else:
            for i in range(n):
                if i % 5 == 0:
                    result *= i
                elif i % 7 == 0:
                    result -= i
                else:
                    result += i
    else:
        result = -1
    return result

def insecure_function(user_input):
    # Bandit issue: Use of eval
    eval(user_input)

def hardcoded_password():
    # Bandit issue: Hardcoded password
    password = "supersecretpassword123"
    x = 10  # Pylint issue: unused variable
    return password
