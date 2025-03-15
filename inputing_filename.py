import tkinter as tk

from constants import INPUTING_WINDOW_X, INPUTING_WINDOW_Y, INPUTING_WINDOW_Y_BIAS
from typing import Callable

class InputingFilename:
    def __init__(self, tk_root: tk.Tk, stop_rec: Callable):
        # создаём диалоговое окно
        self._dialog_window = tk.Toplevel(tk_root)        
        # указываем, что наше диалоговое окно -- временное по отношению к родительскому окну
        # в т.ч. это убирает кнопки Свернуть/Развернуть, оставляя только крестик в углу
        self._dialog_window.transient(tk_root)
        # блокируем кнопки родительского окна
        self._dialog_window.grab_set()

        self._stop_rec = stop_rec

        # задаём расположение окна (используем размеры и расположение родительского окна)
        x = tk_root.winfo_x() + (tk_root.winfo_width() // 2) - INPUTING_WINDOW_X // 2
        y = tk_root.winfo_y() + (tk_root.winfo_height() // 2) - INPUTING_WINDOW_Y // 2 + INPUTING_WINDOW_Y_BIAS

        self._dialog_window.geometry(
            f"{INPUTING_WINDOW_X}x{INPUTING_WINDOW_Y}+{x}+{y}"
        )  # указываем размеры и расположение
        self._dialog_window.title("Записано, введите имя")  # указываем название окна

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
        
        # пропускаем управляющие клавиши -- иначе он их блокирует
        if event.keysym in ["Left", "Right", "Up", "Down", "BackSpace", "Delete"]:
            return
        
        # блокируем запрещённые символы
        if event.char in "/\\:*?\"<>|":
            return "break"  # Отменяет ввод символа
        
    def _on_ok(self, _: tk.Event | None = None) -> None:
        self._filename = self._input_field.get().strip()
        if self._filename:
            self._stop_rec(self._filename)
        self._dialog_window.destroy()

    def _on_cancel(self, _: tk.Event | None = None) -> None:
        self._dialog_window.destroy()
