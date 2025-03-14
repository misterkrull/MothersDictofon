"""
    HUITA 1.0
    This code is govno

    CC-BY-CA (??? huj znaet)
"""

import keyboard
import os
import pyaudio
import wave

DIRECTORY = r"D:\Диктофон мамы 2024"

CHUNK = 1024  # Запись кусками по 1024 сэмпла
SAMPLE_FORMAT = pyaudio.paInt16  # 16 бит на выборку
CHANNELS = 2
RATE = 44100  # Запись со скоростью 44100 выборок(samples) в секунду
SECONDS = 3


def main():
    """
        This function is pizdec
    """

    p = pyaudio.PyAudio()  # Создать интерфейс для PyAudio

    filename = input("Введите название : ")
    print("R")

    stream = p.open(format=SAMPLE_FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    frames_per_buffer=CHUNK,
                    input_device_index=0,
                    input=True)
    frames = []  # Инициализировать список для хранения кадров

    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if keyboard.is_pressed(' '):
            # print('Finished recording!')
            break

    # Остановить и закрыть поток
    stream.stop_stream()
    stream.close()

    # Завершить интерфейс PortAudio
    p.terminate()

    # Сохранить записанные данные в виде файла WAV
    with wave.open(os.path.join(DIRECTORY, f"{filename}.wav"), "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))


if __name__ == "__main__":
    main()
