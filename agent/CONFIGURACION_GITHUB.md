# Configuración del Token de GitHub

## 🚀 Configuración Rápida

**Método más simple:**
```bash
cd agent
./setup_config.sh
```

El script te guiará paso a paso para configurar tu token.

## 📝 Configuración Manual

### Paso 1: Obtener Token de GitHub

1. Ve a: https://github.com/settings/tokens
2. Click en **"Generate new token (classic)"**
3. Dale un nombre: `F3-OS Agent`
4. Selecciona los permisos:
   - ✅ `repo` (acceso completo a repositorios)
   - ✅ `pull_requests` (leer y escribir PRs)
   - ✅ `issues` (leer Issues)
5. Click en **"Generate token"**
6. **Copia el token inmediatamente** (solo se muestra una vez)

### Paso 2: Configurar Token

**Opción A: Script interactivo (Recomendado)**
```bash
./setup_config.sh
```

**Opción B: Editar manualmente**
```bash
nano config/config.yaml
```

Busca la sección `github:` y actualiza:
```yaml
github:
  token: "ghp_tu_token_aqui"
  owner: "AlejandroSteiner"
  repo: "F3-OS"
```

### Paso 3: Verificar

```bash
./run.sh status
```

Si funciona, verás el estado del agente sin errores.

## ✅ Verificación

El script `setup_config.sh` verifica automáticamente que el token funcione.

Si ves:
```
✅ Token válido. Conectado como: tu_usuario
```

¡Está configurado correctamente!

## 🔧 Solución de Problemas

### Error: "Bad credentials"

- El token es inválido o expirado
- Genera un nuevo token y configúralo con `./setup_config.sh`

### Error: "Token no configurado"

- Ejecuta `./setup_config.sh` para configurarlo

### Error: "Permission denied"

- Verifica que el token tenga los permisos:
  - `repo`
  - `pull_requests`
  - `issues`

## 📋 Comandos que Requieren Token

Estos comandos necesitan el token configurado:
- `./run.sh monitor` - Monitorear PRs
- `./run.sh evaluate-pr --pr N` - Evaluar PR
- `./run.sh cycle` - Ciclo completo

Este comando NO requiere token:
- `./run.sh status` - Ver estado (funciona sin token)

## 🔒 Seguridad

- **Nunca compartas tu token**
- **No subas config/config.yaml a GitHub** (ya está en .gitignore)
- Si expusiste el token, revócalo inmediatamente y genera uno nuevo

---

**Una vez configurado, el agente puede gobernar el desarrollo de F3-OS.** 🤖







