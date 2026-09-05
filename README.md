> 🚧 **Synapse V3 is currently in development**
>
> Synapse is undergoing a major architectural redesign for v3.
> This repository currently contains the stable **V2 implementation** while V3 is being designed and developed separately.

# Synapse V2

> **Incremental Repository Memory for AI Systems**

Modern AI coding assistants can reason about code, but they repeatedly forget the repository they are working on.

Every new conversation often starts from scratch, requiring the model to rediscover architecture, features, design decisions, and project evolution from thousands of lines of code.

**Synapse V2** treats a Git repository as a continuously evolving source of knowledge rather than a static snapshot.

Instead of reprocessing an entire repository every time, Synapse incrementally builds and maintains a **Repository Memory** that can be reused across conversations, tools, and AI systems.

---

# Why Synapse?

Large software repositories contain years of engineering knowledge spread across:

- Source code
- Commit history
- Architectural evolution
- Engineering decisions
- Feature additions
- Documentation

Traditional repository summarization tools typically analyze only the latest state of a repository.

As repositories grow, repeatedly asking an LLM to understand the repository becomes increasingly expensive and inefficient.

The repository already contains its own history.

The challenge is transforming that history into a compact, durable memory representation.

---

# Repository Memory Pipeline

```text
Git Repository
        │
        ▼
Repository Changes
        │
        ▼
Knowledge Extraction
        │
        ▼
Repository Memory
        │
        ▼
Future Incremental Updates
```

Rather than producing a one-time summary, Synapse continuously maintains a semantic memory of the repository.

---

# What Synapse Extracts

Synapse attempts to preserve long-term repository knowledge including:

- Repository purpose
- Architecture
- Engineering decisions
- Design principles
- User-facing features
- Current capabilities
- Architectural evolution

The objective is not to summarize every commit, but to construct a stable repository ontology that evolves alongside the project.

---

# Installation

## Requirements

- Python 3.10+
- Git
- Ollama

Install the required model (recommended):

```bash
ollama pull qwen3:14b-q4_K_M
```

Install Synapse:

```bash
pip install synapse-pkg
```

---

# Usage

Initialize Synapse inside any Git repository:

```bash
synapse init
```

This creates the `.synapse/` directory containing:

```text
.synapse/
├── metadata.json
├── context.json
├── compressed_context.json
└── config.json
```

Set up and select the local Ollama model:

```bash
synapse setup
```

Build the initial Repository Context and Repository Memory:

```bash
synapse knowledge
```

On the first execution, Synapse processes the repository history.

Future executions process only commits that have not previously been analyzed, automatically updating the Repository Memory.

---

# Incremental Processing

The first execution processes the repository history.

Subsequent executions process **only commits that have not previously been analyzed**.

```text
First Run
─────────
Entire Repository
        │
        ▼
Repository Memory

Future Runs
───────────
New Commits
        │
        ▼
Updated Repository Memory
```

Repository metadata stores the last processed commit, allowing future executions to continue from where the previous run ended.

---

# Adaptive Processing Strategy

Different repositories require different processing strategies.

Synapse automatically selects one of three strategies.

## Log Strategy

Used for repositories with a relatively small amount of new history.

Each commit is processed individually, preserving architectural evolution with the highest fidelity.

---

## Evolution Diff Strategy

For larger repositories, Synapse periodically compares snapshots of repository evolution instead of processing every individual commit.

This significantly reduces processing cost while preserving long-term architectural changes.

---

## Full Repository Diff

For extremely large repositories (currently **more than 100,000 commits**), Synapse processes a single diff between the **last processed commit** and the current `HEAD`.

This provides a scalable fallback that allows Synapse to continue operating efficiently even on repositories with extremely large histories.

---

# Repository Context

Synapse maintains two persistent representations.

## Repository Context

A structured historical representation containing processed repository changes.

This serves as the historical source of truth during repository processing.

## Repository Memory

A continuously evolving semantic representation optimized for LLM consumption.

The memory is intentionally compact while preserving durable architectural understanding.

---

# Why This Matters

Without persistent repository memory:

```text
Repository
      │
      ▼
Language Model
      │
      ▼
Forget
```

With Synapse:

```text
Repository
      │
      ▼
Repository Memory
      │
      ▼
Any Language Model
```

Repository understanding becomes reusable instead of being reconstructed every conversation.

---

# Current Features

- Git repository initialization
- Automatic repository processing
- Incremental repository updates
- Adaptive processing strategy selection
- Repository Context generation
- Repository Memory generation
- Large commit splitting
- Automatic metadata tracking
- Persistent repository memory

---

# Testing

Synapse V2 is currently in **alpha** and is undergoing testing on repositories of varying sizes and commit histories.

Current testing focuses on:

- Repository memory quality
- Incremental update correctness
- Processing strategy selection
- Large commit handling
- Repository scalability
- LLM extraction consistency
- Memory compression quality

Performance benchmarks will be published after testing has been completed across multiple repositories and hardware configurations.

---

# Current Status

Synapse V2 is currently in **alpha**.

The repository ingestion pipeline is complete, and the current focus is improving repository memory quality, ontology consistency, and extraction accuracy through real-world testing.

---

# Future Work

Repository Memory is intended to become the foundation for additional capabilities built on persistent repository understanding.

The exact direction of future versions is still evolving, with the immediate focus remaining on improving the quality, scalability, and usefulness of Repository Memory.

---

# Vision

Language models provide reasoning.

Repositories contain knowledge.

Synapse aims to separate **repository memory** from the language model itself.

The long-term goal is to create a reusable, incremental, portable memory layer that evolves alongside software projects and can be shared across different AI systems without repeatedly reconstructing repository understanding.

---

# License

MIT License

