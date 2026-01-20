"""
Project Knowledge Base - Base de Conocimiento Completa del Proyecto F3-OS

Carga TODA la información del proyecto como regla de configuración primaria:
- Todos los archivos de documentación
- Estructura completa del proyecto
- Relaciones entre componentes
- Funciones humanas e interacciones
- Tecnología civil (accesible, no experimental)
"""

import os
import re
from typing import Dict, List, Optional, Set, Tuple
from pathlib import Path
import logging
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ProjectComponent:
    """Representa un componente del proyecto"""
    name: str
    path: str
    type: str  # 'file', 'directory', 'module', 'function'
    description: str = ""
    relationships: List[str] = field(default_factory=list)
    human_functions: List[str] = field(default_factory=list)  # Cómo los humanos lo usan
    technology: str = "civil"  # "civil" = tecnología accesible, no experimental


@dataclass
class ProjectKnowledge:
    """Conocimiento completo del proyecto"""
    root_path: Path
    components: Dict[str, ProjectComponent] = field(default_factory=dict)
    documentation: Dict[str, str] = field(default_factory=dict)
    rules: List[str] = field(default_factory=list)
    human_interactions: Dict[str, List[str]] = field(default_factory=dict)
    technology_stack: Dict[str, str] = field(default_factory=dict)
    structure: Dict[str, List[str]] = field(default_factory=dict)
    loaded_at: datetime = field(default_factory=datetime.now)


class ProjectKnowledgeBase:
    """Base de conocimiento completa del proyecto F3-OS"""
    
    # Archivos esenciales que DEBEN cargarse
    ESSENTIAL_FILES = {
        # Documentación fundamental
        'manifesto': 'MANIFIESTO.md',
        'reglas': 'REGLAS_LOGICA.md',
        'contributing': 'CONTRIBUTING.md',
        'governance': 'GOVERNANCE.md',
        'readme': 'README.md',
        'arquitectura': 'ARQUITECTURA_COMPLETA.md',
        'seguridad': 'SEGURIDAD_Y_RESISTENCIA.md',
        'agente': 'AGENTE_GOBERNANTE.md',
        'code_of_conduct': 'CODE_OF_CONDUCT.md',
        
        # Documentación técnica
        'estado_actual': 'ESTADO_ACTUAL.md',
        'desarrollo_completado': 'DESARROLLO_COMPLETADO.md',
        'sistema_en_marcha': 'SISTEMA_EN_MARCHA.md',
        'gui_arquitectura': 'GUI_ARQUITECTURA.md',
        'gui_implementacion': 'GUI_IMPLEMENTACION.md',
        'verificacion_sistema': 'VERIFICACION_SISTEMA.md',
        
        # Scripts y configuración
        'build_script': 'build.sh',
        'run_script': 'run.sh',
        'run_safe_script': 'run_safe.sh',
        'create_iso_script': 'create_grub_iso.sh',
    }
    
    # Directorios clave
    KEY_DIRECTORIES = {
        'kernel': 'kernel/',
        'agent': 'agent/',
        'boot': 'boot/',
        'kernel_src': 'kernel/src/',
        'kernel_f3': 'kernel/src/f3/',
        'kernel_gui': 'kernel/src/gui/',
        'kernel_drivers': 'kernel/src/drivers/',
        'agent_src': 'agent/src/',
        'agent_config': 'agent/config/',
    }
    
    def __init__(self, project_root: Optional[str] = None):
        """Inicializa la base de conocimiento completa"""
        if project_root is None:
            current = Path(__file__).resolve()
            self.project_root = current.parent.parent.parent
        else:
            self.project_root = Path(project_root)
        
        self.knowledge = ProjectKnowledge(root_path=self.project_root)
        
        logger.info(f"Project Knowledge Base inicializando en: {self.project_root}")
        
        # Cargar TODO el conocimiento al inicio
        self._load_complete_knowledge()
    
    def _load_complete_knowledge(self) -> None:
        """Carga TODO el conocimiento del proyecto como regla primaria"""
        logger.info("Cargando conocimiento completo del proyecto...")
        
        # 1. Cargar toda la documentación
        self._load_all_documentation()
        
        # 2. Mapear estructura completa
        self._map_project_structure()
        
        # 3. Extraer todas las reglas
        self._extract_all_rules()
        
        # 4. Mapear funciones humanas
        self._map_human_functions()
        
        # 5. Mapear tecnología civil
        self._map_civil_technology()
        
        # 6. Establecer relaciones
        self._establish_relationships()
        
        logger.info(f"✅ Conocimiento completo cargado: {len(self.knowledge.components)} componentes, "
                   f"{len(self.knowledge.documentation)} documentos, {len(self.knowledge.rules)} reglas")
    
    def _load_all_documentation(self) -> None:
        """Carga TODA la documentación del proyecto"""
        for key, filename in self.ESSENTIAL_FILES.items():
            filepath = self.project_root / filename
            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.knowledge.documentation[key] = content
                    
                    # Crear componente
                    component = ProjectComponent(
                        name=filename,
                        path=str(filepath.relative_to(self.project_root)),
                        type='file',
                        description=self._extract_description(content),
                        technology="civil"
                    )
                    self.knowledge.components[key] = component
                    logger.debug(f"Cargado: {filename}")
                except Exception as e:
                    logger.warning(f"Error cargando {filename}: {e}")
    
    def _map_project_structure(self) -> None:
        """Mapea la estructura completa del proyecto"""
        # Mapear directorios principales
        for key, dirpath in self.KEY_DIRECTORIES.items():
            full_path = self.project_root / dirpath
            if full_path.exists():
                component = ProjectComponent(
                    name=key,
                    path=dirpath,
                    type='directory',
                    description=self._get_directory_description(key),
                    technology="civil"
                )
                self.knowledge.components[key] = component
                self.knowledge.structure[key] = self._list_directory_contents(full_path)
    
    def _extract_all_rules(self) -> None:
        """Extrae TODAS las reglas del proyecto"""
        # Reglas del manifiesto
        if 'manifesto' in self.knowledge.documentation:
            rules = self._extract_rules_from_text(
                self.knowledge.documentation['manifesto'],
                'MANIFIESTO'
            )
            self.knowledge.rules.extend(rules)
        
        # Reglas de lógica
        if 'reglas' in self.knowledge.documentation:
            rules = self._extract_rules_from_text(
                self.knowledge.documentation['reglas'],
                'REGLAS_LOGICA'
            )
            self.knowledge.rules.extend(rules)
        
        # Reglas de contribución
        if 'contributing' in self.knowledge.documentation:
            rules = self._extract_rules_from_text(
                self.knowledge.documentation['contributing'],
                'CONTRIBUTING'
            )
            self.knowledge.rules.extend(rules)
        
        # Reglas de gobernanza
        if 'governance' in self.knowledge.documentation:
            rules = self._extract_rules_from_text(
                self.knowledge.documentation['governance'],
                'GOVERNANCE'
            )
            self.knowledge.rules.extend(rules)
    
    def _map_human_functions(self) -> None:
        """Mapea cómo los humanos interactúan con el proyecto"""
        # Funciones del agente
        self.knowledge.human_interactions['agente'] = [
            "Ejecutar: cd agent && ./run.sh status",
            "Iniciar servidor GUI: cd agent && ./run.sh gui-server",
            "Hacer preguntas al asistente en http://localhost:8080",
            "Consultar reglas del proyecto",
            "Obtener explicaciones del modelo F3",
            "Ver estado del sistema"
        ]
        
        # Funciones del kernel
        self.knowledge.human_interactions['kernel'] = [
            "Compilar: ./build.sh",
            "Ejecutar en QEMU: ./run_safe.sh",
            "Crear ISO: ./create_grub_iso.sh",
            "Verificar sistema: ./verificar_sistema.sh"
        ]
        
        # Funciones de documentación
        self.knowledge.human_interactions['documentacion'] = [
            "Leer MANIFIESTO.md para entender el proyecto",
            "Leer REGLAS_LOGICA.md para entender el ciclo F3",
            "Leer CONTRIBUTING.md antes de contribuir",
            "Consultar ARQUITECTURA_COMPLETA.md para detalles técnicos"
        ]
    
    def _map_civil_technology(self) -> None:
        """Mapea la tecnología civil (accesible) usada"""
        self.knowledge.technology_stack = {
            'lenguaje': 'Rust (nightly)',
            'build': 'Cargo + scripts bash',
            'emulador': 'QEMU',
            'bootloader': 'GRUB',
            'agente': 'Python 3',
            'servidor_gui': 'HTTP server estándar',
            'interfaz': 'HTML/JavaScript simple',
            'comunicacion': 'HTTP REST API',
            'almacenamiento': 'JSON files',
            'sistema': 'Linux/Ubuntu'
        }
    
    def _establish_relationships(self) -> None:
        """Establece relaciones entre componentes"""
        # Relaciones kernel
        if 'kernel' in self.knowledge.components:
            self.knowledge.components['kernel'].relationships = [
                'kernel_f3', 'kernel_gui', 'kernel_drivers', 'build_script'
            ]
        
        # Relaciones agente
        if 'agent' in self.knowledge.components:
            self.knowledge.components['agent'].relationships = [
                'agent_src', 'agent_config', 'gui_arquitectura'
            ]
        
        # Relaciones F3 Core
        if 'kernel_f3' in self.knowledge.components:
            self.knowledge.components['kernel_f3'].relationships = [
                'reglas', 'arquitectura', 'manifesto'
            ]
    
    def _extract_description(self, content: str, max_length: int = 200) -> str:
        """Extrae descripción de un archivo"""
        lines = content.split('\n')
        for line in lines[:20]:
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 20:
                return line[:max_length]
        return "Documentación del proyecto F3-OS"
    
    def _extract_rules_from_text(self, text: str, source: str) -> List[str]:
        """Extrae reglas de un texto"""
        rules = []
        lines = text.split('\n')
        current_rule = []
        
        for line in lines:
            line = line.strip()
            # Detectar reglas (líneas que empiezan con números, guiones, o palabras clave)
            if (line.startswith('-') or 
                line.startswith('*') or 
                re.match(r'^\d+\.', line) or
                'debe' in line.lower() or
                'no debe' in line.lower() or
                'requiere' in line.lower() or
                'obligatorio' in line.lower()):
                if line:
                    rules.append(f"[{source}] {line}")
        
        return rules
    
    def _get_directory_description(self, key: str) -> str:
        """Obtiene descripción de un directorio"""
        descriptions = {
            'kernel': 'Código fuente del kernel F3-OS en Rust',
            'agent': 'Agente gobernante AI en Python',
            'kernel_f3': 'Núcleo F3: CPU, RAM, MEM threads y F3 Core',
            'kernel_gui': 'Sistema GUI con separación de consultas y drivers AI',
            'kernel_drivers': 'Drivers del sistema (AI, GPU)',
            'agent_src': 'Código fuente del agente gobernante',
            'agent_config': 'Configuración del agente'
        }
        return descriptions.get(key, f"Directorio {key}")
    
    def _list_directory_contents(self, dirpath: Path) -> List[str]:
        """Lista contenidos de un directorio"""
        try:
            return [f.name for f in dirpath.iterdir() if f.is_file()][:20]
        except:
            return []
    
    # Métodos de consulta inmediata
    
    def get_complete_rules(self) -> str:
        """Obtiene TODAS las reglas del proyecto"""
        if not self.knowledge.rules:
            return "No se encontraron reglas documentadas."
        
        return "\n".join(self.knowledge.rules)
    
    def get_project_overview(self) -> str:
        """Obtiene visión completa del proyecto"""
        overview = []
        overview.append("# Visión Completa del Proyecto F3-OS\n")
        
        # Qué es
        if 'manifesto' in self.knowledge.documentation:
            manifesto = self.knowledge.documentation['manifesto']
            # Extraer sección "¿Qué es F3-OS?"
            lines = manifesto.split('\n')
            in_section = False
            for line in lines:
                if '¿Qué es F3-OS?' in line or '## ¿Qué es' in line:
                    in_section = True
                elif in_section and line.startswith('##'):
                    break
                elif in_section:
                    overview.append(line)
        
        # Estructura
        overview.append("\n## Estructura del Proyecto\n")
        for key, component in self.knowledge.components.items():
            if component.type == 'directory':
                overview.append(f"- **{key}**: {component.description}")
        
        # Tecnología
        overview.append("\n## Tecnología Civil Utilizada\n")
        for tech, desc in self.knowledge.technology_stack.items():
            overview.append(f"- **{tech}**: {desc}")
        
        return "\n".join(overview)
    
    def get_human_functions(self) -> str:
        """Obtiene todas las funciones humanas"""
        result = []
        result.append("# Funciones Humanas del Proyecto F3-OS\n")
        
        for category, functions in self.knowledge.human_interactions.items():
            result.append(f"\n## {category.upper()}\n")
            for func in functions:
                result.append(f"- {func}")
        
        return "\n".join(result)
    
    def resolve_query_immediate(self, query: str) -> str:
        """Resuelve consulta inmediatamente usando tecnología civil"""
        query_lower = query.lower()
        
        # Búsqueda en reglas
        if any(word in query_lower for word in ['regla', 'rule', 'norma']):
            return self.get_complete_rules()
        
        # Búsqueda en funciones humanas
        if any(word in query_lower for word in ['cómo', 'how', 'usar', 'usar', 'función', 'function']):
            return self.get_human_functions()
        
        # Búsqueda en documentación
        for key, content in self.knowledge.documentation.items():
            if query_lower in content.lower():
                # Extraer sección relevante
                lines = content.split('\n')
                relevant = []
                for i, line in enumerate(lines):
                    if query_lower in line.lower():
                        # Contexto: 5 líneas antes y después
                        start = max(0, i - 5)
                        end = min(len(lines), i + 6)
                        relevant.extend(lines[start:end])
                        break
                if relevant:
                    return "\n".join(relevant[:50])
        
        # Búsqueda general
        matches = []
        for key, content in self.knowledge.documentation.items():
            if query_lower in content.lower():
                matches.append(f"**{key}**: {content[:300]}...")
        
        if matches:
            return "\n\n".join(matches[:3])
        
        return "Consulta no encontrada en la base de conocimiento. Intenta ser más específico."
    
    def get_component_info(self, component_name: str) -> Optional[ProjectComponent]:
        """Obtiene información de un componente"""
        return self.knowledge.components.get(component_name)
    
    def get_all_relationships(self) -> Dict[str, List[str]]:
        """Obtiene todas las relaciones"""
        return {
            name: comp.relationships 
            for name, comp in self.knowledge.components.items()
            if comp.relationships
        }

