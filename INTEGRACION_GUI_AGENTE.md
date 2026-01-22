# Integración GUI del Agente con F3-OS

## 🌐 Configuración de Red

F3-OS ahora tiene acceso a la red para comunicarse con el servidor GUI del agente que corre en el host.

### Configuración Automática

El script `run_safe.sh` ahora incluye:
- **User Networking**: Red virtual aislada pero accesible
- **Port Forwarding**: Puerto 8080 redirigido automáticamente
- **Acceso al Host**: F3-OS puede acceder al host en `10.0.2.2`

### Direcciones de Red

- **Desde F3-OS (dentro de QEMU)**: `http://10.0.2.2:8080`
  - `10.0.2.2` es la IP del host desde la perspectiva de QEMU
  - El puerto 8080 está redirigido automáticamente

- **Desde el Host (Ubuntu)**: `http://localhost:8080`
  - Acceso normal desde el sistema principal

### Servidor GUI Configurado

El servidor GUI del agente ahora:
- Escucha en `0.0.0.0:8080` (todas las interfaces)
- Accesible desde el host y desde F3-OS
- Muestra ambas URLs al iniciar

## 🚀 Uso

### 1. Iniciar el Servidor GUI del Agente

```bash
cd agent
./run.sh gui-server
```

Verás:
```
🌐 Servidor GUI del asistente iniciado en http://0.0.0.0:8080
📱 Accesible desde:
   - Host: http://localhost:8080
   - F3-OS (QEMU): http://10.0.2.2:8080
```

### 2. Iniciar F3-OS con Red

```bash
./run_safe.sh
```

F3-OS ahora tiene acceso a la red y puede:
- Acceder al servidor GUI en `http://10.0.2.2:8080`
- Comunicarse con el agente gobernante
- Usar la interfaz del asistente desde dentro del sistema operativo

## 🔧 Implementación en el Kernel

El kernel de F3-OS puede acceder al servidor GUI usando:

```rust
// Ejemplo de acceso desde F3-OS
let gui_url = "http://10.0.2.2:8080";
// Hacer petición HTTP al servidor GUI
```

### Integración con GUI del Kernel

La GUI del kernel (`kernel/src/gui/`) puede:
- Hacer peticiones HTTP al servidor del agente
- Mostrar la interfaz del asistente dentro de F3-OS
- Integrar el asistente como parte del sistema operativo

## 🔒 Seguridad

- **Red Aislada**: User networking mantiene F3-OS aislado
- **Solo Puerto 8080**: Solo el puerto necesario está expuesto
- **Sin Acceso Inverso**: F3-OS no puede acceder a otros puertos del host
- **Aislamiento Mantenido**: El sistema sigue siendo seguro

## 📝 Notas Técnicas

### User Networking en QEMU

- **IP del Host**: `10.0.2.2` (desde F3-OS)
- **IP de F3-OS**: `10.0.2.15` (asignada automáticamente)
- **DNS**: `10.0.2.3` (proxy DNS de QEMU)
- **Gateway**: `10.0.2.2`

### Port Forwarding

El formato es: `hostfwd=tcp::8080-:8080`
- Puerto del host: `8080`
- Puerto de destino: `8080`
- Protocolo: TCP

## ✅ Verificación

Para verificar que funciona:

1. **Desde el Host:**
   ```bash
   curl http://localhost:8080/api/status
   ```

2. **Desde F3-OS (cuando tenga soporte HTTP):**
   ```bash
   # Dentro de F3-OS
   curl http://10.0.2.2:8080/api/status
   ```

---

**F3-OS ahora puede acceder al servidor GUI del agente desde dentro del emulador.** ✅




