# F3-OS: Funnel / Fiber / Feedback Operating System

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Rust](https://img.shields.io/badge/Rust-1.70+-orange.svg)](https://www.rust-lang.org/)
[![Architecture](https://img.shields.io/badge/Architecture-x86__64-green.svg)](https://en.wikipedia.org/wiki/X86-64)

**F3-OS** is an experimental open-source operating system based on an innovative model of **3 fundamental threads** that merge into a central **funnel**, creating an adaptive feedback flow that governs system scheduling, memory, and execution.

> **⚠️ IMPORTANT**: Read [MANIFESTO.md](MANIFESTO.md) before contributing. F3-OS is not a traditional operating system. It is a cognitive experiment at the kernel level with specific rules and philosophy.

## Governing AI Agent - GUI Interface

F3-OS includes a **specialized AI agent** that governs project development and acts as an interactive assistant for users. The interface features a futuristic Star Wars/Formula 1 style design.

<div align="center">

![F3-OS Assistant Interface](https://raw.githubusercontent.com/AlejandroSteiner/F3-OS/main/agent/gui_web/screenshot.png)

*Assistant interface with agent life indicator (top right), real-time status panel, and interactive chat*

</div>

**Main features:**
- 🟢 **Agent Life Indicator**: Circular F1/Star Wars style clock with real-time active time
- 📊 **Status Panel**: Dynamic metrics (phase, entropy, perfection score, CPU)
- 💬 **Interactive Chat**: Real-time conversation with complete knowledge base
- 🎨 **Futuristic Theme**: Dark design with neon green accents and light effects
- 📚 **Immediate Resolution**: The agent has access to all project documentation

**Start the assistant:**
```bash
cd agent
pip install -r requirements.txt  # Install dependencies
./run.sh gui-server               # Start GUI server
# Open: http://localhost:8080
```

**Optional - Voice Commands:**
```bash
pip install vosk                  # Install Vosk (100% local, free)
./install_vosk_model.sh           # Download language model (50MB)
# Click 🎤 button in web interface to use voice commands
```

See [agent/README.md](agent/README.md) for more information.

## 🚀 Final Implementation Vision

F3-OS is designed as an **autonomous system that acts as a real clone of the user working in the user's matrix**, capable of operating independently for at least one week without supervision.

### Installation Flow from USB Drive

1. **USB Drive Connection**
   - When you connect a USB drive with F3-OS, the system requests assistant download
   - The assistant asks about your hardware and operating system
   - Installation occurs in a **second-layer emulator** (runs on top of your OS)

2. **Kernel Boot with Graphics**
   - After installation, the kernel boots with its graphics
   - Initial screen is displayed showing:
     - F3-OS logo
     - System status (phase, entropy, perfection score)
     - Assistant life indicator
     - Graphical interface ready for interaction

3. **Assistant Active and Listening**
   - The assistant is present and listening
   - You can ask it to do things like:
     - Open the web and search for a topic
     - Execute system tools
     - Manage files and directories
     - Interact with hardware through drivers
   - The assistant executes commands using all available tools

### Funnel System and Hardware Control

**The assistant works with F3-OS's funnel system:**
- Acts directly on any process in terms of hardware and pulse emission
- The funnel system (F3 Core) processes commands and controls hardware directly
- **Frequency-based optimization**: F3-OS drivers decode sub-channels of frequencies in metals (copper, gold, etc.)
- **Hardware optimization**: Uses available elements better through frequency analysis and sub-channel decoding
- **Integration of new rules**: The funnel integrates new rules based on frequency synthesis
- Continuously improves system efficiency through frequency-based feedback

### Civil Technology (No Credits)

**Fundamental principle: "Civil" = Accessible, no hidden costs**
- ✅ **No API credits consumed**: The assistant works completely locally
- ✅ **Open source**: Completely open code
- ✅ **No proprietary dependencies**: Only standard technologies
- ✅ **Accessible to everyone**: No subscriptions or payments required
- ✅ **Hardware improvement**: F3-OS improves user hardware with optimized drivers
- ✅ **Credit-free assistant**: Supports an assistant that doesn't consume credits

### Use Case: Autonomous Server

**Example: ktzchenWe3 on F3-OS Server**

When running a project like ktzchenWe3 on an F3-OS server:
- The server, with hardware consumption levels, invokes its own:
  - **Indexing** (search, cataloging)
  - **Social networks** (posts, interactions)
  - **Emails** (sending, receiving, organization)
  - **Updates** (system, dependencies, content)
- When you turn it on, F3-OS knows what rules to ask you so you can tell it what you want to do
- Everything operates according to defined rules and continuous learning

### Final Goal: Real User Clone

**Current objective for F3-OS**: To run autonomously being **in first person the user** to continue the task for **at least one week without supervision**. A real state of a **controlled alternate user**.

**Definition**: **"A real clone of the user working in the user's matrix"**

**Characteristics**:
- F3-OS acts as if it were the user
- Makes decisions as the user would
- Learns from user behavior
- Replicates work and thinking patterns
- Operates autonomously for extended periods
- Produces real results in the user's real environment

See [COMPLETE_VISION.md](COMPLETE_VISION.md) for the complete vision documentation.

## Main Concept

F3-OS is inspired by the graphic metaphor of **"winding 3 optical fiber threads into their cartridge in reverse"**, which technically translates to:

- **3 Fundamental Threads**: CPU (Executor), RAM (Context Keeper), MEM (Synthesizer)
- **Central Funnel (F3 Core)**: Receives, compresses, and synthesizes flows from the 3 threads
- **Inverse Backpropagation**: The final state rewrites previous decisions
- **Adaptive Cycle**: Logical → Illogical → Synthesis → Perfect

### The Physical Foundation

**The heart of F3-OS - the funnel of the 3 threads - is based on a real physical concept:**

The F3 Core is fundamentally a **frequency synthesizer** that:
- **Decodes sub-channels of frequencies** in metals (copper, gold, etc.)
- **Integrates new rules** through frequency analysis
- **Optimizes hardware** by understanding frequency characteristics in metallic conductors
- **Uses available elements better** because F3-OS drivers work at the frequency level

**F3-OS naturally uses available elements better because it implements F3-OS Drivers** - drivers that decode frequency sub-channels in metals and optimize hardware through frequency-based feedback.

See [F3_CORE_FOUNDATION.md](F3_CORE_FOUNDATION.md) for the complete foundation explanation.

## Architecture

### 3 Fundamental Threads

1. **CPU Thread (Executor)**
   - Executes tasks
   - Measures real cycles
   - Reports latencies

2. **RAM Thread (Context Keeper)**
   - Maintains partial states
   - Creates compressed snapshots
   - Decides what to discard

3. **MEM Thread (Synthesizer)**
   - Semantic memory
   - Summarizes patterns and results
   - Provides feedback

### F3 Core (Funnel)

The heart of the system that:
- Receives flows from the 3 threads
- Compresses state
- Generates structural feedback
- Dynamically modifies scheduling and memory

### System Phase Cycle

F3-OS operates in a 4-phase cycle:

1. **LOGICAL**: Ordered, predictable, low entropy
2. **ILLOGICAL**: Intentional disorder, exploration, high entropy
3. **SYNTHESIS**: The funnel concentrates, reorganizes, entropy decreases
4. **PERFECT**: Optimized state, applies refined feedback

This cycle repeats continuously, improving the system with each iteration.

## 📁 Project Structure

```
f3-os/
├── kernel/                 # Kernel source code
│   ├── src/
│   │   ├── main.rs        # Kernel entry point
│   │   ├── vga.rs         # VGA driver for text output
│   │   ├── f3/            # F3 Core modules
│   │   │   ├── mod.rs
│   │   │   ├── cpu.rs     # CPU Thread
│   │   │   ├── ram.rs     # RAM Thread
│   │   │   ├── mem.rs     # MEM Thread
│   │   │   └── core.rs    # F3 Core (Funnel)
│   │   ├── arch/          # Architecture-specific code
│   │   │   └── x86_64.rs
│   │   └── boot.rs        # Multiboot header
│   ├── linker.ld          # Linker script
│   └── Cargo.toml         # Rust configuration
├── build.sh               # Script to compile the kernel
├── run.sh                 # Script to run in QEMU (direct boot)
├── create_grub_iso.sh     # Script to create bootable ISO with GRUB
├── run_iso.sh             # Script to run ISO in QEMU
└── README.md              # This file
```

## Quick Start

### Requirements

- **Rust** (nightly): `rustup toolchain install nightly`
- **QEMU**: `sudo apt install -y qemu-system-x86`
- **GRUB**: `sudo apt install -y grub-pc-bin grub-common xorriso mtools`
- **LLVM/LLD**: `sudo apt install -y llvm lld`

Or install everything at once:
```bash
./INSTALL_DEPENDENCIES.sh
```

### Compile

```bash
./build.sh
```

This will generate `kernel.bin` in the project root.

### Run

#### Option 1: Direct Boot (no ISO required)
```bash
./run.sh
```

#### Option 2: Bootable ISO (more compatible)
```bash
# Create ISO
./create_grub_iso.sh

# Run ISO
./run_iso.sh
```

## 📖 Documentation

### Essential Documents (Read First)

- **[MANIFESTO.md](MANIFESTO.md)**: ⭐ **MANDATORY** - What F3-OS is and is NOT
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: ⭐ **MANDATORY** - Contribution rules
- **[GOVERNANCE.md](GOVERNANCE.md)**: Governance structure and sacred core
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)**: Community code of conduct
- **[COMPLETE_ARCHITECTURE.md](COMPLETE_ARCHITECTURE.md)**: Complete architecture documentation
- **[LOGIC_RULES.md](LOGIC_RULES.md)**: Explanation of the "Logical → Illogical → Synthesis → Perfect" cycle

### Technical Documents

- **[GOVERNING_AGENT.md](GOVERNING_AGENT.md)**: ⭐ Vision of the AI agent governing development
- **[SECURITY_AND_RESILIENCE.md](SECURITY_AND_RESILIENCE.md)**: ⭐ Security analysis and vulnerability resistance
- **[INNOVATION_AND_VALUE.md](INNOVATION_AND_VALUE.md)**: System innovation and value
- **[SAFE_TESTING_GUIDE.md](SAFE_TESTING_GUIDE.md)**: Guide for safe testing in QEMU
- **[DEBUG_GRUB.md](DEBUG_GRUB.md)**: Troubleshooting GRUB problems
- **[FINAL_SOLUTION.md](FINAL_SOLUTION.md)**: Solutions to common problems

### Current Status

**Version**: 0.1.0 (Initial development)

**Status**: ✅ Basic functional kernel, phase system implemented, boot in QEMU (with some limitations)

**Implemented Features**:
- ✅ Basic kernel in Rust (`#![no_std]`)
- ✅ VGA driver for text output
- ✅ F3 Core system with 3 threads
- ✅ Phase cycle: Logical → Illogical → Synthesis → Perfect
- ✅ Multiboot header for bootloaders
- ✅ Build and execution scripts
- ✅ **Governing AI Agent** with complete GUI interface
- ✅ **Voice Commands** using Vosk (100% local, offline, free)

**Known Issues**:
- ⚠️ GRUB may have problems detecting the Multiboot header (use debugging options)
- ⚠️ System freezes when trying to boot from ISO (bootloader problem)

**Next Steps**:
- [ ] Improve Multiboot header detection in GRUB
- [ ] Implement adaptive scheduler
- [ ] Dynamic memory system
- [ ] Basic drivers (keyboard, disk)
- [ ] Simple file system

## 🔬 Development

### Compile the Kernel

```bash
cd /home/ktzchen/Documentos/f3-os
./build.sh
```

The kernel compiles for the `x86_64-unknown-none` target using Rust nightly and `build-std`.

### Run in QEMU

```bash
# Direct boot (requires Multiboot header)
./run.sh

# From ISO (requires creating ISO first)
./create_grub_iso.sh
./run_iso.sh
```

### Debugging

For debugging in QEMU:

```bash
qemu-system-x86_64 \
  -cdrom f3os.iso \
  -display gtk \
  -m 256M \
  -no-reboot \
  -serial stdio \
  -s -S  # To connect with GDB
```

## 📝 Fundamental System Rule

**"Logical but illogical in its structure until it becomes logical and perfect again"**

This rule is implemented as the system's phase cycle:
1. Starts ordered and predictable (LOGICAL)
2. Introduces intentional disorder to explore (ILLOGICAL)
3. The funnel synthesizes and reorganizes (SYNTHESIS)
4. The system optimizes and returns to improved order (PERFECT)

This cycle repeats continuously, improving the system with each iteration.

## Contributing

**Before contributing, read**:
- [MANIFESTO.md](MANIFESTO.md) - Project philosophy and principles
- [CONTRIBUTING.md](CONTRIBUTING.md) - Strict contribution rules
- [GOVERNING_AGENT.md](GOVERNING_AGENT.md) - How the AI agent governs development

F3-OS has specific rules:
- Small PRs (maximum 200-300 lines)
- Conceptual changes require prior discussion
- No features "just because"
- Respect F3 vocabulary and model

**The Governing Agent**: F3-OS has an AI agent that automatically evaluates PRs according to the F3 model. See [agent/README.md](agent/README.md) for more information.

**Don't contribute if**:
- You're looking for an "easy" or traditional project
- You're not willing to understand the conceptual model
- You want to add POSIX compatibility or generic features

**Do contribute if**:
- You're interested in experimentation in system architecture
- You understand and respect the F3 model
- You're willing to question and be questioned

See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete process.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## Author

**AlejandroSteiner**

## Acknowledgments

- Rust community for the excellent language
- QEMU project for the emulator
- GRUB project for the bootloader
- OSDev community for resources and knowledge

## Resources

- [OSDev Wiki](https://wiki.osdev.org/)
- [Writing an OS in Rust](https://os.phil-opp.com/)
- [Rust Embedded Book](https://docs.rust-embedded.org/book/)

---

## ⚠️ Important Warnings

### What F3-OS is NOT:

- ❌ **NOT a production operating system** - It's experimental
- ❌ **NOT seeking POSIX compatibility** - It has its own model
- ❌ **NOT a traditional project** - It has specific rules and philosophy
- ❌ **NOT for everyone** - Requires understanding the conceptual model

### What F3-OS IS:

- ✅ **It's a cognitive experiment at the kernel level**
- ✅ **It's open source** (GPL-3.0)
- ✅ **It's a laboratory of ideas** about adaptive feedback
- ✅ **It's for those seeking experimentation** in system architecture

**Read [MANIFESTO.md](MANIFESTO.md) to fully understand what F3-OS is.**

---

**⚠️ Warning**: This is an experimental project. Do not use in production. Use at your own risk.

**⭐ If you like this project, consider giving it a star on GitHub!**
DONATIONS - PEPE ETH CONTRACT: 0xf700d6d8fe58421e5937b8a64696775e1449242e
