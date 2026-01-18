# Instrucciones para Configurar la Descripción del Repositorio

## Opción 1: Usar GitHub CLI (Recomendado)

Si tienes GitHub CLI instalado:

```bash
./configurar_repo_github.sh
```

Si no tienes GitHub CLI, instálalo:

```bash
# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh

# Autenticar
gh auth login

# Luego ejecutar el script
./configurar_repo_github.sh
```

## Opción 2: Manualmente desde la Web

1. Ve a: https://github.com/AlejandroSteiner/F3-OS
2. Haz clic en el botón **⚙️ Settings** (configuración)
3. En la sección **"General"**, desplázate hasta **"Repository details"**
4. En el campo **"Description"**, pega:

```
F3-OS: Sistema operativo experimental de código abierto con modelo innovador de 3 hilos (CPU/RAM/MEM) fusionados en un embudo adaptativo. Ciclo: Lógico → Ilógico → Síntesis → Perfecto.
```

5. Haz clic en **"Update description"**

### Agregar Topics

1. En la misma página de Settings → General
2. En la sección **"Topics"**, agrega estos topics:

```
rust
operating-system
kernel
osdev
bare-metal
multiboot
x86-64
experimental
open-source
systems-programming
f3-os
embedded
no-std
qemu
grub
```

3. Haz clic en **"Save changes"**

## Opción 3: Usar la API de GitHub

Si tienes un token de acceso personal:

```bash
# Configurar token (reemplaza YOUR_TOKEN con tu token)
export GITHUB_TOKEN="YOUR_TOKEN"

# Actualizar descripción
curl -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/AlejandroSteiner/F3-OS \
  -d '{
    "description": "F3-OS: Sistema operativo experimental de código abierto con modelo innovador de 3 hilos (CPU/RAM/MEM) fusionados en un embudo adaptativo. Ciclo: Lógico → Ilógico → Síntesis → Perfecto.",
    "homepage": "",
    "topics": ["rust", "operating-system", "kernel", "osdev", "bare-metal", "multiboot", "x86-64", "experimental", "open-source", "systems-programming", "f3-os", "embedded", "no-std", "qemu", "grub"]
  }'
```

## Descripción Completa Recomendada

### Campo "About" (Descripción corta):

```
F3-OS: Sistema operativo experimental de código abierto con modelo innovador de 3 hilos (CPU/RAM/MEM) fusionados en un embudo adaptativo. Ciclo: Lógico → Ilógico → Síntesis → Perfecto.
```

### Topics (Etiquetas):

- rust
- operating-system
- kernel
- osdev
- bare-metal
- multiboot
- x86-64
- experimental
- open-source
- systems-programming
- f3-os
- embedded
- no-std
- qemu
- grub

### Website (opcional):

Dejar vacío por ahora, o agregar la URL del README si tienes una página de documentación.

## Verificar

Después de actualizar, verifica que la descripción aparezca correctamente en:
https://github.com/AlejandroSteiner/F3-OS

La descripción debería aparecer debajo del nombre del repositorio.
