// Multiboot header para que QEMU pueda bootear el kernel
// El header debe estar en los primeros 8KB del archivo ELF
// Format: magic (4 bytes) + flags (4 bytes) + checksum (4 bytes)
#[repr(C, packed)]
pub struct MultibootHeader {
    magic: u32,           // Magic number: 0x1BADB002
    flags: u32,           // Flags
    checksum: u32,        // Checksum: -(magic + flags)
}

// Calcular checksum correcto
// magic = 0x1BADB002
// flags = 0x00000003 (ALIGN_4K | MEMINFO)
// checksum = -(magic + flags) = -(0x1BADB002 + 0x00000003) = -(0x1BADB005) = 0xE4524FFB

// Header Multiboot simplificado para QEMU
// Debe estar en los primeros 8KB del archivo ELF
#[no_mangle]
#[link_section = ".multiboot_header"]
#[used]
pub static MULTIBOOT_HEADER: MultibootHeader = MultibootHeader {
    magic: 0x1BADB002,
    flags: 0x00000003,    // ALIGN_4K (bit 0=1) | MEMINFO (bit 1=1) = 0b11 = 0x03
    checksum: 0xE4524FFB, // -(0x1BADB002 + 0x00000003) & 0xFFFFFFFF
};

