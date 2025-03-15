import pyaudio

DIRECTORY = r"C:\recordings"

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