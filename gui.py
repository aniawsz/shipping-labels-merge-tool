import os.path
import wx

from pdf_utils import Position, generate_composite_pdf, save_pdf

class TestPanel(wx.Panel):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, *a, **kw)

class PositionChooser(wx.Panel):
    RECT_WIDTH = 40
    RECT_HEIGHT = 50
    MARGIN = 10

    COLOR_NEUTRAL = wx.Colour(200, 200, 255)
    COLOR_SELECTED = wx.Colour(120, 120, 255)

    def __init__(self, parent, size, *a, **kw):
        super().__init__(parent, *a, **kw)

        self._rect_selected = self._create_colored_rect(
            self.RECT_WIDTH,
            self.RECT_HEIGHT,
            self.COLOR_SELECTED,
        )
        self._rect_neutral = self._create_colored_rect(
            self.RECT_WIDTH,
            self.RECT_HEIGHT,
            self.COLOR_NEUTRAL,
        )

        is_initially_selected = True

        upper_left = wx.BitmapButton(
            parent=self,
            bitmap=self._rect_selected if is_initially_selected else self._rect_neutral,
            pos=(0, 0),
            size=(self.RECT_WIDTH, self.RECT_HEIGHT),
        )
        lower_left = wx.BitmapButton(
            parent=self,
            bitmap=self._rect_selected if is_initially_selected else self._rect_neutral,
            pos=(0, self.RECT_HEIGHT + self.MARGIN),
            size=(self.RECT_WIDTH, self.RECT_HEIGHT),
        )
        upper_right = wx.BitmapButton(
            parent=self,
            bitmap=self._rect_selected if is_initially_selected else self._rect_neutral,
            pos=(self.RECT_WIDTH + self.MARGIN, 0),
            size=(self.RECT_WIDTH, self.RECT_HEIGHT),
        )
        lower_right = wx.BitmapButton(
            parent=self,
            bitmap=self._rect_selected if is_initially_selected else self._rect_neutral,
            pos=(self.RECT_WIDTH + self.MARGIN, self.RECT_HEIGHT + self.MARGIN),
            size=(self.RECT_WIDTH, self.RECT_HEIGHT),
        )

        self._position_info = {
            Position.upper_left: {'button': upper_left, 'is_selected': is_initially_selected},
            Position.lower_left: {'button': lower_left, 'is_selected': is_initially_selected},
            Position.upper_right: {'button': upper_right, 'is_selected': is_initially_selected},
            Position.lower_right: {'button': lower_right, 'is_selected': is_initially_selected},
        }

        for info in self._position_info.values():
            info['button'].Bind(wx.EVT_BUTTON, self._toggle_select)

    @property
    def available_positions(self):
        return [
            position for position, info in self._position_info.items()
            if info['is_selected']
        ]

    def _create_colored_rect(self, width, height, color):
        r, g, b, a = color.Get(includeAlpha=True)
        bitmap = wx.Bitmap.FromRGBA(width, height, r, g, b, a)
        return bitmap

    def _get_button_position(self, button):
        for pos, info in self._position_info.items():
            if info['button'] == button:
                return pos

    def _toggle_select(self, event):
        button = event.EventObject
        position = self._get_button_position(button)
        is_selected = self._position_info[position]['is_selected']
        button.SetBitmap(self._rect_neutral if is_selected else self._rect_selected)
        self._position_info[position]['is_selected'] = not is_selected

class MainFrame(wx.Frame):
    def __init__(self, *a, **kw):
        self._selected_files = []
        self._filetype_wildcard = "PDF (*.pdf)|*.pdf"

        super().__init__(
            parent=None,
            title="PDF Merge Tool 2.0",
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
        composite_pdf = generate_composite_pdf(
            self._selected_files,
            self._position_chooser.available_positions,
        )

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

        self._position_chooser = PositionChooser(panel, size=wx.Size(100, 120))
        vsizer.Add(self._position_chooser, 0, wx.ALL | wx.EXPAND | wx.SHAPED, 5)

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
