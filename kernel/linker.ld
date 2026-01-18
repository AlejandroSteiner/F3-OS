/* Linker script para F3-OS kernel */
ENTRY(_start)

SECTIONS
{
    /* Dirección de carga del kernel */
    . = 0x100000;

    /* Multiboot header DEBE estar en los primeros 8KB del archivo ELF */
    /* Colocarlo justo al inicio de la sección de carga */
    .multiboot_header : ALIGN(4)
    {
        *(.multiboot_header)
    }
    
    /* Asegurar que el header esté al inicio del archivo */
    . = ALIGN(4);
    
    .text ALIGN(4) :
    {
        *(.text .text.*)
    }

    .rodata :
    {
        *(.rodata .rodata.*)
    }

    .data :
    {
        *(.data .data.*)
    }

    .bss :
    {
        *(COMMON)
        *(.bss .bss.*)
    }

    /DISCARD/ :
    {
        *(.note .note.*)
        *(.comment .comment.*)
    }
}

