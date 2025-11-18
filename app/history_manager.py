from langchain_community.chat_message_histories import SQLChatMessageHistory
from .config import DB_PATH, MAX_HISTORY_MESSAGES
import logging

logger = logging.getLogger(__name__)


def get_sql_history(session_id: str) -> SQLChatMessageHistory:
    """
    Obtiene el historial de chat desde la base de datos SQLite.
    
    Args:
        session_id: ID único de la sesión
        
    Returns:
        Objeto SQLChatMessageHistory con el historial de la sesión
    """
    try:
        history = SQLChatMessageHistory(
            session_id=session_id,
            connection_string=DB_PATH
        )
        messages = history.messages
        
        if len(messages) > MAX_HISTORY_MESSAGES:
            logger.warning(
                f"Historial muy largo para sesión {session_id[:8]}... "
                f"({len(messages)} mensajes). Considerando limpieza."
            )
        
        return history
        
    except Exception as e:
        logger.error(f"Error al obtener historial para sesión {session_id[:8]}: {e}")
        raise


def clear_old_sessions(days_old: int = 7):
    """
    Limpia sesiones antiguas de la base de datos.
    
    Args:
        days_old: Eliminar sesiones más antiguas que este número de días
    """
    import sqlite3
    from datetime import datetime, timedelta
    
    try:
        db_file = DB_PATH.replace("sqlite:///", "")
        
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days_old)

        cursor.execute("""
            DELETE FROM message_store 
            WHERE session_id IN (
                SELECT DISTINCT session_id 
                FROM message_store 
                GROUP BY session_id 
                HAVING MAX(id) < ?
            )
        """, (cutoff_date.timestamp(),))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"Limpiadas {deleted} sesiones antiguas (>{days_old} días)")
        return deleted
        
    except Exception as e:
        logger.error(f"Error al limpiar sesiones antiguas: {e}")
        return 0


def get_session_message_count(session_id: str) -> int:
    """
    Cuenta los mensajes en una sesión.
    
    Args:
        session_id: ID de la sesión
        
    Returns:
        Número de mensajes en la sesión
    """
    try:
        history = get_sql_history(session_id)
        return len(history.messages)
    except Exception as e:
        logger.error(f"Error al contar mensajes: {e}")
        return 0