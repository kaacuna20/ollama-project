import re
import threading
import streamlit as st
#from backend.text_process.document_process import DocumentProcessorFactory
#from backend.text_process.url_process import URLProcessorFactory
#from backend.llm_models.embedding import text_queue, QueueText
import requests

# threading
#threading_text_process = threading.Thread(target=text_queue, daemon=True)
#threading_text_process.start()


st.set_page_config(
    page_title="Video Section",
    page_icon="📄",
    initial_sidebar_state="expanded"
)

st.header("Sube un documento")

with st.form('parametros'):
    uploaded_file = st.file_uploader("Sube un archivo", type=['pdf', 'docx', 'txt'], accept_multiple_files=False)
    btnGenerar = st.form_submit_button('Generar Aprendizaje')
    if btnGenerar:
        if uploaded_file is not None :
            st.session_state.document_loaded = True
            with st.status("Generando aprendizaje al modelo...", expanded=True) as status_training:
                response = requests.post("http://backend:8000/text/upload-documents/", files=uploaded_file)
                #processor = DocumentProcessorFactory.get_processor(uploaded_file)
                #processed_text = processor.process()
                # Muestra el texto extraído
                st.text_area("Document Text", response.json()["text"], height=300)
                #QueueText.text_queue.put((processed_text["text"], uploaded_file.name, processed_text["file_type"]))
            st.success("Aprendizaje generandose satisfactoriamente!")
            
        else:
            st.error("Por favor cargue el archivo")
    
regex = re.compile(
    r"^(https?:\/\/)"  # http:// o https://
    r"(([\da-z\.-]+)\.)"  # subdominio o dominio
    r"([a-z\.]{2,6})"  # dominio principal
    r"([\/\w \.-]*)*\/?$"  # ruta opcional
)

st.header("Sube un enlace de una página web")

with st.form('enlaces'):
    url_input = st.text_input("URL de Página Web")
    name_article = st.text_input("Título del articulo") 
    btnGenerar2 = st.form_submit_button('Generar Aprendizaje')

    if btnGenerar2:
        if regex.match(url_input):
            with st.status("Generando aprendizaje al modelo...", expanded=True) as status_training:
                parameters ={
                    "url": url_input,
                    "name": name_article
                }
                response = requests.post("http://backend:8000/text/upload-url/", params=parameters)
                #processor = URLProcessorFactory.get_processor(url_input)
                #result = processor.process()
                # Muestra el texto extraído
                st.text_area("URL Text", response.json()["text"], height=300)
                #QueueText.text_queue.put((result["text"], name_article, result["file_type"]))
            st.success("Aprendizaje generandose satisfactoriamente!")
        else:
            st.error("no es una url valida")
