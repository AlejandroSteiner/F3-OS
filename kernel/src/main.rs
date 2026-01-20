#![no_std]
#![no_main]
#![feature(alloc_error_handler)]
#![feature(lang_items)]

extern crate alloc;

mod vga;
mod f3;
mod arch;
mod boot;
mod allocator;
mod gui;
mod drivers;

// Re-exportar módulos de lib.rs para uso en main
pub use gui;
pub use drivers;

use core::panic::PanicInfo;

#[no_mangle]
pub extern "C" fn _start() -> ! {
    vga::clear();
    vga::print("F3-OS booting...\n");
    vga::print("Regla: Lógico → Ilógico → Síntesis → Perfecto\n");
    vga::print("===========================================\n\n");

    // Inicializar allocator
    allocator::init();
    
    // Inicializar F3 Core
    f3::init();
    
    // Inicializar GUI
    gui::init();
    
    vga::print("GUI initialized\n");

    // Ciclo principal que demuestra el sistema
    let mut demo_cycle = 0;
    loop {
        // Ejecutar tick del embudo
        f3::tick();
        
        // Mostrar estado cada cierto tiempo
        if demo_cycle % 25 == 0 {
            let phase = f3::get_phase();
            let _entropy = f3::get_entropy();
            let _perfection = f3::get_perfection_score();
            
            let phase_str = match phase {
                f3::SystemPhase::Logical => "LÓGICO",
                f3::SystemPhase::Illogical => "ILÓGICO",
                f3::SystemPhase::Synthesis => "SÍNTESIS",
                f3::SystemPhase::Perfect => "PERFECTO",
            };
            
            // Formatear mensaje (simplificado sin alloc)
            vga::print("\n=== Estado F3 ===\n");
            vga::print("Fase: ");
            vga::print(phase_str);
            vga::print("\n================\n");
        }
        
        demo_cycle += 1;
        
        unsafe { core::arch::asm!("hlt"); }
    }
}

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    vga::print("KERNEL PANIC\n");
    loop {
        unsafe { core::arch::asm!("hlt"); }
    }
}

