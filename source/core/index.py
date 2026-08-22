import json
from pathlib import Path

class Index:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.index_file = self.repo_path / ".minigit" / "index.json"
        self.entries = set()

    def load(self):
        if self.index_file.exists():
            with open(self.index_file, "r", encoding="utf-8") as f:
                self.entries = set(json.load(f))
        else:
            self.entries = set()

    def add(self, filepath: str):
        clean_path = str(Path(filepath).as_posix())
        self.entries.add(clean_path)
        self.save()

    def save(self):
        self.index_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(sorted(list(self.entries)), f, indent=4)

    def remove(self, filepath: str):
        clean_path = str(Path(filepath).as_posix())
        if clean_path in self.entries:
            self.entries.remove(clean_path)
            self.save()