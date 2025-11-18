# MyChatbot con Llama3 via Ollama

Chatbot inteligente construido con LangChain, Ollama y Gradio, con gestión avanzada de sesiones y persistencia de conversaciones.

## Requisitos

- Python 3.8+
- Ollama instalado y en ejecución
- Modelo Llama3 descargado en Ollama

## Instalación

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

# Linux/Mac
source venv/bin/activate
# Windows (Git Bash)
source venv/Scripts/activate
# Windows (CMD)
venv\Scripts\activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Configurar variables de entorno (opcional)

```bash
# Copiar archivo de ejemplo
cp .env.template .env

# Editar según tus necesidades
nano .env
```

## Uso

### Iniciar el chatbot

```bash
python run.py
```

El navegador se abrirá automáticamente en `http://localhost:7860`

## Estructura del Proyecto

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
.env.template              # Ejemplo de configuración
```

## Solución de Problemas

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

## Monitoreo

El sistema genera logs detallados:

```
2024-XX-XX XX:XX:XX - session_manager - INFO - Sesión registrada: 12345678...
2024-XX-XX XX:XX:XX - chatbot_logic - INFO - Procesando pregunta para sesión 12345678...
2024-XX-XX XX:XX:XX - session_manager - INFO - Limpiadas 2 sesiones. Activas: 5
```

## Licencia

Este proyecto está bajo la Licencia MIT.

## Autor

**Antonio Ortega**
