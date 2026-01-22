# Cómo Capturar la Imagen Correctamente

## ⚠️ Importante

La imagen debe capturar **SOLO la ventana del navegador** con la interfaz F3-OS Assistant, NO toda la pantalla.

## Método 1: Captura de Ventana (Recomendado)

1. **Abre la interfaz en el navegador:**
   ```bash
   # Si el servidor no está corriendo:
   cd agent
   ./run.sh gui-server
   ```
   Luego abre: `http://localhost:8080`

2. **Captura solo la ventana del navegador:**
   ```bash
   # Desde la raíz del proyecto
   cd /home/ktzchen/Documentos/f3-os
   
   # Capturar ventana activa (selecciona la ventana del navegador)
   gnome-screenshot -w -f agent/gui_web/screenshot.png
   ```

## Método 2: Captura de Área Seleccionada

1. **Abre la interfaz en el navegador**

2. **Captura área específica:**
   ```bash
   gnome-screenshot -a -f agent/gui_web/screenshot.png
   ```
   Esto te permitirá seleccionar solo el área de la interfaz.

## Método 3: Usando Herramientas del Navegador

1. **Abre la interfaz:** `http://localhost:8080`

2. **Usa las herramientas de desarrollador:**
   - Presiona `F12` para abrir DevTools
   - Presiona `Ctrl+Shift+P` (o `Cmd+Shift+P` en Mac)
   - Busca "Capture screenshot" o "Screenshot"
   - Selecciona "Capture node screenshot" o "Capture full size screenshot"

3. **Guarda la imagen como:** `agent/gui_web/screenshot.png`

## Después de Capturar

```bash
cd /home/ktzchen/Documentos/f3-os
git add agent/gui_web/screenshot.png
git commit -m "docs: agregar captura de pantalla correcta de la interfaz GUI"
git push origin main
```

## Verificación

La imagen debe mostrar:
- ✅ Solo la ventana del navegador con la interfaz
- ✅ Indicador de vida del agente (arriba derecha)
- ✅ Panel de estado
- ✅ Área de chat
- ✅ Input y botón de envío
- ❌ NO debe incluir barras del sistema, otras ventanas, etc.




