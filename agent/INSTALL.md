# Instalación del Agente Gobernante

## Requisitos

- Python 3.8 o superior
- Token de GitHub con permisos: `repo`, `pull_requests`, `issues`

## Instalación

### 1. Instalar dependencias

```bash
cd agent
pip install -r requirements.txt
```

### 2. Configurar

```bash
# Copiar archivo de configuración
cp config/config.example.yaml config/config.yaml

# Editar configuración
nano config/config.yaml  # o tu editor preferido
```

### 3. Configurar token de GitHub

1. Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Genera un nuevo token con permisos:
   - `repo` (acceso completo a repositorios)
   - `pull_requests` (leer y escribir PRs)
   - `issues` (leer Issues)
3. Copia el token y pégalo en `config/config.yaml`:

```yaml
github:
  token: "ghp_tu_token_aqui"
```

## Uso Básico

### Método 1: Usar script de ejecución (Recomendado)

```bash
cd agent
./run.sh evaluate-pr --pr 123
./run.sh monitor
./run.sh status
./run.sh cycle
./run.sh gui-server
```

### Método 2: Ejecutar directamente

```bash
cd agent
python3 run_agent.py evaluate-pr --pr 123
python3 run_agent.py monitor
python3 run_agent.py status
python3 run_agent.py cycle
python3 run_agent.py gui-server
```

### Método 3: Como módulo Python

```bash
cd agent
python3 -m src.main evaluate-pr --pr 123
python3 -m src.main monitor
python3 -m src.main status
python3 -m src.main cycle
python3 -m src.main gui-server
```

### Comandos Disponibles

- `evaluate-pr --pr N`: Evalúa un PR específico
- `monitor`: Monitorea todos los PRs abiertos
- `status`: Muestra estado del agente
- `cycle`: Ejecuta ciclo completo
- `gui-server`: Inicia servidor GUI del asistente

### Modo dry-run (sin hacer cambios)

```bash
./run.sh evaluate-pr --pr 123 --dry-run
```

## Integración con GitHub Actions (Opcional)

Puedes configurar GitHub Actions para que el agente evalúe PRs automáticamente.

Ver `github/workflows/agent.yml` (crear si no existe).

## Troubleshooting

### Error: "GitHub token no configurado"

Asegúrate de haber configurado el token en `config/config.yaml`.

### Error: "Permission denied"

Verifica que el token tenga los permisos necesarios.

### Error: "Archivo de configuración no encontrado"

Asegúrate de haber copiado `config/config.example.yaml` a `config/config.yaml`.

## Próximos Pasos

1. Configura el agente con tu token
2. Prueba evaluando un PR existente
3. Configura monitoreo automático (opcional)
4. Ajusta parámetros en `config/config.yaml` según necesites

