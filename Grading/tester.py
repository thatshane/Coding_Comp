import os
import subprocess

directory = r"C:\Temp\Inputs"
files = os.listdir(directory)

results_dict = {
    '1_single_num.txt': 10,
    '2_single_bool.txt': "True",
    '3_simple_add.txt': 2,
    '4_simple_subtract.txt': 0,
    '5_simple_sum.txt': 6,
    '6_simple_if.txt': 15,
    '7_nested_if.txt': 16,
    '8_if__equal_example.txt': "False",
    '9_nested_add.txt': 9,
    'X_complex_sum_and_if.txt': 23
}

script_command = r"python C:\Users\User\Documents\solution.py"

print(f"{'Filename' : <25}{'Expexted' : ^25}{'Actual' : ^25}")

for file in files:
    current_file = os.path.join(directory, file)
    output = subprocess.check_output(f"{script_command} {current_file}", encoding='UTF-8').strip()
    print(f"{file : <25}{output : ^25}{results_dict[file] : ^25}")