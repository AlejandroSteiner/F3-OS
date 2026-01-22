"""
Project Analyzer - Analiza archivos del proyecto F3-OS para proporcionar respuestas precisas

Lee y analiza documentación del proyecto para dar respuestas basadas en el contenido real.
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ProjectAnalyzer:
    """Analiza archivos del proyecto para proporcionar información precisa"""
    
    # Archivos clave del proyecto
    KEY_FILES = {
        'manifesto': 'MANIFIESTO.md',
        'reglas': 'REGLAS_LOGICA.md',
        'contributing': 'CONTRIBUTING.md',
        'governance': 'GOVERNANCE.md',
        'readme': 'README.md',
        'arquitectura': 'ARQUITECTURA_COMPLETA.md',
        'seguridad': 'SEGURIDAD_Y_RESISTENCIA.md',
        'agente': 'AGENTE_GOBERNANTE.md',
    }
    
    def __init__(self, project_root: Optional[str] = None):
        """Inicializa el analizador con la raíz del proyecto"""
        if project_root is None:
            # Intentar encontrar la raíz del proyecto (subiendo desde agent/)
            current = Path(__file__).resolve()
            # agent/src/project_analyzer.py -> agent/ -> f3-os/
            self.project_root = current.parent.parent.parent
        else:
            self.project_root = Path(project_root)
        
        # Cache de archivos leídos
        self._file_cache: Dict[str, str] = {}
        self._sections_cache: Dict[str, Dict[str, str]] = {}
        
        logger.info(f"Project Analyzer inicializado en: {self.project_root}")
    
    def _read_file(self, filename: str) -> Optional[str]:
        """Lee un archivo del proyecto (con cache)"""
        if filename in self._file_cache:
            return self._file_cache[filename]
        
        filepath = self.project_root / filename
        if not filepath.exists():
            logger.warning(f"Archivo no encontrado: {filepath}")
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self._file_cache[filename] = content
            return content
        except Exception as e:
            logger.error(f"Error leyendo {filename}: {e}")
            return None
    
    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Extrae secciones de un documento Markdown"""
        sections = {}
        current_section = "introducción"
        current_content = []
        
        lines = content.split('\n')
        for line in lines:
            # Detectar encabezados
            if line.startswith('#'):
                # Guardar sección anterior
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Nueva sección
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                current_section = title.lower()
                current_content = []
            else:
                current_content.append(line)
        
        # Guardar última sección
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def get_file_content(self, file_key: str) -> Optional[str]:
        """Obtiene contenido de un archivo clave"""
        filename = self.KEY_FILES.get(file_key)
        if not filename:
            return None
        return self._read_file(filename)
    
    def get_section(self, file_key: str, section_title: str) -> Optional[str]:
        """Obtiene una sección específica de un archivo"""
        filename = self.KEY_FILES.get(file_key)
        if not filename:
            return None
        
        # Cache de secciones
        cache_key = f"{file_key}:{section_title}"
        if cache_key in self._sections_cache:
            return self._sections_cache[cache_key]
        
        content = self._read_file(filename)
        if not content:
            return None
        
        sections = self._extract_sections(content)
        
        # Buscar sección (búsqueda flexible)
        section_lower = section_title.lower()
        for section_name, section_content in sections.items():
            if section_lower in section_name or section_name in section_lower:
                self._sections_cache[cache_key] = section_content
                return section_content
        
        return None
    
    def get_rules(self) -> str:
        """Obtiene todas las reglas del proyecto"""
        rules_parts = []
        
        # Reglas del manifiesto
        manifesto = self.get_file_content('manifesto')
        if manifesto:
            # Extraer principios fundamentales
            manifesto_sections = self._extract_sections(manifesto)
            if 'principios fundamentales' in manifesto_sections:
                rules_parts.append("## Principios Fundamentales (del Manifiesto)")
                rules_parts.append(manifesto_sections['principios fundamentales'])
        
        # Reglas de lógica
        reglas = self.get_file_content('reglas')
        if reglas:
            rules_parts.append("\n## Reglas de Lógica F3-OS")
            # Tomar las primeras 200 líneas (reglas principales)
            reglas_lines = reglas.split('\n')[:200]
            rules_parts.append('\n'.join(reglas_lines))
        
        # Reglas de contribución
        contributing = self.get_file_content('contributing')
        if contributing:
            contributing_sections = self._extract_sections(contributing)
            if 'reglas fundamentales' in contributing_sections:
                rules_parts.append("\n## Reglas de Contribución")
                rules_parts.append(contributing_sections['reglas fundamentales'])
        
        # Reglas de gobernanza
        governance = self.get_file_content('governance')
        if governance:
            governance_sections = self._extract_sections(governance)
            if 'núcleo sagrado' in governance_sections:
                rules_parts.append("\n## Reglas de Gobernanza (Núcleo Sagrado)")
                rules_parts.append(governance_sections['núcleo sagrado'])
        
        return '\n\n'.join(rules_parts) if rules_parts else "No se encontraron reglas documentadas."
    
    def get_f3_model_explanation(self) -> str:
        """Obtiene explicación completa del modelo F3"""
        explanation_parts = []
        
        # Del manifiesto
        manifesto = self.get_file_content('manifesto')
        if manifesto:
            manifesto_sections = self._extract_sections(manifesto)
            if 'el modelo f3' in manifesto_sections:
                explanation_parts.append("## El Modelo F3 (del Manifiesto)")
                explanation_parts.append(manifesto_sections['el modelo f3'])
        
        # De reglas de lógica
        reglas = self.get_file_content('reglas')
        if reglas:
            reglas_sections = self._extract_sections(reglas)
            if 'el ciclo de 4 fases' in reglas_sections:
                explanation_parts.append("\n## El Ciclo de 4 Fases")
                explanation_parts.append(reglas_sections['el ciclo de 4 fases'])
        
        return '\n\n'.join(explanation_parts) if explanation_parts else "No se encontró explicación del modelo F3."
    
    def explain_from_scratch(self) -> str:
        """Explicación completa del proyecto desde cero"""
        parts = []
        
        # 1. ¿Qué es F3-OS?
        manifesto = self.get_file_content('manifesto')
        if manifesto:
            manifesto_sections = self._extract_sections(manifesto)
            if '¿qué es f3-os?' in manifesto_sections:
                parts.append("# ¿Qué es F3-OS?")
                parts.append(manifesto_sections['¿qué es f3-os?'])
            
            if '¿qué no es f3-os?' in manifesto_sections:
                parts.append("\n# ¿Qué NO es F3-OS?")
                parts.append(manifesto_sections['¿qué no es f3-os?'])
        
        # 2. El Modelo F3
        f3_explanation = self.get_f3_model_explanation()
        if f3_explanation:
            parts.append(f"\n{f3_explanation}")
        
        # 3. Principios
        if manifesto:
            manifesto_sections = self._extract_sections(manifesto)
            if 'principios fundamentales' in manifesto_sections:
                parts.append("\n# Principios Fundamentales")
                parts.append(manifesto_sections['principios fundamentales'])
        
        return '\n\n'.join(parts) if parts else "No se pudo generar explicación completa."
    
    def search_in_files(self, query: str, file_keys: Optional[List[str]] = None) -> List[Tuple[str, str]]:
        """Busca texto en archivos del proyecto"""
        if file_keys is None:
            file_keys = list(self.KEY_FILES.keys())
        
        results = []
        query_lower = query.lower()
        
        for file_key in file_keys:
            filename = self.KEY_FILES.get(file_key)
            if not filename:
                continue
            
            content = self._read_file(filename)
            if not content:
                continue
            
            # Buscar líneas que contengan la query
            lines = content.split('\n')
            matching_lines = []
            for i, line in enumerate(lines):
                if query_lower in line.lower():
                    # Contexto: 2 líneas antes y después
                    start = max(0, i - 2)
                    end = min(len(lines), i + 3)
                    context = '\n'.join(lines[start:end])
                    matching_lines.append(context)
            
            if matching_lines:
                results.append((filename, '\n\n---\n\n'.join(matching_lines[:5])))  # Máximo 5 matches por archivo
        
        return results
    
    def get_project_summary(self) -> str:
        """Obtiene un resumen general del proyecto"""
        summary_parts = []
        
        # Del README
        readme = self.get_file_content('readme')
        if readme:
            # Primera sección del README
            readme_lines = readme.split('\n')[:50]
            summary_parts.append('\n'.join(readme_lines))
        
        # Del manifiesto
        manifesto = self.get_file_content('manifesto')
        if manifesto:
            manifesto_sections = self._extract_sections(manifesto)
            if '¿qué es f3-os?' in manifesto_sections:
                summary_parts.append("\n" + manifesto_sections['¿qué es f3-os?'])
        
        return '\n\n'.join(summary_parts) if summary_parts else "No se pudo generar resumen."




