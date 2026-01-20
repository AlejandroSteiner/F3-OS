use crate::vga;

#[derive(Debug, Clone, Copy)]
pub struct MemFlow {
    pub task_id: u64,
    pub success_score: i8, // -128 to 127: performance score
    pub anomaly: bool,
    pub active: bool,
}

static mut MEM_FLOW: MemFlow = MemFlow {
    task_id: 0,
    success_score: 0,
    anomaly: false,
    active: false,
};

pub fn init() {
    unsafe {
        MEM_FLOW.active = true;
    }
    vga::print("[MEM] synthesizer online\n");
}

pub fn synthesize(cpu_cycles: u64, ram_pressure: u8, latency: u32) -> MemFlow {
    unsafe {
        // Simple synthesis: lower cycles + lower pressure + lower latency = better score
        let mut score = 0i8;
        
        if cpu_cycles < 1000 {
            score += 10;
        }
        if ram_pressure < 50 {
            score += 10;
        }
        if latency < 100 {
            score += 10;
        }
        
        if cpu_cycles > 10000 || ram_pressure > 200 || latency > 1000 {
            score -= 20;
            MEM_FLOW.anomaly = true;
        } else {
            MEM_FLOW.anomaly = false;
        }
        
        MEM_FLOW.success_score = score;
        MEM_FLOW
    }
}

pub fn get_flow() -> MemFlow {
    unsafe { MEM_FLOW }
}

pub fn reset() {
    unsafe {
        MEM_FLOW.success_score = 0;
        MEM_FLOW.anomaly = false;
    }
}

