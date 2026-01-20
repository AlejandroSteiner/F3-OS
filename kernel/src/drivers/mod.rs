// Drivers Module - Drivers de última tecnología para F3-OS
extern crate alloc;
// Especialmente drivers de AI

pub mod ai;
pub mod gpu;

pub use ai::AIDriverModule;
pub use gpu::GPURenderDriver;

