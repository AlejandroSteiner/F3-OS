#![no_std]
#![feature(alloc_error_handler)]
#![feature(lang_items)]

extern crate alloc;

pub mod vga;
pub mod f3;
pub mod arch;
pub mod gui;
pub mod drivers;
pub mod allocator;

