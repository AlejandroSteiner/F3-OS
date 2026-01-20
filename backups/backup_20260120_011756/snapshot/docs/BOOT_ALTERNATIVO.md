# Solución Alternativa: Boot en QEMU

## Problema Actual

QEMU no está cargando el kernel directamente con `-kernel` porque puede requerir un formato específico o un bootloader.

## Soluciones Posibles

### Opción 1: Usar Bootloader Limine (RECOMENDADO)

Limine es un bootloader moderno que funciona bien con kernels personalizados.

```bash
# 1. Descargar Limine
git clone https://github.com/limine-bootloader/limine.git --branch=v5.x-branch --depth=1
cd limine
make

# 2. Crear ISO
cd /home/ktzchen/Documentos/f3-os
mkdir -p iso/boot
cp kernel.bin iso/boot/
cp boot/limine.cfg iso/boot/
cp limine/limine-bios.sys iso/
cp limine/limine-bios-cd.bin iso/

xorriso -as mkisofs \
  -b limine-bios-cd.bin \
  -no-emul-boot \
  -boot-load-size 4 \
  -boot-info-table \
  --protective-msdos-label \
  iso -o f3os.iso

./limine/limine bios-install f3os.iso

# 3. Ejecutar
qemu-system-x86_64 -cdrom f3os.iso -display gtk
```

### Opción 2: Usar formato Linux bzImage (NO APLICABLE)

Requiere formato Linux específico, no aplicable para nuestro kernel.

### Opción 3: Corregir Multiboot Header

El header está correcto pero QEMU puede necesitar:
- Header exactamente al inicio del archivo (offset 0)
- O formato específico del ELF

### Opción 4: Usar `-append` con formato raw

Algunas versiones de QEMU pueden cargar kernels raw.

## Próximo Paso

**Recomendación**: Usar Limine bootloader (Opción 1) porque es más confiable para kernels bare metal personalizados.

