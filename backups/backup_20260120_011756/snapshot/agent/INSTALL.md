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

### Evaluar un PR específico

```bash
python -m src.main evaluate-pr --pr 123
```

### Monitorear todos los PRs abiertos

```bash
python -m src.main monitor
```

### Ver estado del agente

```bash
python -m src.main status
```

### Ejecutar ciclo completo

```bash
python -m src.main cycle
```

### Modo dry-run (sin hacer cambios)

```bash
python -m src.main evaluate-pr --pr 123 --dry-run
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

