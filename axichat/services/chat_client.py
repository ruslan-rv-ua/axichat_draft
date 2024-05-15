from data_models import ChatMessage, ProviderData
from openai import OpenAI
from services.chat import Chat
from services.preset import Preset


class ChatClient:
    def __init__(self, chat: Chat, preset: Preset, provider: ProviderData):
        self.chat = chat
        self.preset = preset
        self.provider = provider

        self.client = OpenAI(api_key=preset.api_key, base_url=provider.base_url)

    def send_request(self):
        messages = [{"role": m.role, "content": m.content} for m in self.chat.messages]
        response = self.client.chat.completions.create(
            model=self.preset.data.model, messages=messages
        )
        reply = response.choices[0].message.content
        print(">>>", reply)
        return reply
