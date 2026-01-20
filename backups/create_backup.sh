#!/bin/bash
# Script para crear backup documentado de F3-OS

set -e

BACKUP_DIR="backups/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR/snapshot"

echo "📦 Creando backup en: $BACKUP_DIR"

# 1. Información de Git
echo "📝 Guardando información de Git..."
git log --oneline -50 > "$BACKUP_DIR/git_log.txt"
git log --stat -20 > "$BACKUP_DIR/git_log_detailed.txt"
git diff HEAD > "$BACKUP_DIR/git_diff_current.txt" 2>/dev/null || true
git status > "$BACKUP_DIR/git_status.txt"

# 2. Copiar archivos importantes
echo "📋 Copiando archivos importantes..."

# Documentación
mkdir -p "$BACKUP_DIR/snapshot/docs"
cp -r *.md "$BACKUP_DIR/snapshot/docs/" 2>/dev/null || true

# Configuración
mkdir -p "$BACKUP_DIR/snapshot/config"
cp -r .github "$BACKUP_DIR/snapshot/config/" 2>/dev/null || true
cp -r agent/config "$BACKUP_DIR/snapshot/config/agent_config" 2>/dev/null || true

# Código del kernel
mkdir -p "$BACKUP_DIR/snapshot/kernel"
cp -r kernel/src "$BACKUP_DIR/snapshot/kernel/" 2>/dev/null || true
cp kernel/Cargo.toml "$BACKUP_DIR/snapshot/kernel/" 2>/dev/null || true
cp kernel/linker.ld "$BACKUP_DIR/snapshot/kernel/" 2>/dev/null || true

# Agente
mkdir -p "$BACKUP_DIR/snapshot/agent"
cp -r agent/src "$BACKUP_DIR/snapshot/agent/" 2>/dev/null || true
cp agent/requirements.txt "$BACKUP_DIR/snapshot/agent/" 2>/dev/null || true
cp agent/README.md "$BACKUP_DIR/snapshot/agent/" 2>/dev/null || true
cp agent/*.md "$BACKUP_DIR/snapshot/agent/" 2>/dev/null || true

# Scripts
mkdir -p "$BACKUP_DIR/snapshot/scripts"
cp *.sh "$BACKUP_DIR/snapshot/scripts/" 2>/dev/null || true

# Configuración del proyecto
cp Cargo.toml "$BACKUP_DIR/snapshot/" 2>/dev/null || true
cp LICENSE "$BACKUP_DIR/snapshot/" 2>/dev/null || true
cp x86_64-unknown-none.json "$BACKUP_DIR/snapshot/" 2>/dev/null || true

# 3. Lista de archivos
echo "📄 Generando lista de archivos..."
find "$BACKUP_DIR/snapshot" -type f > "$BACKUP_DIR/FILES.txt"

# 4. Información del sistema
echo "💻 Guardando información del sistema..."
{
    echo "Fecha: $(date)"
    echo "Usuario: $(whoami)"
    echo "Sistema: $(uname -a)"
    echo "Rust: $(rustc --version 2>/dev/null || echo 'No instalado')"
    echo "Git: $(git --version)"
    echo "Directorio: $(pwd)"
} > "$BACKUP_DIR/SYSTEM_INFO.txt"

# 5. Resumen de cambios recientes
echo "📊 Generando resumen de cambios..."
cat > "$BACKUP_DIR/CHANGELOG.md" << 'EOF'
# Changelog del Backup

## Cambios Recientes

EOF

# Agregar commits recientes al changelog
git log --oneline --since="1 week ago" >> "$BACKUP_DIR/CHANGELOG.md" 2>/dev/null || echo "No hay commits recientes" >> "$BACKUP_DIR/CHANGELOG.md"

# 6. Crear archivo de resumen
cat > "$BACKUP_DIR/SUMMARY.md" << EOF
# Resumen del Backup

**Fecha**: $(date)
**Directorio**: $BACKUP_DIR

## Contenido

- Documentación completa del proyecto
- Código fuente del kernel
- Agente gobernante completo
- Configuración de GitHub
- Scripts de build y ejecución
- Historial de Git

## Archivos Incluidos

Ver \`FILES.txt\` para lista completa.

## Cambios Recientes

Ver \`CHANGELOG.md\` para detalles.

## Restaurar

Para restaurar archivos específicos:

\`\`\`bash
cp $BACKUP_DIR/snapshot/ruta/archivo ./
\`\`\`
EOF

echo "✅ Backup completado: $BACKUP_DIR"
echo "📁 Archivos guardados en: $BACKUP_DIR/snapshot/"
echo "📝 Ver resumen en: $BACKUP_DIR/SUMMARY.md"

