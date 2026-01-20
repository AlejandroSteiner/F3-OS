"""
Internet Learning Module - Aprendizaje Libre en Internet

El agente puede aprender libremente de internet para completar el propósito del proyecto.
Consume hasta 50% de la disponibilidad de conexión de red.
"""

import requests
import time
import threading
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import logging
from urllib.parse import urljoin, urlparse
import re

logger = logging.getLogger(__name__)


@dataclass
class NetworkLimits:
    """Límites de red para el agente"""
    max_bandwidth_percent: float = 50.0  # Máximo 50% de ancho de banda disponible
    target_bandwidth_percent: float = 40.0  # Objetivo 40%
    check_interval: float = 1.0
    request_delay: float = 0.5  # Delay entre peticiones para respetar límites


@dataclass
class LearningSource:
    """Fuente de aprendizaje"""
    url: str
    title: str
    content: str
    relevance_score: float
    learned_at: datetime
    tags: List[str]


class NetworkManager:
    """Gestiona uso de red del agente"""
    
    def __init__(self, config: dict):
        self.config = config
        network_config = config.get('network', {})
        
        self.limits = NetworkLimits(
            max_bandwidth_percent=network_config.get('max_bandwidth_percent', 50.0),
            target_bandwidth_percent=network_config.get('target_bandwidth_percent', 40.0),
            check_interval=network_config.get('check_interval', 1.0),
            request_delay=network_config.get('request_delay', 0.5),
        )
        
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.current_bandwidth_usage = 0.0
        self.total_bytes_sent = 0
        self.total_bytes_received = 0
        self.request_count = 0
        
        # Session para reutilizar conexiones
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'F3-OS-Agent/1.0 (Learning Agent)'
        })
    
    def start_monitoring(self) -> None:
        """Inicia monitoreo de red"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_network, daemon=True)
        self.monitor_thread.start()
        logger.info(f"📡 Monitoreo de red iniciado (límite: {self.limits.max_bandwidth_percent}%)")
    
    def stop_monitoring(self) -> None:
        """Detiene monitoreo de red"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
    
    def _monitor_network(self) -> None:
        """Monitorea uso de red"""
        import psutil
        
        while self.monitoring:
            try:
                # Obtener estadísticas de red del proceso
                net_io = psutil.net_io_counters()
                # Calcular uso aproximado (simplificado)
                # En producción, se calcularía basado en velocidad de conexión
                time.sleep(self.limits.check_interval)
            except Exception as e:
                logger.error(f"Error en monitoreo de red: {e}")
                time.sleep(self.limits.check_interval)
    
    def throttle_request(self) -> None:
        """Aplica throttling a peticiones de red"""
        time.sleep(self.limits.request_delay)
    
    def get_network_stats(self) -> dict:
        """Obtiene estadísticas de red"""
        return {
            'bytes_sent': self.total_bytes_sent,
            'bytes_received': self.total_bytes_received,
            'requests': self.request_count,
            'bandwidth_usage_percent': self.current_bandwidth_usage,
        }


class InternetLearner:
    """Módulo de aprendizaje libre en internet"""
    
    def __init__(self, config: dict, network_manager: NetworkManager):
        self.config = config
        self.network_manager = network_manager
        self.learned_sources: List[LearningSource] = []
        self.learning_enabled = config.get('internet_learning', {}).get('enabled', True)
        
        # Fuentes de aprendizaje permitidas
        self.allowed_domains = config.get('internet_learning', {}).get('allowed_domains', [
            'github.com',
            'stackoverflow.com',
            'rust-lang.org',
            'osdev.org',
            'wikipedia.org',
            'docs.rs',
        ])
        
        logger.info("Internet Learner inicializado - Aprendizaje libre habilitado")
    
    def learn_from_url(self, url: str, query: Optional[str] = None) -> Optional[LearningSource]:
        """Aprende de una URL específica"""
        if not self.learning_enabled:
            return None
        
        # Verificar dominio permitido
        parsed = urlparse(url)
        if parsed.netloc not in self.allowed_domains and not any(
            domain in parsed.netloc for domain in self.allowed_domains
        ):
            logger.warning(f"Dominio no permitido: {parsed.netloc}")
            return None
        
        # Aplicar throttling de red
        self.network_manager.throttle_request()
        
        try:
            response = self.network_manager.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Actualizar estadísticas
            self.network_manager.total_bytes_received += len(response.content)
            self.network_manager.request_count += 1
            
            # Extraer contenido relevante
            content = self._extract_content(response.text, query)
            title = self._extract_title(response.text)
            
            # Calcular relevancia
            relevance = self._calculate_relevance(content, query) if query else 0.5
            
            source = LearningSource(
                url=url,
                title=title,
                content=content[:5000],  # Limitar tamaño
                relevance_score=relevance,
                learned_at=datetime.now(),
                tags=self._extract_tags(content, query)
            )
            
            self.learned_sources.append(source)
            logger.info(f"✅ Aprendido de: {url} (relevancia: {relevance:.2f})")
            
            return source
            
        except Exception as e:
            logger.error(f"Error aprendiendo de {url}: {e}")
            return None
    
    def search_and_learn(self, query: str, max_results: int = 5) -> List[LearningSource]:
        """Busca y aprende de múltiples fuentes"""
        if not self.learning_enabled:
            return []
        
        sources = []
        
        # Búsqueda en fuentes conocidas
        search_queries = self._generate_search_queries(query)
        
        for search_query in search_queries[:max_results]:
            # Buscar en GitHub (API)
            github_results = self._search_github(search_query)
            sources.extend(github_results)
            
            # Buscar en Stack Overflow (web scraping básico)
            # stack_results = self._search_stackoverflow(search_query)
            # sources.extend(stack_results)
        
        return sources[:max_results]
    
    def _extract_content(self, html: str, query: Optional[str] = None) -> str:
        """Extrae contenido relevante de HTML"""
        # Remover tags HTML básicos
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Si hay query, priorizar secciones relevantes
        if query:
            # Buscar párrafos que contengan términos de la query
            paragraphs = text.split('.')
            relevant = [p for p in paragraphs if any(term.lower() in p.lower() for term in query.split())]
            if relevant:
                text = '. '.join(relevant[:10])
        
        return text.strip()[:5000]  # Limitar tamaño
    
    def _extract_title(self, html: str) -> str:
        """Extrae título de HTML"""
        match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()[:200]
        return "Sin título"
    
    def _calculate_relevance(self, content: str, query: str) -> float:
        """Calcula relevancia del contenido respecto a la query"""
        if not query:
            return 0.5
        
        query_terms = set(query.lower().split())
        content_lower = content.lower()
        
        matches = sum(1 for term in query_terms if term in content_lower)
        relevance = matches / len(query_terms) if query_terms else 0.0
        
        return min(relevance, 1.0)
    
    def _extract_tags(self, content: str, query: Optional[str] = None) -> List[str]:
        """Extrae tags relevantes del contenido"""
        tags = []
        
        # Tags comunes de F3-OS
        f3_terms = ['f3', 'kernel', 'rust', 'os', 'operating system', 'thread', 'synthesis']
        content_lower = content.lower()
        
        for term in f3_terms:
            if term in content_lower:
                tags.append(term)
        
        if query:
            query_terms = query.lower().split()[:3]
            tags.extend(query_terms)
        
        return list(set(tags))[:10]
    
    def _generate_search_queries(self, query: str) -> List[str]:
        """Genera queries de búsqueda a partir de una query"""
        queries = [query]
        
        # Agregar variaciones
        if 'f3' in query.lower():
            queries.append(f"{query} rust kernel")
            queries.append(f"{query} operating system")
        
        if 'rust' in query.lower():
            queries.append(f"{query} no_std")
            queries.append(f"{query} kernel")
        
        return queries[:5]
    
    def _search_github(self, query: str) -> List[LearningSource]:
        """Busca en GitHub API"""
        github_token = self.config.get('github', {}).get('token')
        if not github_token:
            return []
        
        try:
            self.network_manager.throttle_request()
            
            # Buscar repositorios
            url = "https://api.github.com/search/repositories"
            params = {
                'q': query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': 3
            }
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = self.network_manager.session.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            sources = []
            
            for repo in data.get('items', [])[:3]:
                source = LearningSource(
                    url=repo['html_url'],
                    title=repo['full_name'],
                    content=repo.get('description', '')[:500],
                    relevance_score=0.7,
                    learned_at=datetime.now(),
                    tags=repo.get('topics', [])[:5]
                )
                sources.append(source)
            
            return sources
            
        except Exception as e:
            logger.error(f"Error buscando en GitHub: {e}")
            return []
    
    def get_learned_knowledge(self, query: Optional[str] = None) -> List[LearningSource]:
        """Obtiene conocimiento aprendido, filtrado por query si se proporciona"""
        if query:
            query_lower = query.lower()
            return [
                source for source in self.learned_sources
                if query_lower in source.content.lower() or 
                   query_lower in source.title.lower() or
                   any(query_lower in tag.lower() for tag in source.tags)
            ]
        return self.learned_sources
    
    def apply_learned_knowledge(self, context: Dict) -> Dict:
        """Aplica conocimiento aprendido a un contexto"""
        # Buscar fuentes relevantes
        relevant_sources = self.get_learned_knowledge(context.get('query', ''))
        
        if relevant_sources:
            # Sintetizar conocimiento aprendido
            synthesized = {
                'sources_count': len(relevant_sources),
                'top_sources': [
                    {
                        'url': s.url,
                        'title': s.title,
                        'relevance': s.relevance_score,
                        'tags': s.tags
                    }
                    for s in sorted(relevant_sources, key=lambda x: x.relevance_score, reverse=True)[:3]
                ],
                'insights': self._synthesize_insights(relevant_sources)
            }
            return synthesized
        
        return {'sources_count': 0, 'insights': []}
    
    def _synthesize_insights(self, sources: List[LearningSource]) -> List[str]:
        """Sintetiza insights de las fuentes aprendidas"""
        insights = []
        
        # Agrupar por tags
        tag_groups = {}
        for source in sources:
            for tag in source.tags:
                if tag not in tag_groups:
                    tag_groups[tag] = []
                tag_groups[tag].append(source)
        
        # Generar insights
        for tag, tag_sources in tag_groups.items():
            if len(tag_sources) >= 2:
                insights.append(f"Encontradas {len(tag_sources)} fuentes sobre '{tag}'")
        
        return insights[:5]

