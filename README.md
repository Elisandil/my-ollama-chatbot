# 🤖 Chatbot con Llama3 via Ollama

Chatbot inteligente construido con LangChain, Ollama y Gradio, con gestión avanzada de sesiones y persistencia de conversaciones.

## ✨ Características

- 🔄 **Streaming de respuestas** en tiempo real
- 💾 **Persistencia de historial** con SQLite
- 🔐 **Gestión de sesiones** por usuario con UUID único
- ⏱️ **Heartbeat automático** para mantener sesiones activas
- 🧹 **Limpieza automática** de sesiones inactivas
- 📝 **Logging completo** para debugging
- ⚙️ **Configuración flexible** mediante variables de entorno
- 🛡️ **Manejo robusto de errores**

## 📋 Requisitos Previos

- Python 3.8+
- Ollama instalado y en ejecución
- Modelo Llama3 descargado en Ollama

## 🚀 Instalación

### 1. Instalar Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: descargar desde https://ollama.com/download
```

### 2. Descargar el modelo Llama3

```bash
ollama pull llama3:latest
```

### 3. Clonar e instalar dependencias

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd chatbot-llama3

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Configurar variables de entorno (opcional)

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar según tus necesidades
nano .env
```

## 🎮 Uso

### Iniciar el chatbot

```bash
python run.py
```

El navegador se abrirá automáticamente en `http://localhost:7860`

### Verificar que Ollama está activo

```bash
# En otra terminal
ollama list
```

## 🏗️ Estructura del Proyecto

```
app/
├── __init__.py
├── config.py              # Configuración centralizada
├── gradio_app.py          # Aplicación principal
├── ui.py                  # Interfaz de Gradio
├── chatbot_logic.py       # Lógica del chatbot
├── session_manager.py     # Gestión de sesiones
└── history_manager.py     # Gestión de historial

run.py                     # Punto de entrada
requirements.txt           # Dependencias
.env.example              # Ejemplo de configuración
```

## ⚙️ Configuración

### Variables de Entorno Disponibles

| Variable | Descripción | Por Defecto |
|----------|-------------|-------------|
| `MODEL_NAME` | Modelo de Ollama a usar | `llama3:latest` |
| `OLLAMA_BASE_URL` | URL del servidor Ollama | `http://localhost:11434` |
| `MAX_TOKENS` | Máximo de tokens por respuesta | `2048` |
| `SESSION_TIMEOUT` | Timeout de sesión (segundos) | `600` (10 min) |
| `DB_PATH` | Ruta de base de datos | `sqlite:///chat_history.db` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |
| `GRADIO_SERVER_PORT` | Puerto del servidor | `7860` |
| `MAX_MESSAGE_LENGTH` | Longitud máxima de mensaje | `4000` |
| `MAX_HISTORY_MESSAGES` | Mensajes máximos en historial | `50` |

## 🔧 Mejoras Implementadas

### Respecto a la Versión Original

1. ✅ **Sistema de sesiones corregido**: Usa UUID único por usuario en lugar de PID compartido
2. ✅ **Prompt mejorado**: Sistema prompt más útil y específico
3. ✅ **Manejo de errores robusto**: Try-catch en todas las operaciones críticas
4. ✅ **Validación de Ollama**: Verifica disponibilidad antes de iniciar
5. ✅ **Configuración externa**: Variables de entorno en lugar de hardcoded
6. ✅ **Logging apropiado**: Sistema de logging completo
7. ✅ **Thread-safe**: Uso de locks para operaciones concurrentes
8. ✅ **Validación de entrada**: Sanitización de inputs del usuario
9. ✅ **UI mejorada**: Ejemplos, mejor UX, temas de Gradio

## 🐛 Solución de Problemas

### Error: "No se puede conectar con Ollama"

```bash
# Verificar que Ollama está activo
ollama serve

# En otra terminal
ollama list
```

### Error: "Modelo no encontrado"

```bash
# Descargar el modelo
ollama pull llama3:latest
```

### Sesiones expiran demasiado rápido

```bash
# Aumentar el timeout en .env
SESSION_TIMEOUT=1800  # 30 minutos
```

### Base de datos bloqueada

```bash
# Eliminar la base de datos y reiniciar
rm chat_history.db
python run.py
```

## 📊 Monitoreo

El sistema genera logs detallados:

```
2024-XX-XX XX:XX:XX - session_manager - INFO - Sesión registrada: 12345678...
2024-XX-XX XX:XX:XX - chatbot_logic - INFO - Procesando pregunta para sesión 12345678...
2024-XX-XX XX:XX:XX - session_manager - INFO - Limpiadas 2 sesiones. Activas: 5
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 👤 Autor

**Antonio Ortega**

## 🙏 Agradecimientos

- [LangChain](https://python.langchain.com/) - Framework de LLM
- [Ollama](https://ollama.com/) - Servidor de modelos locales
- [Gradio](https://gradio.app/) - UI para ML
- [Meta](https://ai.meta.com/) - Modelo Llama3