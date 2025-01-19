import os
import whisper
from abc import ABC, abstractmethod
from moviepy.editor import VideoFileClip


# Clase abstracta para procesar medios
class MediaProcessor(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.model = whisper.load_model("base")

    @abstractmethod
    def process(self):
        pass

# Clase concreta para procesar audios
class AudioProcessor(MediaProcessor):
    def process(self) -> dict:
        result = self.model.transcribe(self.file_path)
        return {"text": result['text'], "file_type": "Audio"}

# Clase concreta para procesar videos
class VideoProcessor(MediaProcessor):
    def process(self) -> dict:
        # Convertir el video a audio
        video = VideoFileClip(self.file_path)
        audio_path = "temp_audio.mp3"
        video.audio.write_audiofile(audio_path)

        # Transcribir el audio
        result = self.model.transcribe(audio_path)

        # Eliminar el archivo de audio temporal
        os.remove(audio_path)

        return {"text": result['text'], "file_type": "Video"}

# Fábrica para seleccionar el procesador adecuado
class MediaProcessorFactory:
    @staticmethod
    def get_processor(file_path, file_type):
        if file_type.startswith('audio/'):
            return AudioProcessor(file_path)
        elif file_type.startswith('video/'):
            return VideoProcessor(file_path)
        else:
            raise ValueError(f"Unsupported media type: {file_type}")
        
        
