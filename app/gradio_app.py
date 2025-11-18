import logging
from .ui import create_interface
from .session_manager import start_session_monitor
from .config import (
    validate_config, 
    LOG_LEVEL, 
    LOG_FORMAT,
    GRADIO_SERVER_NAME,
    GRADIO_SERVER_PORT,
    GRADIO_SHARE,
    MODEL_NAME,
    OLLAMA_BASE_URL
)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT
)

logger = logging.getLogger(__name__)


def check_ollama_connection():
    """
    Verifica que Ollama esté disponible antes de iniciar.
    """
    try:
        import requests
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            
            logger.info(f"✓ Ollama conectado. Modelos disponibles: {model_names}")
            
            if MODEL_NAME not in model_names:
                logger.warning(
                    f"Modelo '{MODEL_NAME}' no encontrado. "
                    f"Disponibles: {model_names}"
                )
                return False
            
            return True
        else:
            logger.error(f"✗ Ollama respondió con código {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"✗ No se pudo conectar con Ollama en {OLLAMA_BASE_URL}: {e}")
        return False


def main():
    """
    Función principal que inicia la aplicación.
    """
    logger.info("="*60)
    logger.info("Iniciando Chatbot con Llama3")
    logger.info("="*60)
    
    try:
        validate_config()
        logger.info("✓ Configuración validada")

        if not check_ollama_connection():
            logger.error(
                "No se pudo conectar con Ollama. "
                "Asegúrate de que el servicio esté activo y el modelo instalado."
            )
            logger.info(f"Comando para instalar el modelo: ollama pull {MODEL_NAME}")
            return

        start_session_monitor()
        logger.info("✓ Monitor de sesiones iniciado")

        iface = create_interface()
        logger.info("✓ Interfaz creada")

        logger.info(f"Iniciando servidor en {GRADIO_SERVER_NAME}:{GRADIO_SERVER_PORT}")
        iface.launch(
            server_name=GRADIO_SERVER_NAME,
            server_port=GRADIO_SERVER_PORT,
            share=GRADIO_SHARE,
            inbrowser=True
        )
        
    except KeyboardInterrupt:
        logger.info("\n👋 Aplicación detenida por el usuario")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}", exc_info=True)
        raise