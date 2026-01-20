// Wrapper para alloc - permite usar alloc solo cuando está disponible
extern crate alloc;
// En main.rs, alloc está disponible. En lib.rs, no.

#[cfg(feature = "alloc")]
pub use alloc::{vec, string::String, format, vec::Vec};

#[cfg(not(feature = "alloc"))]
pub mod alloc_stub {
    // Stubs para cuando alloc no está disponible
    // Estos no se usarán en main.rs donde alloc está disponible
}

