import threading
from starlette import status
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from pydantic import BaseModel, HttpUrl
from typing import Optional, Annotated
from queue_process.queue_process import QueueTextFactory
from text_process_factory.document_process import DocumentProcessorFactory
from text_process_factory.url_process import URLProcessorFactory
from text_process_factory.media_process import MediaProcessorFactory

router = APIRouter(
    prefix='/text',
    tags=['text-process']
)

queue_text = QueueTextFactory()

# threading
threading_text_process = threading.Thread(target=queue_text.text_queue, daemon=True)
threading_text_process.start()


@router.post("/upload-documents/", status_code=status.HTTP_200_OK)
async def upload_document(
        uploaded_file: Annotated[UploadFile, File()]
    ):
    try:
        processor = await DocumentProcessorFactory.get_processor(uploaded_file)
        processed_text = processor.process()
        queue_text.text_queue.put((processed_text["text"], uploaded_file.filename, processed_text["file_type"]))
        # with open(file_path, "wb") as f:
        #     content = await file.read()
        #     f.write(content)
        return {"text": processed_text["text"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file {uploaded_file.filename}: {e}")

@router.post("/upload-url/", status_code=status.HTTP_200_OK)
async def upload_url(url: HttpUrl, name: str):
    try:
        processor = await URLProcessorFactory.get_processor(url)
        result = processor.process()
        queue_text.text_queue.put((result["text"], name, result["file_type"]))
        
        return {"text": result["text"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesing {url}: {e}")

@router.post("/upload-media/", status_code=status.HTTP_200_OK)
async def upload_media(
        uploaded_media_file: Annotated[UploadFile, File()],
        media_file_type: str
    ):
    try:
        processor = await MediaProcessorFactory.get_processor(uploaded_media_file, media_file_type)
        transcription = processor.process()
        queue_text.text_queue.put((transcription["text"], uploaded_media_file.filename, transcription["file_type"]))
        # with open(file_path, "wb") as f:
        #     content = await file.read()
        #     f.write(content)
        return {"text": transcription["text"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesing file {uploaded_media_file.filename}: {e}")

@router.get("/current-process-loading/", status_code=status.HTTP_200_OK)
async def get_current_progress():
    """ Devuelve el progreso actual del procesamiento de aprendizaje """
    if queue_text.progress_queue.empty():
        return {"current_status": "No hay aprendizaje en proceso"}

    latest_progress = queue_text.progress_queue.get()  # Obtiene el progreso más reciente
    return {"current_status": latest_progress}
