# Guía: Pruebas Seguras de F3-OS en Ubuntu 24.04 LTS

## Resumen

Esta guía explica cómo probar F3-OS de forma **100% segura** usando **QEMU**, un emulador completo de hardware que ejecuta el sistema operativo en un entorno **completamente aislado** de tu Ubuntu.

**Ventajas de QEMU:**
- ✅ 100% seguro: no puede afectar tu sistema Ubuntu
- ✅ Aislamiento completo: ejecuta en una máquina virtual
- ✅ Interfaz gráfica: ves la pantalla del OS en una ventana
- ✅ Fácil de detener: solo cierras la ventana
- ✅ Sin instalación: no necesita disco duro real
- ✅ Gratis y código abierto

---

## Paso 1: Instalar QEMU

### En Ubuntu 24.04 LTS:

```bash
sudo apt update
sudo apt install -y qemu-system-x86 qemu-kvm
```

**Verificar instalación:**
```bash
qemu-system-x86_64 --version
```

**Dependencias adicionales útiles:**
```bash
sudo apt install -y xorriso grub-pc-bin  # Para crear ISOs (opcional)
```

---

## Paso 2: Instalar Rust Nightly

F3-OS necesita Rust Nightly:

```bash
# Instalar rustup si no lo tienes
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Instalar Rust Nightly
rustup toolchain install nightly
rustup default nightly
rustup component add rust-src --toolchain nightly-x86_64-unknown-linux-gnu

# Verificar
rustc --version
```

---

## Paso 3: Compilar F3-OS

```bash
cd /home/ktzchen/Documentos/f3-os

# Dar permisos de ejecución al script de build
chmod +x build.sh

# Compilar el kernel
./build.sh
```

**Salida esperada:**
- Se genera `kernel.bin` en el directorio raíz
- Mensaje: "Kernel built successfully: kernel.bin"

---

## Paso 4: Ejecutar F3-OS en QEMU (Métodos)

### Método 1: Kernel Directo (MÁS SIMPLE) ⭐ Recomendado

```bash
qemu-system-x86_64 \
  -kernel kernel.bin \
  -display gtk \
  -m 256M \
  -no-reboot
```

**Opciones:**
- `-kernel kernel.bin`: Carga el kernel directamente (sin ISO)
- `-display gtk`: Interfaz gráfica GTK (ventana visible)
- `-m 256M`: Asigna 256 MB de RAM
- `-no-reboot`: No reinicia al terminar

**Para cerrar:** Presiona `Ctrl+Alt+G` para capturar el cursor, luego `Ctrl+Alt+Q` o cierra la ventana.

---

### Método 2: Con Interfaz VNC (Red local)

```bash
qemu-system-x86_64 \
  -kernel kernel.bin \
  -display vnc=:1 \
  -m 256M \
  -no-reboot
```

**Acceder:**
- Conecta con un cliente VNC a `localhost:5901`
- O usa: `vncviewer localhost:1`

---

### Método 3: Con Terminal Serial (Sin gráficos)

```bash
qemu-system-x86_64 \
  -kernel kernel.bin \
  -nographic \
  -serial stdio \
  -m 256M \
  -no-reboot
```

**Para salir:** `Ctrl+A` luego `X`

---

## Paso 5: Script de Ejecución Rápida

Crear un script para facilitar las pruebas:

```bash
# Crear script
cat > /home/ktzchen/Documentos/f3-os/run.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"

# Verificar que kernel.bin existe
if [ ! -f kernel.bin ]; then
    echo "Error: kernel.bin no encontrado. Ejecuta ./build.sh primero."
    exit 1
fi

echo "Iniciando F3-OS en QEMU..."
echo "Para salir: Ctrl+Alt+G para capturar cursor, luego Ctrl+Alt+Q"
echo ""

qemu-system-x86_64 \
  -kernel kernel.bin \
  -display gtk \
  -m 256M \
  -no-reboot \
  -boot order=d
EOF

chmod +x run.sh
```

**Ejecutar:**
```bash
cd /home/ktzchen/Documentos/f3-os
./run.sh
```

---

## Paso 6: Ver el Sistema en Acción

### Qué deberías ver:

1. **Pantalla negra inicial** (bootloader)
2. **Mensajes de boot:**
   ```
   F3-OS booting...
   Regla: Lógico → Ilógico → Síntesis → Perfecto
   ===========================================
   
   Initializing F3 Core...
   [CPU] flow initialized
   [RAM] flow initialized
   [MEM] synthesizer online
   [F3 Core] embudo activo - Fase LÓGICA inicial
   F3 Core online.
   ```

3. **Transiciones de fases:**
   ```
   [LÓGICO] estructura ordenada
   [TRANSICIÓN] LÓGICO → ILÓGICO
   [ILÓGICO] explorando caos
   [TRANSICIÓN] ILÓGICO → SÍNTESIS
   [SÍNTESIS] embudo concentrando
   [TRANSICIÓN] SÍNTESIS → PERFECTO
   [PERFECTO] nuevo orden superior
   [CICLO COMPLETO] PERFECTO → LÓGICO (mejorado)
   ```

---

## Métodos Alternativos de Visualización

### Opción A: QEMU con SDL (Mejor rendimiento gráfico)

```bash
sudo apt install -y qemu-system-x86 libsdl2-dev

qemu-system-x86_64 \
  -kernel kernel.bin \
  -display sdl \
  -m 256M \
  -no-reboot
```

---

### Opción B: VirtualBox (Más familiar)

**Limitación:** VirtualBox no puede bootear kernels directos fácilmente. Necesitarías crear una ISO completa.

**Mejor usar:** QEMU (más simple para kernels bare metal).

---

### Opción C: QEMU con grabación/replay (Debugging)

```bash
# Grabar sesión
qemu-system-x86_64 \
  -kernel kernel.bin \
  -display gtk \
  -m 256M \
  -record-and-replay \
  -icount shift=7,rr=record,rrfile=replay.log

# Reproducir sesión
qemu-system-x86_64 \
  -kernel kernel.bin \
  -display gtk \
  -m 256M \
  -record-and-replay \
  -icount shift=7,rr=replay,rrfile=replay.log
```

---

## Comandos Útiles de QEMU

### Mientras QEMU está ejecutándose:

| Acción | Comando |
|--------|---------|
| Capturar cursor | `Ctrl+Alt+G` |
| Liberar cursor | `Ctrl+Alt+G` (otra vez) |
| Cerrar QEMU | `Ctrl+Alt+Q` o cerrar ventana |
| Monitoreo | `Ctrl+Alt+2` (entrar a monitor) |
| Salir del monitor | `Ctrl+Alt+1` |

### Opciones útiles de QEMU:

```bash
# Más RAM
-m 512M  # 512 MB

# Más CPUs (simulado)
-smp 2   # 2 CPUs virtuales

# Redirección de puerto serial
-serial telnet:localhost:4444,server,nowait

# Guardar screenshot
-display gtk,gl=on,show-cursor=on

# Debugging con GDB
-s -S    # Espera conexión GDB en localhost:1234
```

---

## Solución de Problemas

### Problema 1: "kernel.bin not found"

**Solución:**
```bash
cd /home/ktzchen/Documentos/f3-os
./build.sh
```

---

### Problema 2: "Permission denied" en build.sh

**Solución:**
```bash
chmod +x build.sh
```

---

### Problema 3: QEMU no inicia / error de display

**Solución:**
```bash
# Instalar dependencias GTK
sudo apt install -y gtk3

# O usar display VNC
qemu-system-x86_64 -kernel kernel.bin -display vnc=:1
```

---

### Problema 4: "Rust nightly not found"

**Solución:**
```bash
rustup toolchain install nightly
rustup default nightly
rustup component add rust-src
```

---

### Problema 5: Kernel panic al bootear

**Solución:**
- Verificar que compiló correctamente: `./build.sh`
- Verificar mensajes de error en la pantalla
- Probar con más RAM: `-m 512M`

---

## Seguridad: ¿Es Realmente Seguro?

### ✅ SÍ, 100% Seguro

**QEMU ejecuta el OS en:**
- Una máquina virtual aislada
- Sin acceso a tu disco duro real (por defecto)
- Sin acceso a tu sistema Ubuntu
- Solo en memoria RAM

**No puede:**
- ❌ Modificar archivos de tu Ubuntu
- ❌ Acceder a tu sistema de archivos
- ❌ Infectar tu sistema
- ❌ Causar problemas de hardware

**Es equivalente a:**
- Ver un video en YouTube
- Ejecutar una aplicación web en un navegador
- Probar código en un entorno sandbox

---

## Mejores Prácticas

1. **Usa `-no-reboot`**: Evita loops infinitos si hay kernel panic
2. **Monitorea RAM**: QEMU usa RAM real de tu sistema
3. **Cierra cuando termines**: No dejes QEMU corriendo indefinidamente
4. **Prueba primero con poco RAM**: `-m 128M` para verificar que funciona

---

## Siguiente Paso: Desarrollar y Probar

Una vez que veas F3-OS booteando, puedes:

1. **Modificar código** en `kernel/src/`
2. **Recompilar**: `./build.sh`
3. **Re-ejecutar**: `./run.sh`
4. **Ver cambios** en tiempo real

**Ciclo rápido de desarrollo:**
```bash
# En una terminal
cd /home/ktzchen/Documentos/f3-os
nano kernel/src/main.rs  # Editar

# En otra terminal
./build.sh && ./run.sh   # Probar
```

---

## Resumen de Comandos Rápidos

```bash
# 1. Instalar QEMU
sudo apt install -y qemu-system-x86

# 2. Instalar Rust
rustup toolchain install nightly && rustup default nightly

# 3. Compilar
cd /home/ktzchen/Documentos/f3-os
./build.sh

# 4. Ejecutar
./run.sh

# O directamente:
qemu-system-x86_64 -kernel kernel.bin -display gtk -m 256M -no-reboot
```

---

## Preguntas Frecuentes

**¿Puedo probar varios OS a la vez?**
Sí, cada QEMU corre independiente. Abre múltiples ventanas.

**¿Puedo guardar el estado?**
No directamente con kernel directo. Para eso necesitarías una ISO completa.

**¿Funciona en WSL2?**
Sí, pero necesitas X11 forwarding para ver la ventana gráfica.

**¿Puedo usar SSH para acceder?**
No, F3-OS actualmente no tiene red. Solo pantalla VGA.

---

**¡Listo para probar F3-OS de forma segura!** 🚀

