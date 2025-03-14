"""
    HUITA 1.0
    This code is govno

    CC-BY-CA (??? huj znaet)
"""

import numpy as np
import os
import pyaudio
import threading
import tkinter as tk
import wave

from pydub import AudioSegment
from typing import Callable

DIRECTORY = r"G:\codes\projects\_archive"

CHUNK = 1024  # Запись кусками по 1024 сэмпла

SAMPLE_FORMAT = pyaudio.paInt16  # 16 бит на выборку
CHANNELS = 1
RATE = 44100  # Запись со скоростью 44100 выборок(samples) в секунду

MAIN_WINDOW_X = 300
MAIN_WINDOW_Y = 100
INPUTING_WINDOW_X = 250
INPUTING_WINDOW_Y = 100
INPUTING_WINDOW_Y_BIAS = 100

NORMALIZING = True
VOLUME_BOOST = 60.0

TO_WAV = False
TO_MP3 = True

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
        self._dialog_window.title("Ввести имя аудиозаписи")  # указываем название окна

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

    def _on_ok(self, _: tk.Event | None = None) -> None:
        self._filename = self._input_field.get()
        if self._filename:
            self._stop_rec(self._filename)
        self._dialog_window.destroy()

    def _on_cancel(self, _: tk.Event | None = None) -> None:
        self._dialog_window.destroy()


class AppLogic:
    def __init__(self):
        self.pya = pyaudio.PyAudio()  # Создать интерфейс для PyAudio
        self.is_started = False

    def start_rec(self) -> None:
        self.stream = self.pya.open(
            format=SAMPLE_FORMAT,
            channels=CHANNELS,
            rate=RATE,
            frames_per_buffer=CHUNK,
            input_device_index=0,
            input=True
        )
        frames = []  # Инициализировать список для хранения кадров

        while True:
            data = self.stream.read(CHUNK)
            frames.append(data)
            if not self.is_started:
                break
            
        audio_data = np.frombuffer(b"".join(frames), dtype=np.int16)
        
        # Нормализация или увеличение громкости
        if NORMALIZING:
            max_val = np.max(np.abs(audio_data))
            # print("Коэффициент нормализации:", 32767 / max_val)
            audio_data = (audio_data / max_val * 32767).astype(np.int16)
        else:
            audio_data = (audio_data * VOLUME_BOOST).astype(np.int16)
        self.audio_data_bytes = audio_data.tobytes()

    def stop_rec(self, filename: str) -> None:
        if TO_WAV:
            with wave.open(os.path.join(DIRECTORY, f"{filename}.wav"), "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.pya.get_sample_size(SAMPLE_FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(self.audio_data_bytes)
        if TO_MP3:
            sound = AudioSegment(
                data=self.audio_data_bytes,
                frame_rate=RATE,
                sample_width=2,  # 16-битное аудио
                channels=CHANNELS
            )
            sound.export(os.path.join(DIRECTORY, f"{filename}.mp3"), format="mp3")

    def close(self) -> None:
        self.is_started = False
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.pya.terminate()
        except:
            pass


class GuiInit:
    def __init__(self, tk_root: tk.Tk):
        self.tk_root = tk_root

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

    def _start_stop(self) -> None:
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
    tk_root = tk.Tk()
    gui = GuiInit(tk_root)
    tk_root.mainloop()
