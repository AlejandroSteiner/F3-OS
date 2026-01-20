# Guía de Uso del Agente F3-OS

## ⚠️ Errores Comunes y Soluciones

### Error: "cd: agent: No existe el archivo o el directorio"

**Problema:** Ya estás en el directorio `agent/`, no necesitas hacer `cd agent` de nuevo.

**Solución:** Simplemente ejecuta:
```bash
./run.sh status
# NO hagas: cd agent && ./run.sh status
```

### Error: "Address already in use" (Puerto 8080 ocupado)

**Problema:** Hay un servidor GUI corriendo en segundo plano.

**Solución 1 - Usar el script:**
```bash
./detener_servidor.sh
```

**Solución 2 - Manual:**
```bash
# Encontrar proceso
lsof -ti :8080

# Detener proceso
kill $(lsof -ti :8080)

# O forzar si no se detiene
kill -9 $(lsof -ti :8080)
```

**Solución 3 - Usar otro puerto:**
```bash
./run.sh gui-server --port 8081
# Luego abre: http://localhost:8081
```

### Error: "kernel.bin: No existe el archivo o el directorio"

**Problema:** Estás buscando `kernel.bin` desde el directorio `agent/`, pero está en la raíz del proyecto.

**Solución:** Ve a la raíz del proyecto:
```bash
cd ..
ls -lh kernel.bin f3os.iso
```

O desde `agent/`:
```bash
ls -lh ../kernel.bin ../f3os.iso
```

## 📍 Ubicación de Archivos

### Desde el directorio `agent/`:

```
f3-os/
├── agent/          ← Estás aquí
│   ├── run.sh
│   ├── src/
│   └── ...
├── kernel.bin       ← Está aquí (raíz)
├── f3os.iso         ← Está aquí (raíz)
└── build.sh         ← Está aquí (raíz)
```

### Comandos correctos desde `agent/`:

```bash
# Ver estado del agente
./run.sh status

# Iniciar servidor GUI
./run.sh gui-server

# Detener servidor GUI
./detener_servidor.sh

# Verificar kernel (desde raíz)
cd ..
ls -lh kernel.bin f3os.iso
```

## 🚀 Comandos Principales

### Desde `agent/`:

```bash
# Estado del agente
./run.sh status

# Servidor GUI (puerto 8080)
./run.sh gui-server

# Servidor GUI (otro puerto)
./run.sh gui-server --port 8081

# Monitorear PRs (requiere token GitHub)
./run.sh monitor

# Evaluar PR (requiere token GitHub)
./run.sh evaluate-pr --pr 1

# Ciclo completo (requiere token GitHub)
./run.sh cycle
```

### Desde la raíz del proyecto:

```bash
# Compilar kernel
./build.sh

# Crear ISO
./create_grub_iso.sh

# Ejecutar F3-OS en QEMU
./run_safe.sh

# Verificar sistema
./verificar_sistema.sh
```

## 🔍 Verificar que el Servidor Está Corriendo

```bash
# Verificar puerto 8080
lsof -i :8080

# Ver procesos del agente
ps aux | grep "gui-server\|run_agent"

# Probar conexión
curl http://localhost:8080/api/status
```

## 🛑 Detener el Servidor

### Método 1 - Script automático:
```bash
./detener_servidor.sh
```

### Método 2 - Manual:
```bash
# Encontrar y detener
kill $(lsof -ti :8080)

# O forzar
kill -9 $(lsof -ti :8080)
```

### Método 3 - Desde la terminal donde corre:
Presiona `Ctrl+C`

## ✅ Checklist de Verificación

Cuando ejecutes `./run.sh status`, deberías ver:

```
📊 Estado del Agente F3-OS
============================================================
Fase actual: LOGICAL
Entropía: 0/255
Perfection Score: 0
Ciclos completados: 0

✅ Recursos del Agente:
  CPU: X.X% (límite: 20.0%)
  Memoria: XX.X MB
```

Si ves esto, **el agente está funcionando correctamente**.

## 🌐 Acceder al Servidor GUI

1. **Inicia el servidor:**
   ```bash
   ./run.sh gui-server
   ```

2. **Abre en navegador:**
   ```
   http://localhost:8080
   ```

3. **Deberías ver:**
   - Panel de estado del agente
   - Campo de chat
   - Interfaz del asistente

## 💡 Consejos

1. **No hagas `cd agent` si ya estás en `agent/`**
   - Verifica con: `pwd`
   - Si estás en `/home/ktzchen/Documentos/f3-os/agent`, ya estás en el lugar correcto

2. **Si el puerto está ocupado, detén el proceso anterior**
   - Usa: `./detener_servidor.sh`

3. **Los archivos del kernel están en la raíz**
   - `kernel.bin` y `f3os.iso` están en `f3-os/`, no en `agent/`

4. **El agente funciona sin token de GitHub**
   - `status` y `gui-server` funcionan sin token
   - Solo `monitor` y `evaluate-pr` requieren token

---

**Recuerda: Si ya estás en `agent/`, solo ejecuta `./run.sh [comando]` sin hacer `cd agent` primero.**

