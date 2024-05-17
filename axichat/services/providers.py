from pathlib import Path

from data_types import Provider

PROVIDERS_DIR = "providers"


class Providers:
    def __init__(self, data_dir: Path):
        self.providers_dir = data_dir / PROVIDERS_DIR
        self.providers_dir.mkdir(parents=True, exist_ok=True)
        self.update()

    def update(self):
        self.data: list[Provider] = [
            Provider.load(file_path) for file_path in self.providers_dir.glob("*.json")
        ]

    def get(self, id: str) -> Provider:
        for provider in self.data:
            if provider.id == id:
                return provider
        raise ValueError(f"Provider not found: {id}")

    def ids_list(self):
        return [provider.id for provider in self.data]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)
