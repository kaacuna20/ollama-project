import re
import time
import requests
import streamlit as st


st.set_page_config(
    page_title="Media Section",
    page_icon="🎧",
    initial_sidebar_state="expanded"
)

youtube_regex = re.compile(r'^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$')

st.header("URL del Video YouTube")
st.warning("Extrae transcripción del video de youtube solo si el video lo trae, sino, no podrá extraer nada!")
with st.form('parametros'):
    name_video = st.text_input("Nombre del video")
    parmVideo = st.text_input("URL del video de Youtube")
    btnGenerar =st.form_submit_button('Generar Aprendizaje')
    
    if btnGenerar and parmVideo is not None:
        if youtube_regex.match(parmVideo):
            with st.status("Generando aprendizaje al modelo...", expanded=True) as status_document:
                #processor = URLProcessorFactory.get_processor(parmVideo)
                #result = processor.process()
                parameters ={
                    "url": parmVideo,
                    "name": name_video
                }
                response = requests.post("http://backend:8000/text/upload-url/", params=parameters)
                st.text_area("URL Text", response.json()["text"], height=300)
                #QueueText.text_queue.put((result["text"], name_video, result["file_type"]))
               
            st.success("Aprendizaje generado satisfactoriamente!")
        else:
            st.error("no es una url valida")
        
    
st.header("Sube el archivo media")

with st.form('parametros2'):
    uploaded_file = st.file_uploader("Choose a file", type=["mp3", "wav", "flac", "aac", "mp4", "mov", "avi", "mkv"], accept_multiple_files=False)
    btnGenerar2 =st.form_submit_button('Generar2')
    if btnGenerar2 and uploaded_file is not None:
        with st.status("Procesando contenido...", expanded=True) as status_document:
            time.sleep(2)
            parameters = {
                "media_file_type": uploaded_file.type
            }
            response = requests.post("http://backend:8000/text/upload-media/", params=parameters, files=uploaded_file)
            #processor = MediaProcessorFactory.get_processor(uploaded_file, uploaded_file.type)
            #transcription = processor.process()
            #QueueText.text_queue.put((transcription["text"], uploaded_file.name, transcription["file_type"]))
            # Muestra el texto extraído
            st.text_area("Media Text", response.json()["text"], height=300)
        st.success("Aprendizaje generado satisfactoriamente!")
                
    else:
        st.error("Por favor cargue el archivo")