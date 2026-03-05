# Verificación del Sistema F3-OS

Guía completa para verificar que todos los componentes del sistema están funcionando correctamente.

## 🚀 Verificación Rápida

### Script Automático

**Ejecuta el script de verificación:**
```bash
./verificar_sistema.sh
```

Este script verifica:
- ✅ Estructura del proyecto
- ✅ Kernel compilado
- ✅ Agente gobernante
- ✅ Dependencias instaladas
- ✅ Configuración correcta
- ✅ Herramientas de build

## 📋 Verificación Manual Paso a Paso

### 1. Verificar Kernel

**Compilar kernel:**
```bash
./build.sh
```

**Verificar que compiló:**
```bash
ls -lh kernel.bin
file kernel.bin
# Debe mostrar: "kernel.bin: ELF 64-bit LSB executable"
```

**Crear ISO:**
```bash
./create_grub_iso.sh
ls -lh f3os.iso
```

### 2. Verificar Agente Gobernante

**Ver estado del agente:**
```bash
cd agent
./run.sh status
```

**Deberías ver:**
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

**Si hay errores:**
- Verifica que Python 3 esté instalado: `python3 --version`
- Verifica entorno virtual: `ls agent/venv/`
- Instala dependencias: `cd agent && pip install -r requirements.txt`

### 3. Verificar Servidor GUI

**Iniciar servidor:**
```bash
cd agent
./run.sh gui-server
```

**Deberías ver:**
```
🎨 Iniciando servidor GUI del asistente en puerto 8080...
📊 Monitoreo de recursos iniciado (límite: 20.0% CPU)
🌐 Servidor GUI del asistente iniciado en http://localhost:8080
✅ Servidor iniciado. GUI puede conectarse a http://localhost:8080
```

**Probar en navegador:**
1. Abre: `http://localhost:8080`
2. Deberías ver la interfaz web del asistente
3. Prueba enviar un mensaje: "Hola"

**Si el puerto está ocupado:**
```bash
./run.sh gui-server --port 8081
# Luego abre: http://localhost:8081
```

### 4. Verificar Análisis de Proyecto

**Probar capacidad de análisis:**
1. Abre el servidor GUI: `./run.sh gui-server`
2. Abre `http://localhost:8080`
3. Prueba estas preguntas:
   - "¿Cuáles son tus reglas?"
   - "Explicame desde cero"
   - "¿Qué es el modelo F3?"

**Deberías recibir respuestas detalladas basadas en los archivos del proyecto.**

### 5. Verificar Ejecución de F3-OS

**Ejecutar en QEMU:**
```bash
./run_safe.sh
```

**Deberías ver:**
- Ventana QEMU abriéndose
- Mensajes de boot del kernel
- Sistema funcionando

**Si QEMU no está instalado:**
```bash
sudo apt install qemu-system-x86
```

## 🔍 Diagnóstico de Problemas

### Problema: "kernel.bin no encontrado"

**Solución:**
```bash
./build.sh
```

### Problema: "Python 3 no encontrado"

**Solución:**
```bash
sudo apt install python3 python3-venv
```

### Problema: "Dependencias no instaladas"

**Solución:**
```bash
cd agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Problema: "Puerto 8080 ya en uso"

**Solución:**
```bash
# Encontrar proceso usando el puerto
lsof -i :8080
# O usar otro puerto
./run.sh gui-server --port 8081
```

### Problema: "Token de GitHub no configurado"

**Solución (opcional):**
```bash
cd agent
./setup_config.sh
```

**Nota:** El agente funciona sin token, pero algunas funciones (monitoreo de PRs) requieren token.

### Problema: "QEMU no encontrado"

**Solución:**
```bash
sudo apt install qemu-system-x86
```

## ✅ Checklist de Verificación

Marca cada elemento cuando esté funcionando:

- [ ] Kernel compila sin errores (`./build.sh`)
- [ ] ISO se crea correctamente (`./create_grub_iso.sh`)
- [ ] Agente muestra estado (`cd agent && ./run.sh status`)
- [ ] Servidor GUI inicia (`cd agent && ./run.sh gui-server`)
- [ ] Interfaz web accesible (`http://localhost:8080`)
- [ ] Asistente responde preguntas
- [ ] Análisis de proyecto funciona ("¿Cuáles son tus reglas?")
- [ ] F3-OS ejecuta en QEMU (`./run_safe.sh`)

## 📊 Comandos de Diagnóstico

### Ver estado completo del agente
```bash
cd agent
./run.sh status
```

### Verificar recursos del agente
```bash
cd agent
./run.sh status | grep -A 5 "Recursos"
```

### Verificar que el servidor GUI está corriendo
```bash
curl http://localhost:8080/api/status
```

### Verificar procesos del agente
```bash
ps aux | grep "gui-server\|main.py"
```

### Verificar puerto
```bash
netstat -tuln | grep 8080
# O
lsof -i :8080
```

### Verificar logs (si existen)
```bash
cd agent
ls -la logs/
cat logs/*.log 2>/dev/null
```

## 🎯 Verificación Rápida (30 segundos)

**Ejecuta estos 3 comandos:**

```bash
# 1. Verificar agente
cd agent && ./run.sh status && cd ..

# 2. Verificar kernel
ls -lh kernel.bin f3os.iso 2>/dev/null && echo "✅ Kernel e ISO existen" || echo "⚠️  Compila con ./build.sh"

# 3. Verificar herramientas
command -v python3 && command -v rustc && command -v qemu-system-x86_64 && echo "✅ Herramientas instaladas" || echo "⚠️  Faltan herramientas"
```

## 🚨 Señales de que el Sistema Funciona Correctamente

### ✅ Agente
- `./run.sh status` muestra información del estado
- CPU del agente está por debajo del 20%
- No hay errores en la salida

### ✅ Servidor GUI
- `./run.sh gui-server` inicia sin errores
- `http://localhost:8080` muestra la interfaz web
- El asistente responde a preguntas
- Las respuestas son relevantes y basadas en el proyecto

### ✅ Kernel
- `./build.sh` compila sin errores
- `kernel.bin` existe y es un binario ELF válido
- `f3os.iso` existe y es booteable

### ✅ Sistema Completo
- F3-OS ejecuta en QEMU
- El kernel muestra mensajes de boot
- El sistema no se congela

## 📞 Obtener Ayuda

Si encuentras problemas:

1. **Ejecuta el script de verificación:**
   ```bash
   ./verificar_sistema.sh
   ```

2. **Revisa la documentación:**
   - `agent/README.md` - Documentación del agente
   - `agent/INICIO_RAPIDO.md` - Inicio rápido
   - `SISTEMA_EN_MARCHA.md` - Estado del sistema

3. **Verifica logs:**
   ```bash
   cd agent
   ls -la logs/
   ```

---

**Si todos los checks pasan, el sistema está funcionando correctamente.** ✅






