from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import Ollama


custom_prompt_template = """
        usa la siguiente información para responder a la pregunta del usuario.
        si no sabes la respuesta, simplemente di que no lo sabes, no trates de inventar una respuesta.

        contexto: {context}
        pregunta: {question}

        solo devuelve la respuesta útil a continuación y solamente la respuesta útil
    """

def prompt_llm_response(vector_store, user_input: str):
    prompt = PromptTemplate(
        template=custom_prompt_template,
        input_variables=['context', 'question']
    )

    model = Ollama(model="llama3.1", base_url='http://ollama:11434')

    qa_chain = RetrievalQA.from_chain_type(
        llm=model,  # Este debe ser un modelo de lenguaje
        chain_type="stuff",
        retriever=vector_store.as_retriever(),  # Este es tu retriever, asegurándote de que esté correctamente configurado
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    response = qa_chain.invoke({"query": user_input})
    return response["result"]