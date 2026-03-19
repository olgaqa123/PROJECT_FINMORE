import json
import os
 
def load_test_data(file_name):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "Tests", "data", file_name)
 
    with open(file_path, "r") as file:
        return json.load(file)