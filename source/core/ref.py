from pathlib import Path

class Head:
    def __init__(self, git_dir: str | Path):
        self.git_dir = Path(git_dir)

    def read_head(self):
        with open(self.git_dir,"r", encoding='utf-8') as archivo:
            contenido = archivo.read()
        return contenido

    def write_rama(self,breach: str):
        with open(self.git_dir, 'w', encoding='utf-8') as archivo:
            archivo.write(f"ref: refs/heads/{breach}")

    def write_head(self,data: str):
            with open(self.git_dir, 'w', encoding='utf-8') as archivo:
                archivo.write(f"{data}")