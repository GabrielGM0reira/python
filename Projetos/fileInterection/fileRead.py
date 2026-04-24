# python reading files (.txt, .json, .csv, .xlsx, .xml, .html, .pdf, .docx, .pptx)

import os
import json

file_path = 'data.json'

try:
    with open(file_path, 'r') as file:
        data = json.load(file)
        print(data)
except FileNotFoundError:
    print("File not found.")
except json.JSONDecodeError:
    print("Invalid JSON format.")