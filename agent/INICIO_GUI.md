# Inicio Rápido - GUI del Asistente

## 🚀 Pasos Simples

### 1. Iniciar Servidor

**Desde el directorio `agent/`:**
```bash
cd agent
./run.sh gui-server
```

**O si ya estás en `agent/`:**
```bash
./run.sh gui-server
```

### 2. Abrir en Navegador

**Abre tu navegador y ve a:**
```
http://localhost:8080
```

### 3. ¡Listo!

Verás la interfaz web del asistente donde puedes:
- Ver el estado del agente
- Chatear con el asistente
- Hacer consultas sobre F3-OS

## 🖥️ Interfaz Web

**Lo que verás:**
- Panel de estado (arriba) - Se actualiza automáticamente
- Campo de chat (centro) - Escribe y presiona Enter
- Respuestas del asistente - Aparecen en tiempo real

## 💬 Ejemplos de Consultas

```
¿Qué es el modelo F3?
¿Cuál es el estado actual?
¿Qué fase estamos en?
Explícame el ciclo adaptativo
```

## ⚠️ Si el Servidor No Responde

1. **Verifica que esté corriendo:**
   ```bash
   ps aux | grep gui-server
   ```

2. **Verifica el puerto:**
   ```bash
   netstat -tuln | grep 8080
   ```

3. **Si el puerto está ocupado:**
   ```bash
   ./run.sh gui-server --port 8081
   ```
   Luego abre: `http://localhost:8081`

## ✅ Verificación

Si ves la página web con el asistente, **está funcionando correctamente.**

---

**Solo ejecuta `./run.sh gui-server` y abre http://localhost:8080** 🎯




