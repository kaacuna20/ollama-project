from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from newspaper import Article

class YouTubeProcessor:
    def __init__(self, url):
        self.url = url

    def process(self) -> dict:
        parsed_url = urlparse(self.url)
        video_id = parse_qs(parsed_url.query)['v'][0]

        # Obtener las transcripciones del video en inglés y español
        transcripcion = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'es'])
        
        # Concatenar la transcripción
        transcripcionTexto=''
        chunk = 2000
        for frase in transcripcion:
            transcripcionTexto =transcripcionTexto + frase['text'] + " "
            if len(transcripcionTexto) > chunk:
                transcripcionTexto =transcripcionTexto + frase['text'] + "\n"
                chunk += 2000
        
        return {"text": transcripcionTexto, "file_type": "YouTube"}


class WebpageProcessor:
    def __init__(self, url):
        self.url = url

    def process(self) -> dict:
        article = Article(self.url)
        article.download()
        article.parse()
        
        return {"text": article.text, "file_type": "WebSite"}


class URLProcessorFactory:
    @staticmethod
    def get_processor(url: str):
        parsed_url = urlparse(url)

        if 'youtube.com' in parsed_url.netloc or 'youtu.be' in parsed_url.netloc:
            
            return YouTubeProcessor(url)
        else:
            return WebpageProcessor(url)