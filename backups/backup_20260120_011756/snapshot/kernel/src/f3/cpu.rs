use crate::vga;

#[derive(Debug, Clone, Copy)]
pub struct CpuFlow {
    pub task_id: u64,
    pub cycles_used: u64,
    pub last_latency: u32,
    pub active: bool,
}

static mut CPU_FLOW: CpuFlow = CpuFlow {
    task_id: 0,
    cycles_used: 0,
    last_latency: 0,
    active: false,
};

pub fn init() {
    unsafe {
        CPU_FLOW.active = true;
    }
    vga::print("[CPU] flow initialized\n");
}

pub fn record_execution(task_id: u64, cycles: u64, latency: u32) {
    unsafe {
        CPU_FLOW.task_id = task_id;
        CPU_FLOW.cycles_used = cycles;
        CPU_FLOW.last_latency = latency;
    }
}

pub fn get_flow() -> CpuFlow {
    unsafe { CPU_FLOW }
}

pub fn reset() {
    unsafe {
        CPU_FLOW.cycles_used = 0;
        CPU_FLOW.last_latency = 0;
    }
}

