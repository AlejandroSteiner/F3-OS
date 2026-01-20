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

static mut QUERY_PROCESSOR: Option<QueryProcessor> = None;

/// Inicializa el sistema GUI
pub fn init() {
    use crate::vga;
    unsafe {
        QUERY_PROCESSOR = Some(QueryProcessor::new());
        vga::print("[GUI] Query Processor initialized\n");
        vga::print("[GUI] Ready for user queries\n");
    }
}

/// Procesa una consulta del usuario
pub fn process_user_query(query: &str) {
    unsafe {
        if let Some(ref mut processor) = QUERY_PROCESSOR {
            if let Some(query_id) = processor.create_query_process(query.to_string()) {
                use crate::vga;
                vga::print("[GUI] Query #");
                // TODO: Imprimir número
                vga::print(" created\n");
            }
        }
    }
}

