"""
Capability Memory - Memoria de Capacidades para Auto-Evolución

Permite al asistente aprender de consultas no resueltas y expandir sus capacidades.
Principio F3-OS: el asistente se auto-construye y mejora hasta alcanzar
razonamiento puro y conversación fluida.
"""

import json
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from collections import Counter

logger = logging.getLogger(__name__)


class CapabilityMemory:
    """Memoria que almacena consultas y aprende intents dinámicamente"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent.parent / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.data_dir / 'capability_memory.json'
        self.learned_file = self.data_dir / 'learned_intents.json'
        self.unhandled_queries: List[Dict] = []
        self.learned_intents: List[Dict] = []  # {triggers: [str], intent: str, confidence: float}
        self.successful_patterns: List[Dict] = []  # Refuerzo: queries que sí funcionaron
        self._load()
    
    def _load(self) -> None:
        """Carga memoria y intents aprendidos desde disco"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.unhandled_queries = data.get('unhandled_queries', [])[-500:]
                    self.successful_patterns = data.get('successful_patterns', [])[-200:]
            except Exception as e:
                logger.warning(f"Error cargando capability_memory: {e}")
        if self.learned_file.exists():
            try:
                with open(self.learned_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.learned_intents = data.get('learned_intents', [])
            except Exception as e:
                logger.warning(f"Error cargando learned_intents: {e}")
    
    def _save(self) -> None:
        """Guarda memoria a disco"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'unhandled_queries': self.unhandled_queries[-500:],
                    'successful_patterns': self.successful_patterns[-200:],
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error guardando capability_memory: {e}")
    
    def _save_learned(self) -> None:
        """Guarda intents aprendidos a disco"""
        try:
            with open(self.learned_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'learned_intents': self.learned_intents,
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error guardando learned_intents: {e}")
    
    def record_unhandled(self, query: str, intent_used: str = 'general') -> None:
        """Registra una consulta que no pudo resolverse bien"""
        entry = {
            'query': query[:500],
            'intent': intent_used,
            'timestamp': datetime.now().isoformat()
        }
        # Evitar duplicados recientes
        recent = [q['query'] for q in self.unhandled_queries[-20:]]
        if query[:100] not in recent:
            self.unhandled_queries.append(entry)
            self._save()
            logger.info(f"Memoria: consulta no resuelta registrada para evolución")
    
    def record_web_lookup_attempt(self, query: str, url: str, success: bool) -> None:
        """Registra intento de web lookup para mejorar detección"""
        entry = {
            'type': 'web_lookup',
            'query': query[:300],
            'url': url,
            'success': success,
            'timestamp': datetime.now().isoformat()
        }
        self.unhandled_queries.append(entry)
        self._save()
    
    def get_patterns_to_expand(self) -> List[str]:
        """Obtiene patrones frecuentes en consultas no resueltas (para futura expansión)"""
        from collections import Counter
        words = []
        for entry in self.unhandled_queries[-100:]:
            q = entry.get('query', '')
            words.extend(q.lower().split())
        common = Counter(w for w in words if len(w) > 3).most_common(10)
        return [w for w, _ in common]
    
    def should_try_web_lookup(self, query: str) -> bool:
        """
        Indica si la consulta sugiere que deberíamos intentar web lookup.
        Usado para auto-evolución: cuando falla 'general', probar web.
        Incluye triggers base + triggers aprendidos dinámicamente.
        """
        q = query.lower()
        triggers = [
            'entra a', 'entrá a', 'busca en', 've a', 'accede a',
            'dime la', 'cuál es la', 'cuanto está', 'cuánto está',
            'cotización', 'cotizacion', 'precio', 'valor',
            'dolar', 'dólar', 'blue', 'euro',
            'peso argentino', 'ars'
        ]
        if any(t in q for t in triggers):
            return True
        # Verificar triggers aprendidos
        for li in self.learned_intents:
            if li.get('intent') == 'web_lookup':
                for t in li.get('triggers', []):
                    if t in q:
                        return True
        return False
    
    def get_learned_intent(self, query: str) -> Optional[str]:
        """
        Retorna un intent aprendido si la consulta coincide con patrones aprendidos.
        Prioridad alta: el asistente evoluciona reconociendo nuevas formas de preguntar.
        """
        q = query.lower()
        words = set(re.findall(r'\w+', q))
        stopwords = {'el', 'la', 'los', 'las', 'de', 'del', 'en', 'y', 'a', 'que', 
                     'es', 'por', 'con', 'para', 'al', 'se', 'como', 'un', 'una'}
        words -= stopwords
        
        for li in self.learned_intents:
            triggers = set(li.get('triggers', []))
            if words & triggers and len(words & triggers) >= li.get('min_matches', 1):
                return li.get('intent', 'general')
        return None
    
    def record_success(self, query: str, intent: str, response_preview: str = '') -> None:
        """Registra una resolución exitosa para reforzar patrones"""
        entry = {
            'query': query[:200],
            'intent': intent,
            'timestamp': datetime.now().isoformat()
        }
        if query[:100] not in [s['query'][:100] for s in self.successful_patterns[-50:]]:
            self.successful_patterns.append(entry)
            self._save()
    
    def evolve_from_unhandled(self) -> bool:
        """
        Ciclo de auto-evolución: analiza consultas no resueltas y aprende nuevos patrones.
        Retorna True si se agregó algún intent aprendido.
        """
        unhandled = [e for e in self.unhandled_queries 
                     if e.get('type') != 'web_lookup' and 'query' in e]
        if len(unhandled) < 2:
            return False
        
        # Extraer palabras significativas de consultas no resueltas
        all_words = Counter()
        for entry in unhandled[-30:]:
            q = entry.get('query', '').lower()
            words = re.findall(r'\w+', q)
            for w in words:
                if len(w) >= 4 and w not in {'entra', 'dime', 'cuanto', 'cotizacion', 'cotización'}:
                    all_words[w] += 1
        
        # Si hay palabras que aparecen en 2+ consultas, considerar nuevo intent
        common_words = [w for w, c in all_words.most_common(15) if c >= 2]
        if not common_words:
            return False
        
        # Verificar si ya tenemos un intent similar
        existing_triggers = set()
        for li in self.learned_intents:
            existing_triggers.update(li.get('triggers', []))
        
        new_triggers = [w for w in common_words[:5] if w not in existing_triggers]
        if not new_triggers:
            return False
        
        # Agregar intent aprendido para web_lookup (la mayoría de consultas externas son web)
        new_intent = {
            'triggers': new_triggers,
            'intent': 'web_lookup',
            'min_matches': 1,
            'learned_at': datetime.now().isoformat(),
            'source': 'auto_evolution'
        }
        self.learned_intents.append(new_intent)
        self._save_learned()
        logger.info(f"🔬 Auto-evolución: nuevo intent aprendido - triggers: {new_triggers}")
        return True
