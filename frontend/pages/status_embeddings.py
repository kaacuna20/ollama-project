import requests
import streamlit as st


st.set_page_config(
    page_title="Status learning",
    page_icon="🎚️",
    initial_sidebar_state="expanded"
)

st.header("Progreso de Aprendizaje")

# Diccionario para almacenar barras de progreso por nombre de tarea
progress_bars = {}

# Mientras haya tareas en la cola de texto, seguimos mostrando progreso
response_loading = requests.get("http://backend:8000/text/current-process-loading/")

if response_loading.json()['current_status'] != 'No hay aprendizaje en proceso':
    try:
            # Obtener la actualización del progreso desde la cola
            progress = response_loading.json()['current_status']
            task_name = progress["name"]
            progress_percentage = progress["level"]

            # Si no existe una barra de progreso para esta tarea, crearla
            if task_name not in progress_bars:
                progress_bars[task_name] = st.progress(0)

            # Actualizar la barra de progreso correspondiente
            progress_bars[task_name].progress(progress_percentage / 100)

            if progress_percentage >= 100:
                st.success(f"Tarea {task_name} completada!")

    except Exception as e:
            st.error(f"Error: {str(e)}")


else:
    st.info("No hay tareas en progreso actualmente.")
