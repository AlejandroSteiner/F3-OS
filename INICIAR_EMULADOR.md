# Cómo Iniciar el Emulador F3-OS

## 🚀 Método Automático (Recomendado)

### Opción 1: Sistema Completo (Servidor GUI + QEMU)

```bash
./iniciar_sistema_completo.sh
```

Este script:
- ✅ Verifica que el servidor GUI esté corriendo
- ✅ Lo inicia automáticamente si no está
- ✅ Abre QEMU con red habilitada
- ✅ F3-OS puede acceder al servidor GUI en `http://10.0.2.2:8080`

### Opción 2: Solo Emulador (si el servidor GUI ya está corriendo)

```bash
./abrir_emulador_ventana.sh
```

O simplemente:
```bash
./run_safe.sh
```

## 📋 Pasos Manuales

Si los scripts automáticos no funcionan:

### 1. Iniciar Servidor GUI

```bash
cd agent
./run.sh gui-server
```

Deja esta terminal abierta.

### 2. En otra terminal, iniciar QEMU

```bash
cd /home/ktzchen/Documentos/f3-os
./run_safe.sh
```

## 🔍 Verificación

### Verificar que el servidor GUI está corriendo:

```bash
curl http://localhost:8080/api/status
```

Deberías recibir un JSON con el estado del agente.

### Verificar que QEMU se abrió:

La ventana de QEMU debería aparecer automáticamente. Si no aparece:

1. **Verifica que QEMU esté instalado:**
   ```bash
   which qemu-system-x86_64
   ```

2. **Verifica que el kernel esté compilado:**
   ```bash
   ls -la kernel.bin f3os.iso
   ```

3. **Ejecuta QEMU manualmente para ver errores:**
   ```bash
   qemu-system-x86_64 -cdrom f3os.iso -display gtk -m 256M
   ```

## 🌐 Acceso desde F3-OS

Una vez que F3-OS esté corriendo en QEMU:

- **Servidor GUI del agente**: `http://10.0.2.2:8080`
- **API del agente**: `http://10.0.2.2:8080/api/status`
- **Interfaz web**: `http://10.0.2.2:8080` (cuando el kernel tenga soporte HTTP)

## ⚠️ Problemas Comunes

### QEMU no se abre

- Verifica que `DISPLAY` esté configurado: `echo $DISPLAY`
- Prueba con `-display sdl` en lugar de `-display gtk`
- Ejecuta desde una sesión gráfica (no SSH sin X11 forwarding)

### Servidor GUI no responde

- Verifica que esté corriendo: `lsof -i :8080`
- Revisa los logs: `cat /tmp/f3os_gui_server.log`
- Reinicia: `cd agent && ./detener_servidor.sh && ./run.sh gui-server`

### Red no funciona en QEMU

- Verifica que el script incluya las opciones de red
- Asegúrate de que el servidor GUI escuche en `0.0.0.0:8080`

---

**Para iniciar todo automáticamente: `./iniciar_sistema_completo.sh`**

