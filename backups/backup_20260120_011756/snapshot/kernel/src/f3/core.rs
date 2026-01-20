use crate::vga;
use crate::f3::cpu;
use crate::f3::ram;
use crate::f3::mem;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum SystemPhase {
    /// Fase 1: LÓGICO - Estructura ordenada y predecible
    Logical,
    /// Fase 2: ILÓGICO - Desordena, explora, experimenta
    Illogical,
    /// Fase 3: SÍNTESIS - Concentra y reorganiza en el embudo
    Synthesis,
    /// Fase 4: PERFECTO - Nuevo orden superior optimizado
    Perfect,
}

#[derive(Debug, Clone, Copy)]
pub struct F3State {
    pub hash: u64,
    pub priority_bias: i8,
    pub memory_bias: i8,
    pub cycle_count: u64,
    pub phase: SystemPhase,
    pub entropy: u8,        // 0-255: medida de caos/orden
    pub perfection_score: i16, // -32768 a 32767: qué tan perfecto es el estado
}

static mut F3_STATE: F3State = F3State {
    hash: 0,
    priority_bias: 0,
    memory_bias: 0,
    cycle_count: 0,
    phase: SystemPhase::Logical,
    entropy: 0,
    perfection_score: 0,
};

pub fn init() {
    unsafe {
        F3_STATE.hash = 0xDEADBEEFCAFEBABE;
        F3_STATE.cycle_count = 0;
        F3_STATE.phase = SystemPhase::Logical; // Empezamos lógico
        F3_STATE.entropy = 0; // Sin caos inicial
        F3_STATE.perfection_score = 0; // Estado neutro
    }
    vga::print("[F3 Core] embudo activo - Fase LÓGICA inicial\n");
}

pub fn process_funnel() {
    unsafe {
        // Step 1: Collect flows from 3 threads
        let cpu_flow = cpu::get_flow();
        let ram_flow = ram::get_flow();
        let mem_flow = mem::get_flow();
        
        // CICLO: LÓGICO → ILÓGICO → SÍNTESIS → PERFECTO
        
        match F3_STATE.phase {
            SystemPhase::Logical => {
                // FASE 1: LÓGICO - Estructura ordenada
                // Todo es predecible, ordenado, funciona bien
                vga::print("[LÓGICO] estructura ordenada\n");
                
                // Cuando todo es demasiado ordenado, necesitamos explorar
                if F3_STATE.cycle_count > 0 && F3_STATE.cycle_count % 50 == 0 {
                    // Transición: LÓGICO → ILÓGICO
                    F3_STATE.phase = SystemPhase::Illogical;
                    F3_STATE.entropy = 100; // Introducir caos
                    vga::print("[TRANSICIÓN] LÓGICO → ILÓGICO\n");
                }
            },
            
            SystemPhase::Illogical => {
                // FASE 2: ILÓGICO - Desordena y explora
                // Las reglas se vuelven inconsistentes, experimentación activa
                vga::print("[ILÓGICO] explorando caos\n");
                
                // Desordenar los hilos intencionalmente
                introduce_illogical_behavior(&cpu_flow, &ram_flow, &mem_flow);
                
                // Cuando hay suficiente caos, sintetizar
                if F3_STATE.entropy > 200 || F3_STATE.cycle_count % 100 == 0 {
                    // Transición: ILÓGICO → SÍNTESIS
                    F3_STATE.phase = SystemPhase::Synthesis;
                    vga::print("[TRANSICIÓN] ILÓGICO → SÍNTESIS\n");
                }
            },
            
            SystemPhase::Synthesis => {
                // FASE 3: SÍNTESIS - Embudo concentra todo
                // Los 3 hilos convergen en el embudo, se reorganiza
                vga::print("[SÍNTESIS] embudo concentrando\n");
                
                let synthesized = mem::synthesize(
                    cpu_flow.cycles_used,
                    ram_flow.pressure,
                    cpu_flow.last_latency,
                );
                
                // Generar nuevo estado hash (reordenamiento)
                F3_STATE.hash = calculate_hash(
                    cpu_flow.task_id,
                    ram_flow.task_id,
                    mem_flow.task_id,
                    F3_STATE.cycle_count,
                );
                
                // Reducir entropía (orden emergiendo del caos)
                if F3_STATE.entropy > 0 {
                    F3_STATE.entropy = F3_STATE.entropy.saturating_sub(20);
                }
                
                // Calcular perfección del nuevo estado
                F3_STATE.perfection_score = calculate_perfection_score(&synthesized, &cpu_flow, &ram_flow);
                
                // Transición: SÍNTESIS → PERFECTO
                if F3_STATE.entropy < 50 {
                    F3_STATE.phase = SystemPhase::Perfect;
                    vga::print("[TRANSICIÓN] SÍNTESIS → PERFECTO\n");
                }
            },
            
            SystemPhase::Perfect => {
                // FASE 4: PERFECTO - Nuevo orden superior
                // Estado optimizado, mejor que el lógico inicial
                vga::print("[PERFECTO] nuevo orden superior\n");
                
                // Aplicar feedback optimizado (enrollado inverso)
                let synthesized = mem::synthesize(
                    cpu_flow.cycles_used,
                    ram_flow.pressure,
                    cpu_flow.last_latency,
                );
                
                F3_STATE.priority_bias = synthesized.success_score;
                F3_STATE.memory_bias = if ram_flow.pressure > 128 {
                    -(ram_flow.pressure as i8)
                } else {
                    0
                };
                
                apply_feedback(F3_STATE.priority_bias, F3_STATE.memory_bias);
                
                // Reiniciar ciclo: PERFECTO → LÓGICO (pero con mejor estado)
                if F3_STATE.cycle_count % 200 == 0 {
                    F3_STATE.phase = SystemPhase::Logical;
                    F3_STATE.entropy = 0;
                    // Mantener perfection_score (memoria del ciclo anterior)
                    vga::print("[CICLO COMPLETO] PERFECTO → LÓGICO (mejorado)\n");
                }
            },
        }
        
        // Incrementar ciclo
        F3_STATE.cycle_count += 1;
    }
}

/// Introduce comportamiento ilógico: desordena intencionalmente
fn introduce_illogical_behavior(cpu_flow: &cpu::CpuFlow, ram_flow: &ram::RamFlow, _mem_flow: &mem::MemFlow) {
    unsafe {
        // Invertir temporalmente las métricas (ilógico)
        // Esto fuerza al sistema a explorar soluciones no obvias
        
        // CPU puede reportar métricas contradictorias
        if F3_STATE.cycle_count % 3 == 0 {
            cpu::record_execution(
                cpu_flow.task_id.wrapping_add(1), // ID diferente
                cpu_flow.cycles_used.wrapping_mul(2), // Ciclos alterados
                cpu_flow.last_latency.saturating_sub(10), // Latencia contradictoria
            );
        }
        
        // RAM puede reportar presión inconsistente
        if F3_STATE.cycle_count % 5 == 0 {
            ram::record_usage(
                ram_flow.task_id.wrapping_add(1),
                ram_flow.memory_used.saturating_add(1000), // Memoria alterada
                255u8.saturating_sub(ram_flow.pressure), // Presión invertida
            );
        }
        
        // Incrementar entropía
        F3_STATE.entropy = F3_STATE.entropy.saturating_add(5).min(255);
    }
}

/// Calcula qué tan perfecto es el nuevo estado
fn calculate_perfection_score(synthesized: &mem::MemFlow, cpu_flow: &cpu::CpuFlow, ram_flow: &ram::RamFlow) -> i16 {
    let mut score = synthesized.success_score as i16 * 10;
    
    // Recompensar eficiencia
    if cpu_flow.cycles_used < 1000 {
        score += 50;
    }
    if ram_flow.pressure < 50 {
        score += 50;
    }
    if cpu_flow.last_latency < 100 {
        score += 50;
    }
    
    // Penalizar anomalías
    if synthesized.anomaly {
        score -= 100;
    }
    
    score
}

fn calculate_hash(cpu_id: u64, ram_id: u64, mem_id: u64, cycle: u64) -> u64 {
    // Simple hash function for state identification
    let mut hash = cpu_id;
    hash = hash.wrapping_mul(31).wrapping_add(ram_id);
    hash = hash.wrapping_mul(31).wrapping_add(mem_id);
    hash = hash.wrapping_mul(31).wrapping_add(cycle);
    hash
}

fn apply_feedback(priority_bias: i8, memory_bias: i8) {
    // This is where feedback would modify scheduler behavior
    // For now, just log it conceptually
    if priority_bias != 0 || memory_bias != 0 {
        // Feedback would be applied in next scheduling cycle
        // priority = base + priority_bias
        // memory_limit = base + memory_bias
    }
}

pub fn get_state() -> F3State {
    unsafe { F3_STATE }
}

pub fn get_phase() -> SystemPhase {
    unsafe { F3_STATE.phase }
}

pub fn get_entropy() -> u8 {
    unsafe { F3_STATE.entropy }
}

pub fn get_perfection_score() -> i16 {
    unsafe { F3_STATE.perfection_score }
}

