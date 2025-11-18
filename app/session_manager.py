import time
import threading
from typing import Dict
from .config import SESSION_TIMEOUT
import logging

logger = logging.getLogger(__name__)
sessions: Dict[str, float] = {}
sessions_lock = threading.Lock()


def register_session(session_id: str) -> bool:
    """
    Registra una nueva sesión.
    
    Args:
        session_id: ID único de la sesión
        
    Returns:
        True si se registró exitosamente
    """
    with sessions_lock:
        sessions[session_id] = time.time()
        logger.info(f"Sesión registrada: {session_id[:8]}...")
        return True


def heartbeat(session_id: str) -> str:
    """
    Actualiza el timestamp de la sesión para mantenerla viva.
    
    Args:
        session_id: ID de la sesión
        
    Returns:
        Estado de la sesión
    """
    with sessions_lock:
        if session_id in sessions:
            sessions[session_id] = time.time()
            return "alive"
        else:
            logger.warning(f"Heartbeat para sesión inexistente: {session_id[:8]}...")
            return "expired"


def get_session_info(session_id: str) -> dict:
    """
    Obtiene información sobre una sesión.
    
    Args:
        session_id: ID de la sesión
        
    Returns:
        Diccionario con información de la sesión
    """
    with sessions_lock:
        if session_id in sessions:
            last_activity = sessions[session_id]
            age = time.time() - last_activity
            return {
                "exists": True,
                "last_activity": last_activity,
                "age_seconds": age,
                "is_active": age < SESSION_TIMEOUT
            }
        return {"exists": False}


def session_cleaner(timeout: int = SESSION_TIMEOUT):
    """
    Limpia sesiones expiradas periódicamente.
    
    Args:
        timeout: Tiempo en segundos antes de considerar una sesión expirada
    """
    logger.info(f"Iniciando limpiador de sesiones (timeout: {timeout}s)")
    
    while True:
        try:
            now = time.time()
            
            with sessions_lock:
                dead_sessions = [
                    sid for sid, last in sessions.items() 
                    if now - last > timeout
                ]
                
                for sid in dead_sessions:
                    logger.info(f"Limpiando sesión expirada: {sid[:8]}...")
                    del sessions[sid]
                
                if dead_sessions:
                    logger.info(f"Limpiadas {len(dead_sessions)} sesiones. "
                              f"Activas: {len(sessions)}")
            
            time.sleep(5)
            
        except Exception as e:
            logger.error(f"Error en session_cleaner: {e}")
            time.sleep(5)


def get_active_sessions_count() -> int:
    """
    Retorna el número de sesiones activas.
    """
    with sessions_lock:
        return len(sessions)


def start_session_monitor():
    """
    Inicia el monitor de sesiones en un thread daemon.
    """
    cleaner_thread = threading.Thread(
        target=session_cleaner,
        daemon=True,
        name="SessionCleaner"
    )
    cleaner_thread.start()
    logger.info("Monitor de sesiones iniciado")