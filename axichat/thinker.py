import os
import threading

import wx.lib.newevent
from data_types import Chat, Preset, Provider, ProviderType
from openai import OpenAI

ResponseReceivedEvent, EVT_RESPONSE_RECEIVED = wx.lib.newevent.NewEvent()


class Thinker(threading.Thread):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.chat: Chat = window.current_chat
        self.preset: Preset = self.chat.preset
        self.provider: Provider = self.window.providers.get(self.preset.provider_id)
        self.api_key = self.preset.api_key
        if self.api_key.startswith("%") and self.api_key.endswith("%"):
            self.api_key = os.environ.get(self.api_key[1:-1])
        self.model = self.preset.model_id

    def run(self):
        match self.provider.type:
            case ProviderType.OPENAI:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.provider.base_url,
                )
            case _:
                raise NotImplementedError(
                    f"Unsupported provider type: {self.provider.type}"
                )

        messages = [{"role": m.role, "content": m.content} for m in self.chat.messages]

        response = self.client.chat.completions.create(
            model=self.preset.model_id, messages=messages
        )

        wx.PostEvent(self.window, ResponseReceivedEvent(response=response))
