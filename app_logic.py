import numpy as np
import os
import pyaudio
import wave

from pydub import AudioSegment

from constants import (
    CHUNK,
    SAMPLE_FORMAT, CHANNELS, RATE,
    NORMALIZING, VOLUME_BOOST,
    DIRECTORY,
    TO_WAV, TO_MP3
)


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