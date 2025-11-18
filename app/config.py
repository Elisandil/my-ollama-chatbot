import os
from pathlib import Path

# ===== CONFIGURACIÓN DEL MODELO =====
MODEL_NAME = os.getenv("MODEL_NAME", "llama3:latest")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))

# ===== CONFIGURACIÓN DE SESIONES =====
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "600")) 

# ===== CONFIGURACIÓN DE BASE DE DATOS =====
DB_PATH = os.getenv("DB_PATH", "sqlite:///chat_history.db")

# ===== CONFIGURACIÓN DE LOGGING =====
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ===== CONFIGURACIÓN DE GRADIO =====
GRADIO_SERVER_NAME = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
GRADIO_SERVER_PORT = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
GRADIO_SHARE = os.getenv("GRADIO_SHARE", "False").lower() == "true"

# ===== LÍMITES Y RESTRICCIONES =====
MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "4000"))
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "50"))


def validate_config():
    """
    Valida que la configuración sea correcta.
    """
    errors = []
    
    if SESSION_TIMEOUT < 60:
        errors.append("SESSION_TIMEOUT debe ser al menos 60 segundos")
    
    if MAX_TOKENS < 100:
        errors.append("MAX_TOKENS debe ser al menos 100")
    
    if MAX_MESSAGE_LENGTH < 10:
        errors.append("MAX_MESSAGE_LENGTH debe ser al menos 10")
    
    if errors:
        raise ValueError(f"Errores en configuración: {', '.join(errors)}")
    
    return True