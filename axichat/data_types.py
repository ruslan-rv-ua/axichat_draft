from enum import StrEnum

from config_abc import ConfigABC
from msgspec import Struct


class ProviderType(StrEnum):
    OPENAI = "openai"
    GPT4FREE_OPENAI = "gpt4free_openai"


class Model(Struct):
    id: str
    description: str = ""
    modality: str | None = None
    tokenizer: str | None = None
    instruct_type: str | None = None
    object: str = "model"
    owned_by: str | None = None
    max_tokens: int | None = None
    price_prompt: float | None = None
    price_completion: float | None = None
    price_images: float | None = None
    price_request: float | None = None


class Provider(ConfigABC):
    id: str
    type: ProviderType
    base_url: str
    models: list[Model]

    description: str = ""
    homepage_url: str | None = None
    get_api_key_url: str | None = None


class Preset(ConfigABC):
    id: str
    provider_id: str
    model_id: str
    api_key: str
    system_prompt: str = ""
    max_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 1
    n: int = 1


class ChatMessage(Struct):
    role: str
    content: str


class Chat(ConfigABC):
    id: str
    preset: Preset
    messages: list[ChatMessage] = []
