# Inicio Rápido - Agente Gobernante F3-OS

## 🚀 Ejecución Rápida

### Paso 1: Instalar dependencias

```bash
cd agent
pip3 install -r requirements.txt
```

### Paso 2: Configurar

```bash
# Copiar archivo de configuración
cp config/config.example.yaml config/config.yaml

# Editar y agregar tu token de GitHub
nano config/config.yaml
```

### Paso 3: Ejecutar

```bash
# Usar script de ejecución (recomendado)
./run.sh status

# O directamente
python3 run_agent.py status
```

## ✅ Verificación

Si ves el estado del agente, ¡está funcionando!

```bash
./run.sh status
```

Deberías ver:
- Fase actual del agente
- Entropía
- Perfection Score
- Ciclos completados

## 📝 Próximos Pasos

1. **Configurar token de GitHub** en `config/config.yaml`
2. **Probar evaluación de PR**: `./run.sh evaluate-pr --pr 1 --dry-run`
3. **Iniciar monitoreo**: `./run.sh monitor`
4. **Iniciar servidor GUI**: `./run.sh gui-server`

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'github'"

```bash
pip3 install -r requirements.txt
```

### Error: "config/config.yaml no encontrado"

```bash
cp config/config.example.yaml config/config.yaml
```

### Error: "GitHub token no configurado"

Edita `config/config.yaml` y agrega tu token de GitHub.

---

*El agente está listo para gobernar el desarrollo de F3-OS.* 🤖

