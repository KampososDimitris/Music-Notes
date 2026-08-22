import tkinter as tk
from tkinter import ttk

MIN_X = 860
MIN_Y = 480


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry = f"{MIN_X}x{MIN_Y}"
        self.minsize(MIN_X, MIN_Y)
        self.title('Music Notes')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.build_window()

        self.update()
        self.mainloop()

    def build_window(self):
        """
        This will be used to create all the components of the main window.
        This is done by creating a MenuFrame instance, that in turn 
        is calling the ContentFrame once for each radio button option.
        The content frames are then controlled by the menu frame, with the radio buttons.
        """
        MenuFrame(self).grid(row=0, column=0, sticky="ew")


class MenuFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # Instance variables
        self.container = container
        self.frames = {}

        # Styling
        self['border'] = 1.0
        self['relief'] = 'sunken'

        # Components in frame
        self.columnconfigure(2, weight=3)

        tk.Label(self, text="Note").grid(row=0, column=0, padx=5, pady=5)
        ttk.Combobox(self).grid(row=0, column=1, pady=5)

        self.selected_option = tk.StringVar()

        radio_btn_frame = tk.Frame(self)
        radio_btn_frame.grid(row=0, column=2, sticky='e')

        ttk.Radiobutton(
            radio_btn_frame,
            text = "Chords",
            value="chords",
            variable=self.selected_option,
            command=self.set_content
        ).grid(row=0, column=0, padx=5, pady=5)

        ttk.Radiobutton(
            radio_btn_frame,
            text = "Scales",
            value="scales",
            variable=self.selected_option,
            command=self.set_content
        ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Radiobutton(
            radio_btn_frame,
            text = "Circle of 5ths",
            value="chords",
            variable=self.selected_option,
            command=self.set_content
        ).grid(row=0, column=2, padx=5, pady=5)

        # TODO Check how to retrive the correct frame from the class' frame dict. By index or by text? Get text from radio btns or fixed?

    
    def set_content(self):
        frame = self.frames[self.selected_option.get()]
        frame.tkraise()


# TODO Rename GUI folder and main_window module, while keeping track in git.
# TODO Create ContentFrame class, that will contain all the components of the app's content.