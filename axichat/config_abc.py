from pathlib import Path

import msgspec

json_encoder = msgspec.json.Encoder()
json_decoder = msgspec.json.Decoder()


class ConfigABC(msgspec.Struct):
    _file_path: str

    def __post_init__(self):
        if self.__class__.__name__ == "ConfigABC":
            raise TypeError("ConfigABC is an abstract class and cannot be instantiated")
        Path(self._file_path).parent.mkdir(parents=True, exist_ok=True)
        self.save()

    def save(self):
        Path(self._file_path).write_bytes(json_encoder.encode(self))

    @classmethod
    def load(cls, file_path: str | Path):
        file_path = Path(file_path)
        return cls(**json_decoder.decode(file_path.read_bytes()))

    @classmethod
    def create(cls, file_path: str | Path, **kwargs):
        file_path = Path(file_path)
        return cls(_file_path=str(file_path.resolve()), **kwargs)
