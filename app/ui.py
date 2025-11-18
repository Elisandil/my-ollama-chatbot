import gradio as gr
import uuid
from .session_manager import heartbeat, sessions, register_session
from .chatbot_logic import run_chat
import logging

logger = logging.getLogger(__name__)


def chatbot(input_value, history, session_state):
    """
    Maneja las interacciones del chatbot con gestión de sesiones mejorada.
    """
    if not input_value or not input_value.strip():
        yield "Por favor, escribe un mensaje."
        return

    session_id = session_state.get("session_id")
    
    if not session_id or session_id not in sessions:
        yield "Sesión expirada. Por favor, recarga la página."
        return

    try:
        response = run_chat(input_value.strip(), session_id)
        
        output = ""
        for chunk in response:
            if session_id not in sessions:
                yield output + "\n\nSesión expirada durante la respuesta."
                break
            
            output += chunk
            yield output
            
    except ConnectionError as e:
        logger.error(f"Error de conexión con Ollama: {e}")
        yield "No se puede conectar con Ollama. Verifica que el servicio esté activo."
    except Exception as e:
        logger.error(f"Error en chatbot: {e}")
        yield f"Error inesperado: {str(e)}"


def initialize_session():
    """
    Inicializa una nueva sesión con un ID único.
    """
    session_id = str(uuid.uuid4())
    register_session(session_id)
    logger.info(f"Nueva sesión creada: {session_id}")
    return {"session_id": session_id}


def keep_alive(session_state):
    """
    Mantiene la sesión activa mediante heartbeat.
    """
    session_id = session_state.get("session_id")
    if session_id:
        return heartbeat(session_id)
    return "no_session"


def create_interface():
    """
    Crea la interfaz de Gradio con gestión de sesiones mejorada.
    """
    with gr.Blocks(
        title="Chatbot con Llama3",
        theme=gr.themes.Soft()
    ) as iface:
        session_state = gr.State(value=initialize_session)
        timer = gr.Timer(value=5.0)

        timer.tick(
            fn=keep_alive,
            inputs=[session_state],
            outputs=None
        )

        gr.Markdown("#Chatbot con Llama3 via Ollama")
        gr.Markdown("Asistente de IA construido con LangChain y Gradio")
        
        chat_interface = gr.ChatInterface(
            fn=chatbot,
            additional_inputs=[session_state],
            title=None,
            description="Escribe tu mensaje y presiona Enter",
            examples=[
                "¿Qué puedes hacer?",
                "Explícame qué es Python en términos simples",
                "Dame consejos para aprender programación"
            ],
            retry_btn="🔄 Reintentar",
            undo_btn="↩️ Deshacer",
            clear_btn="🗑️ Limpiar chat",
        )
    
    return iface