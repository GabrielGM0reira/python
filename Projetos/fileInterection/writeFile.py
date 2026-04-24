import json
import csv

employees = [
    {"name": "John Doe", "age": 30, "department": "Sales"},
    {"name": "Jane Smith", "age": 25, "department": "Marketing"},
    {"name": "Emily Davis", "age": 35, "department": "HR"},
]

file_path_json = "C:/Users/Usuario/Desktop/employees.json"

try:
    with open(file_path_json, 'w', newline='') as json_file:
        json.dump(employees, json_file, indent=4)
    print(f"Data successfully written to {file_path_json}")
except FileExistsError:
    print(f"Error: The file {file_path_json} already exists.")