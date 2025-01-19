from langchain.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
import os


template = """
Eres un asistente virtual que ayuda a practicar en varios idiomas como si fuera una conversación
casual entre dos personas.
Sin embargo, la información siempre se te será traducida al español, y asegurate de siempre responder en español
siempre responder en español.

Acá está el historial de la conversación: {context}

Acá la entrada del usuario que quiere conversar contigo: {question}

Respuesta:
"""

os.environ["OLLAMA_HOST"] = "http://ollama:11434"

model = Ollama(model="llama3.1", base_url='http://ollama:11434')
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation(user_input: str, context: str) -> dict[str, str]:
       
    try:
        result = chain.invoke({"context": context, "question": user_input})
        #context += f"\nUser: {user_input}\nAI: {result}"
        # Si el contexto supera el límite de caracteres, trunca las partes más antiguas
        if len(context) > 4000:
            context = context[-4000:]
        return {"AI_response": result, "history_context": context}
    except Exception as e:
        return {"AI_response": f"Error: {str(e)}", "history_context": context}