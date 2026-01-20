# Cómo Navegar en el GUI del Asistente

## 🚀 Inicio Rápido

### 1. Iniciar el Servidor GUI

```bash
cd agent
./run.sh gui-server
```

Verás:
```
🌐 Servidor GUI del asistente iniciado en http://localhost:8080
📱 Abre en tu navegador: http://localhost:8080
💬 Interfaz web disponible para chatear con el asistente
```

### 2. Abrir en el Navegador

**Abre tu navegador web y ve a:**
```
http://localhost:8080
```

## 🖥️ Interfaz Web

### Lo que Verás

1. **Panel de Estado** (arriba):
   - Fase actual del agente (LOGICAL, ILLOGICAL, SYNTHESIS, PERFECT)
   - Entropía (0-255)
   - Perfection Score
   - Uso de CPU

2. **Chat con el Asistente** (centro):
   - Historial de conversación
   - Campo para escribir consultas
   - Botón "Enviar"

### Cómo Usar

1. **Escribe tu consulta** en el campo de texto
2. **Presiona Enter** o click en "Enviar"
3. **El asistente responde** basándose en:
   - Tu consulta
   - El estado actual del sistema F3
   - El contexto del proyecto

### Ejemplos de Consultas

```
¿Qué es el modelo F3?
¿Cuál es el estado actual del sistema?
¿Qué fase estamos en?
Explícame el ciclo adaptativo
¿Cómo funciona el embudo?
```

## 🔌 API REST (Opcional)

Si prefieres usar la API directamente:

### Obtener Estado
```bash
curl http://localhost:8080/api/status
```

### Enviar Consulta
```bash
curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "¿Qué es el modelo F3?"}'
```

## 📱 Desde F3-OS (Futuro)

Cuando F3-OS tenga GUI completa, se conectará automáticamente a:
- `http://localhost:8080`
- O a través de WebSocket (si se implementa)

## 🎯 Funcionalidades

**El asistente puede:**
- ✅ Responder preguntas sobre F3-OS
- ✅ Explicar el modelo F3
- ✅ Mostrar estado del sistema
- ✅ Ayudar con navegación
- ✅ Proporcionar contexto del proyecto

**Todo sin necesidad de GitHub configurado.**

---

**Abre http://localhost:8080 en tu navegador y comienza a chatear.** 💬

