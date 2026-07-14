import zipfile
import os

os.makedirs("test_project", exist_ok=True)

code_content = """# bad_code.py
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
"""

with open("test_project/bad_code.py", "w") as f:
    f.write(code_content)

# Also write a simpler clean file to test multiple files
clean_code = """# clean_code.py
def add(a, b):
    return a + b
"""

with open("test_project/clean_code.py", "w") as f:
    f.write(clean_code)

with zipfile.ZipFile("test_project.zip", "w") as zip_ref:
    zip_ref.write("test_project/bad_code.py", "bad_code.py")
    zip_ref.write("test_project/clean_code.py", "clean_code.py")

print("Created test_project.zip successfully.")
