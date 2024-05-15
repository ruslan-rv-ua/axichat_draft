import os
from pathlib import Path

import msgspec
from data_models import PresetData

PRESETS_DIR = "presets"


class Preset:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data = msgspec.json.decode(file_path.read_bytes(), type=PresetData)

    def save(self):
        self.file_path.write_bytes(msgspec.json.encode(self.data))

    @property
    def name(self):
        return self.data.name

    @property
    def api_key(self):
        key = self.data.api_key
        if key.startswith("%") and key.endswith("%"):
            env_var = key[1:-1]
            key = os.environ.get(env_var)
            if key is None:
                raise ValueError(f"Environment variable {env_var} is not set.")
        return key

    @classmethod
    def create(cls, file_path: Path, **kwargs):
        if file_path.exists():
            raise ValueError("File already exists")
        data = PresetData(**kwargs)
        file_path.write_bytes(msgspec.json.encode(data))
        return cls(file_path)


class Presets:
    def __init__(self, data_dir: Path):
        self.presets_dir = data_dir / PRESETS_DIR
        self.presets_dir.mkdir(parents=True, exist_ok=True)

    def update(self) -> None:
        self.data = [Preset(file_path) for file_path in self.presets_dir.glob("*.json")]

    def get(self, name: str) -> Preset | None:
        for preset in self.data:
            if preset.data.name == name:
                return preset
        return None

    def create(self, name: str, **kwargs):
        file_path = self.presets_dir / f"{name}.json"
        if file_path.exists():
            raise ValueError(f"File already exists: {file_path}")
        preset = Preset.create(file_path, **kwargs)
        self.update()
        return preset

    def delete(self, name: str):
        preset = self.get(name)
        if preset is not None:
            preset.file_path.unlink()
            self.update()

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)
