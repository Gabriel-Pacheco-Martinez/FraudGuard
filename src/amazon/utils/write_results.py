import json

class Writer:
    def __init__(self, RESULTS_FILE_PATH: str):
        self.results_file_path = RESULTS_FILE_PATH

    def write_results(self, data: dict):
        with open(self.results_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)