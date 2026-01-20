// GUI Module - Interfaz gráfica completa de F3-OS
// Basada en separación de consultas de procesos y drivers de AI

pub mod query_processor;
pub mod query_process;
pub mod ai_driver;
pub mod renderer;
pub mod windows;

pub use query_processor::QueryProcessor;
pub use query_process::QueryProcess;
pub use ai_driver::AIDriver;
pub use renderer::GUIRenderer;

/// Inicializa el sistema GUI
pub fn init() {
    // TODO: Inicializar GUI
}

/// Procesa una consulta del usuario
pub fn process_user_query(query: &str) {
    // TODO: Procesar consulta
}

