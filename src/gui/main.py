import os

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from PIL import Image, ImageTk

from utils import resource_path

import theory.structures as st

X_AXIS = 800
Y_AXIS = 500
MENU_OPTIONS = ['Chords', 'Scales', 'Circle of Fifths']
N_OF_ITEMS_ROWS = 3

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry = f"{X_AXIS}x{Y_AXIS}"
        self.minsize(X_AXIS, Y_AXIS)
        self.maxsize(X_AXIS, Y_AXIS)
        self.title('Music Notes')
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.build_window()
        
        self.update()
        self.mainloop()

    def build_window(self):
        MenuFrame(self).grid(row=0, column=0, sticky="ew", padx=5, pady=5)


class MenuFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # Instance variables
        self.container = container
        self.frames = {}
        self.selected_option = tk.StringVar()
        self.selected_note = tk.StringVar()

        # Styling
        self['borderwidth'] = 1.0
        self['relief'] = 'sunken'

        # Components in frame
        self.columnconfigure(2, weight=3)

        tk.Label(self, text="Root").grid(row=0, column=0, padx=5, pady=5)

        notes_list = ttk.Combobox(self, textvariable=self.selected_note, state='readonly')
        notes_list['values'] = [note for note in st.roots]
        notes_list.grid(row=0, column=1, pady=5)
        notes_list.bind('<<ComboboxSelected>>', self.pass_note_to_chord_frames)

        radio_btn_frame = tk.Frame(self)
        radio_btn_frame.grid(row=0, column=2, sticky='e')

        for idx, option in enumerate(MENU_OPTIONS):
            ttk.Radiobutton(
                radio_btn_frame,
                text=option,
                value=option,
                variable=self.selected_option,
                command=self.set_content
            ).grid(row=0, column=idx, padx=5, pady=5)
        self.selected_option.set('')

        # Create one ContentFrame for each radio button option
        for option in MENU_OPTIONS:
            self.frames[option] = ContentFrame(container, option)
            self.frames[option].grid(row=1, column=0, sticky='nsew')
        self.frames['default'] = ContentFrame(container)
        self.frames['default'].grid(row=1, column=0, sticky='nsew')

    def set_content(self):
        frame = self.frames[self.selected_option.get()]
        frame.tkraise()

    def pass_note_to_chord_frames(self, *args):
        for child in self.master.winfo_children():
            for grandchild in child.winfo_children():
                try:
                    grandchild.current_note.set(self.selected_note.get())
                except:
                    pass


class ContentFrame(tk.Frame):
    def __init__(self, container, option='default'):
        super().__init__(container)

        # Instance variables
        self.container = container
        self.option = option

        # Styling
        self['borderwidth'] = 1.0
        self['relief'] = 'sunken'

        # Components in frame
        match self.option:
            case 'Chords':
                self.create_chord_frames()
            case 'Scales':
                self.create_scale_frames()
            case 'Circle of Fifths':
                self.create_cof_frame()
            case 'default':
                tk.Label(self, text="Welcome to Music Notes!\nChoose a note and mode to begin.")\
                    .pack(expand=True)
            case _:
                messagebox.showwarning('Warning', f'Invalid option: {self.option}.\nChoose a valid option from the menu.')

    def create_chord_frames(self):
        row = column = 0

        for variant in st.chord_variants:
            self.rowconfigure(row, weight=1)
            self.columnconfigure(column, weight=1)

            StructureFrame(
                self,
                self.option,
                variant,
                st.chord_variants[variant]['notation'],
                st.chord_variants[variant]['labels'],
            ).grid(row=row, column=column, sticky='nsew')

            column = column + 1 if column < N_OF_ITEMS_ROWS else 0
            if column == 0: row += 1

    def create_scale_frames(self):
        row = column = 0

        for scale in st.scales:
            self.rowconfigure(row, weight=1)
            self.columnconfigure(column, weight=1)

            StructureFrame(
                self,
                self.option,
                scale,
                st.scales[scale]['notation'],
                st.scales[scale]['labels'],
            ).grid(row=row, column=column, sticky='nsew')

            column = column + 1 if column < N_OF_ITEMS_ROWS else 0
            if column == 0: row += 1

    def create_cof_frame(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        CoFFrame(self).grid(sticky='nsew')


class StructureFrame(tk.Frame):
    def __init__(self, container, kind, structure_name, notation, labels):
        super().__init__(container)

        # Instance variables
        self.kind = kind
        self.structure_name = structure_name
        self.notation = notation
        self.labels = labels
        self.current_note = tk.StringVar()
        self.current_note.trace_add('write', self.update_structure_notes)
        self.structure_notes = tk.StringVar()

        # Styling
        self['borderwidth'] = 0.5
        self['relief'] = 'raised'

        # Components in frame
        self.columnconfigure(0, weight=1)

        tk.Label(self, text=f'{self.structure_name}{f'({self.notation})' if self.notation != '' else ''}', borderwidth=0.5, relief='groove')\
            .grid(sticky='ew')

        notes_label = ' - '.join(self.labels)
        tk.Label(self, text=notes_label).grid(sticky='ns')
        tk.Label(self, textvariable=self.structure_notes).grid(sticky='ns')

    def update_structure_notes(self, *args):
        try:
            tmp_notes = st.calculate_structure_notes(
                self.kind,
                self.current_note.get(),
                self.structure_name
            )
        except Exception as e:
            messagebox.showwarning('Warning', e)

        if tmp_notes:
            self.structure_notes.set(' - '.join(tmp_notes))


class CoFFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Components in frame
        img_path = resource_path('assets/img/circle_of_fifths_transparent.png')
        img = Image.open(img_path)
        img = img.resize((400, 360), Image.Resampling.LANCZOS)

        img_tk = ImageTk.PhotoImage(img)

        img_label = tk.Label(self, image=img_tk, anchor=tk.CENTER)
        img_label.image = img_tk
        img_label.grid(sticky='nsew')