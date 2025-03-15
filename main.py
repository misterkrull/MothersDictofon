import threading
import tkinter as tk

from constants import MAIN_WINDOW_X, MAIN_WINDOW_Y
from inputing_filename import InputingFilename
from app_logic import AppLogic


class MainWindow:
    def __init__(self):
        self.tk_root = tk.Tk()

        self.tk_root.title("Диктофон для Марины")
        self.tk_root.geometry(f"{MAIN_WINDOW_X}x{MAIN_WINDOW_Y}")
        self.tk_root.resizable(False, False)
        self.tk_root.protocol("WM_DELETE_WINDOW", self._on_closing) 

        self.app = AppLogic()

        self.startstop_button = tk.Button(
            self.tk_root,
            font=("Helvetica", 16),
            text="Cтарт",
            command=self._start_stop,
            width=20
        )
        self.startstop_button.pack(pady=30)
        
        self.tk_root.bind("<space>", self._start_stop)
        
        self.tk_root.mainloop()

    def _start_stop(self, _: tk.Event | None = None) -> None:
        if not self.app.is_started:         # СТАРТ!
            self.app.is_started = True
            self.startstop_button.config(text="Стоп")
            threading.Thread(target=self.app.start_rec).start()
        else:                               # СТОП!
            self.app.is_started = False 
            self.startstop_button.config(text="Старт")
            InputingFilename(self.tk_root, self.app.stop_rec)

    def _on_closing(self) -> None:
        self.app.close()
        self.tk_root.destroy()


if __name__ == "__main__":
    MainWindow()
