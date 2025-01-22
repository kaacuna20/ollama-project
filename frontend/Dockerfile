# Usa una imagen base de Python 3.11
FROM python:3.11-slim

WORKDIR /app
# Actualizar el sistema e instalar dependencias
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    libffi-dev \
    && apt-get clean

RUN apt-get update && apt-get install -y \
    libasound-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    && pip install pyaudio


RUN apt-get update && apt-get install -y curl

# Copia solo los archivos necesarios para reducir el tamaño de la imagen
COPY requirements.txt .

# Actualiza pip
RUN pip install --upgrade pip

# Instala las dependencias del archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]