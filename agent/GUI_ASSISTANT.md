# Asistente GUI de F3-OS

## Visión

El agente gobernante de F3-OS también funciona como **asistente/amigo del usuario** dentro de la interfaz gráfica del sistema operativo.

## Características

### 🤖 Asistente Inteligente

- **Conversacional**: Interfaz de chat amigable
- **Contexto del Sistema**: Conoce la fase actual del sistema F3
- **Personalidad Adaptable**: Se adapta al contexto y usuario
- **Sugerencias**: Ofrece sugerencias de preguntas/comandos

### 💬 Capacidades

El asistente puede ayudar con:

- **Explicar el modelo F3**: Qué son los 3 hilos, el embudo, el ciclo de fases
- **Estado del sistema**: Fase actual, entropía, perfection score
- **Navegación**: Ayudar a navegar por el sistema
- **Desarrollo**: Responder preguntas sobre desarrollo y contribución
- **Conversación general**: Interactuar de forma amigable

### 🎨 Integración con GUI

El asistente se integra con la GUI de F3-OS mediante:

1. **API HTTP**: Servidor HTTP simple en `localhost:8080`
2. **Callbacks**: Sistema de callbacks para actualizaciones en tiempo real
3. **Estado compartido**: Acceso al estado del sistema F3

## Uso

### Desde Python

```python
from src.gui_integration import GUIIntegration, AssistantAPI
from src.governance_core import GovernanceCore
from src.resource_manager import ResourceManager

# Inicializar
governance = GovernanceCore(config, data_dir)
resource_manager = ResourceManager(config)
gui = GUIIntegration(governance, resource_manager, config)

# API simplificada
api = AssistantAPI(gui)

# Abrir asistente
greeting = api.open()

# Hacer pregunta
response = api.ask("¿Qué es el modelo F3?")

# Obtener estado para renderizado
state = api.get_state()
```

### Desde HTTP (para GUI del sistema)

```bash
# Abrir asistente
curl -X POST http://localhost:8080/assistant/open

# Enviar mensaje
curl -X POST http://localhost:8080/assistant/message \
  -H "Content-Type: application/json" \
  -d '{"message": "¿En qué fase está el sistema?"}'

# Obtener estado
curl http://localhost:8080/assistant/status

# Obtener sugerencias
curl http://localhost:8080/assistant/suggestions
```

### Iniciar Servidor HTTP

```python
from src.gui_server import GUIServer

server = GUIServer(gui, port=8080)
server.start()
```

## Personalidad

El asistente tiene 3 personalidades configurables:

- **friendly**: Amigable y conversacional
- **technical**: Técnico y preciso
- **adaptive**: Se adapta al contexto (por defecto)

Configurar en `config/config.yaml`:

```yaml
gui_assistant:
  personality: "adaptive"
  user_name: "Usuario"
  context_aware: true
```

## Límites de Recursos

El asistente respeta los mismos límites de recursos que el agente gobernante:
- Máximo 20% CPU
- Objetivo 15% CPU
- Throttling automático entre operaciones

## Integración con Kernel

Para integrar con la GUI del kernel de F3-OS:

1. **Iniciar servidor HTTP** cuando el sistema arranque
2. **Conectar GUI** al servidor en `localhost:8080`
3. **Renderizar ventana** del asistente en la GUI
4. **Actualizar en tiempo real** usando callbacks

## Ejemplo de Ventana GUI

```rust
// En el kernel (pseudo-código)
struct AssistantWindow {
    is_open: bool,
    conversation: Vec<Message>,
    suggestions: Vec<String>,
}

impl AssistantWindow {
    fn open(&mut self) {
        // Llamar a API HTTP
        let response = http_post("http://localhost:8080/assistant/open");
        self.is_open = true;
    }
    
    fn send_message(&mut self, message: &str) {
        let response = http_post("http://localhost:8080/assistant/message", 
                                 json!({"message": message}));
        // Actualizar conversación
    }
}
```

## Próximos Pasos

1. **Implementar GUI en el kernel**: Ventana gráfica del asistente
2. **Integrar con sistema de ventanas**: Cuando se implemente
3. **Mejorar respuestas**: Usar AI para respuestas más naturales
4. **Agregar comandos**: Comandos del sistema desde el asistente

## Notas

- El asistente comparte el mismo agente gobernante
- Respeta límites de recursos (15-20% CPU)
- Mantiene contexto del sistema F3
- Historial de conversación persistente


