import time
from queue import Queue
from llm_models.embedding import generate_embeding


class QueueTextFactory:
    text_queue = Queue()
    progress_queue = Queue()

    @staticmethod
    def process_text_queue():
        process_text_queue = QueueTextFactory.text_queue

        while True:
            if not process_text_queue.empty():
                body = process_text_queue.get()
                if isinstance(body, tuple) and len(body) == 3:
                    text, name, data_type = body 
                    for progress in generate_embeding(text, name, data_type):
                        print(progress)
                        QueueTextFactory.get_current_progress(progress)
                        
                process_text_queue.task_done()
                print("Aprendizaje generado satisfactoriamente!")
            time.sleep(1)
    
    @staticmethod
    def get_current_progress(progress):
        """ Almacena y retorna el progreso actual del procesamiento """
        name = progress.get('name', 'Desconocido')  # Evita error si la clave no existe
        current_level = progress.get('level', 0)  # Valor por defecto 0
        status = {"name": name, "level": current_level}

        # Guardar el estado en la cola de progreso
        QueueTextFactory.progress_queue.put(status)

        return status