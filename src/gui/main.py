import tkinter as tk
from tkinter import ttk

import theory.chords as chords
import theory.scales as scales

MIN_X = 860
MIN_Y = 480
MENU_OPTIONS = ['Chords', 'Scales', 'Circle of Fifths']
N_OF_CHORDS_IN_ROW = 3


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
        MenuFrame(self).grid(row=0, column=0, sticky="ew", padx=5, pady=5)


class MenuFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # Instance variables
        self.container = container
        self.frames = {}

        # Styling
        self['borderwidth'] = 1.0
        self['relief'] = 'sunken'

        # Components in frame
        self.columnconfigure(2, weight=3)

        self.selected_option = tk.StringVar()
        self.selected_note = tk.StringVar()

        tk.Label(self, text="Note").grid(row=0, column=0, padx=5, pady=5)

        notes_list = ttk.Combobox(self, textvariable=self.selected_note, state='readonly')
        notes_list['values'] = ['--'] + [note for note in chords.notes]
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
        # TODO Create a frame depending on the option argument. Use the classes defined below.
        match option:
            case 'Chords':
                self.create_chord_frames()
            case 'Scales':
                # TODO Make scale frame scrollable.
                self.create_scale_frames()
            case 'Circle of Fifths':
                pass
            case 'default':
                tk.Label(self, text="Welcome to Music Notes!\nChoose a note and mode to begin.")\
                    .pack(expand=True)
            case _:
                # TODO How to handle this elegantly? Where should this exception lead? Open error window? Then what?
                # Should this frame be deleted (somehow) before returning to caller?
                raise Exception("Invalid content argument")

    def create_chord_frames(self):
        row = 0
        column = 0

        for variant in chords.chord_variants:
            self.rowconfigure(row, weight=1)
            self.columnconfigure(column, weight=1)

            ChordFrame(
                self,
                variant,
                chords.chord_variants[variant]['notation'],
                chords.chord_variants[variant]['labels'],
            ).grid(row=row, column=column, sticky='nsew')

            column = column + 1 if column < N_OF_CHORDS_IN_ROW else 0
            if column == 0: row += 1

    def create_scale_frames(self):
        self.columnconfigure(0, weight=1)

        for row, scale in enumerate(scales.scales):
            self.rowconfigure(row, weight=1)

            ScaleFrame(
                self,
                scale,
                scales.scales[scale]['notation'],
                scales.scales[scale]['labels'],
            ).grid(row=row, column=0, sticky='ew')


class ChordFrame(tk.Frame):
    def __init__(self, container, chord_name, notation, labels):
        super().__init__(container)

        # Instance variables
        self.container = container
        self.chord_name = chord_name
        self.notation = notation
        self.labels = labels

        self['borderwidth'] = 0.5
        self['relief'] = 'raised'

        # Components in frame
        self.columnconfigure(0, weight=1)

        self.current_note = tk.StringVar()
        self.current_note.trace_add('write', self.update_chord_notes)
        self.chord_notes = tk.StringVar()

        tk.Label(self, text=f'{self.chord_name}{f'({self.notation})' if self.notation != '' else ''}', borderwidth=0.5, relief='groove')\
            .grid(sticky='ew')

        notes_label = ' - '.join(self.labels)
        tk.Label(self, text=notes_label).grid(sticky='ns')
        # TODO Make labels and notes sit in the center of the frame
        tk.Label(self, textvariable=self.chord_notes).grid(sticky='ns')

    def update_chord_notes(self, *args):
        tmp_notes = chords.calculate_chord_notes(
            self.current_note.get(),
            chords.chord_variants[self.chord_name]['formula']
        )
        self.chord_notes.set(' - '.join(tmp_notes))


class ScaleFrame(tk.Frame):
    def __init__(self, container, scale_name, notation, labels):
        super().__init__(container)

        # Instance variables
        self.container = container
        self.scale_name = scale_name
        self.notation = notation
        self.labels = labels

        self['borderwidth'] = 0.5
        self['relief'] = 'raised'

        # Components in frame
        self.columnconfigure(0, weight=1)

        self.current_note = tk.StringVar()
        self.current_note.trace_add('write', self.update_scale_notes)
        self.scale_notes = tk.StringVar()

        tk.Label(self, text=f'{self.scale_name}{f'({self.notation})' if self.notation != '' else ''}', borderwidth=0.5, relief='groove')\
            .grid(sticky='ew')

        notes_label = ' - '.join(self.labels)
        tk.Label(self, text=notes_label).grid(sticky='ns', pady=(5,0))

        tk.Label(self, textvariable=self.scale_notes).grid(sticky='ns', pady=(0,5))

    def update_scale_notes(self, *args):
        tmp_notes = scales.calculate_scale_notes(
            self.current_note.get(),
            self.scale_name
        )
        self.scale_notes.set(' - '.join(tmp_notes))

class CoFFrame(tk.Frame):
    pass

