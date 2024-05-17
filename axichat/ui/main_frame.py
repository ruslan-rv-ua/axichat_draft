from datetime import datetime
from pathlib import Path

import wx
from data_models import ChatMessage
from services.chat import Chat, Chats
from services.chat_client import ChatClient
from services.preset import Presets
from services.providers import Providers
from ui.presets_dialog import PresetsDialog


class MainFrame(wx.Frame):
    def __init__(self, data_dir: Path):
        super().__init__(None, title="Axy Chat 2")

        self.data_dir = data_dir
        self.providers = Providers(data_dir=data_dir)
        self.presets = Presets(data_dir=data_dir)
        self.chats = Chats(data_dir=data_dir)

        self.init_ui()
        self.init_menu_bar()
        self.Maximize()
        self.Show()

    def init_ui(self):
        panel = wx.Panel(self)

        self.chat_log = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.input_box = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER | wx.TE_MULTILINE)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.chat_log, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.input_box, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(sizer)

        self.input_box.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)

    def init_menu_bar(self):
        menu_bar = wx.MenuBar()

        chat_menu = wx.Menu()
        menu_item = chat_menu.Append(wx.ID_NEW, "&New Chat\tCtrl-N")
        self.Bind(wx.EVT_MENU, self.on_menu_new_chat, menu_item)
        menu_item = chat_menu.Append(wx.ID_EXIT, "&Exit")
        self.Bind(wx.EVT_MENU, self.on_menu_exit, menu_item)

        menu_bar.Append(chat_menu, "&Chat")

        self.SetMenuBar(menu_bar)

    def init_status_bar(self):
        pass

    ######################################################################
    # Event handlers
    ######################################################################

    def OnEnter(self, event):
        text = self.input_box.GetValue().strip()
        self.input_box.Clear()
        self.chat_client.chat.add_message(
            chat_message=ChatMessage(role="user", content=text)
        )
        self.update_chat_log(self.chat_client.chat)
        self.chat_log.SetFocus()
        self.chat_log.SetSelection(self.chat_log.GetCount() - 1)

        # reply = wx.CallAfter(self.chat_client.send_request)
        reply = self.chat_client.send_request()
        
        self.chat_client.chat.add_message(
            chat_message=ChatMessage(role="assistant", content=reply)
        )
        self.update_chat_log(self.chat_client.chat)
        self.chat_log.SetFocus()
        self.chat_log.SetSelection(self.chat_log.GetCount() - 1)

    ######################################################################
    # Menu event handlers
    ######################################################################

    def on_menu_new_chat(self, event):
        self.presets.update()
        if len(self.presets) == 0:
            wx.MessageBox(
                message="No presets found. Please create a new one first.",
                caption="No presets found",
                style=wx.ICON_ERROR,
            )
            return
        dlg = PresetsDialog(
            self, presets=self.presets, title="Select Preset for New Chat"
        )
        if dlg.ShowModal() == wx.ID_OK:
            preset_name = dlg.get_selected_preset_name()
        dlg.Destroy()

        chat_name = f"{datetime.now():%Y-%m-%d_%H-%M-%S}"
        chat = self.chats.create(chat_name=chat_name, preset_name=preset_name)
        self.chat_client = self.get_chat_client(chat)
        self.update_chat_log(chat)

    def on_menu_exit(self, event):
        self.Close()

    ######################################################################
    # Other
    ######################################################################

    def update_chat_log(self, chat: Chat):
        self.chat_log.Clear()
        for message in chat.messages:
            self.chat_log.Append(f"{message.role}: {message.content}")

    def get_chat_client(self, chat: Chat):
        preset = self.presets.get(chat.data.preset_name)
        if preset is None:
            raise ValueError(f"Preset not found: {chat.data.preset_name}")
        provider = self.providers.get(preset.data.provider_name)
        if provider is None:
            raise ValueError(f"Provider not found: {preset.name}")
        return ChatClient(chat=chat, preset=preset, provider=provider)
