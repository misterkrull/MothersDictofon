import win32com.client

class SpeechManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # если экземпляр класса уже есть, то повторная инициализация не требуется
            self._speaker = win32com.client.Dispatch("Sapi.SpVoice")
            voices = self._speaker.GetVoices()
            self._speaker.Voice = voices[0]
            self._speaker.Rate = 4
            self._speaker.Volume = 100
        
    def speak(self, text: str):
        if self._speaker:
            self._speaker.Speak(text)
