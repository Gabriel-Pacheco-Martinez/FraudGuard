import json

class Writer:
    def __init__(self, RESULTS_FILE_PATH: str):
        self.results_file_path = RESULTS_FILE_PATH
        with open(self.results_file_path, "w") as f:
            json.dump([], f)