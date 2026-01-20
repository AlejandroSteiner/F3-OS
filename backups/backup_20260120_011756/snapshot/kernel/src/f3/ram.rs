use crate::vga;

#[derive(Debug, Clone, Copy)]
pub struct RamFlow {
    pub task_id: u64,
    pub memory_used: usize,
    pub pressure: u8, // 0-255: memory pressure indicator
    pub active: bool,
}

static mut RAM_FLOW: RamFlow = RamFlow {
    task_id: 0,
    memory_used: 0,
    pressure: 0,
    active: false,
};

pub fn init() {
    unsafe {
        RAM_FLOW.active = true;
    }
    vga::print("[RAM] flow initialized\n");
}

pub fn record_usage(task_id: u64, memory: usize, pressure: u8) {
    unsafe {
        RAM_FLOW.task_id = task_id;
        RAM_FLOW.memory_used = memory;
        RAM_FLOW.pressure = pressure;
    }
}

pub fn get_flow() -> RamFlow {
    unsafe { RAM_FLOW }
}

pub fn reset() {
    unsafe {
        RAM_FLOW.memory_used = 0;
        RAM_FLOW.pressure = 0;
    }
}

