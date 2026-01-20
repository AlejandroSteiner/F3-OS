// Query Processor - Separador de consultas de procesos
extern crate alloc;
// Cada consulta del usuario crea un proceso separado

extern crate alloc;
use alloc::vec::Vec;
use alloc::string::String;

use super::query_process::QueryProcess;

/// Procesador de consultas que separa cada consulta en un proceso independiente
pub struct QueryProcessor {
    /// Pool de procesos de consulta activos
    query_processes: Vec<Option<QueryProcess>>, // Máximo 32 procesos simultáneos
    /// Contador de consultas
    query_counter: u64,
    /// Próximo índice disponible
    next_index: usize,
}

impl QueryProcessor {
    /// Crea un nuevo procesador de consultas
    pub fn new() -> Self {
        let mut processes = Vec::new();
        for _ in 0..32 {
            processes.push(None);
        }
        Self {
            query_processes: processes,
            query_counter: 0,
            next_index: 0,
        }
    }
    
    /// Crea un nuevo proceso de consulta separado
    pub fn create_query_process(&mut self, query: String) -> Option<u64> {
        // Buscar slot disponible
        for i in 0..32 {
            let idx = (self.next_index + i) % 32;
            if self.query_processes[idx].is_none() {
                self.query_counter += 1;
                let query_id = self.query_counter;
                
                // Crear proceso separado para esta consulta
                let process = QueryProcess::new(query_id, query);
                self.query_processes[idx] = Some(process);
                self.next_index = (idx + 1) % 32;
                
                return Some(query_id);
            }
        }
        None // No hay slots disponibles
    }
    
    /// Obtiene un proceso de consulta por ID
    pub fn get_process(&mut self, query_id: u64) -> Option<&mut QueryProcess> {
        for process in &mut self.query_processes {
            if let Some(ref mut p) = process {
                if p.query_id() == query_id {
                    return Some(p);
                }
            }
        }
        None
    }
    
    /// Procesa todos los procesos activos
    pub fn process_all(&mut self) {
        for process in &mut self.query_processes {
            if let Some(ref mut p) = process {
                // Cada proceso se ejecuta independientemente
                p.process();
            }
        }
    }
    
    /// Sintetiza resultados de todos los procesos en el F3 Core
    pub fn synthesize_results(&mut self) {
        // Recopilar flujos de todos los procesos
        let mut all_flows = Vec::new();
        
        for process in &mut self.query_processes {
            if let Some(ref mut p) = process {
                let flows = p.get_flows();
                all_flows.push(flows);
            }
        }
        
        // Sintetizar en F3 Core
        // TODO: Integrar con F3 Core para síntesis
    }
    
    /// Obtiene lista de procesos activos
    pub fn get_active_queries(&self) -> Vec<u64> {
        self.query_processes
            .iter()
            .filter_map(|p| p.as_ref().map(|proc| proc.query_id()))
            .collect()
    }
    
    /// Limpia procesos completados
    pub fn cleanup_completed(&mut self) {
        for process in &mut self.query_processes {
            if let Some(ref mut p) = process {
                if p.is_completed() {
                    *process = None;
                }
            }
        }
    }
}

