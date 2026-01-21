// AI Query Processor - Procesador de consultas con AI
extern crate alloc;

use super::language_model::LanguageModel;

/// Procesador de consultas usando AI
pub struct AIQueryProcessor {
    language_model: LanguageModel,
}

impl AIQueryProcessor {
    pub fn new() -> Self {
        Self {
            language_model: LanguageModel::new(),
        }
    }
    
    /// Procesa una consulta del usuario
    pub fn process(&self, query: &str) -> ProcessedQuery {
        self.language_model.process_query(query)
    }
}

use super::language_model::ProcessedQuery;


