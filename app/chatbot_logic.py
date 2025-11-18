import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from .history_manager import get_sql_history
from .config import MODEL_NAME, OLLAMA_BASE_URL, MAX_TOKENS
import logging

logger = logging.getLogger(__name__)


def create_llm():
    """
    Crea una instancia del modelo de lenguaje con configuración robusta.
    """
    try:
        llm = ChatOllama(
            model=MODEL_NAME,
            base_url=OLLAMA_BASE_URL,
            temperature=0.7,
            num_predict=MAX_TOKENS,
        )
        llm.invoke("test")
        logger.info(f"Modelo {MODEL_NAME} inicializado correctamente")
        return llm
    except Exception as e:
        logger.error(f"Error al inicializar modelo: {e}")
        raise ConnectionError(f"No se pudo conectar con Ollama: {e}")

llm = create_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", """Eres un asistente de IA útil y amigable creado por Antonio Ortega.

Tus capacidades principales:
- Responder preguntas con información precisa y actualizada
- Ayudar con tareas de programación y análisis de código
- Explicar conceptos complejos de forma simple
- Proporcionar consejos y recomendaciones prácticas
- Mantener conversaciones naturales y contextuales

Directrices:
- Sé conciso pero completo en tus respuestas
- Si no sabes algo, admítelo honestamente
- Usa ejemplos cuando ayuden a clarificar
- Mantén un tono profesional pero amigable
- Responde en el idioma del usuario"""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()

with_history = RunnableWithMessageHistory(
    chain,
    get_sql_history,
    input_messages_key="question",
    output_messages_key="output",
    history_messages_key="history"
)


def run_chat(question: str, session_id: str):
    """
    Ejecuta el chatbot con la pregunta del usuario.
    
    Args:
        question: Pregunta del usuario
        session_id: ID de sesión único
        
    Yields:
        Chunks de la respuesta generada
    """
    if not question or not question.strip():
        raise ValueError("La pregunta no puede estar vacía")
    
    if not session_id:
        raise ValueError("Se requiere un session_id válido")
    
    try:
        logger.info(f"Procesando pregunta para sesión {session_id[:8]}...")
        
        for chunk in with_history.stream(
            {"question": question},
            config={"configurable": {"session_id": session_id}},
        ):
            yield chunk
            
    except Exception as e:
        logger.error(f"Error en run_chat: {e}")
        raise