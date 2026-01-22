# Sistema de Backups de F3-OS

Este directorio contiene backups documentados del proyecto F3-OS.

## Estructura

Cada backup tiene el formato: `backup_YYYYMMDD_HHMMSS/`

Contiene:
- `CHANGELOG.md` - Resumen detallado de cambios
- `FILES.md` - Lista de archivos incluidos
- `git_log.txt` - Historial de commits
- `git_diff.txt` - Diferencias desde último backup
- `snapshot/` - Copia de archivos importantes

## Restaurar un Backup

```bash
# Ver backups disponibles
ls backups/

# Restaurar archivos específicos
cp backups/backup_YYYYMMDD_HHMMSS/snapshot/ruta/archivo ./

# Ver cambios del backup
cat backups/backup_YYYYMMDD_HHMMSS/CHANGELOG.md
```




