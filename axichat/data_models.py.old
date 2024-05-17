from msgspec import Struct


class ProviderData(Struct):
    name: str
    base_url: str
    openai_compatible: bool
    homepage_url: str
    get_api_key_url: str


class PresetData(Struct):
    name: str
    provider_name: str
    api_key: str
    model: str
    system_prompt: str = ""
    max_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 1
    n: int = 1


class PricingData(Struct):
    prompt: float | None = None
    completion: float | None = None
    images: float | None = None
    request: float | None = None


class ModelData(Struct):
    id: str
    pricing: PricingData
    name: str = ""
    description: str = ""
    modality: str | None = None
    tokenizer: str | None = None
    instruct_type: str | None = None
    object: str = "model"
    owned_by: str | None = None
    max_tokens: int | None = None


class ChatMessage(Struct):
    role: str
    content: str


class ChatData(Struct):
    name: str
    preset_name: str
    messages: list[ChatMessage] = []
