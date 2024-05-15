import wx
from services.preset import Presets


class PresetsDialog(wx.Dialog):
    def __init__(self, parent, presets: Presets, title: str):
        super().__init__(parent, title=title)

        self.presets = presets

        self.init_ui()
        self.update_presets_list()

    def init_ui(self):
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # List with preset names
        self.preset_list = wx.ListBox(panel, style=wx.LB_SINGLE)
        main_sizer.Add(self.preset_list, 1, wx.EXPAND | wx.ALL, 5)

        # Separator
        main_sizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.ALL, 5)

        # "OK" and "Cancel" buttons
        button_sizer = wx.StdDialogButtonSizer()
        ok_button = wx.Button(panel, wx.ID_OK)
        ok_button.SetDefault()
        button_sizer.AddButton(ok_button)
        cancel_button = wx.Button(panel, wx.ID_CANCEL)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()

        main_sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        panel.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def get_selected_preset_name(self):
        return self.preset_list.GetStringSelection()

    def update_presets_list(self):
        self.preset_list.Clear()
        for preset in self.presets:
            self.preset_list.Append(preset.name)
