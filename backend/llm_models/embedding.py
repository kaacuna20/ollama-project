import os
import pickle
import faiss
import numpy as np
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.schema import Document
from langchain.docstore.in_memory import InMemoryDocstore
from langchain.vectorstores import FAISS


embedding_model = OllamaEmbeddings(model='llama3.1',  base_url='http://ollama:11434')

def generate_embeding(text: str, name: str, type: str):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=5000,
        chunk_overlap=200,
        length_function=len
    )
    text_split = text_splitter.split_text(text)
    
    # Generar embeddings usando Ollama
    #embeddings = [embedding_model.embed_query(chunk) for chunk in text_split]
    
    embeddings = []
    i = 0
    for embedd_text in text_split:
        embedding_query = embedding_model.embed_query(embedd_text)
        embeddings.append(embedding_query)
        value = (i/len(text_split))*100
        i += 1
        yield {"name": name, "level": round(value, 2)}
    
    # Convertir los embeddings en una matriz numpy
    embeddings_np = np.array(embeddings)

    # Crear el índice FAISS
    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dimension)

    # Agregar los embeddings al índice FAISS
    index.add(embeddings_np)

    # Guardar el índice FAISS en un archivo
    faiss.write_index(index, f"backend/db_vectorial/{name}-{type}.index")
    
    # serializar el mapeo de índices a documentos
    index_to_docstore_id = {i: i for i in range(len(text_split))}
    # Crear documentos LangChain
    doc_class = [Document(page_content=text) for text in text_split]
    
    doc_and_index = {"index_docstore_id": index_to_docstore_id, "doc_langchain": doc_class}
    
    with open(f"backend/binaries_files/{name}-{type}.pkl", "wb") as f:
        pickle.dump(doc_and_index, f) 


def generate_vectore_store(db_faiss: str, file_pickle: str):
    
    faiss_path = os.path.join("db_vectorial", db_faiss)
    pickle_path = os.path.join("binaries_files", file_pickle)

    # Cargar el índice FAISS desde el archivo
    index = faiss.read_index(faiss_path)
    
    # Cargar el mapeo de índices a documentos (si lo guardaste en un archivo)
    with open(pickle_path, "rb") as f:
        doc_and_index = pickle.load(f)
    
    doc_class = doc_and_index["doc_langchain"]
    index_to_docstore_id = doc_and_index["index_docstore_id"]
    docstore = InMemoryDocstore({i: doc_class[i] for i in range(len(doc_class))})
    
    # Crear la instancia de FAISS vector store
    vector_store = FAISS(index=index, docstore=docstore, index_to_docstore_id=index_to_docstore_id, embedding_function=embedding_model)
    
    return vector_store



        
