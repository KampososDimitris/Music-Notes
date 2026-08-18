import tkinter as tk
from tkinter import ttk

class GUI():
    min_size = (640, 320)
    title = "Music Notes"

    def __init__(self, x_axis=640, y_axis=320):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.geometry = f"{self.x_axis}x{self.y_axis}"

        # call create window wich eventually calls mainloop

    def create_window(self):
        pass
        # TODO Create main window with all its widgets.