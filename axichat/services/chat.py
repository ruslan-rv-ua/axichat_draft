from pathlib import Path

import msgspec
from data_models import ChatData, ChatMessage

CHATS_DIR = "chats"


class Chat:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data = msgspec.json.decode(file_path.read_bytes(), type=ChatData)

    def save(self):
        self.file_path.write_bytes(msgspec.json.encode(self.data))

    @property
    def name(self):
        return self.data.name

    @property
    def messages(self):
        return self.data.messages

    def rename(self, new_name: str):
        file_path = self.file_path.parent / f"{new_name}.json"
        if file_path.exists():
            raise ValueError(f"File already exists: {file_path}")
        self.file_path.rename(file_path)
        self.data.name = new_name
        self.save()

    @classmethod
    def create(cls, file_path: Path, preset_name: str):
        if file_path.exists():
            raise ValueError("File already exists")
        data = ChatData(name=file_path.stem, preset_name=preset_name)
        file_path.write_bytes(msgspec.json.encode(data))
        return cls(file_path)

    def add_message(self, chat_message: ChatMessage):
        self.data.messages.append(chat_message)
        self.save()


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
        self.data = []
        for file in self.chats_dir.glob("*.json"):
            self.data.append(Chat(file))
        self.data = [Chat(file) for file in self.chats_dir.glob("*.json")]

    def get(self, name: str) -> Chat | None:
        for chat in self.data:
            if chat.name == name:
                return chat
        return None

    def create(self, chat_name: str, preset_name: str) -> Chat:
        file_path = self.chats_dir / f"{chat_name}.json"
        chat = Chat.create(file_path, preset_name)
        self.update()
        return chat

    def delete(self, chat_name: str):
        chat = self.get(chat_name)
        if chat is not None:
            chat.file_path.unlink()
            self.update()

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)
