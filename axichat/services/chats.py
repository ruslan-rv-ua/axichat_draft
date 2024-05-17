from pathlib import Path

from data_types import Chat, Preset

CHATS_DIR = "chats"


class Chats:
    def __init__(self, data_dir: Path):
        self.chats_dir = data_dir / CHATS_DIR
        self.chats_dir.mkdir(parents=True, exist_ok=True)
        self.update()

    def update(self) -> None:
        """
        Update the list of chats from the directory.

        Returns:
            None
        """
        self.data = [
            Chat.load(file_path) for file_path in self.chats_dir.glob("*.json")
        ]

    def get(self, id: str) -> Chat:
        for chat in self.data:
            if chat.id == id:
                return chat
        raise ValueError(f"Chat not found: {id}")

    def create(self, id: str, preset: Preset) -> Chat:
        file_path = self.chats_dir / f"{id}.json"
        chat = Chat.create(file_path, preset=preset)
        self.update()
        return chat

    def delete(self, id: str):
        self.get(id).delete()
        self.update()

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)
