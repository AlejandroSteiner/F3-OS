// AI Response Generator - Generador de respuestas con AI

use super::language_model::{LanguageModel, ProcessedQuery};

/// Generador de respuestas usando AI
pub struct AIResponseGenerator {
    language_model: LanguageModel,
}

impl AIResponseGenerator {
    pub fn new() -> Self {
        Self {
            language_model: LanguageModel::new(),
        }
    }
    
    /// Genera respuesta para una consulta procesada
    pub fn generate(&self, processed: &ProcessedQuery, context: &str) -> String {
        self.language_model.generate_response(processed, context)
    }
}

