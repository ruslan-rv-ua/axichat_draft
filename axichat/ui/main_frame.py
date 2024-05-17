from datetime import datetime
from pathlib import Path

import wx
from data_types import Chat, ChatMessage
from services import Chats, Presets, Providers
from thinker import EVT_RESPONSE_RECEIVED, Thinker
from ui.presets_dialog import PresetsDialog


def _(string: str) -> str:
    return string


class MainFrame(wx.Frame):
    def __init__(self, data_dir: Path):
        super().__init__(None, title="Axy Chat 2")

        self.data_dir = data_dir
        self.providers = Providers(data_dir=data_dir)
        self.presets = Presets(data_dir=data_dir)
        self.chats = Chats(data_dir=data_dir)

        self.current_chat: Chat | None = None

        self.init_ui()
        self.init_menu_bar()
        self.init_status_bar()

        self.Maximize()
        self.update_chat_log()
        self.Show()

    def init_ui(self):
        panel = wx.Panel(self)

        self.chat_log = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.input_box = wx.TextCtrl(
            panel,
            style=wx.TE_PROCESS_ENTER | wx.TE_MULTILINE | wx.TE_RICH | wx.TE_READONLY,
        )

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.chat_log, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.input_box, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(sizer)

        self.input_box.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(EVT_RESPONSE_RECEIVED, self.OnResponseRecieved)

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

    def on_close(self, event):
        self.Destroy()

    def OnEnter(self, event):
        if self.current_chat is None:
            return
        text = self.input_box.GetValue().strip()
        self.current_chat.messages.append(ChatMessage(role="user", content=text))
        Thinker(self).start()
        self.update_chat_log(focus_item_index=-1)
        self.input_box.Clear()

    def OnResponseRecieved(self, event):
        if event.error:
            # show error message
            wx.MessageBox(
                message=str(event.response),
                caption="Error",
                style=wx.ICON_ERROR,
                parent=self,
            )
            return

        response = event.response
        if self.current_chat is None:
            return
        self.current_chat.messages.append(
            ChatMessage(role="assistant", content=response.choices[0].message.content)
        )
        self.update_chat_log(focus_item_index=-1)

    def OnRequestSent(self, event):
        print("Request sent")

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

        chat_id = f"{datetime.now():%Y-%m-%d_%H-%M-%S}"
        self.current_chat = self.chats.create(
            id=chat_id, preset=self.presets.get(preset_name)
        )
        self.update_chat_log(focus_item_index=None)
        self.input_box.SetFocus()
        self.input_box.SetEditable(True)

    def on_menu_exit(self, event):
        self.Close()

    ######################################################################
    # Other
    ######################################################################

    def update_chat_log(self, focus_item_index: int | None = None):
        self.chat_log.Clear()
        if self.current_chat is None:
            self.chat_log.Append(_("There is no chat. Create new or open one."))
            self.chat_log.SetFocus()
            self.chat_log.SetSelection(0)
            return
        if len(self.current_chat.messages) == 0:
            self.chat_log.Append(_("There are no messages in the chat yet."))
            self.chat_log.SetFocus()
            self.chat_log.SetSelection(0)
        for message in self.current_chat.messages:
            self.chat_log.Append(f"{message.role}: {message.content}")
        if focus_item_index is None:
            return
        self.chat_log.SetFocus()
        if focus_item_index < 0:
            focus_item_index = self.chat_log.GetCount() + focus_item_index
        self.chat_log.SetSelection(focus_item_index)
