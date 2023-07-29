import os.path
import wx

from pdf_utils import generate_composite_pdf, save_pdf

class MainFrame(wx.Frame):
    def __init__(self, *a, **kw):
        self._selected_files = []
        self._filetype_wildcard = "PDF (*.pdf)|*.pdf"

        super().__init__(
            parent=None,
            title="PDF Merge Tool",
            size=wx.Size(400,400),
            style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN,
        )
        self._create_widgets()

        self.Show()

    def _select_files(self, *a):
        with wx.FileDialog(
            self,
            "Select files",
            wildcard=self._filetype_wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE,
        ) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            self._selected_files = file_dialog.GetPaths()

            filenames = [os.path.split(path)[1] for path in self._selected_files]
            self._filename_label.SetValue(
                "\n".join([f"{i+1}. {fname}" for i, fname in enumerate(filenames)]),
            )
            self._generated_info.SetLabel("")

    def _generate(self, *a):
        composite_pdf = generate_composite_pdf(self._selected_files)

        with wx.FileDialog(
            self,
            "Save as",
            defaultFile="ShippingLabels.pdf",
            wildcard=self._filetype_wildcard,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        ) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            output_filepath = file_dialog.GetPath()
            try:
                save_pdf(composite_pdf, output_filepath)
            finally:
                output_filename = os.path.split(output_filepath)[1]
                self._generated_info.SetLabel(
                    f"Saved the combined labels as {output_filename}"
                )

    def _create_widgets(self):
        panel = wx.Panel(self)
        vsizer = wx.BoxSizer(wx.VERTICAL)

        open_button = wx.Button(panel, label="Select Files with Shipping Labels")
        open_button.Bind(wx.EVT_BUTTON, self._select_files)
        vsizer.Add(open_button, 0, wx.ALL | wx.CENTER, 5)

        self._filename_label = wx.TextCtrl(
            panel,
            size=wx.Size(50, 20),
            style=wx.TE_READONLY | wx.TE_MULTILINE,
        )
        vsizer.Add(self._filename_label, 0, wx.ALL | wx.EXPAND | wx.SHAPED, 5)

        generate_button = wx.Button(panel, label="Generate")
        generate_button.Bind(wx.EVT_BUTTON, self._generate)
        vsizer.Add(generate_button, 0, wx.ALL | wx.CENTER, 5)

        self._generated_info = wx.StaticText(panel)
        vsizer.Add(self._generated_info, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vsizer)

def run_gui():
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
