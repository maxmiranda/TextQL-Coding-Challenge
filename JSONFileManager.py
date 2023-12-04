import json
import os

class JSONFileManager:
    def __init__(self):
         # Dictionary to keep track of files and their contents
        self.files = {}

    def import_file(self, file_path):
        # Check if file_path is valid
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            return

        # Read and store the file content
        with open(file_path, 'r') as file:
            file_content = json.load(file)
            file_name = file_path.replace(".json", "")
            self.files[file_name] = file_content
            # Give user feedback that file has been successfully imported
            print(f"File imported: {file_path}")

    def get_file_content(self, file_path):
        return self.files.get(file_path)

    def list_files(self):
        return list(self.files.keys())