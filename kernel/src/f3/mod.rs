pub mod cpu;
pub mod ram;
pub mod mem;
mod core;

pub use core::{SystemPhase, get_phase, get_entropy, get_perfection_score};

use crate::vga;

pub fn init() {
    vga::print("Initializing F3 Core...\n");
    vga::print("Ciclo: LÓGICO → ILÓGICO → SÍNTESIS → PERFECTO\n");

    cpu::init();
    ram::init();
    mem::init();
    
    core::init();

    vga::print("F3 Core online.\n");
}

pub fn tick() {
    core::process_funnel();
}

