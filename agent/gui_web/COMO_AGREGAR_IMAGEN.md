# Cómo Agregar la Captura de Pantalla

## Opción 1: Desde la Raíz del Proyecto (Recomendado)

```bash
# Ve a la raíz del proyecto
cd /home/ktzchen/Documentos/f3-os

# Agrega la imagen (debe estar guardada como screenshot.png)
git add agent/gui_web/screenshot.png

# Commit
git commit -m "docs: agregar captura de pantalla de la interfaz GUI"

# Push
git push origin main
```

## Opción 2: Desde el Directorio agent/

Si estás en `agent/`, usa la ruta relativa:

```bash
# Desde agent/
cd /home/ktzchen/Documentos/f3-os/agent

# Agrega usando ruta relativa
git add gui_web/screenshot.png

# O ruta absoluta desde la raíz
git add ../agent/gui_web/screenshot.png

# Commit y push
git commit -m "docs: agregar captura de pantalla de la interfaz GUI"
git push origin main
```

## Cómo Capturar la Imagen

1. **Inicia el servidor GUI:**
   ```bash
   cd agent
   ./run.sh gui-server
   ```

2. **Abre en el navegador:**
   ```
   http://localhost:8080
   ```

3. **Captura la pantalla:**
   - En Linux: `gnome-screenshot` o `scrot`
   - O usa la herramienta de captura de tu sistema

4. **Guarda la imagen como:**
   ```
   agent/gui_web/screenshot.png
   ```

## Verificar que Funciona

Después de hacer push, la imagen debería aparecer en:
- README principal del proyecto
- README del agente

La URL en el README es:
```
https://raw.githubusercontent.com/AlejandroSteiner/F3-OS/main/agent/gui_web/screenshot.png
```




