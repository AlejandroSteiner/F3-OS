# Ejecución Rápida del Agente

## ⚠️ IMPORTANTE: Estar en el Directorio Correcto

**Debes estar en el directorio `agent/` para ejecutar el agente:**

```bash
cd agent
./run.sh status
```

## 🚀 Comandos Rápidos

### 1. Ver Estado
```bash
cd agent
./run.sh status
```

### 2. Iniciar Servidor GUI
```bash
cd agent
./run.sh gui-server
```

### 3. Monitorear PRs (requiere GitHub)
```bash
cd agent
./run.sh monitor
```

## 📍 Ubicación Correcta

**❌ Incorrecto (directorio raíz):**
```bash
cd /home/ktzchen/Documentos/f3-os
./run.sh status  # Esto ejecuta QEMU, no el agente
```

**✅ Correcto (directorio agent):**
```bash
cd /home/ktzchen/Documentos/f3-os/agent
./run.sh status  # Esto ejecuta el agente
```

## 🎯 Resumen

**Para el agente:**
```bash
cd agent
./run.sh [comando]
```

**Para F3-OS (QEMU):**
```bash
./run_safe.sh  # Desde directorio raíz
```

---

**Siempre ejecuta el agente desde `agent/`** 📁


