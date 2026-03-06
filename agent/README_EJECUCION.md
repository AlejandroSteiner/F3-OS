# Ejecución del Agente F3-OS

## 🚀 Método Más Simple

**Solo ejecuta:**
```bash
cd agent
./run.sh status
```

El script `run.sh` automáticamente:
- ✅ Crea entorno virtual si no existe
- ✅ Instala dependencias automáticamente
- ✅ Ejecuta el agente

**No necesitas hacer nada más.** El script lo hace todo por ti.

## 📋 Comandos Disponibles

```bash
./run.sh status              # Ver estado del agente
./run.sh monitor             # Monitorear PRs abiertos
./run.sh evaluate-pr --pr 1  # Evaluar un PR específico
./run.sh cycle               # Ejecutar ciclo completo
./run.sh gui-server          # Iniciar servidor GUI
```

## 🔧 Si Algo Sale Mal

### Error: "python3-venv no encontrado"

```bash
sudo apt install python3-venv
```

### Error: "config/config.yaml no encontrado"

El script lo crea automáticamente, pero si necesitas editarlo:

```bash
nano config/config.yaml
```

Agrega tu token de GitHub:
```yaml
github:
  token: "ghp_tu_token_aqui"
```

### Error: "Dependencias no instaladas"

El script las instala automáticamente. Si falla:

```bash
# Crear entorno virtual manualmente
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ✅ Verificación

Si ves el estado del agente, está funcionando:

```bash
./run.sh status
```

Deberías ver:
- Fase actual
- Entropía
- Perfection Score
- Ciclos completados

---

**El script `run.sh` hace todo automáticamente. Solo ejecútalo.** 🎯







