from pathlib import Path

import wx
from ui.main_frame import MainFrame


class App(wx.App):
    def OnInit(self):
        data_dir = Path(__file__).parent.resolve() / "data"
        data_dir.mkdir(exist_ok=True)
        frame = MainFrame(data_dir=data_dir)
        frame.Show(True)
        return True


if __name__ == "__main__":
    app = App()
    app.MainLoop()
