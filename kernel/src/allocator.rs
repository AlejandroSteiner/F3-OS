// Heap Allocator para F3-OS
// Permite usar Vec, String, format! y otras estructuras dinámicas

use core::alloc::{GlobalAlloc, Layout};
use core::ptr::null_mut;

// Tamaño del heap: 1MB
const HEAP_SIZE: usize = 1024 * 1024;

// Heap estático
static mut HEAP: [u8; HEAP_SIZE] = [0; HEAP_SIZE];
static mut HEAP_POS: usize = 0;

pub struct F3Allocator;

unsafe impl GlobalAlloc for F3Allocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        // Alinear a múltiplo de align
        let align = layout.align();
        let size = layout.size();
        
        // Alinear posición actual
        let aligned_pos = (HEAP_POS + align - 1) & !(align - 1);
        
        // Verificar si hay espacio
        if aligned_pos + size > HEAP_SIZE {
            return null_mut();
        }
        
        // Asignar memoria
        let ptr = HEAP.as_mut_ptr().add(aligned_pos);
        HEAP_POS = aligned_pos + size;
        
        ptr
    }
    
    unsafe fn dealloc(&self, _ptr: *mut u8, _layout: Layout) {
        // Simple allocator: no libera memoria (bump allocator)
        // Para producción, implementar un allocator más sofisticado
    }
}

#[global_allocator]
static ALLOCATOR: F3Allocator = F3Allocator;

#[alloc_error_handler]
fn alloc_error_handler(layout: Layout) -> ! {
    use crate::vga;
    vga::print("ALLOC ERROR: Out of memory!\n");
    loop {
        unsafe { core::arch::asm!("hlt"); }
    }
}

pub fn init() {
    unsafe {
        HEAP_POS = 0;
    }
    use crate::vga;
    vga::print("[Allocator] Heap initialized (1MB)\n");
}


