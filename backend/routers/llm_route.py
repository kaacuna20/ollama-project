import os
from starlette import status
from pydantic import BaseModel
from fastapi import APIRouter, Form, HTTPException
from llm_models.embedding import generate_vectore_store
from llm_models.llm_from_knowledge import prompt_llm_response


router = APIRouter(
    prefix='/llm',
    tags=['llm-actions']
)

class PromptRequest(BaseModel):
    vectore_store_name: str
    user_input: str
    
@router.get("/all-learnings/", status_code=status.HTTP_200_OK)
async def get_all_learnings():
    """
    Lista los documentos el cual se generaron un índice FAISS de aprendizaje listos para ser usados
    """
    path_files = os.listdir(fr"{os.getcwd()}/db_vectorial")
    print(os.getcwd())

   
    files = [{"FileName": file.split("-")[0], "format": file.split("-")[1].split(".")[0], "is_learned": True} for file in path_files if file.endswith(".index")]

    return {"learning-documents":  files}


@router.post("/promp-user/", status_code=status.HTTP_200_OK)
async def prompt_llm(request: PromptRequest):
    """
    Cargar un índice FAISS desde el sistema de archivos y procesar la solicitud
    """
    try:
        # Ruta del archivo FAISS and pikle
        fais_path = f"{request.vectore_store_name}.index"
        pickle_path = f"{request.vectore_store_name}.pkl"
        
        # Leer el índice FAISS desde el archivo
        vector_store = generate_vectore_store(db_faiss=fais_path, file_pickle=pickle_path)

        # Generar la respuesta usando el índice FAISS
        response = prompt_llm_response(vector_store, user_input=request.user_input)
        return {"llm_response": response}

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la solicitud: {str(e)}"
        )