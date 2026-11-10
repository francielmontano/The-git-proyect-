import json
from pathlib import Path

IGNORE_DIRS = {".git", "__pycache__", ".venv", "index.json", ".minigit"}

class Index:
    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path).resolve()
        self.index_file = self.repo_path / "index.json"
        self.entries: dict[str, dict[str, float | int]] = {}
        self.load()

    def load(self) -> None:
        """Carga el índice desde el disco si existe."""
        if self.index_file.exists():
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    self.entries = json.load(f)
            except json.JSONDecodeError:
                self.entries = {}
        else:
            self.entries = {}

    def save(self) -> None:
        """Guarda el diccionario de entradas ordenado en el disco."""
        self.index_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(dict(sorted(self.entries.items())), f, indent=4)

    def _should_ignore(self, path: Path) -> bool:
        """Verifica si la ruta debe ser ignorada."""
        return any(part in IGNORE_DIRS for part in path.parts)

    def _scan_workspace(self) -> dict[str, dict[str, float | int]]:
        """Escanea el proyecto actual y extrae los metadatos de los archivos válidos."""
        workspace_files = {}
        root = self.repo_path.parent
        for p in root.rglob("*"):
            if p.is_file() and not self._should_ignore(p.relative_to(root)):
                try:
                    stat = p.stat()
                    workspace_files[p.relative_to(root).as_posix()] = {
                        "size": stat.st_size,
                        "mtime": stat.st_mtime
                    }
                except FileNotFoundError:
                    pass
        return workspace_files

    def add(self, target_path: str = ".") -> None:
        """Añade archivos al índice y limpia automáticamente los que hayan sido eliminados."""
        self.load()

        status = self.get_status_report()
        for deleted_file in status.get("deleted", []):
            self.entries.pop(deleted_file, None)

        target = Path(target_path)
        root = self.repo_path.parent

        files = [target] if target.is_file() else [
            p for p in target.rglob("*") if p.is_file() and not self._should_ignore(p.relative_to(root))
        ]

        for file_path in files:
            try:
                stat = file_path.stat()
                rel_path = file_path.relative_to(root).as_posix()
                self.entries[rel_path] = {"size": stat.st_size, "mtime": stat.st_mtime}
            except FileNotFoundError:
                continue

        self.save()

    def remove(self, filepath: str) -> None:
        """Elimina una ruta específica del índice."""
        self.load()
        if (clean_path := Path(filepath).as_posix()) in self.entries:
            del self.entries[clean_path]
            self.save()

    def clear(self) -> None:
        """Vacía completamente el índice."""
        self.entries.clear()
        self.save()

    def get_status_report(self) -> dict[str, list[str]]:
        """Contrasta el disco actual con el índice y retorna un reporte de cambios."""
        self.load()
        workspace_files = self._scan_workspace()

        indexed_keys, workspace_keys = set(self.entries.keys()), set(workspace_files.keys())

        modified_files = [
            f for f in (indexed_keys & workspace_keys)
            if workspace_files[f] != self.entries[f]
        ]

        return {
            "new": sorted(workspace_keys - indexed_keys),
            "modified": sorted(modified_files),
            "deleted": sorted(indexed_keys - workspace_keys)
        }