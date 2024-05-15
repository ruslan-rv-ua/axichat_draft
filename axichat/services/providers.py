from pathlib import Path

import msgspec
from data_models import ProviderData

PROVIDERS_DIR = "providers"


class Providers:
    def __init__(self, data_dir: Path):
        self.providers_dir = data_dir / PROVIDERS_DIR
        self.providers_dir.mkdir(parents=True, exist_ok=True)
        self.update()

    def update(self):
        self.data: list[ProviderData] = [
            msgspec.json.decode(file_path.read_bytes(), type=ProviderData)
            for file_path in self.providers_dir.glob("*.json")
        ]

    def get(self, name: str) -> ProviderData | None:
        for provider in self.data:
            if provider.name == name:
                return provider
        return None

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)
