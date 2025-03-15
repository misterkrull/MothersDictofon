import os
import tkinter as tk
from typing import Callable

from constants import INPUTING_WINDOW_X, INPUTING_WINDOW_Y, INPUTING_WINDOW_Y_BIAS, DIRECTORY, TO_WAV, TO_MP3
from speech_manager import SpeechManager


class InputingFilename:
    def __init__(self, tk_root: tk.Tk, stop_rec: Callable):
        self._stop_rec = stop_rec
        self.tk_root = tk_root

        # создаём диалоговое окно
        self._dialog_window = tk.Toplevel(self.tk_root)        
        # указываем, что наше диалоговое окно -- временное по отношению к родительскому окну
        # в т.ч. это убирает кнопки Свернуть/Развернуть, оставляя только крестик в углу
        self._dialog_window.transient(self.tk_root)
        # блокируем кнопки родительского окна
        self._dialog_window.grab_set()

        self._is_listened = False  # флаг, который отслеживает, прослушан ли введённый текст и можно ли сохранять

        # задаём расположение окна (используем размеры и расположение родительского окна)
        x = self.tk_root.winfo_x() + (self.tk_root.winfo_width() // 2) - INPUTING_WINDOW_X // 2
        y = self.tk_root.winfo_y() + (self.tk_root.winfo_height() // 2) - INPUTING_WINDOW_Y // 2 + INPUTING_WINDOW_Y_BIAS

        self._dialog_window.geometry(
            f"{INPUTING_WINDOW_X}x{INPUTING_WINDOW_Y}+{x}+{y}"
        )  # указываем размеры и расположение
        self._dialog_window.title("Записано, введите имя и нажмите энтер, хотите отменить - нажмите эскейп")

        self._add_widgets()  # добавляем все элементы на наше окно

        self._dialog_window.bind("<Return>", self._on_ok)
        self._dialog_window.bind("<Escape>", self._on_cancel)

        self._filename: str = ""

    def _add_widgets(self) -> None:
        # добавляем надпись
        label = tk.Label(
            self._dialog_window,
            text="Введите название аудиозаписи:",
            font=("Segoe UI", 10),
        )
        label.pack(pady=2)

        # добавляем поле для ввода
        self._input_field = tk.Entry(
            self._dialog_window, width=25, font=("Segoe UI", 12), justify="center"
        )
        self._input_field.pack(pady=3)
        self._input_field.focus_set()
        self._input_field.bind("<Key>", self._validate_input)

        # фрейм для кнопок
        button_frame = tk.Frame(self._dialog_window)
        button_frame.pack(pady=7)

        self._ok_button = tk.Button(
            button_frame, text="ОК", command=self._on_ok, width=12, font=("Segoe UI", 10)
        )
        self._ok_button.pack(side=tk.LEFT, padx=10, pady=0)

        self._cancel_button = tk.Button(
            button_frame, text="Отмена", command=self._on_cancel, width=12, font=("Segoe UI", 10)
        )
        self._cancel_button.pack(side=tk.LEFT, padx=2, pady=0)
    
    def _validate_input(self, event: tk.Event | None = None) -> None | str:
        """Блокирует ввод запрещённых символов."""
        
        if event.keysym not in ["Return"]:
            self._is_listened = False
            
        # пропускаем управляющие клавиши -- иначе он их блокирует
        if event.keysym in ["Left", "Right", "Up", "Down", "Home", "End", "BackSpace", "Delete"]:
            return
        
        # блокируем запрещённые символы
        if event.char in "/\\:*?\"<>|":
            return "break"  # Отменяет ввод символа
        
    def _on_ok(self, _: tk.Event | None = None) -> None:
        self._filename = self._input_field.get().strip()
        if self._filename == "":
            self._speak("Вы ничего не ввели")
        else:
            if not self._is_listened:
                fullpath = os.path.join(DIRECTORY, f"{self._filename}")
                if TO_WAV and os.path.exists(fullpath + ".wav") or TO_MP3 and os.path.exists(fullpath + ".mp3"):
                    self._speak(f"Вы ввели: {self._filename}: файл с таким именем уже существует: переименуйте")
                else:
                    self._speak(f"Вы ввели: {self._filename}: для сохранения нажимите Ентер")
                    self._is_listened = True
            else:
                self._speak("Сохранено: диктофон готов к следующей записи")
                self._stop_rec(self._filename)
                self._dialog_window.destroy()

    def _speak(self, text: str) -> None:
        self.tk_root.after(50, lambda: SpeechManager().speak(text))      

    def _on_cancel(self, _: tk.Event | None = None) -> None:
        self._dialog_window.destroy()
