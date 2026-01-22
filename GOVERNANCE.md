# F3-OS Governance

## Fundamental Principle

**F3-OS is not a democratic project in all its aspects.**

Some components are "sacred" and require special custody. This is not authoritarianism, it's protection of the conceptual core.

---

## Governance Structure

### Sacred Core (Core Team)

The **sacred core** of F3-OS is guarded by the founder and main maintainers. This core includes:

1. **F3 Core** (`kernel/src/f3/core.rs`)
   - The central funnel and its synthesis logic
   - The phase cycle (Logical → Illogical → Synthesis → Perfect)
   - Inverse feedback

2. **The 3 Structural Threads**
   - CPU Thread (`kernel/src/f3/cpu.rs`)
   - RAM Thread (`kernel/src/f3/ram.rs`)
   - MEM Thread (`kernel/src/f3/mem.rs`)

3. **The Conceptual Model**
   - The "logical → illogical → synthesis → perfect" philosophy
   - Project vocabulary
   - Fundamental rules

**Changes to the sacred core**:
- Require mandatory prior discussion (Issue with `[CONCEPTUAL]` label)
- Must have solid justification
- Are not voted on, evaluated by conceptual coherence
- Main maintainer has final veto

### Open Areas

These areas are more flexible and accept contributions with fewer restrictions:

- Drivers (except if they affect the F3 model)
- Build tools
- Documentation (except the manifesto)
- Utility scripts
- Tests

**Changes in open areas**:
- Follow normal PR process
- Require review but not mandatory prior discussion
- Evaluated by technical quality and alignment with project

---

## Decision Process

### Decision Levels

#### Level 1: Minor Technical Changes
- **Examples**: Bug fixes, implementation improvements, refactorings
- **Process**: Normal PR → Review → Merge
- **Time**: 1-3 days

#### Level 2: Major Technical Changes
- **Examples**: New drivers, significant performance improvements
- **Process**: Discussion Issue → PR → Extended review → Merge
- **Time**: 1-2 weeks

#### Level 3: Conceptual Changes
- **Examples**: Modifications to F3 Core, changes to phase cycle
- **Process**: `[CONCEPTUAL]` Issue → Deep discussion → Justification → PR → Exhaustive review → Maintainer decision
- **Time**: 2-4 weeks (or more if necessary)

### Decision Criteria

A change is accepted if:

1. ✅ **Conceptual coherence**: Aligns with the F3 model
2. ✅ **Solid justification**: Solves a real problem
3. ✅ **Technical quality**: Clean and maintainable code
4. ✅ **Doesn't break philosophy**: Respects manifesto principles

A change is rejected if:

1. ❌ **Breaks the model**: Goes against F3 philosophy
2. ❌ **Without justification**: "Would be cool" is not enough
3. ❌ **Incompatible**: Seeks to turn F3-OS into another project
4. ❌ **Premature**: Not necessary now

---

## Roles and Responsibilities

### Main Maintainer (Founder)

**Responsibilities**:
- Guard the sacred core
- Final decision on conceptual changes
- Maintain project coherence
- Review critical PRs

**Powers**:
- Veto on changes to sacred core
- Accept/reject PRs without consensus
- Modify manifesto and governance

### Maintainers

**Responsibilities**:
- Review PRs
- Maintain code quality
- Guide contributors
- Propose improvements

**Powers**:
- Approve PRs in open areas
- Suggest conceptual changes
- Label Issues

### Contributors

**Responsibilities**:
- Follow contribution rules
- Respect the F3 model
- Maintain quality in their PRs

**Powers**:
- Open Issues and PRs
- Participate in discussions
- Propose improvements

---

## Conflict Resolution

### If there's disagreement:

1. **Discussion in Issue**: Open an Issue with `[DISCUSSION]` label
2. **Technical arguments**: Present justification based on F3 model
3. **Reflection time**: No hasty decisions
4. **Final decision**: Main maintainer decides if there's no consensus

### Resolution principles:

- **Coherence > Consensus**: Better a coherent decision than a compromise that dilutes the project
- **F3 Model > Personal opinions**: Decisions are based on the model, not preferences
- **Mutual respect**: Ideas are questioned, not people

---

## Transparency

### What is public:

- ✅ All decisions are documented in Issues/PRs
- ✅ Rejection reasons are clearly explained
- ✅ The process is transparent

### What is not public:

- ❌ Private discussions (if any) are summarized publicly
- ❌ No "backroom deals"

---

## Governance Evolution

This document can evolve, but:

- Any change requires public discussion
- The sacred core will always be guarded
- Fundamental principles don't change without exceptional justification

---

## Frequently Asked Questions

### Why isn't it completely democratic?

Because F3-OS has a specific conceptual model. Unlimited democracy dilutes the vision. Linux works this way (Linus has veto). Rust works this way (core team decides). F3-OS too.

### Can I become a maintainer?

Over time, if you demonstrate:
- Deep understanding of the F3 model
- Consistent and quality contributions
- Respect for project philosophy

But there's no formal process yet. The project is young.

### What if I disagree with a decision?

You can:
1. Discuss in the corresponding Issue
2. Present technical arguments
3. Fork the project (it's open source)

But the main maintainer has final decision on the sacred core.

---

## Conclusion

**F3-OS is not a social experiment. It's a cognitive operating system experiment.**

Governance protects the conceptual core while allowing evolution in open areas. This is not authoritarianism, it's coherence.

If this doesn't seem right to you, F3-OS is probably not for you. And that's fine.

---

*Last updated: 2025*
