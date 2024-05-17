from pathlib import Path

from data_types import Preset

PRESETS_DIR = "presets"


class Presets:
    def __init__(self, data_dir: Path):
        self.presets_dir = data_dir / PRESETS_DIR
        self.presets_dir.mkdir(parents=True, exist_ok=True)
        self.update()

    def update(self) -> None:
        self.data = [
            Preset.load(file_path) for file_path in self.presets_dir.glob("*.json")
        ]

    def get(self, id: str) -> Preset:
        for preset in self.data:
            if preset.id == id:
                return preset
        raise ValueError(f"Preset not found: {id}")

    def create(self, id: str, **kwargs):
        file_path = self.presets_dir / f"{id}.json"
        if file_path.exists():
            raise ValueError(f"Preset already exists: {id}")
        preset = Preset.create(file_path, **kwargs)
        self.update()
        return preset

    def delete(self, id: str):
        self.get(id).delete()
        self.update()

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)
