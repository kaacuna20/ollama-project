import time
import pickle 
import os
import requests
import pandas as pd
import streamlit as st
#from backend.llm_models.llm_from_knowledge import prompt_llm_response
#from backend.llm_models.embedding import generate_vectore_store


st.set_page_config(
    page_title="Study Agent",
    page_icon="🤖",
    initial_sidebar_state="collapsed"
)

st.title("Study Agent")

stream = """ Bienvenidos a su aplicación para estudiar e interactuar con AI, donde
        pueden cargar documentos de diferentes archivos y estudiar en base a ellos, practicar algún idioma o 
        sacar resumenes de videos de youtube, acortando el tiempo de estudia y haciendolo mas eficiente!
    """

# Mostrar el contenido procesado del stream
st.write(stream)

response = requests.get("http://backend:8000/llm/all-learnings/")

if len(response.json()["learning-documents"]) == 0:
    df = pd.DataFrame(
        [
        {"FileName": "empty", "format": "empty", "is_learned": "empty"},
        ]
    )

else:

    df = pd.DataFrame(
        response.json()["learning-documents"]
    )

st.write(df)
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize chat history
if "vectore" not in st.session_state:
    st.session_state.vectore = None

path_files = [file['FileName'] for file in response.json()["learning-documents"]]
        
with st.form('parametros con Ollama'):
    files_select = st.selectbox("Escoge el documento", options=path_files)
    btnGenerar2 =st.form_submit_button('Usar llama3')
    
    if btnGenerar2:
        pickle_ext = f"{files_select.split('.')[0]}.pkl"
        with st.status("Generando aprendizaje al modelo...", expanded=True) as status_document:
            time.sleep(2)
            st.session_state.vectore = files_select

        print(st.session_state.vectore)
        st.success("Modelo cargado con información de aprendizaje!")
    

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# React to user input
if user_input := st.chat_input("Escribí tu mensaje 😎"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})


if user_input != None:
    if st.session_state.messages and user_input.strip() != "":
        # Serializar el objeto vectore
        vector_selected = st.session_state.vectore
      
        # Enviar a la API usando POST
        response = requests.post(
            "http://backend:8000/llm/promp-user/",
            data={"vectore_store_name": vector_selected, "user_input": user_input}
        )
            
        response_llm = response.json()["llm_response"]
        
        def stream_data():
            for word in response_llm.split(" "):
                yield word + " "
                time.sleep(0.02)
                
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            #st.markdown(st.write_stream(stream_data))
            st.write_stream(stream_data)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_llm})
