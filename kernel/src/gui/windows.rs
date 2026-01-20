// Windows System - Sistema de ventanas para GUI
// Cada consulta puede tener su propia ventana

use super::query_process::QueryProcess;

/// Ventana de GUI
pub struct Window {
    /// ID de la ventana
    window_id: u64,
    /// Posición X
    x: i32,
    /// Posición Y
    y: i32,
    /// Ancho
    width: u32,
    /// Alto
    height: u32,
    /// Proceso de consulta asociado
    query_process_id: Option<u64>,
    /// Título de la ventana
    title: String,
    /// Contenido de la ventana
    content: WindowContent,
}

#[derive(Debug, Clone)]
pub enum WindowContent {
    /// Ventana de consulta
    QueryWindow {
        query: String,
        result: Option<String>,
        status: String,
    },
    /// Ventana de visualización F3
    F3Visualizer {
        phase: String,
        entropy: u8,
        perfection_score: i16,
    },
    /// Ventana de procesos
    ProcessList {
        processes: Vec<u64>,
    },
}

impl Window {
    /// Crea una nueva ventana
    pub fn new(window_id: u64, x: i32, y: i32, width: u32, height: u32, title: String) -> Self {
        Self {
            window_id,
            x,
            y,
            width,
            height,
            query_process_id: None,
            title,
            content: WindowContent::QueryWindow {
                query: String::new(),
                result: None,
                status: "created".to_string(),
            },
        }
    }
    
    /// Asocia un proceso de consulta a la ventana
    pub fn associate_query_process(&mut self, query_id: u64) {
        self.query_process_id = Some(query_id);
    }
    
    /// Actualiza el contenido de la ventana
    pub fn update_content(&mut self, content: WindowContent) {
        self.content = content;
    }
}

/// Gestor de ventanas
pub struct WindowManager {
    /// Ventanas abiertas
    windows: Vec<Window>,
    /// Contador de ventanas
    window_counter: u64,
}

impl WindowManager {
    /// Crea un nuevo gestor de ventanas
    pub fn new() -> Self {
        Self {
            windows: Vec::new(),
            window_counter: 0,
        }
    }
    
    /// Crea una nueva ventana de consulta
    pub fn create_query_window(&mut self, query: String, query_id: u64) -> u64 {
        self.window_counter += 1;
        let window_id = self.window_counter;
        
        let mut window = Window::new(
            window_id,
            100 + (self.windows.len() as i32 * 50), // Posición escalonada
            100 + (self.windows.len() as i32 * 50),
            600,
            400,
            // TODO: format! requiere alloc
            "Consulta".to_string(),
        );
        
        window.associate_query_process(query_id);
        window.update_content(WindowContent::QueryWindow {
            query,
            result: None,
            status: "processing".to_string(),
        });
        
        self.windows.push(window);
        window_id
    }
    
    /// Obtiene una ventana por ID
    pub fn get_window(&mut self, window_id: u64) -> Option<&mut Window> {
        self.windows.iter_mut().find(|w| w.window_id == window_id)
    }
    
    /// Obtiene todas las ventanas
    pub fn get_windows(&self) -> &[Window] {
        &self.windows
    }
}

