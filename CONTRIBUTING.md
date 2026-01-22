# F3-OS Contribution Guide

## Before Contributing

**Read this first**: F3-OS is not a traditional project. It has strict rules and a conceptual model that must be respected.

If you haven't read [MANIFESTO.md](MANIFESTO.md), do it now. If you don't understand the F3 model, read [COMPLETE_ARCHITECTURE.md](COMPLETE_ARCHITECTURE.md) and [LOGIC_RULES.md](LOGIC_RULES.md).

---

## Fundamental Rules

### 1. Small PRs

**Don't send massive PRs.**

- A PR should solve a specific problem
- Maximum 200-300 lines of changes
- If you need to make large changes, split them into multiple PRs

**Why**: Facilitates review and maintains conceptual focus.

### 2. Conceptual Changes → Discussion First

**If your change affects the F3 model, discuss it before coding.**

This includes:
- Modifications to F3 Core
- Changes to the 3 threads (CPU/RAM/MEM)
- Alterations to the phase cycle
- Changes to inverse feedback

**How to discuss**:
1. Open an Issue with the `[CONCEPTUAL]` label
2. Explain the problem it solves
3. Justify why the change is necessary
4. Wait for feedback before implementing

**Why**: The conceptual core of F3-OS is carefully guarded. Not everything is voted on, but everything is discussed.

### 3. No Features "Just Because"

**Every change must have justification.**

Before adding a feature, ask yourself:
- Does it solve a real problem of the F3 model?
- Does it align with the project philosophy?
- Is it necessary now or can it wait?

If the answer is "it would be cool to have this", you probably shouldn't add it.

**Why**: F3-OS doesn't seek to be a "kitchen sink". It seeks conceptual coherence.

### 4. Respect Project Vocabulary

F3-OS has specific terms:
- **Threads** (not "threads" in the traditional sense)
- **Funnel** (Funnel, F3 Core)
- **Synthesis** (not "average" or "aggregation")
- **Inverse feedback** (reverse winding)
- **Phases**: Logical, Illogical, Synthesis, Perfect

Use these terms correctly. Don't replace them with generic synonyms.

**Why**: Vocabulary defines the mental model. Changing it confuses.

---

## Contribution Process

### Step 1: Fork and Clone

```bash
git clone https://github.com/your-username/f3-os.git
cd f3-os
```

### Step 2: Create a Branch

```bash
git checkout -b feature/short-description
# or
git checkout -b fix/short-description
```

**Nomenclature**:
- `feature/`: New functionality
- `fix/`: Bug fix
- `docs/`: Documentation only
- `refactor/`: Refactoring without functional change

### Step 3: Develop

- Follow Rust code conventions
- Comment complex code
- Keep PRs small
- Test your changes (if possible in current state)

### Step 4: Commit

```bash
git commit -m "type: short description

More detailed description if necessary.

Refs: #issue-number"
```

**Commit types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Maintenance

### Step 5: Push and PR

```bash
git push origin feature/short-description
```

Then open a Pull Request on GitHub.

---

## Pull Request Structure

### Title

Must be clear and descriptive:
- ✅ `feat: add latency measurement in CPU Thread`
- ❌ `changes`
- ❌ `various improvements`

### Description

**Mandatory** to include:

1. **What changes?** (brief description)
2. **Why?** (justification)
3. **How?** (if relevant)
4. **Does it affect the F3 model?** (yes/no and explanation)

### Description Example

```markdown
## What changes?
Adds average latency measurement in CPU Thread.

## Why?
CPU Thread currently only reports latency of the last cycle. 
We need average latency for better synthesis in F3 Core.

## How?
Adds `avg_latency` field to `CpuFlow` and calculates average 
in each cycle.

## Does it affect the F3 model?
No. Only improves the metric that already exists. Doesn't change the phase 
cycle or synthesis.
```

---

## The Sacred Core

**These components require mandatory prior discussion:**

### F3 Core (`kernel/src/f3/core.rs`)
- Changes to `process_funnel()`
- Modifications to phase cycle
- Changes to `apply_feedback()`
- Alterations to synthesis logic

### The 3 Threads
- `kernel/src/f3/cpu.rs` - CPU Thread
- `kernel/src/f3/ram.rs` - RAM Thread  
- `kernel/src/f3/mem.rs` - MEM Thread

**Structural changes** (not just implementation improvements) require prior Issue.

### The Phase Cycle
- Modify `SystemPhase`
- Change transitions between phases
- Alter phase duration
- Modify entropy logic

---

## Code of Conduct

### Respect

- Respect others' opinions
- Question ideas, not people
- Be constructive in criticism

### Patience

- Conceptual discussions can take time
- Not all PRs are accepted
- Learn from rejections

### Coherence

- Keep focus on the F3 model
- Don't try to turn F3-OS into another project
- Respect the project philosophy

---

## PR Review

### Acceptance Criteria

A PR is accepted if:

1. ✅ Solves a real problem
2. ✅ Aligns with the F3 model
3. ✅ Doesn't break existing functionality
4. ✅ Has clear justification
5. ✅ Code is readable and maintainable
6. ✅ Doesn't affect core without prior discussion

### Rejection Criteria

A PR is rejected if:

1. ❌ Adds features without justification
2. ❌ Modifies core without prior discussion
3. ❌ Breaks the conceptual model
4. ❌ Is too large (split into smaller PRs)
5. ❌ Doesn't follow project conventions

---

## Frequently Asked Questions

### Can I add a driver for X?

It depends. If it's necessary for kernel development and aligns with the F3 model, yes. If it's "because it would be useful", probably not.

**Ask first** by opening an Issue.

### Can I change the phase cycle?

Only if you have a solid conceptual justification. **Discuss first** in an Issue with `[CONCEPTUAL]` label.

### Can I add POSIX compatibility?

No. F3-OS doesn't seek POSIX compatibility. It's part of its philosophy.

### How do I know if my change is "conceptual"?

If it affects:
- F3 Core
- The 3 threads (structure, not implementation)
- The phase cycle
- Inverse feedback

Then it's conceptual. **Discuss first**.

---

## Resources

- [MANIFESTO.md](MANIFESTO.md) - Project philosophy
- [COMPLETE_ARCHITECTURE.md](COMPLETE_ARCHITECTURE.md) - Technical architecture
- [LOGIC_RULES.md](LOGIC_RULES.md) - Phase cycle explanation
- [README.md](README.md) - General documentation

---

## Contact

If you have questions about whether your contribution is appropriate, open an Issue with the `[QUESTION]` label.

**Remember**: F3-OS is not a traditional project. Respect the conceptual model and contribute with coherence.

---

*Last updated: 2025*
